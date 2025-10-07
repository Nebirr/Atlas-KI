import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QStatusBar

from atlas.atlas_gui.views.login_view import LoginView
from atlas.atlas_gui.views.main_view import MainView
from atlas.atlas_gui.services.auth_service import AuthService
from atlas.atlas_gui.services.atlas_service import AtlasService

from atlas.atlas_gui.services.settings_service import load_settings, save_settings, UserSettings

from PySide6.QtGui import QIcon
from pathlib import Path

#Start

class AtlasWindow(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Atlas")
        self.resize(640,400)

        icon_path = Path("assets/icons/atlas_icon.ico")
        self.setWindowIcon(QIcon(str(icon_path)))

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_view = LoginView()
        self.main_view = MainView()
        self.atlas = AtlasService()
        self.main_view.set_atlas_service(self.atlas)
        self.main_view.logout_requested.connect(self.goto_login)
        
        self.auth =AuthService()
        self.login_view.set_auth_service(self.auth)

        self.stack.addWidget(self.login_view)
        self.stack.addWidget(self.main_view)
        self.stack.setCurrentIndex(0)

        self.login_view.login_success.connect(self.goto_main)

        self.username: str | None = None
    
    def goto_main(self, username: str) -> None:
        self.username = username
        self.main_view.set_username(username)
        self.status.showMessage(f"Logged in as: {username}", 3000)
        s = load_settings(username)
        self.resize(s.window_width, s.window_height)
        self.stack.setCurrentIndex(1)

    def goto_login(self) -> None:
        self.stack.setCurrentIndex(0)
        self.status.showMessage("Logged out", 2000)
        self.username = None

    def closeEvent(self, event) -> None:
        if self.username:
            s = load_settings(self.username)
            s.window_width, s.window_height = self.width(), self.height()
            save_settings(self.username, s)
        super().closeEvent(event)

def main() -> int:
    app = QApplication(sys.argv)
    window = AtlasWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())