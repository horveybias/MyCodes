import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class testsql {
    // Database connection details
    private static final String URL = "jdbc:mysql://127.0.0.1:3306/student_registration";
    private static final String USERNAME = "root";
    private static final String PASSWORD = "horve";

    public static void main(String[] args) {
        System.out.println("Connecting to the database...");
        try (Connection connection = DriverManager.getConnection(URL, USERNAME, PASSWORD)) {
            System.out.println("Database connected successfully!");
        } catch (SQLException e) {
            System.err.println("Cannot connect to the database. Error: " + e.getMessage());
            e.printStackTrace(); // Optional: Print detailed stack trace for debugging
        }
    }
}

