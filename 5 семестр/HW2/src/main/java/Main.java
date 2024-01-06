import java.io.File;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

interface DBConnection {
    Connection getConnection() throws SQLException;
}

class H2Connection implements DBConnection {

    private static final String URL = "jdbc:h2:~/treeDB";
    private static final String USER = "userTree";
    private static final String PASSWORD = "pass";

    public Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}

class PostgresConnection implements DBConnection {

    private static final String URL = "jdbc:postgresql://localhost/treeDB";
    private static final String USER = "userTree";
    private static final String PASSWORD = "pass";

    public Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}
class TreeBuilder {
    public static List<Tree> buildTreesFromDB(DBConnection dbConnection) throws SQLException {
        List<Tree> trees = new ArrayList<>();
        Tree currentTree = null;

        try (Connection conn = dbConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT * FROM TREES")) {

            while (rs.next()) {
                int nodeId = rs.getInt("id");
                int parentId = rs.getInt("parent_id");

                if (nodeId == parentId) {
                    // Если узел является корнем, начинаем новое дерево
                    currentTree = new Tree(new TreeNode(nodeId));
                    trees.add(currentTree);
                } else if (currentTree != null) {
                    // Добавляем узел в текущее дерево
                    TreeNode parentNode = findNode(currentTree.getRoot(), parentId);
                    if (parentNode != null) {
                        parentNode.addChild(new TreeNode(nodeId));
                    }
                }
            }
        }

        return trees;
    }

    private static TreeNode findNode(TreeNode current, int id) {
        if (current == null) {
            return null;
        }
        if (current.getID() == id) {
            return current;
        }
        for (TreeNode child : current.getChildNodes()) {
            TreeNode result = findNode(child, id);
            if (result != null) {
                return result;
            }
        }
        return null;
    }
    public static int getTotalLeaves(List<Tree> trees) {
        int totalLeaves = 0;
        for (Tree tree : trees) {
            totalLeaves += tree.getLeaves().size();
        }
        return totalLeaves;
    }
}


public class Main {
    public static void main(String[] args) throws Exception {
        List<Tree> trees = TreeBuilder.buildTreesFromDB(new H2Connection());
        int totalLeaves = TreeBuilder.getTotalLeaves(trees);
        try (PrintWriter out = new PrintWriter(new File("output.csv"))) {
            out.println(totalLeaves);
        }
    }
}

class TreeNode {
    private int id; // id узла
    private List<TreeNode> childNodes; // список дочерних узлов (т.е. ссылок на дочерние узлы)
    private TreeNode parentNode; // родительский узел

    public TreeNode(int id) {
        // конструктор класса TreeNode
        this.id = id;
        this.childNodes = new ArrayList<>();
    }

    public int getID() {
        // Получить id
        return id;
    }

    public TreeNode getParent() {
        // Получить родительский узел
        return parentNode;
    }

    public List<TreeNode> getChildNodes() {
        // Получить список всех нижележащих (дочерних) узлов, соединенных с ним
        // переходом
        return childNodes;
    }

    public boolean isLeaf() {
        // Является ли узел листом (т.е. узлом, у которого нет дочерних узлов)
        return childNodes.isEmpty();
    }

    public boolean isRoot() {
        // Является ли узел корнем (т.е. узлом, у которого нет родительских узлов)
        return parentNode == null;
    }

    public void addChild(TreeNode childNode) {
        childNodes.add(childNode);
        childNode.parentNode = this;

    }
}
class Tree {
    private TreeNode root; // корень дерева

    public Tree(TreeNode root) {
        // конструктор класса
        this.root = root;
    }

    public TreeNode getRoot() {
        // получить корень
        return root;
    }

    public void insertNode(int id, int parentId) {
        // вставить узел
        if (root == null) {
            root = new TreeNode(parentId);
        }

        TreeNode parentNode = findNode(root, parentId);
        if (parentNode != null) {
            parentNode.addChild(new TreeNode(id));
        }
    }

    private TreeNode findNode(TreeNode current, int id) {
        if (current == null) {
            return null;
        }
        if (current.getID() == id) {
            return current;
        }
        for (TreeNode child : current.getChildNodes()) {
            TreeNode result = findNode(child, id);
            if (result != null) {
                return result;
            }
        }
        return null;
    }

    public List<TreeNode> getNodes() {
        // получить список всех узлов
        List<TreeNode> nodes = new ArrayList<>();
        getNodesRecursive(root, nodes);
        return nodes;
    }

    private void getNodesRecursive(TreeNode current, List<TreeNode> nodes) {
        // рекурсивная функция для обхода всех узлов дерева
        nodes.add(current);
        for (TreeNode child : current.getChildNodes()) {
            getNodesRecursive(child, nodes);
        }
    }

    public List<TreeNode> getLeaves() {
        // получить список всех листов дерева
        List<TreeNode> leaves = new ArrayList<>();
        getLeavesRecursive(root, leaves);
        return leaves;
    }

    private void getLeavesRecursive(TreeNode current, List<TreeNode> leaves) {
        if (current.isLeaf()) {
            leaves.add(current);
        }
        for (TreeNode child : current.getChildNodes()) {
            getLeavesRecursive(child, leaves);
        }
    }
}