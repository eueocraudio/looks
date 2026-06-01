import sys;
import gc;
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox;
from PySide6.QtGui import QAction;


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__();
        self.setWindowTitle("looks");
        self.setFixedSize(850, 450);
        self._build_menu();

    def _build_menu(self):
        menu_bar = self.menuBar();

        file_menu = menu_bar.addMenu("File");

        open_action = QAction("Open", self);
        create_action = QAction("Create", self);
        close_action = QAction("Close", self);

        close_action.triggered.connect(self._close_app);

        file_menu.addAction(open_action);
        file_menu.addAction(create_action);
        file_menu.addSeparator();
        file_menu.addAction(close_action);

        particao_menu = menu_bar.addMenu("Partition");

        resize_action = QAction("Resize", self);
        change_secret_action = QAction("Change Secret", self);
        close_particao_action = QAction("Close", self);

        close_particao_action.triggered.connect(self.close);

        particao_menu.addAction(resize_action);
        particao_menu.addAction(change_secret_action);
        particao_menu.addSeparator();
        particao_menu.addAction(close_particao_action);

        about_menu = menu_bar.addMenu("About");

        about_action = QAction("About looks", self);
        about_action.triggered.connect(self._show_about);

        about_menu.addAction(about_action);

    def _close_app(self):
        self.close();
        gc.collect();
        QApplication.instance().quit();

    def _show_about(self):
        QMessageBox.about(self, "About looks", "looks\nGerenciador de sistemas de arquivos LUKS.");


def main():
    app = QApplication(sys.argv);
    window = MainWindow();
    window.show();
    sys.exit(app.exec());


if __name__ == "__main__":
    main();
