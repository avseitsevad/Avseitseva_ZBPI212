import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class PostgresConnection implements DBConnection {

    private static final String URL = "jdbc:postgresql://localhost/treeDB";
    private static final String USER = "userTree";
    private static final String PASSWORD = "pass";

    public Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}
