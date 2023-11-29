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

        try (Connection conn = dbConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT * FROM TREES")) {

            while (rs.next()) {
                int nodeId = rs.getInt("id");
                int parentId = rs.getInt("parent_id");

                boolean foundTree = false;
                for (Tree tree : trees){
                    if (tree.getRoot().getID() == parentId){
                        foundTree = true;
                        break;
                    }
                }
                if (nodeId == parentId) {
                    // в случае, если узел=корень, создаем новое дерево
                    if (!foundTree) {
                        TreeNode node = new TreeNode(nodeId);
                        Tree tree = new Tree(node);
                        trees.add(tree);
                    }
                } else {
                    //в обратном случае добавляем узел к дереву с соответствующим корнем
                    if (!foundTree){
                        TreeNode parentNode = new TreeNode(parentId);
                        Tree tree = new Tree(parentNode);
                        trees.add(tree);
                        tree.insertNode(nodeId);
                    } else {
                        for (Tree tree : trees){
                            if (tree.getRoot().getID() == parentId){
                                tree.insertNode(nodeId);
                            }
                        }
                    }
                }
            }
        }
        return trees;
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
    private int id; //id узла
    private List<TreeNode> childNodes; //список дочерних узлов (т.е. ссылок на дочерние узлы)
    private TreeNode parentNode; //родительский узел
    private TreeNode leftChild; //левый потомок
    private TreeNode rightChild; //правый потомок

    public TreeNode(int id){
        //конструктор класса TreeNode
        this.id = id;
        this.childNodes = new ArrayList<>();
    }
    public int getID() {
        //Получить id
        return id;
    }
    public TreeNode getParent() {
        //Получить родительский узел
        return parentNode;
    }
    public TreeNode getLeftChild(){
        return leftChild;
    }
    public void setLeftChild(TreeNode leftChild){
        this.leftChild = leftChild;
    }
    public TreeNode getRightChild(){
        return rightChild;
    }
    public void setRightChild(TreeNode rightChild){
        this.rightChild = rightChild;
    }
    public List<TreeNode> getChildNodes() {
        //Получить список всех нижележащих (дочерних) узлов, соединенных с ним переходом
        return childNodes;
    }
    public boolean isLeaf() {
        //Является ли узел листом (т.е. узлом, у которого нет дочерних узлов)
        return childNodes.isEmpty();
    }
    public boolean isRoot() {
        //Является ли узел корнем (т.е. узлом, у которого нет родительских узлов)
        return parentNode == null;
    }
    public void addChild(TreeNode childNode) {
        childNodes.add(childNode);
        childNode.parentNode = this;

    }
}

class Tree {
    private TreeNode root; //корень дерева

    public Tree(TreeNode root) {
        //конструктор класса
        this.root = root;
    }
    public TreeNode getRoot() {
        //получить корень
        return root;
    }
    public void insertNode (int id){
        TreeNode node = new TreeNode(id);
        TreeNode currentNode = root;
        TreeNode parentNode;
        while (true){
            parentNode = currentNode;
            if (id == currentNode.getID()){
                // если такой элемент в дереве уже есть, выходим из цикла
                return;
            }
            else if (id < currentNode.getID()) { //идём налево
                //добавляем левого потомка
                currentNode = currentNode.getLeftChild();
                if (currentNode == null) {
                    parentNode.setLeftChild(node);
                    parentNode.addChild(node);
                    return;
                }
            }
            else if(id >= currentNode.getID()){ //идём направо
                //добавляем правого потомка
                currentNode = currentNode.getRightChild();
                if (currentNode == null){
                    parentNode.setRightChild(node);
                    parentNode.addChild(node);
                    return;
                }
            }
        }

    }
    public List<TreeNode> getNodes() {
        //получить список всех узлов
        List<TreeNode> nodes = new ArrayList<>();
        getNodesRecursive (root, nodes);
        return nodes;
    }
    private void getNodesRecursive(TreeNode current, List<TreeNode> nodes) {
        //рекурсивная функция для обхода всех узлов дерева
        nodes.add(current);
        for(TreeNode child : current.getChildNodes()) {
            getNodesRecursive(child, nodes);
        }
    }
    public List<TreeNode> getLeaves() {
        //получить список всех листов дерева
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