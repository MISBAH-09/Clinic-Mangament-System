from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont

class DashboardButton(QPushButton):
    def __init__(self, parent=None,switch_function=None):
        super().__init__("Dashboard", parent)
        self.switch_function = switch_function
        self.clicked.connect(self.on_click)

    def on_click(self):
        if self.switch_function:
            print('dxfgch')
            self.switch_function()