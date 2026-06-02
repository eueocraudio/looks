import sys;
import gc;
import os;
import signal;
import subprocess;
import time;
from pathlib import Path;
from dotenv import load_dotenv;
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton;
from PySide6.QtGui import QAction;
from open import OpenWindow;
from create import CreateWindow;

load_dotenv(Path(__file__).parent.parent / ".env");
APPLICATION_PATH = os.getenv("APPLICATION_PATH", "./application/run.py");


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__();
        self.setWindowTitle("looks");
        self.setFixedSize(850, 450);
        self.active_path = None;
        self.child_process = None;
        self._build_menu();
        self._build_central();

    def _build_menu(self):
        menu_bar = self.menuBar();

        file_menu = menu_bar.addMenu("File");

        open_action = QAction("Open", self);
        create_action = QAction("Create", self);
        close_action = QAction("Close", self);

        open_action.triggered.connect(self._open_open_window);
        create_action.triggered.connect(self._open_create_window);
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

    def _build_central(self):
        central = QWidget();
        layout = QVBoxLayout(central);

        panic_layout = QHBoxLayout();
        panic_layout.addStretch();
        self.panic_button = QPushButton("PANIC");
        self.panic_button.setFixedSize(180, 180);
        self.panic_button.setEnabled(False);
        self.panic_button.setStyleSheet(
            "QPushButton:enabled { background-color: #cc0000; color: white; font-size: 28px; font-weight: bold; border-radius: 90px; }"
            "QPushButton:enabled:pressed { background-color: #880000; }"
            "QPushButton:disabled { background-color: #888888; color: #cccccc; font-size: 28px; font-weight: bold; border-radius: 90px; }"
        );
        self.panic_button.clicked.connect(self._panic);
        panic_layout.addWidget(self.panic_button);
        panic_layout.addStretch();

        btn_layout = QHBoxLayout();
        btn_layout.addStretch();
        self.open_app_button = QPushButton("Open Application");
        self.open_app_button.setEnabled(False);
        self.open_app_button.clicked.connect(self._launch_application);
        btn_layout.addWidget(self.open_app_button);

        self.close_app_button = QPushButton("Close Application");
        self.close_app_button.setEnabled(False);
        self.close_app_button.clicked.connect(self._close_child_process);
        btn_layout.addWidget(self.close_app_button);

        layout.addStretch();
        layout.addLayout(panic_layout);
        layout.addStretch();
        layout.addLayout(btn_layout);

        self.setCentralWidget(central);

    def _open_create_window(self):
        dialog = CreateWindow(self);
        if dialog.exec() and dialog.result_path:
            self.active_path = dialog.result_path;
            self.panic_button.setEnabled(True);
            self.open_app_button.setEnabled(True);

    def _open_open_window(self):
        dialog = OpenWindow(self);
        if dialog.exec() and dialog.result_path:
            self.active_path = dialog.result_path;
            self.panic_button.setEnabled(True);
            self.open_app_button.setEnabled(True);

    def _launch_application(self):
        if self.active_path and Path(self.active_path).is_dir():
            sudo_user = os.getenv("SUDO_USER", os.getenv("USER"));
            self.child_process = subprocess.Popen(
                ["runuser", "-u", sudo_user, "--", "python3", APPLICATION_PATH, self.active_path],
                start_new_session=True
            );
            self.close_app_button.setEnabled(True);

    def _panic(self):
        if self.child_process and self.child_process.poll() is None:
            os.killpg(os.getpgid(self.child_process.pid), signal.SIGKILL);
            self.child_process = None;
        if self.active_path:
            name = Path(self.active_path).name;
            script = Path(__file__).parent.parent / "bash" / "close.sh";
            for _ in range(5):
                try:
                    subprocess.run(["sudo", str(script), self.active_path, name]);
                    if Path(self.active_path).exists() and not Path(self.active_path).is_mount():
                        subprocess.run(["rm", "-r", self.active_path]);
                    time.sleep(1);
                except Exception:
                    pass;
        self.panic_button.setEnabled(False);
        self.open_app_button.setEnabled(False);
        self.close_app_button.setEnabled(False);

    def _close_child_process(self):
        if self.child_process and self.child_process.poll() is None:
            self.child_process.terminate();
            self.child_process = None;
            self.close_app_button.setEnabled(False);

    def _close_app(self):
        self.close();
        gc.collect();
        QApplication.instance().quit();

    def _show_about(self):
        QMessageBox.about(self, "About looks", "looks\nGerenciador de sistemas de arquivos LUKS.");


def main():
    if os.getuid() != 0:
        app = QApplication(sys.argv);
        QMessageBox.critical(None, "Permissão negada", "Este programa deve ser executado como superusuário (sudo).");
        sys.exit(1);

    app = QApplication(sys.argv);
    window = MainWindow();
    window.show();
    sys.exit(app.exec());


if __name__ == "__main__":
    main();
