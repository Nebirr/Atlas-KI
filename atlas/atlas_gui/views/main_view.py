from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QPlainTextEdit, QLineEdit
from atlas.help_cmd import matches_help
from atlas.atlas_gui.views.help_dialog import HelpDialog
from atlas.atlas_gui.views.system_info_dialog import SystemInfoDialog

class MainView(QWidget):

    logout_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        self.title = QLabel("Atlas")
        self.title.setStyleSheet("font-size: 22px; font-weight: 600;")

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText(" ...")

        row_input = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask a Question or give me a Task ...")
        btn_send = QPushButton("Send")
        btn_send.clicked.connect(self._on_send)
        self.input.returnPressed.connect(btn_send.click)

        btn_help = QPushButton("Help")
        btn_help.clicked.connect(self._open_help)
        
        btn_sysinfo = QPushButton("System Info")
        btn_sysinfo.clicked.connect(self.open_system_info_dialog)

        row_input.addWidget(self.input)
        row_input.addWidget(btn_send)
        row_input.addWidget(btn_help)
        row_input.addWidget(btn_sysinfo)

        row = QHBoxLayout()
        row.addStretch(1)
        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(self.logout_requested.emit)
        row.addWidget(btn_logout)


        layout.addWidget(self.title)
        layout.addWidget(self.log)
        layout.addLayout(row_input)   
        layout.addStretch(1)
        layout.addLayout(row)

        self._atlas = None
    
    def open_system_info_dialog(self):
        if not hasattr(self, "_sysinfo_dlg") or self._sysinfo_dlg is None:
            self._sysinfo_dlg = SystemInfoDialog(self)
            self._sysinfo_dlg.destroyed.connect(lambda: setattr(self, "_sysinfo_dlg", None))
        self._sysinfo_dlg.show()
        self._sysinfo_dlg.raise_()
        self._sysinfo_dlg.activateWindow()

    def _open_help(self) -> None:
        dlg = HelpDialog(self)
        dlg.exec()

    def _append(self, text: str, role: str = "sys") -> None:
        if role == "user":
           prefix = "🧑 [USER] "
        else:
           prefix = "🤖 [ATLAS] "
        
        if text:
            self.log.appendPlainText(f"{prefix}{text}")
            self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())

    def set_username(self, name: str) -> None:
        self.title.setText(f"Atlas - Menu (User: {name})")
    
    def set_atlas_service(self, atlas_service) -> None:
        self._atlas = atlas_service

    def _on_send(self) -> None:
        cmd = self.input.text().strip()
        self.input.clear()
        if not cmd:
            return
        self._append(cmd, role="user")

        if matches_help(cmd.lower()):
            self._open_help()
            return

        if not self._atlas:
            self._append("Atlas-Service not connected.", role="sys")
            return

        out = self._atlas.process_command(cmd)
        if out:
            self._append(out, role="sys")