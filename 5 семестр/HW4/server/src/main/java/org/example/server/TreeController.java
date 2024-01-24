package org.example.server;

import jakarta.persistence.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.jpa.repository.*;
import org.springframework.data.jpa.repository.Query;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.ArrayList;

@RestController
@RequestMapping("/trees")
public class TreeController {
	private final TreeService treeService;

	@Autowired
	public TreeController(TreeService treeService) {
		this.treeService = treeService;
	}

	@GetMapping
	public ResponseEntity<List<TreeEntity>> getAllTrees() {
		return ResponseEntity.ok(treeService.getAllTrees());
	}

	@GetMapping("/{rootId}")
	public ResponseEntity<TreeEntity> getTreeStructure(@PathVariable long rootId) {
		TreeEntity treeStructure = treeService.getTreeStructure(rootId);
		if (treeStructure == null) {
			return ResponseEntity.notFound().build();
		}
		return ResponseEntity.ok(treeStructure);
	}

	@PostMapping
	public ResponseEntity<Void> addTree(@RequestBody TreeEntity root) {
		treeService.addTree(root);
		return ResponseEntity.ok().build();
	}

	@DeleteMapping("/{nodeId}")
	public ResponseEntity<Void> deleteNode(@PathVariable long nodeId) {
		treeService.deleteNode(nodeId);
		return ResponseEntity.ok().build();
	}

	@PostMapping("/{parentId}/addChild")
	public ResponseEntity<Void> addChildNode(@PathVariable int parentId, @RequestBody int childId) {
		treeService.addChildNode(parentId, childId);
		return ResponseEntity.ok().build();
	}
}


@Entity
@Table(name = "TREES")
class TreeEntity {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long primaryId;

	@Column(name = "id")
	private Integer id;

	@Column(name = "parent_id")
	private Integer parentId;

	// Геттеры
	public Long getPrimaryId() {
		return primaryId;
	}

	public Integer getId() {
		return id;
	}

	public Integer getParentId() {
		return parentId;
	}

	// Сеттеры
	public void setPrimaryId(Long primaryId) {
		this.primaryId = primaryId;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public void setParentId(Integer parentId) {
		this.parentId = parentId;
	}
}


@Repository
interface TreeRepository extends JpaRepository<TreeEntity, Long> {
	@Query("SELECT t.id FROM TreeEntity t WHERE t.parentId IS NULL OR t.parentId = t.id")
	List<Integer> findRootNodeIds();
}


@Service
class TreeService {
	private final TreeRepository treeRepository;

	@Autowired
	public TreeService(TreeRepository treeRepository) {
		this.treeRepository = treeRepository;
	}

	public List<TreeEntity> getAllTrees() {
		return treeRepository.findAll();
	}

	public TreeEntity getTreeStructure(Long primaryId) {
		return treeRepository.findById(primaryId).orElse(null);
	}

	public void deleteNode(Long primaryId) {
		treeRepository.deleteById(primaryId);
	}

	public void addChildNode(Integer parentId, Integer childId) {
		TreeEntity childNode = new TreeEntity();
		childNode.setId(childId);
		childNode.setParentId(parentId);
		treeRepository.save(childNode);
	}

	public void addTree(TreeEntity treeEntity) {
		treeRepository.save(treeEntity);
	}

	public List<Integer> getRootNodeIds() {
		return treeRepository.findRootNodeIds();
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

