import java.util.Map;

public class Utils {
    public static String renderTemplate(String template, Map<String, String> data) {
        for (Map.Entry<String, String> entry : data.entrySet()) {
            String key = "{{" + entry.getKey() + "}}";
            template = template.replace(key, entry.getValue() == null ? "" : entry.getValue());
        }
        return template;
    }
}