import java.util.ArrayList;
import java.util.List;

public class TreeNode {
    private int id; // id узла
    private int parentId; // id родительского узла
    private List<TreeNode> childNodes; // список дочерних узлов

    public TreeNode(int id, int parentId) {
        this.id = id;
        this.parentId = parentId;
        this.childNodes = new ArrayList<>();
    }

    public int getId() {
        return id;
    }

    public int getParentId() {
        return parentId;
    }

    public List<TreeNode> getChildNodes() {
        return childNodes;
    }

    public boolean isLeaf() {
        return childNodes.isEmpty();
    }

    public boolean isRoot() {
        return parentId == id;
    }

    public void addChild(TreeNode childNode) {
        childNodes.add(childNode);
    }
}
