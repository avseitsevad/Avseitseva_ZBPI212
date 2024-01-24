package org.example;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class TreeService {
    private DBConnection dbConnection;

    public TreeService(DBConnection dbConnection) {
        this.dbConnection = dbConnection;
    }

    public List<Tree> readTreesFromDatabase() throws SQLException {
        return TreeBuilder.readTreesFromDB(dbConnection);
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
        return TreeBuilder.readTreesFromDB(dbConnection);
    }

    public void saveTreesToDatabase(List<Tree> trees) throws SQLException {
        try (Connection conn = dbConnection.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("INSERT INTO TREES (ID, PARENT_ID) VALUES (?, ?)");
            for (Tree tree : trees) {
                for (TreeNode node : tree.getNodes()) {
                    stmt.setInt(1, node.getId());
                    stmt.setInt(2, node.getParentId());
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
        List<Tree> trees = TreeBuilder.readTreesFromDB(dbConnection);
        for (Tree tree : trees) {
            if (tree.getRoot().getId() == rootId) {
                return new TreeStructure(tree);
            }
        }
        return null;
    }
}
