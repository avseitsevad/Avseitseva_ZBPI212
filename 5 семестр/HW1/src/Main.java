import java.io.*;
import java.util.*;

public class Main {

    public static List<Tree> readInput(String fileName) throws Exception {
        //метод для чтения деревьев из файла
        List<Tree> trees = new ArrayList<>(); //список для деревьев

        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            String line;
            while ((line = br.readLine()) != null) {
                line = line.replace("\"","");
                String[] parts = line.split(",");
                int nodeId = Integer.parseInt(parts[0].trim());
                int parentId = Integer.parseInt(parts[1].trim());
                //читаем строки из файла, разбиваем их, удаляем возможные кавычки
                if (nodeId == parentId) {
                    // в случае, если узел=корень, создаем новое дерево
                    TreeNode node = new TreeNode(nodeId);
                    Tree tree = new Tree(node);
                    trees.add(tree);
                } else {
                    //в обратном случае добавляем узел к дереву с соответствующим корнем
                    for (Tree tree : trees){
                        if (tree.getRoot().getID() == parentId){
                            tree.insertNode(nodeId);
                        }

                    }
                }
            }
        }

        return trees;
    }
    public static int[] maxLeavesTree (List<Tree> trees) throws Exception {
        //метод для нахождения дерева с макс кол-вом листов
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
            //генерируем исключение в случае, если деревьев с макс. кол-вом листов несколько
            throw new Exception("Несколько деревьев с максимальным количеством листьев");
        }
        return new int[] {maxLeavesTreeId, maxLeaves};
    }
    public static void main(String[] args) throws Exception {
        List<Tree> trees = readInput("input.csv");
        try {
            int[] maxTreeData = maxLeavesTree(trees);
            int maxTreeId = maxTreeData[0];
            int maxLeaves = maxTreeData[1];
            //записываем дерево с макс. кол-вом листов в файл вывода
            try (PrintWriter writer = new PrintWriter(new File("output.csv"))) {
                writer.println(maxTreeId + "," + maxLeaves);
            }
        } catch (Exception e) {
            //если было вызвано исключение, то записываем 0,0
            try (PrintWriter writer = new PrintWriter(new File("output.csv"))) {
                writer.println("0,0");
            }
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