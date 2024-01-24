package org.example;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import javafx.scene.layout.HBox;

public class TreeAppFX extends Application {

    private TreeService treeService;
    private TextArea textArea;

    @Override
    public void start(Stage primaryStage) {
        treeService = new TreeService(new H2Connection());

        // Создание основного макета
        BorderPane root = new BorderPane();

        // Текстовая область для отображения информации
        textArea = new TextArea();
        textArea.setEditable(false);
        root.setCenter(textArea);

        // Панель с кнопками
        HBox buttonPanel = new HBox(10);
        Button showTreesButton = new Button("Показать список всех деревьев");
        Button readFromDBButton = new Button("Прочитать список всех деревьев из БД");
        Button writeToDBButton = new Button("Записать список всех деревьев в БД");
        Button deleteNodeButton = new Button("Удалить узел из дерева");
        Button addChildButton = new Button("Добавить узел-потомок текущего узла");

        // Добавление кнопок на панель
        buttonPanel.getChildren().addAll(showTreesButton, readFromDBButton, writeToDBButton, deleteNodeButton, addChildButton);
        root.setTop(buttonPanel);

        // Обработчики событий для кнопок
        showTreesButton.setOnAction(e -> showTreeList());
        readFromDBButton.setOnAction(e -> readTreesFromDB());
        writeToDBButton.setOnAction(e -> writeTreesToDB());
        deleteNodeButton.setOnAction(e -> deleteNode());
        addChildButton.setOnAction(e -> addChild());

        // Создание и отображение сцены
        Scene scene = new Scene(root, 800, 600);
        primaryStage.setTitle("Tree Application");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    private void showTreeList() {
        // Ваша логика для показа списка деревьев
    }

    private void readTreesFromDB() {
        // Ваша логика для чтения деревьев из БД
    }

    private void writeTreesToDB() {
        // Ваша логика для записи деревьев в БД
    }

    private void deleteNode() {
        // Ваша логика для удаления узла из дерева
    }

    private void addChild() {
        // Ваша логика для добавления узла-потомка текущего узла
    }

    public static void main(String[] args) {
        launch(args);
    }
}
