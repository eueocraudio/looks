from pathlib import Path;
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit;
from PySide6.QtGui import QRegularExpressionValidator;
from PySide6.QtCore import QRegularExpression;

PROJECT_ROOT = Path(__file__).parent.parent;


class CreateWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent);
        self.setWindowTitle("Create");
        self.setFixedSize(400, 400);
        self.result_path = None;
        self._build_ui();

    def _build_ui(self):
        layout = QVBoxLayout(self);

        name_layout = QHBoxLayout();
        name_label = QLabel("Name:");
        self.name_input = QLineEdit();
        self.name_input.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Z]+")));
        self.name_input.textChanged.connect(self._update_shell_command);
        name_layout.addWidget(name_label);
        name_layout.addWidget(self.name_input);

        layout.addLayout(name_layout);

        shell_label = QLabel("Execute no shell:");
        self.shell_output = QTextEdit();
        self.shell_output.setReadOnly(True);

        layout.addWidget(shell_label);
        layout.addWidget(self.shell_output);

        btn_layout = QHBoxLayout();
        btn_layout.addStretch();
        criar_button = QPushButton("Continue");
        criar_button.clicked.connect(self._on_continue);
        btn_layout.addWidget(criar_button);

        layout.addLayout(btn_layout);

    def _update_shell_command(self, name):
        cmd = f"sudo {PROJECT_ROOT}/bash/create.sh {name}" if name else "";
        self.shell_output.setPlainText(cmd);

    def _on_continue(self):
        name = self.name_input.text();
        tmp_path = f"/tmp/{name}";
        if Path(tmp_path).is_dir():
            self.result_path = tmp_path;
            self.accept();
