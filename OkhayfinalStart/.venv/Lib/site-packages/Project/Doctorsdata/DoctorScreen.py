from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Import the separate screens
from Doctorsdata.add_doctors import AddDoctorScreen
from Doctorsdata.delete_doctors import DeleteDoctorScreen
from Doctorsdata.update_doctors import UpdateDoctorScreen
from Doctorsdata.view_doctors import ViewDoctorScreen  # New screen for viewing patients

class DoctorsdataScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clinic Reception")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Main Layout
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Doctors Registration")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("color: #333333; margin-bottom: 20px;")
        main_layout.addWidget(title)

        # Button Panel for Navigation
        self.button_panel = QVBoxLayout()

        add_doctor_button = QPushButton("Add Doctor")
        add_doctor_button.setFont(QFont("Arial", 14))
        add_doctor_button.clicked.connect(self.show_add_doctor_screen)
        self.button_panel.addWidget(add_doctor_button)

        update_doctor_button = QPushButton("Update Doctor")
        update_doctor_button.setFont(QFont("Arial", 14))
        update_doctor_button.clicked.connect(self.show_update_doctor_screen)
        self.button_panel.addWidget(update_doctor_button)

        view_doctor_button = QPushButton("View Doctors")  # New button
        view_doctor_button.setFont(QFont("Arial", 14))
        view_doctor_button.clicked.connect(self.show_view_doctor_screen)
        self.button_panel.addWidget(view_doctor_button)

        main_layout.addLayout(self.button_panel)

        # Stacked Widget to hold different screens
        self.stacked_widget = QStackedWidget()
        self.add_doctor_screen = AddDoctorScreen(self)
        # self.delete_doctor_screen = DeleteDoctorScreen(self)
        self.update_doctor_screen = UpdateDoctorScreen(self)  # Corrected variable name
        self.view_doctor_screen = ViewDoctorScreen(self)  # Initialize new screen

        # Add screens to the stacked widget
        self.stacked_widget.addWidget(self.add_doctor_screen)
        # self.stacked_widget.addWidget(self.delete_doctor_screen)
        self.stacked_widget.addWidget(self.update_doctor_screen)  # Corrected variable name
        self.stacked_widget.addWidget(self.view_doctor_screen)  # Add to stacked widget

        # Add stacked widget to the main layout
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def show_add_doctor_screen(self):
        """Switch to the Add Doctor screen."""
        self.stacked_widget.setCurrentWidget(self.add_doctor_screen)

    # def show_delete_doctor_screen(self):
    #     """Switch to the Delete Doctor screen."""
    #     self.stacked_widget.setCurrentWidget(self.delete_doctor_screen)

    def show_update_doctor_screen(self):
        """Switch to the Update Doctor screen."""
        self.stacked_widget.setCurrentWidget(self.update_doctor_screen)

    def show_view_doctor_screen(self):
        """Switch to the View Doctors screen."""
        self.stacked_widget.setCurrentWidget(self.view_doctor_screen)
