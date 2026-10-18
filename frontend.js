import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
const h = React.createElement;
const API = "http://127.0.0.1:5000";

function App() {
  const [skills, setSkills] = useState([]);
  const [error, setError] = useState("");
  async function refresh() {
    try {
      const response = await fetch(`${API}/skills`);
      if (!response.ok) throw new Error("Could not load skills. Is the API running?");
      setSkills(await response.json()); setError("");
    } catch (err) { setError(err.message); }
  }
  useEffect(() => { refresh(); }, []);
  async function changeLevel(skill, value) {
    const response = await fetch(`${API}/skills/${skill.id}`, {
      method: "PATCH", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ proficiency: Number(value) })
    });
    if (response.ok) refresh();
  }
  async function addSkill(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const name = new FormData(form).get("name");
    const response = await fetch(`${API}/skills`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, proficiency: 0 })
    });
    if (response.ok) { form.reset(); refresh(); }
    else setError((await response.json()).error);
  }
  const started = skills.filter(skill => skill.proficiency > 0).length;
  return h("main", { className: "shell" },
    h("header", { className: "hero" }, h("div", null,
      h("p", { className: "eyebrow" }, "SKILLGAP / PERSONAL DASHBOARD"),
      h("h1", null, "Build your next skill."),
      h("p", { className: "intro" }, "Track the tools and techniques you want to learn.")),
      h("div", { className: "score" }, h("strong", null, `${started}/${skills.length}`), h("span", null, "skills started"))),
    error && h("p", { className: "error", role: "alert" }, error),
    h("section", { className: "card" },
      h("div", { className: "section-heading" }, h("div", null,
        h("p", { className: "eyebrow" }, "YOUR ROADMAP"), h("h2", null, "Required skills")),
        h("span", { className: "count" }, `${skills.length} skills`)),
      h("div", { className: "skill-list" }, skills.map(skill => h("article", { className: "skill", key: skill.id },
        h("div", { className: "skill-name" }, h("span", { className: "dot" }),
          h("strong", null, skill.name), h("span", { className: "required" }, "REQUIRED")),
        h("label", { className: "level" }, h("span", null, `Level ${skill.proficiency}/5`),
          h("input", { type: "range", min: 0, max: 5, value: skill.proficiency,
            "aria-label": `${skill.name} proficiency`, onChange: event => changeLevel(skill, event.target.value) }))))),
      h("form", { className: "add-form", onSubmit: addSkill },
        h("input", { name: "name", placeholder: "Add another skill", required: true }),
        h("button", { type: "submit" }, "Add skill"))));
}

createRoot(document.getElementById("root")).render(h(App));
