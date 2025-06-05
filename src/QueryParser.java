import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.HashMap;
import java.util.Map;

public class QueryParser {
    public static Map<String, String> parse(String query) {
        Map<String, String> result = new HashMap<>();
        if (query == null || query.isEmpty()) return result;

        for (String pair : query.split("&")) {
            String[] parts = pair.split("=", 2);
            try {
                String key = URLDecoder.decode(parts[0], "UTF-8");
                String value = parts.length > 1 ? URLDecoder.decode(parts[1], "UTF-8") : "";
                result.put(key, value);
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace(); // логгирование
            }
        }
        return result;
    }
}
