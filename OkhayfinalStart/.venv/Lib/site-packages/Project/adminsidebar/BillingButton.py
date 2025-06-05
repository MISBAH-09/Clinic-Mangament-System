from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont

class BillingButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Billing", parent)
        self.setFont(QFont("Arial", 12))
        self.setStyleSheet("padding: 5px;")
        self.clicked.connect(self.show_billing)

    def show_billing(self):
        print("Showing Billing")
        # Add the code to switch to the billing content
