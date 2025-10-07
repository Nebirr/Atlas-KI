from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)

from atlas.intern_tasks import collect_system_info_rows

class SystemInfoDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("System Information")
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Category", "Value"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTriggers.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)

        self.btn_refresh = QPushButton("Refresh")
        self.btn_close = QPushButton("Close")

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        btn_row.addWidget(self.btn_refresh)
        btn_row.addWidget(self.btn_close)

        layout = QHBoxLayout(self)
        layout.addWidget(self.table)
        layout.addLayout(btn_row)
        self.setLayout(layout)

        self.btn_refresh.clicked.connect(self.load_info)
        self.btn_close.clicked.connect(self.close)

        self.load_info

    def load_info(self):
        rows = collect_system_info_rows()
        self.table.setRowCount(len(rows))
        for r, (k, v) in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(str(k)))
            self.table.setItem(r, 1, QTableWidgetItem(str(v)))
        self.table.resizeRowsToContents()