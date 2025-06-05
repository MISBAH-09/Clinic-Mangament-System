from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont

# from PyQt5.QtWidgets import QPushButton

class DoctorsButton(QPushButton):
    def __init__(self, parent=None, switch_function=None):
        super().__init__("Doctors", parent)
        self.switch_function = switch_function
        self.clicked.connect(self.on_click)

    def on_click(self):
        if self.switch_function:
            self.switch_function()
