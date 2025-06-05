from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Import the separate screens
from Staffdata.add_staff import AddStaffScreen
from Staffdata.update_staff import UpdateStaffScreen
from Staffdata.delete_staff import DeleteStaffScreen
from Staffdata.view_staff import ViewStaffScreen # New screen for viewing patients

class StaffdataScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clinic Reception")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Main Layout
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Staff Registration")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("color: #333333; margin-bottom: 20px;")
        main_layout.addWidget(title)

        # Button Panel for Navigation
        self.button_panel = QVBoxLayout()

        add_staff_button = QPushButton("Add Staff")
        add_staff_button.setFont(QFont("Arial", 14))
        add_staff_button.clicked.connect(self.show_add_staff_screen)
        self.button_panel.addWidget(add_staff_button)

        # delete_staff_button = QPushButton("Delete Staff")
        # delete_staff_button.setFont(QFont("Arial", 14))
        # delete_staff_button.clicked.connect(self.show_delete_staff_screen)
        # self.button_panel.addWidget(delete_staff_button)

        update_staff_button = QPushButton("Update Staff")
        update_staff_button.setFont(QFont("Arial", 14))
        update_staff_button.clicked.connect(self.show_update_staff_screen)
        self.button_panel.addWidget(update_staff_button)

        view_staff_button = QPushButton("View Staff")  # New button
        view_staff_button.setFont(QFont("Arial", 14))
        view_staff_button.clicked.connect(self.show_view_staff_screen)
        self.button_panel.addWidget(view_staff_button)

        main_layout.addLayout(self.button_panel)

      # Stacked Widget to hold different screens
        self.stacked_widget = QStackedWidget()

        # Correct initialization with consistent naming
        self.add_staff_screen = AddStaffScreen(self)  # Corrected variable name
        self.delete_staff_screen = DeleteStaffScreen(self)  # Assuming similar logic for delete
        self.update_staff_screen = UpdateStaffScreen(self)  # Corrected variable name
        self.view_staff_screen = ViewStaffScreen(self)  # Initialize new screen

        # Add screens to the stacked widget
        self.stacked_widget.addWidget(self.add_staff_screen)
        self.stacked_widget.addWidget(self.delete_staff_screen)
        self.stacked_widget.addWidget(self.update_staff_screen)
        self.stacked_widget.addWidget(self.view_staff_screen)

        # Add stacked widget to the main layout
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def show_add_staff_screen(self):
        """Switch to the Add Doctor screen."""
        self.stacked_widget.setCurrentWidget(self.add_staff_screen)

    def show_delete_staff_screen(self):
        """Switch to the Delete Doctor screen."""
        self.stacked_widget.setCurrentWidget(self.delete_staff_screen)

    def show_update_staff_screen(self):
        """Switch to the Update Doctor screen."""
        self.stacked_widget.setCurrentWidget(self.update_staff_screen)

    def show_view_staff_screen(self):
        """Switch to the View Doctors screen."""
        self.stacked_widget.setCurrentWidget(self.view_staff_screen)
