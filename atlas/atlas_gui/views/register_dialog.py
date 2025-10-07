from __future__ import annotations
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from atlas.atlas_gui.services.settings_service import create_user

class RegisterDialog(QDialog):
    registered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Account")
        self.setModal(True)
        self.resize(420, 180)

        self.le_user = QLineEdit()
        self.le_pass = QLineEdit()
        self.lbl_user = QLabel("Username:")
        self.lbl_pass = QLabel("Password:")
        self.btn_create = QPushButton("Create")
        self.btn_cancel = QPushButton("Cancel")

        self.le_user.setPlaceholderText("Enter username")
        self.le_pass.setPlaceholderText("Enter password")
        self.le_user.setMinimumWidth(240)
        self.le_pass.setMinimumWidth(240)
        self.le_user.setClearButtonEnabled(True)
        self.le_pass.setClearButtonEnabled(True)
        self.le_pass.setEchoMode(QLineEdit.EchoMode.Password)

        field_css = "QLineEdit { border: 1px solid palette(mid); border-radius: 6px; padding: 4px; }"
        self.le_user.setStyleSheet(field_css)
        self.le_pass.setStyleSheet(field_css)

        row_u = QHBoxLayout()
        row_u.addWidget(self.lbl_user)
        row_u.addWidget(self.le_user, 1)

        row_p = QHBoxLayout()
        row_p.addWidget(self.lbl_pass)
        row_p.addWidget(self.le_pass, 1)

        row_btn = QHBoxLayout()
        row_btn.addStretch(1)
        row_btn.addWidget(self.btn_cancel)
        row_btn.addWidget(self.btn_create)

        layout = QVBoxLayout(self)
        layout.addLayout(row_u)
        layout.addLayout(row_p)
        layout.addLayout(row_btn)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_create.clicked.connect(self.on_create)


    def on_create(self):
        u = self.le_user.text().strip().lower()
        p = self.le_pass.text().strip()
        if not u or not p:
            QMessageBox.warning(self, "Invalid", "Please enter username and password.")
            return
        if create_user(u, p):
            QMessageBox.information(self, "Success", f"User '{u}' created.")
            self.registered.emit(u)
            self.accept()
        else:
            QMessageBox.warning(self, "Exists", f"User '{u}' already exists.")