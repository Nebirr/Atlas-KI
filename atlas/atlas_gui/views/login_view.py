from PySide6.QtCore import Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (QFormLayout, QVBoxLayout, QLabel, QWidget, QGraphicsOpacityEffect, 
                               QLineEdit,  
                               QPushButton, QCheckBox
                               )
from atlas.atlas_gui.views.register_dialog import RegisterDialog
from atlas.atlas_gui.views.reset_password_dialog import ResetPasswordDialog

class LoginView(QWidget):
    login_success= Signal(str)

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        # Title + Subtitle
        title = QLabel("Login")
        title.setStyleSheet("font-size: 22px; font-weight: 600;")
        subtitle = QLabel("Enter Username and Password")
        subtitle.setWordWrap(True)

        # Formular
        form = QFormLayout()
        self.input_user = QLineEdit()
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Username:", self.input_user)
        form.addRow("Password:", self.input_pass)

        # Status-Label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 12px;")
        self.status_opacity = QGraphicsOpacityEffect(self.status_label)
        self.status_label.setGraphicsEffect(self.status_opacity)
        self.status_opacity.setOpacity(0.0)
       
        # Show-Password
        self.chk_show = QCheckBox("Show Password")
        self.chk_show.toggled.connect(
            lambda checked: self.input_pass.setEchoMode(
                QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password      
            )
        )

        # Login-Button
        self.btn_login = QPushButton("Login")
        self.btn_login.setEnabled(False)
        self.btn_login.clicked.connect(self._on_login_clicked)

        # Register-Button
        self.btn_register = QPushButton("Register")
        self.btn_register.clicked.connect(self.open_register_dialog)

        self.btn_reset_pw = QPushButton("Reset Password")
        self.btn_reset_pw.clicked.connect(self.open_reset_dialog)

        # Layout
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(form)
        layout.addWidget(self.status_label)
        layout.addWidget(self.chk_show)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_register)
        layout.addWidget(self.btn_reset_pw)
        layout.addStretch(1)

        # UX: Placeholder
        self.input_user.setPlaceholderText("Username")
        self.input_pass.setPlaceholderText("Password")
        self.input_user.returnPressed.connect(self.input_pass.setFocus)
        self.input_pass.returnPressed.connect(self.btn_login.click)

        # Button-Enable-Logik
        self.input_user.textChanged.connect(self._update_btn_state)
        self.input_pass.textChanged.connect(self._update_btn_state)

        # Timer + Animation for Status-Fade
        self.status_timer = QTimer(self)
        self.status_timer.setSingleShot(True)
        self.status_timer.timeout.connect(self._fade_out_status)
    
        self.fade_anim = QPropertyAnimation(self.status_opacity, b"opacity", self)
        self.fade_anim.setDuration(450)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Auth-Service placed from Outside
        self._auth = None

    #-----------------------------
    # Outside (__init__)
    #-----------------------------
    
    def open_register_dialog(self):
        dlg = RegisterDialog(self)
        dlg.registered.connect(self.on_registered)
        dlg.exec()

    def on_registered(self, username: str):
        self.input_user.setText(username)
        self.input_pass.setFocus()
        self._update_btn_state()
    
    def open_reset_dialog(self):
        dlg = ResetPasswordDialog(self)
        dlg.le_user.setText(self.input_user.text().strip())
        dlg.reset_done.connect(self.on_reset_done)
        dlg.exec()

    def on_reset_done(self, username: str):
        self.input_user.setText(username)
        self.input_pass.clear()
        self.input_pass.setFocus()
        self._show_status("Password reset. Please log in.", "#2e7d32", visible_ms=3000)

    def set_auth_service(self, auth) -> None:
        self._auth = auth

    def _update_btn_state(self) -> None:
        self.btn_login.setEnabled(bool(self.input_user.text().strip() and self.input_pass.text().strip()))  

    def _show_status(self, text: str, color_hex: str, visible_ms: int = 3000) -> None:
        
            self.status_label.setText(text)
            self.status_label.setStyleSheet(f"color: {color_hex}; font-size: 12px;")

            self.fade_anim.stop()
            self.status_timer.stop()

            self.status_opacity.setOpacity(0.0)
            self.fade_anim.setStartValue(0.0)
            self.fade_anim.setEndValue(1.0)
            self.fade_anim.start()

            self.status_timer.start(max(0, visible_ms))


    def _fade_out_status(self) -> None:

        self.fade_anim.stop()
        self.fade_anim.setStartValue(self.status_opacity.opacity())
        self.fade_anim.setEndValue(0.0)

        def _clear():
            self.status_label.clear()
            try:    
                self.fade_anim.finished.disconnect(_clear)
            except TypeError:
                pass
        
        self.fade_anim.finished.connect(_clear)
        self.fade_anim.start()

    def _clear_status_immediately(self) -> None:
        self.status_timer.stop()
        self.fade_anim.stop()
        self.status_opacity.setOpacity(0.0)
        self.status_label.clear()

    def _on_login_clicked(self) -> None:

        user = self.input_user.text().strip()
        pw = self.input_pass.text().strip()

        if self._auth.verify(user, pw):
            self._show_status("Login succeeded", "#2e7d32", visible_ms=600)

            QTimer.singleShot(600, lambda:(
                self.login_success.emit(user),
                self.input_pass.clear(),
                self._clear_status_immediately()
             ))

        else:
            self._show_status("Invalid username or password", "#c62828", visible_ms=3000)
            self.input_pass.selectAll()
            self.input_pass.setFocus()