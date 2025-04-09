from __future__ import annotations

import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dolitl")

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        open_folder_action = QAction("Open folder", self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Open folder",
            directory="",  # current directory
        )
        return folder_path

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
