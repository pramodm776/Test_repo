import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/** Tiny Java client for the Flask skills API. */
public class SkillsClient {
    public static void main(String[] args) throws Exception {
        var request = HttpRequest.newBuilder(URI.create("http://127.0.0.1:5000/skills")).GET().build();
        var response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("HTTP " + response.statusCode());
        System.out.println(response.body());
    }
}
