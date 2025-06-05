from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont

class ReportsButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Reports", parent)
        self.setFont(QFont("Arial", 12))
        self.setStyleSheet("padding: 5px;")
        self.clicked.connect(self.show_reports)

    def show_reports(self):
        print("Showing Reports")
        # Add the code to switch to the reports content
