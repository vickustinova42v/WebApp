import java.util.HashMap;
import java.util.UUID;

public class SessionManager {
    private static final HashMap<String, Integer> sessions = new HashMap<>();

    public static String createSession(int userId) {
        String sessionId = UUID.randomUUID().toString();
        sessions.put(sessionId, userId);
        return sessionId;
    }

    public static Integer getUserId(String sessionId) {
        return sessions.get(sessionId);
    }

    public static void removeSession(String sessionId) {
        sessions.remove(sessionId);
    }
}
