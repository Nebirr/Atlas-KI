from __future__ import annotations
from PySide6.QtWidgets import (
    QDialog, QTabWidget, QVBoxLayout, QTableWidget, QWidget, QLineEdit,
    QTableWidgetItem, QHBoxLayout, QLabel
)
from PySide6.QtCore import Qt

from atlas.help_cmd import COMMANDS
from atlas.lists import WEBSITES, PROGRAMME

class HelpDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Atlas - Help")
        self.resize(800, 540)

        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        #--- Tab 1: Commands ---
        self.cmd_tab = QWidget()
        self._cmd_filter = QLineEdit()
        self._cmd_filter.setPlaceholderText("Filter commands...")
        self._cmd_table = QTableWidget(0, 4)
        self._cmd_table.setHorizontalHeaderLabels(["Category", "Command", "Description", "Example"])
        self._cmd_table.horizontalHeader().setStretchLastSection(True)
        self._cmd_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._cmd_table.setSelectionBehavior(QTableWidget.SelectRows)

        cmd_layout = QVBoxLayout(self.cmd_tab)
        cmd_layout.addWidget(self._cmd_filter)
        cmd_layout.addWidget(self._cmd_table)
        self.tabs.addTab(self.cmd_tab, "Commands")

        #--- Tab 2: Websites ---
        self.web_tab = QWidget()
        self._web_filter = QLineEdit() 
        self._web_filter.setPlaceholderText("Filter websites...")
        self._web_table = QTableWidget(0, 2)
        self._web_table.setHorizontalHeaderLabels(["Alias(es)", "URL"])
        self._web_table.horizontalHeader().setStretchLastSection(True)
        self._web_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._web_table.setSelectionBehavior(QTableWidget.SelectRows)

        web_layout = QVBoxLayout(self.web_tab)
        web_layout.addWidget(self._web_filter)
        web_layout.addWidget(self._web_table)
        self.tabs.addTab(self.web_tab, "Websites")

        # --- Tab 3: Programs ---
        self.prog_tab = QWidget()
        self._prog_filter = QLineEdit()
        self._prog_filter.setPlaceholderText("Filter programs/folders")
        self._prog_table = QTableWidget(0, 2)
        self._prog_table.setHorizontalHeaderLabels(["Name", "Target"])
        self._prog_table.horizontalHeader().setStretchLastSection(True)
        self._prog_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._prog_table.setSelectionBehavior(QTableWidget.SelectRows)

        prog_layout = QVBoxLayout(self.prog_tab)
        prog_layout.addWidget(self._prog_filter)
        prog_layout.addWidget(self._prog_table)
        self.tabs.addTab(self.prog_tab, "Programs")

        # Daten laden
        self._fill_commands()
        self._fill_websites()
        self._fill_programs()

        # Filter verbinden
        self._cmd_filter.textChanged.connect(self._filter_commands)
        self._web_filter.textChanged.connect(self._filter_websites)
        self._prog_filter.textChanged.connect(self._filter_programs)
    
    # ---- Fillers ----

    def _fill_commands(self) -> None:
        self._cmd_table.setRowCount(0)
        for c in COMMANDS:
            r = self._cmd_table.rowCount()
            self._cmd_table.insertRow(r)
            self._cmd_table.setItem(r, 0, QTableWidgetItem(str(c.get("Category",""))))
            self._cmd_table.setItem(r, 1, QTableWidgetItem(str(c.get("Command",""))))
            self._cmd_table.setItem(r, 2, QTableWidgetItem(str(c.get("Description",""))))
            self._cmd_table.setItem(r, 3, QTableWidgetItem(str(c.get("Example",""))))
        self._cmd_table.resizeColumnsToContents()

    def _fill_websites(self) -> None:
        self._web_table.setRowCount(0)
        for keys, url in WEBSITES.items():
            aliases = ", ".join(keys) if isinstance(keys, (list, tuple)) else str(keys)
            r = self._web_table.rowCount()
            self._web_table.insertRow(r)
            self._web_table.setItem(r, 0, QTableWidgetItem(aliases))
            self._web_table.setItem(r, 1, QTableWidgetItem(str(url)))
        self._web_table.resizeColumnsToContents()
    
    def _fill_programs(self) -> None:
        self._prog_table.setRowCount(0)
        for name, target in PROGRAMME.items():
            r = self._prog_table.rowCount()
            self._prog_table.insertRow(r)
            self._prog_table.setItem(r, 0, QTableWidgetItem(str(name)))
            self._prog_table.setItem(r, 1, QTableWidgetItem(str(target)))
        self._prog_table.resizeColumnsToContents()
    
    # ---- Filters ----

    def _filter_commands(self, text: str) -> None:
        t = (text or "").lower().strip()
        for r in range(self._cmd_table.rowCount()):
            row_text = " ".join(self._cmd_table.item(r, c).text().lower() for c in range (4))
            self._cmd_table.setRowHidden(r, t not in row_text)

    def _filter_websites(self, text: str) -> None:
        t = (text or "").lower().strip()
        for r in range(self._web_table.rowCount()):
            row_text = " ".join(self._web_table.item(r, c).text().lower() for c in range(2))
            self._web_table.setRowHidden(r, t not in row_text)

    def _filter_programs(self, text: str) -> None:
        t = (text or "").lower().strip()
        for r in range(self._prog_table.rowCount()):
            row_text = " ".join(self._prog_table.item(r, c).text().lower() for c in range(2))
            self._prog_table.setRowHidden(r, t not in row_text)