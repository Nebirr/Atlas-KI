from __future__ import annotations
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
    )
from atlas.atlas_gui.services.settings_service import user_exists, set_user_password, verify_user


class ResetPasswordDialog(QDialog):
    reset_done = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reset Password")
        self.setModal(True)
        self.resize(500, 260)

        self.le_user = QLineEdit()
        self.le_user.setPlaceholderText("Username")
        self.le_user.setMinimumWidth(280)
        self.le_user.setClearButtonEnabled(True)

        self.le_old = QLineEdit()
        self.le_old.setPlaceholderText("Current password")
        self.le_old.setMinimumWidth(280)
        self.le_old.setClearButtonEnabled(True)
        self.le_old.setEchoMode(QLineEdit.EchoMode.Password)

        self.le_new = QLineEdit()
        self.le_new.setPlaceholderText("New Password")
        self.le_new.setMinimumWidth(280)
        self.le_new.setClearButtonEnabled(True)
        self.le_new.setEchoMode(QLineEdit.EchoMode.Password)

        self.le_new2 = QLineEdit()
        self.le_new2.setPlaceholderText("New password (repeat)")
        self.le_new2.setMinimumWidth(280)
        self.le_new2.setClearButtonEnabled(True)
        self.le_new2.setEchoMode(QLineEdit.EchoMode.Password)

        self.lbl_user = QLabel("Username:")
        self.lbl_old  = QLabel("Current:")
        self.lbl_new = QLabel("New Password:")
        self.lbl_new2 = QLabel("Confirm Password:")

        self.btn_apply = QPushButton("Apply")
        self.btn_cancel = QPushButton("Cancel")

        row_u = QHBoxLayout(); row_u.addWidget(self.lbl_user); row_u.addWidget(self.le_user, 1)
        row_o = QHBoxLayout(); row_o.addWidget(self.lbl_old ); row_o.addWidget(self.le_old , 1)
        row_n = QHBoxLayout(); row_n.addWidget(self.lbl_new); row_n.addWidget(self.le_new, 1)
        row_c = QHBoxLayout(); row_c.addWidget(self.lbl_new2); row_c.addWidget(self.le_new2, 1)
        row_btn = QHBoxLayout(); row_btn.addStretch(1); row_btn.addWidget(self.btn_cancel); row_btn.addWidget(self.btn_apply)

        layout = QVBoxLayout(self)
        layout.addLayout(row_u)
        layout.addLayout(row_o)
        layout.addLayout(row_n)
        layout.addLayout(row_c)
        layout.addLayout(row_btn)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_apply.clicked.connect(self.on_apply)

        self.le_user.returnPressed.connect(self.le_old.setFocus)
        self.le_old.returnPressed.connect(self.le_new.setFocus)
        self.le_new.returnPressed.connect(self.le_new2.setFocus)
        self.le_new2.returnPressed.connect(self.on_apply)

    def on_apply(self):
        u = self.le_user.text().strip().lower()
        old = self.le_old.text().strip()
        new = self.le_new.text().strip()
        rep = self.le_new2.text().strip()


        if not u or not old or not new or not rep:
            QMessageBox.warning(self, "Invalid", "Please fill in all fields.")
            return
        if not user_exists(u):
            QMessageBox.warning(self, "Unknown user", f"User '{u}' does not exist.")
            return
        if not verify_user(u, old):
            QMessageBox.warning(self, "Wrong password", "Current password is incorrect.")
            self.le_old.selectAll(); self.le_old.setFocus()
            return

        if len(new) < 4:
            QMessageBox.warning(self, "Too short", "New password must be at least 4 characters.")
            self.le_new.selectAll(); self.le_new.setFocus()
            return
        if new != rep:
            QMessageBox.warning(self, "Mismatch", "New passwords do not match.")
            self.le_new2.selectAll(); self.le_new2.setFocus()
            return
        if new == old:
            QMessageBox.warning(self, "No change", "New password must be different from current.")
            self.le_new.selectAll(); self.le_new.setFocus()
            return

        if set_user_password(u, new):
            QMessageBox.information(self, "Success", f"Password for '{u}' updated.")
            self.reset_done.emit(u)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Could not update the password.")