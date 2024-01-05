import java.io.*;
import java.util.*;

public class Main {

    public static List<Tree> readInput(String fileName) throws Exception {
        List<Tree> trees = new ArrayList<>();
        Tree currentTree = null;

        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            String line;
            while ((line = br.readLine()) != null) {
                line = line.replace("\"", "");
                String[] parts = line.split(",");
                int nodeId = Integer.parseInt(parts[0].trim());
                int parentId = Integer.parseInt(parts[1].trim());

                if (nodeId == parentId) {
                    // Начинаем новое дерево, если childId равен parentId
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

    public static int[] maxLeavesTree(List<Tree> trees) throws Exception {
        // метод для нахождения дерева с макс кол-вом листов
        int maxLeaves = 0;
        int maxLeavesTreeId = 0;
        boolean multipleMax = false;
        for (Tree tree : trees) {
            int leaves = tree.getLeaves().size();
            if (leaves > maxLeaves) {
                maxLeaves = leaves;
                maxLeavesTreeId = tree.getRoot().getID();
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

    public static void main(String[] args) throws Exception {
        List<Tree> trees = readInput("input.csv");
        try {
            int[] maxTreeData = maxLeavesTree(trees);
            int maxTreeId = maxTreeData[0];
            int maxLeaves = maxTreeData[1];
            // записываем дерево с макс. кол-вом листов в файл вывода
            try (PrintWriter writer = new PrintWriter(new File("output.csv"))) {
                writer.println(maxTreeId + "," + maxLeaves);
            }
        } catch (Exception e) {
            // если было вызвано исключение, то записываем 0,0
            try (PrintWriter writer = new PrintWriter(new File("output.csv"))) {
                writer.println("0,0");
            }
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