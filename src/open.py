from pathlib import Path;
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QMessageBox;
from PySide6.QtCore import QDir;

PROJECT_ROOT = Path(__file__).parent.parent;


class OpenWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent);
        self.setWindowTitle("Open");
        self.setFixedSize(400, 400);
        self.result_path = None;
        self._build_ui();

    def _build_ui(self):
        layout = QVBoxLayout(self);

        file_layout = QHBoxLayout();
        file_label = QLabel("Arquivo .img:");
        self.file_input = QLineEdit();
        self.file_input.setPlaceholderText("Selecione um arquivo .img...");
        self.file_input.setReadOnly(True);
        browse_button = QPushButton("Procurar");
        browse_button.clicked.connect(self._browse_file);

        file_layout.addWidget(file_label);
        file_layout.addWidget(self.file_input);
        file_layout.addWidget(browse_button);

        layout.addLayout(file_layout);

        shell_label = QLabel("Execute no shell:");
        self.shell_output = QTextEdit();
        self.shell_output.setReadOnly(True);

        layout.addWidget(shell_label);
        layout.addWidget(self.shell_output);

        btn_layout = QHBoxLayout();
        btn_layout.addStretch();
        abrir_button = QPushButton("Continue");
        abrir_button.clicked.connect(self._on_continue);
        btn_layout.addWidget(abrir_button);

        layout.addLayout(btn_layout);

    def _browse_file(self):
        dialog = QFileDialog(self, "Selecionar arquivo .img", "/home/");
        dialog.setNameFilter("Imagens LUKS (*.img)");
        dialog.setFilter(dialog.filter() | QDir.Filter.Hidden);
        path = dialog.selectedFiles()[0] if dialog.exec() else None;
        if path:
            self.file_input.setText(path);
            name = Path(path).stem;
            cmd = (
                f"echo -n \"SENHA\" | sudo /usr/sbin/cryptsetup open --type luks {path} {name}\n"
                f"sudo mkdir -p /tmp/{name}\n"
                f"sudo mount /dev/mapper/{name} /tmp/{name}"
            );
            self.shell_output.setPlainText(cmd);

    def _on_continue(self):
        path = self.file_input.text();
        if path:
            name = Path(path).stem;
            tmp_path = f"/tmp/{name}";
            if not Path(tmp_path).is_mount():
                QMessageBox.warning(self, "Volume não montado", "Execute o comando no shell antes de continuar.");
                return;
            self.result_path = tmp_path;
            self.accept();
