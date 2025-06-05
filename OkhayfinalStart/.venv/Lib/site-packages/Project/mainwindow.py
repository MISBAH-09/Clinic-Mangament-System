import os
from PyQt5.QtWidgets import (
    QMainWindow, QStackedWidget, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout
)
from PyQt5.QtGui import QIcon
from loginpage import LoginPage
from AdminScreen import AdminScreen
from admin import AdminDashboard
from loginbackend import fetch_login
from ReceptionScreen import ReceptionScreen
from DoctorScreen import DoctorScreen
from Doctorsdata.DoctorScreen import DoctorsdataScreen
from Inventory.InventoryScreen import InventoryScreen


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Base directory setup
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Window properties
        self.setWindowTitle("ASM clinic")
        self.setWindowIcon(QIcon(base_dir + '/Pictures/logo.png'))
        self.setGeometry(0, 0, 1800, 950)

        # Stacked widget initialization
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Page instances
        self.login_page = LoginPage(self)
        self.admin_screen = AdminScreen(self)
        self.reception_screen = ReceptionScreen(self)
        self.doctor_screen = DoctorScreen(self)

        self.inventory_screen =InventoryScreen(self)

        # Creating a scroll area for doctor data screen
        self.scroll_area_doctor_data = QScrollArea(self)
        self.doctor_data_screen = DoctorsdataScreen(self)
        self.scroll_area_doctor_data.setWidgetResizable(True)

        # Scrollable content setup
        self.scroll_content_doctor_data = QWidget(self.scroll_area_doctor_data)
        self.scroll_layout_doctor_data = QVBoxLayout(self.scroll_content_doctor_data)
        self.scroll_layout_doctor_data.addWidget(self.doctor_data_screen)
        self.scroll_content_doctor_data.setLayout(self.scroll_layout_doctor_data)
        self.scroll_area_doctor_data.setWidget(self.scroll_content_doctor_data)

        # Adding widgets to the stacked widget
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.admin_screen)
        self.stacked_widget.addWidget(self.reception_screen)
        self.stacked_widget.addWidget(self.doctor_screen)
        self.stacked_widget.addWidget(self.scroll_area_doctor_data)
        self.stacked_widget.addWidget(self.inventory_screen)

        # Default page
        self.stacked_widget.setCurrentWidget(self.login_page)

    # Method to check user role and navigate accordingly
    def checkwho(self, username, password):
        role_id = fetch_login(username, password)

        if role_id == 1:  # Assuming 1 represents Admin
            self.showAdminScreen()
        elif role_id == 2:  # Assuming 2 represents Doctor
            self.showReceptionScreen()
        elif role_id == 3: # Assuming 3 represents
            self.showDoctorScreen()
            # self.showDoctorDataScreen()
        else:  # Default case for other roles
            print("Login failed: invalid username or password")

    # Navigation methods
    def showAdminScreen(self):
        self.stacked_widget.setCurrentWidget(self.admin_screen)

    def showReceptionScreen(self):
        self.stacked_widget.setCurrentWidget(self.reception_screen)

    def showDoctorScreen(self):
        self.stacked_widget.setCurrentWidget(self.doctor_screen)

    def showLoginPage(self):
        self.stacked_widget.setCurrentWidget(self.login_page)
