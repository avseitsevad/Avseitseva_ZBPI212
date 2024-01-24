package org.example;

import javax.swing.*;
import java.awt.*;
import java.util.List;
import java.sql.SQLException;
import java.util.stream.Collectors;


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
            sb.append("Дочерние узлы: ").append(treeStructure.getChildNodes()).append("\n");

            for (TreeNode node : treeStructure.getNonRootNodes()) {
                sb.append("Узел: ").append(node.getId())
                        .append(", Родитель: ").append(node.getParentId())
                        .append(", Потомки: ").append(node.getChildNodes().stream().map(TreeNode::getId).collect(Collectors.toList())).append("\n");
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
                sb.append("Tree ID: ").append(tree.getRoot().getId()).append("\n");
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
