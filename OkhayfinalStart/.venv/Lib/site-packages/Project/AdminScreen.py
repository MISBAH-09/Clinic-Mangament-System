from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel, QScrollArea, QPushButton, \
    QMessageBox
from PyQt5.QtCore import Qt
from adminsidebar.DashboardButton import DashboardButton  # type: ignore
from adminsidebar.PatientsButton import PatientsButton  # type: ignore
from adminsidebar.DoctorsButton import DoctorsButton  # type: ignore
from adminsidebar.InventoryButton import InventoryButton  # type: ignore
from adminsidebar.StaffButton import StaffButton
from ReceptionScreen import ReceptionScreen
from Doctorsdata.DoctorScreen import DoctorsdataScreen
from Inventory.InventoryScreen import InventoryScreen
from Staffdata.StaffScreen import StaffdataScreen
from dashboard import DashboardWindow  # type: ignore


class AdminScreen(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Main Layout with 1/4 Sidebar and 3/4 Content Area
        main_layout = QHBoxLayout(self)

        # Sidebar container widget
        sidebar_widget = QWidget()
        sidebar_widget.setStyleSheet("background-color: #d3d3d3; padding: 0px;")
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)  # Remove spacing between buttons

        # Add stretch above buttons to center them vertically
        sidebar_layout.addStretch()

        # Create buttons using separate files
        buttons = [
            DashboardButton(self, switch_function=self.show_dashboard),
            PatientsButton(self, switch_function=self.show_patients),
            DoctorsButton(self, switch_function=self.show_doctors_data),
            InventoryButton(self, switch_function=self.show_inventory),
            StaffButton(self, switch_function=self.show_staff),
        ]

        # Apply style to buttons and add them to the sidebar
        button_style = """
            QPushButton {
                padding: 20px 50px;
                border: 2px solid #555;
                border-radius: 5px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """
        for button in buttons:
            button.setStyleSheet(button_style)
            button.setFixedWidth(200)  # Ensure consistent width
            sidebar_layout.addWidget(button, alignment=Qt.AlignCenter)

        # Add the Login Button below StaffButton
        login_button = QPushButton("Login")
        login_button.setStyleSheet(button_style)
        login_button.setFixedWidth(200)  # Ensure consistent width
        login_button.setStyleSheet("""
            QPushButton {
                padding: 20px 50px;
                border: 2px solid #555;
                border-radius: 5px;
                background-color: #ff4d4d;  /* Red color for differentiation */
                color: white;               /* White text for better visibility */
            }
            QPushButton:hover {
                background-color: #ff3333;  /* Slightly darker red on hover */
            }
            QPushButton:pressed {
                background-color: #cc0000;  /* Even darker red when pressed */
            }
        """)
        login_button.clicked.connect(self.logout)
        sidebar_layout.addWidget(login_button, alignment=Qt.AlignCenter)

        # Add stretch below buttons to center them vertically
        sidebar_layout.addStretch()

        # Content layout
        content_layout = QVBoxLayout()

        # Stacked widget for switching between different content views
        self.stacked_widget = QStackedWidget()

        # Add the different content widgets to the stacked widget
        self.stacked_widget.addWidget(self.create_dashboard_widget())  # Index 0
        self.stacked_widget.addWidget(self.create_scrollable_widget(ReceptionScreen()))  # Index 1 (AddPatientScreen)
        self.stacked_widget.addWidget(self.create_scrollable_widget(DoctorsdataScreen()))  # Index 2 (DoctorsdataScreen)
        self.stacked_widget.addWidget(self.create_scrollable_widget(InventoryScreen()))  # Index 3
        self.stacked_widget.addWidget(self.create_scrollable_widget(StaffdataScreen()))  # Index 4
        self.stacked_widget.addWidget(self.create_scrollable_widget(DashboardWindow()))  # Index 5

        # Set Dashboard as the default view
        self.stacked_widget.setCurrentIndex(5)  # Display the dashboard by default

        # Add the stacked widget to the content layout
        content_layout.addWidget(self.stacked_widget)

        # Add the sidebar and content layout to the main layout
        main_layout.addWidget(sidebar_widget)  # Sidebar widget
        main_layout.addLayout(content_layout)  # Content layout

        # Set the proportions for the sidebar and content area
        main_layout.setStretch(0, 1)  # Sidebar width (1/4)
        main_layout.setStretch(1, 3)  # Content area width (3/4)

    def create_dashboard_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dashboard"))
        widget.setLayout(layout)
        return widget

    def create_scrollable_widget(self, widget):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.addWidget(widget)
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        return scroll_area

    def show_patients(self):
        """Switch to the Patients widget (AddPatientScreen)"""
        self.stacked_widget.setCurrentIndex(1)  # Switch to AddPatientScreen

    def show_doctors_data(self):
        """Switch to the Doctors widget (DoctorsdataScreen)"""
        self.stacked_widget.setCurrentIndex(2)  # Switch to DoctorsdataScreen

    def show_inventory(self):
        self.stacked_widget.setCurrentIndex(3)

    def show_staff(self):
        self.stacked_widget.setCurrentIndex(4)

    def show_dashboard(self):
        self.stacked_widget.setCurrentIndex(5)

    from PyQt5.QtWidgets import QMessageBox

    def logout(self):
        # Create a QMessageBox for confirmation
        confirmation_box = QMessageBox()
        confirmation_box.setWindowTitle("Logout Confirmation")
        confirmation_box.setText("Are you sure you want to logout?")
        confirmation_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation_box.setDefaultButton(QMessageBox.No)

        # Check the user's response
        response = confirmation_box.exec_()
        if response == QMessageBox.Yes:
            # User confirmed logout
            self.main_window.showLoginPage()  # Call the method to go back to the login screen


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = AdminScreen()
    window.show()
    sys.exit(app.exec_())
