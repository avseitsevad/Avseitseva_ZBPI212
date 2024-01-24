import java.util.ArrayList;
import java.util.List;

public class Tree {
    private TreeNode root;

    public Tree(TreeNode root) {
        this.root = root;
    }

    public TreeNode getRoot() {
        return root;
    }

    public void insertNode(int id, int parentId) {
        if (root == null) {
            root = new TreeNode(id, parentId);
        }

        TreeNode parentNode = findNode(root, parentId);
        if (parentNode != null) {
            parentNode.addChild(new TreeNode(id, parentId));
        }
    }

    private TreeNode findNode(TreeNode current, int id) {
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

    public List<TreeNode> getNodes() {
        List<TreeNode> nodes = new ArrayList<>();
        getNodesRecursive(root, nodes);
        return nodes;
    }

    private void getNodesRecursive(TreeNode current, List<TreeNode> nodes) {
        nodes.add(current);
        for (TreeNode child : current.getChildNodes()) {
            getNodesRecursive(child, nodes);
        }
    }

    public List<TreeNode> getLeaves() {
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
    // получение узлов на расстоянии n переходов от корня
    public int getNodesAtDepth(int depth) {
        return getNodesAtDepthRecursive(root, depth, 0);
    }

    private int getNodesAtDepthRecursive(TreeNode node, int depth, int currentDepth) {
        if (node == null) {
            return 0;
        }
        if (currentDepth == depth) {
            return 1;
        }
        int count = 0;
        for (TreeNode child : node.getChildNodes()) {
            count += getNodesAtDepthRecursive(child, depth, currentDepth + 1);
        }
        return count;
    }

}
