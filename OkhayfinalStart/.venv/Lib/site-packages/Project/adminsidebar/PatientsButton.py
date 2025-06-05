from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont

class PatientsButton(QPushButton):
    def __init__(self, parent=None, switch_function=None):
        super().__init__("Patients", parent)
        # self.setFont(QFont("Arial", 12))
        # self.setStyleSheet("padding: 5px;")
        self.switch_function = switch_function  # Function to switch the content
        self.clicked.connect(self.show_patients)

    def show_patients(self):
        print("Switching to Patients view")
        if self.switch_function:
            self.switch_function()  # Switch to Patients widget
