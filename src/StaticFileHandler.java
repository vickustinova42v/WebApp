import com.sun.net.httpserver.*;

import java.io.*;
import java.net.URLConnection;
import java.nio.file.*;

public class StaticFileHandler implements HttpHandler {
    private final String baseDir;

    public StaticFileHandler(String baseDir) {
        this.baseDir = baseDir;
    }

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        if (path.equals("/")) path = "/index.html";

        File file = new File(baseDir + path).getCanonicalFile();

        if (!file.getPath().startsWith(new File(baseDir).getCanonicalPath())) {
            exchange.sendResponseHeaders(403, -1);
            return;
        }

        if (!file.isFile()) {
            exchange.sendResponseHeaders(404, -1);
            return;
        }

        String mime = URLConnection.guessContentTypeFromName(file.getName());
        exchange.getResponseHeaders().set("Content-Type", mime != null ? mime : "application/octet-stream");

        byte[] bytes = Files.readAllBytes(file.toPath());
        exchange.sendResponseHeaders(200, bytes.length);
        OutputStream os = exchange.getResponseBody();
        os.write(bytes);
        os.close();
    }
}
