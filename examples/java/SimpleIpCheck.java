import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetSocketAddress;
import java.net.Proxy;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;

/**
 * 01 - Simple IP Check via Thordata Proxy (Java)
 *
 * Usage:
 *   cd examples/java
 *   javac SimpleIpCheck.java
 *   java SimpleIpCheck
 */
public class SimpleIpCheck {
    public static void main(String[] args) {
        String username = System.getenv("THORDATA_RESIDENTIAL_USERNAME");
        String password = System.getenv("THORDATA_RESIDENTIAL_PASSWORD");
        String host = System.getenv("THORDATA_PROXY_HOST");
        String portStr = System.getenv("THORDATA_PROXY_PORT");

        if (username == null || password == null) {
            System.out.println("[ERROR] Please set THORDATA_RESIDENTIAL_USERNAME and THORDATA_RESIDENTIAL_PASSWORD in .env");
            return;
        }
        if (host == null || host.isEmpty()) {
            host = "pr.thordata.net";
        }
        int port = 9999;
        if (portStr != null && !portStr.isEmpty()) {
            try {
                port = Integer.parseInt(portStr);
            } catch (NumberFormatException ignored) {
            }
        }

        String proxyUser = "td-customer-" + username;
        String auth = proxyUser + ":" + password;

        System.setProperty("https.proxyHost", host);
        System.setProperty("https.proxyPort", String.valueOf(port));
        System.setProperty("https.proxyUser", proxyUser);
        System.setProperty("https.proxyPassword", password);

        try {
            URL url = new URL("https://httpbin.org/ip");

            Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress(host, port));
            HttpsURLConnection conn = (HttpsURLConnection) url.openConnection(proxy);

            String basicAuth = "Basic " + java.util.Base64.getEncoder().encodeToString(auth.getBytes());
            conn.setRequestProperty("Proxy-Authorization", basicAuth);
            conn.setConnectTimeout(30000);
            conn.setReadTimeout(30000);

            System.out.println("Requesting: " + url);
            System.out.println("   via Thordata proxy network...");

            int status = conn.getResponseCode();
            if (status != 200) {
                System.out.println("[ERROR] HTTP status: " + status);
                return;
            }

            try (BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = in.readLine()) != null) {
                    response.append(line);
                }
                System.out.println("[SUCCESS] Response: " + response);
            }
        } catch (IOException e) {
            System.out.println("[ERROR] " + e.getMessage());
        }
    }
}

