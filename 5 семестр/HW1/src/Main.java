import java.io.*;
import java.util.*;

public class Main {

    public static List<Tree> readInput(String fileName) throws Exception {
        List<TreeNode> nodes = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            String line;
            while ((line = br.readLine()) != null) {
                line = line.replace("\"", "");
                String[] parts = line.split(",");
                int nodeId = Integer.parseInt(parts[0].trim());
                int parentId = Integer.parseInt(parts[1].trim());

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



    /* public static int[] maxLeavesTree(List<Tree> trees) throws Exception {
        // метод для нахождения дерева с макс кол-вом листов
        int maxLeaves = 0;
        int maxLeavesTreeId = 0;
        boolean multipleMax = false;
        for (Tree tree : trees) {
            int leaves = tree.getLeaves().size();
            if (leaves > maxLeaves) {
                maxLeaves = leaves;
                maxLeavesTreeId = tree.getRoot().getId();
                multipleMax = false;
            } else if (leaves == maxLeaves) {
                multipleMax = true;
            }
        }
        if (multipleMax) {
            // генерируем исключение в случае, если деревьев с макс. кол-вом листов
            // несколько
            throw new Exception("Несколько деревьев с максимальным количеством листьев");
        }
        return new int[] { maxLeavesTreeId, maxLeaves };
    }
    */
    public static int[] findMaxNodesAtDepthTree(List<Tree> trees, int n) throws Exception {
        int maxNodes = 0;
        int maxNodesTreeId = 0;
        boolean multipleMax = false;

        for (Tree tree : trees) {
            int nodesAtDepth = tree.getNodesAtDepth(n);
            if (nodesAtDepth > maxNodes) {
                maxNodes = nodesAtDepth;
                maxNodesTreeId = tree.getRoot().getId();
                multipleMax = false;
            } else if (nodesAtDepth == maxNodes) {
                multipleMax = true;
            }
        }

        if (multipleMax) {
            throw new Exception("Несколько деревьев с макс. кол-вом листьев на таком числе переходов: " + n);
        }

        return new int[] { maxNodesTreeId, maxNodes };
    }

    public static void main(String[] args) throws Exception {
        List<Tree> trees = readInput("input.csv");
        int n = 5;
        try {
            int[] maxTreeData = findMaxNodesAtDepthTree(trees, n);
            int maxTreeId = maxTreeData[0];
            int maxNodes = maxTreeData[1];

            try (PrintWriter writer = new PrintWriter(new File("output.csv"))) {
                writer.println(maxTreeId + "," + maxNodes);
            }
        } catch (Exception e) {
            try (PrintWriter writer = new PrintWriter(new File("output.csv"))) {
                writer.println("0,0");
            }
        }
    }

}
