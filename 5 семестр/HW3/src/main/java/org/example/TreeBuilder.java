package org.example;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class TreeBuilder {
    public static List<Tree> readTreesFromDB(DBConnection dbConnection) throws SQLException {
        Tree currentTree = null;
        List<TreeNode> nodes = new ArrayList<>();
        try (Connection conn = dbConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT * FROM TREES")) {
            while (rs.next()) {
                int nodeId = rs.getInt("id");
                int parentId = rs.getInt("parent_id");
                nodes.add(new TreeNode(nodeId, parentId));
            }
        }

        List<Tree> trees = buildTrees(nodes);
        return trees;
    }
    public static List<Tree> buildTrees(List<TreeNode> nodes) {
        Map<Integer, TreeNode> treeNodeMap = new HashMap<>();
        List<Tree> trees = new ArrayList<>();

        // Создаем объекты TreeNode для всех узлов и добавляем их в карту
        for (TreeNode node : nodes) {
            treeNodeMap.put(node.getId(), node);
        }

        // Строим деревья и связи между узлами
        for (TreeNode node : nodes) {
            if (node.getId() == node.getParentId()) {
                // Начинаем новое дерево, если id равен parentId
                trees.add(new Tree(node));
            } else {
                // Находим родительский узел и добавляем текущий узел как дочерний
                TreeNode parentNode = treeNodeMap.get(node.getParentId());
                if (parentNode != null) {
                    parentNode.addChild(node);
                }
            }
        }

        return trees;
    }
    private static TreeNode findNode(TreeNode current, int id) {
        if (current == null) {
            return null;
        }
        if (current.getId() == id) {
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
