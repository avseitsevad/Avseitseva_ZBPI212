package org.example;

import javax.swing.*;
import java.awt.*;
import java.util.List;
import java.sql.SQLException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.stream.Collectors;



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

class TreeService {
    private DBConnection dbConnection;

    public TreeService(DBConnection dbConnection) {
        this.dbConnection = dbConnection;
    }
    public List<Tree> readTreesFromDatabase() throws SQLException {
        return TreeBuilder.buildTreesFromDB(dbConnection);
    }
    // Метод для сохранения деревьев в базу данных
    public List<Integer> getRootNodeIds() throws SQLException {
        List<Integer> rootIds = new ArrayList<>();
        try (Connection conn = dbConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT DISTINCT PARENT_ID FROM TREES WHERE ID = PARENT_ID")) {
            while (rs.next()) {
                rootIds.add(rs.getInt("PARENT_ID"));
            }
        }
        return rootIds;
    }
    public List<Tree> getAllTrees() throws SQLException {
        // Метод возвращает список всех деревьев из базы данных
        return TreeBuilder.buildTreesFromDB(dbConnection);
    }

    public void saveTreesToDatabase(List<Tree> trees) throws SQLException {
        try (Connection conn = dbConnection.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("INSERT INTO TREES (ID, PARENT_ID) VALUES (?, ?)");
            for (Tree tree : trees) {
                for (TreeNode node : tree.getNodes()) {
                    stmt.setInt(1, node.getID());
                    stmt.setInt(2, node.getParent() != null ? node.getParent().getID() : node.getID());
                    stmt.executeUpdate();
                }
            }
        }
    }

    // Метод для удаления узла из дерева
    public void deleteNode(int nodeId) throws SQLException {
        try (Connection conn = dbConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement("DELETE FROM TREES WHERE ID = ?")) {
            stmt.setInt(1, nodeId);
            stmt.executeUpdate();
        }
    }

    // Метод для добавления дочернего узла
    public void addChildNode(int parentId, int childId) throws SQLException {
        try (Connection conn = dbConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement("INSERT INTO TREES (ID, PARENT_ID) VALUES (?, ?)")) {
            stmt.setInt(1, childId);
            stmt.setInt(2, parentId);
            stmt.executeUpdate();
        }
    }

    // Метод для получения структуры дерева
    public TreeStructure getTreeStructure(int rootId) throws SQLException {
        List<Tree> trees = TreeBuilder.buildTreesFromDB(dbConnection);
        for (Tree tree : trees) {
            if (tree.getRoot().getID() == rootId) {
                return new TreeStructure(tree);
            }
        }
        return null;
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
class TreeStructure {
    private TreeNode root;

    public TreeStructure(Tree tree) {
        this.root = tree.getRoot();
    }

    public int getRootId() {
        return root.getID();
    }

    public List<Integer> getChildrenIds() {
        List<Integer> childrenIds = new ArrayList<>();
        for (TreeNode child : root.getChildNodes()) {
            childrenIds.add(child.getID());
        }
        return childrenIds;
    }

    public List<TreeNode> getNonRootNodes() {
        List<TreeNode> nonRootNodes = new ArrayList<>();
        addNonRootNodes(root, nonRootNodes);
        return nonRootNodes;
    }

    private void addNonRootNodes(TreeNode node, List<TreeNode> nonRootNodes) {
        if (node == null) {
            return;
        }
        if (!node.isRoot()) {
            nonRootNodes.add(node);
        }
        for (TreeNode child : node.getChildNodes()) {
            addNonRootNodes(child, nonRootNodes);
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

public class TreeApp {
    private JFrame frame;
    private JPanel panel;
    private JButton showTreesButton;
    private JButton readFromDBButton;
    private JButton writeToDBButton;
    private JButton deleteNodeButton;
    private JButton addChildButton;
    private JTextArea textArea;

    private TreeService treeService;

    public TreeApp() {
        this.treeService = new TreeService(new H2Connection());
        initializeUI();
    }

    private void initializeUI() {
        frame = new JFrame("Tree Application");
        panel = new JPanel(new BorderLayout());
        textArea = new JTextArea(30, 50);
        textArea.setEditable(false);

        showTreesButton = new JButton("Показать список всех деревьев");
        readFromDBButton = new JButton("Прочитать список всех деревьев из БД");
        writeToDBButton = new JButton("Записать список всех деревьев в БД");
        deleteNodeButton = new JButton("Удалить узел из дерева");
        addChildButton = new JButton("Добавить узел-потомок текущего узла");

        showTreesButton.addActionListener(e -> showTreeList());
        readFromDBButton.addActionListener(e -> {
            try {
                readTreesFromDB();
            } catch (SQLException ex) {
                textArea.setText("Ошибка при чтении из БД: " + ex.getMessage());
            }
        });
        writeToDBButton.addActionListener(e -> writeTreesToDB());
        deleteNodeButton.addActionListener(e -> deleteNode());
        addChildButton.addActionListener(e -> addChild());

        JPanel buttonPanel = new JPanel();
        buttonPanel.add(showTreesButton);
        buttonPanel.add(readFromDBButton);
        buttonPanel.add(writeToDBButton);
        buttonPanel.add(deleteNodeButton);
        buttonPanel.add(addChildButton);

        panel.add(buttonPanel, BorderLayout.NORTH);
        panel.add(new JScrollPane(textArea), BorderLayout.CENTER);

        frame.add(panel);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();
        frame.setVisible(true);
    }

    private void createTreeStructureButtons() throws SQLException {
        List<Integer> rootIds = treeService.getRootNodeIds(); // Получаем ID всех корневых узлов
        JPanel treeButtonsPanel = new JPanel(new FlowLayout());
        panel.remove(treeButtonsPanel); // Удаляем предыдущую панель с кнопками, если она существует
        for (Integer rootId : rootIds) {
            JButton button = new JButton("Дерево с корнем " + rootId);
            button.addActionListener(e -> {
                displayTreeStructure(rootId);
            });
            treeButtonsPanel.add(button);
        }
        panel.add(treeButtonsPanel, BorderLayout.SOUTH);
        panel.revalidate(); // Перерисовываем панель, чтобы обновить интерфейс
        panel.repaint();
    }


    private void displayTreeStructure(int rootId) {
        try {
            TreeStructure treeStructure = treeService.getTreeStructure(rootId);
            StringBuilder sb = new StringBuilder();
            sb.append("Корень: ").append(treeStructure.getRootId()).append("\n");
            sb.append("Дочерние узлы: ").append(treeStructure.getChildrenIds()).append("\n");

            for (TreeNode node : treeStructure.getNonRootNodes()) {
                sb.append("Узел: ").append(node.getID())
                        .append(", Родитель: ").append(node.getParent() != null ? node.getParent().getID() : "нет")
                        .append(", Потомки: ").append(node.getChildNodes().stream().map(TreeNode::getID).collect(Collectors.toList())).append("\n");
            }

            textArea.setText(sb.toString());
        } catch (SQLException e) {
            textArea.setText("Ошибка при отображении структуры дерева: " + e.getMessage());
        }
    }

    private void showTreeList() {
        try {
            List<Tree> trees = treeService.getAllTrees();
            StringBuilder sb = new StringBuilder();
            for (Tree tree : trees) {
                sb.append("Tree ID: ").append(tree.getRoot().getID()).append("\n");
            }
            textArea.setText(sb.toString());
            createTreeStructureButtons(); // Добавляем вызов этого метода здесь
        } catch (SQLException e) {
            e.printStackTrace();
            textArea.setText("Ошибка при получении списка деревьев.");
        }
    }
    private void readTreesFromDB() throws SQLException {
        List<Tree> trees = treeService.readTreesFromDatabase(); // Чтение деревьев из БД
        // Аналогично предыдущему методу, отобразить результаты в textArea
    }

    private void writeTreesToDB() {
        try {
            List<Tree> trees = treeService.readTreesFromDatabase(); // Получаем текущие деревья
            treeService.saveTreesToDatabase(trees); // Сохраняем изменения
            textArea.setText("Деревья сохранены в БД.");
        } catch (SQLException e) {
            e.printStackTrace();
            textArea.setText("Ошибка при сохранении деревьев в БД: " + e.getMessage());
        }
    }

    private void deleteNode() {
        try {
            String nodeId = JOptionPane.showInputDialog(frame, "Введите ID узла для удаления:");
            treeService.deleteNode(Integer.parseInt(nodeId));
            textArea.setText("Узел с ID " + nodeId + " удален.");
        } catch (SQLException e) {
            e.printStackTrace();
            textArea.setText("Ошибка при удалении узла.");
        } catch (NumberFormatException e) {
            textArea.setText("Неверный формат ID.");
        }
    }


    private void addChild() {
        try {
            String parentId = JOptionPane.showInputDialog(frame, "Введите ID родительского узла:");
            String childId = JOptionPane.showInputDialog(frame, "Введите ID нового узла:");
            treeService.addChildNode(Integer.parseInt(parentId), Integer.parseInt(childId));
            textArea.setText("Узел с ID " + childId + " добавлен как потомок узла с ID " + parentId + ".");
        } catch (SQLException e) {
            e.printStackTrace();
            textArea.setText("Ошибка при добавлении узла.");
        } catch (NumberFormatException e) {
            textArea.setText("Неверный формат ID.");
        }
    }


    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                new TreeApp();
            } catch (Exception e) {
                JOptionPane.showMessageDialog(null, "Ошибка при запуске приложения: " + e.getMessage());
            }
        });

    }
}
