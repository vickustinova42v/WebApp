import java.sql.*;

public class Database {
    private static final String DB_URL = "jdbc:sqlite:library.db";

    public static Connection getConnection() {
        try {
            Class.forName("org.sqlite.JDBC"); // важно!
            return DriverManager.getConnection("jdbc:sqlite:library.db");
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public static void init() {
        try (Connection conn = getConnection(); Statement stmt = conn.createStatement()) {
            stmt.executeUpdate("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            """);

            stmt.executeUpdate("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    is_rented INTEGER NOT NULL DEFAULT 0,
                    rented_by INTEGER,
                    FOREIGN KEY(rented_by) REFERENCES users(id)
                )
            """);

            // Создаём дефолтного админа
            stmt.executeUpdate("""
                INSERT OR IGNORE INTO users (username, password, role)
                VALUES ('admin', 'admin123', 'admin')
            """);

            System.out.println("✅ Database initialized.");
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }
}
