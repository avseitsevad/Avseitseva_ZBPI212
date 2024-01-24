import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class H2Connection implements DBConnection {

    private static final String URL = "jdbc:h2:~/treeDB";
    private static final String USER = "userTree";
    private static final String PASSWORD = "pass";

    public Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}
