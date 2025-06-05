from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget
from add_patient_data import AddPatientScreen

class AdminScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Main layout for AdminScreen
        self.layout = QVBoxLayout(self)

        # Button to toggle Add New Patient form
        self.add_patient_button = QPushButton("Add New Patient")
        self.add_patient_button.clicked.connect(self.toggle_add_new_patient_form)

        # Add the AddNewPatientScreen widget
        self.add_patient_form = AddPatientScreen(self)
        self.add_patient_form.setVisible(False)  # Initially hidden

        # Add widgets to the layout
        self.layout.addWidget(self.add_patient_button)
        self.layout.addWidget(self.add_patient_form)

    def toggle_add_new_patient_form(self):
        """Shows or hides the 'Add New Patient' form."""
        if self.add_patient_form.isVisible():
            self.add_patient_form.setVisible(False)
            self.add_patient_button.setText("Add New Patient")
        else:
            self.add_patient_form.setVisible(True)
            self.add_patient_button.setText("Close Add Patient Form")
