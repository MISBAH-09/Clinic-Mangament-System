from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QStackedWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Import the separate screens
from add_patient_data import AddPatientScreen
from delete_patient_data import DeletePatientScreen
from update_patient_data import UpdatePatientScreen
from view_patient_data import ViewPatientScreen
from appointment_patient_data import ManageVisitScreen

class ReceptionScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clinic Reception")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Main Layout
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Patient Registration")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("color: #333333; margin-bottom: 20px;")
        main_layout.addWidget(title)

        # Button Panel for Navigation
        self.button_panel = QGridLayout()
        self.button_panel.setSpacing(10)  # Set spacing between buttons

        # Add buttons to the grid layout
        buttons = [
            ("Add Patient", self.show_add_patient_screen),
            ("Previous Patient", self.show_previous_patient_screen),
            ("Delete Patient", self.show_delete_patient_screen),
            ("Update Patient", self.show_update_patient_screen),
            ("View Patients", self.show_view_patient_screen),
        ]

        # First row: 2 buttons spanning 3 columns each
        button1 = QPushButton("Add Patient")
        button1.setFont(QFont("Arial", 14))
        button1.clicked.connect(self.show_add_patient_screen)
        self.button_panel.addWidget(button1, 0, 0, 1, 3)  # Row 0, Columns 0-2

        button2 = QPushButton("Previous Patient")
        button2.setFont(QFont("Arial", 14))
        button2.clicked.connect(self.show_previous_patient_screen)
        self.button_panel.addWidget(button2, 0, 3, 1, 3)  # Row 0, Columns 3-5

        # Second row: 3 buttons spanning 2 columns each
        button3 = QPushButton("Delete Patient")
        button3.setFont(QFont("Arial", 14))
        button3.clicked.connect(self.show_delete_patient_screen)
        self.button_panel.addWidget(button3, 1, 0, 1, 2)  # Row 1, Columns 0-1

        button4 = QPushButton("Update Patient")
        button4.setFont(QFont("Arial", 14))
        button4.clicked.connect(self.show_update_patient_screen)
        self.button_panel.addWidget(button4, 1, 2, 1, 2)  # Row 1, Columns 2-3

        button5 = QPushButton("View Patients")
        button5.setFont(QFont("Arial", 14))
        button5.clicked.connect(self.show_view_patient_screen)
        self.button_panel.addWidget(button5, 1, 4, 1, 2)  # Row 1, Columns 4-5

        main_layout.addLayout(self.button_panel)

        # Stacked Widget to hold different screens
        self.stacked_widget = QStackedWidget()
        self.add_patient_screen = AddPatientScreen(self)
        self.previous_patient_screen = ManageVisitScreen(self)
        self.delete_patient_screen = DeletePatientScreen(self)
        self.update_patient_screen = UpdatePatientScreen(self)
        self.view_patient_screen = ViewPatientScreen(self)

        # Add screens to the stacked widget
        self.stacked_widget.addWidget(self.add_patient_screen)
        self.stacked_widget.addWidget(self.previous_patient_screen)
        self.stacked_widget.addWidget(self.delete_patient_screen)
        self.stacked_widget.addWidget(self.update_patient_screen)
        self.stacked_widget.addWidget(self.view_patient_screen)

        # Add stacked widget to the main layout
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def show_add_patient_screen(self):
        """Switch to the Add Patient screen."""
        self.stacked_widget.setCurrentWidget(self.add_patient_screen)

    def show_previous_patient_screen(self):
        """Switch to the Previous Patient screen."""
        self.stacked_widget.setCurrentWidget(self.previous_patient_screen)

    def show_delete_patient_screen(self):
        """Switch to the Delete Patient screen."""
        self.stacked_widget.setCurrentWidget(self.delete_patient_screen)

    def show_update_patient_screen(self):
        """Switch to the Update Patient screen."""
        self.stacked_widget.setCurrentWidget(self.update_patient_screen)

    def show_view_patient_screen(self):
        """Switch to the View Patients screen."""
        self.stacked_widget.setCurrentWidget(self.view_patient_screen)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = ReceptionScreen()
    window.show()
    sys.exit(app.exec_())
