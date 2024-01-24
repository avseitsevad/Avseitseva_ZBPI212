package org.example;

import java.util.ArrayList;
import java.util.List;

public class TreeStructure {
    private TreeNode root;
    List<TreeNode> childNodes;
    public TreeStructure(Tree tree) {
        this.root = tree.getRoot();
        this.childNodes = tree.getNodes();
    }

    public int getRootId() {
        return root.getId();
    }

    public List<Integer> getChildNodes() {
        List<Integer> nodes = new ArrayList<>();
        for (TreeNode node : childNodes){
            nodes.add(node.getId());
        }
        return nodes;
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
