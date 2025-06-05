# DoctorScreen.py

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget, QLabel,
    QPushButton, QHBoxLayout, QGroupBox, QScrollArea, QMainWindow, QStackedWidget, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from patient_data_page import PatientDataPage
from diagnosis_page import DiagnosisPage
from medicine_page import MedicinePage
from history_page import HistoryPage
from DoctorScreenBackend import show_error, search_patient_by_visitID  # Import the backend functions

class DoctorScreen(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setWindowTitle("Doctor Panel")
        self.setGeometry(100, 100, 800, 600)
        self.visit_id = None  # Store the visit ID
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Top bar with doctor's name and logout button
        top_bar = QHBoxLayout()
        doctor_name_label = QLabel("Dr. ...")
        doctor_name_label.setFont(QFont("Arial", 16))
        doctor_name_label.setStyleSheet("padding: 10px;")

        logout_button = QPushButton("Logout")
        logout_button.setFont(QFont("Arial", 12))
        logout_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")
        logout_button.clicked.connect(self.logout)

        top_bar.addWidget(doctor_name_label, alignment=Qt.AlignLeft)
        top_bar.addWidget(logout_button, alignment=Qt.AlignRight)

        # Main content area
        main_content = QHBoxLayout()

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(0, 0, 0, 0)  # Remove layout margins
        sidebar.setSpacing(5)  # Remove spacing between buttons

        sidebar_buttons = {
            "Patient Data": self.show_patient_data,
            "Diagnosis": self.show_diagnosis,
            "Medicine and Test": self.show_medicine,
            "Slip": self.show_history,

        }

        for text, action in sidebar_buttons.items():
            btn = QPushButton(text)
            btn.setFont(QFont("Arial", 14))
            btn.setStyleSheet("padding: 5px;")  # Add consistent padding for the buttons
            btn.clicked.connect(action)
            sidebar.addWidget(btn)

        # Center the sidebar in the frame
        centered_layout = QVBoxLayout()
        centered_layout.addStretch()  # Add stretchable space above
        centered_layout.addLayout(sidebar)  # Add the sidebar layout
        centered_layout.addStretch()  # Add stretchable space below

        sidebar_frame = QFrame()
        sidebar_frame.setLayout(centered_layout)
        sidebar_frame.setStyleSheet("background-color: #d3d3d3; padding: 5px;")

        # Content area with search bar included
        content_with_search = QVBoxLayout()

        # Search bar
        search_bar = QHBoxLayout()
        search_bar.setSpacing(10)  # Add spacing between search input and button
        search_bar.setContentsMargins(0, 0, 0, 0)  # Remove any unnecessary margins

        self.search_input = QLineEdit()
        self.search_input.setMaximumWidth(400)
        self.search_input.setFont(QFont("Arial", 12))
        self.search_input.setAlignment(Qt.AlignCenter)

        search_button = QPushButton("Search")
        search_button.setFont(QFont("Arial", 12))
        search_button.setMaximumWidth(150)
        search_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 5px;")
        search_button.clicked.connect(self.search_patient)

        search_bar.addWidget(self.search_input, alignment=Qt.AlignRight)
        search_bar.addWidget(search_button, alignment=Qt.AlignLeft)

        # Add the search bar to the top of the content area
        content_with_search.addLayout(search_bar)

        # Content display area
        self.content_area = QStackedWidget()
        content_with_search.addWidget(self.content_area)

        # Add instances of the separate page classes (initialize without visit_id)
        self.patient_data_page = PatientDataPage()
        self.diagnosis_page = DiagnosisPage()
        self.medicine_page = MedicinePage()  # Initialize without visit_id
        self.history_page = HistoryPage()

        self.content_area.addWidget(self.patient_data_page)
        self.content_area.addWidget(self.diagnosis_page)
        self.content_area.addWidget(self.medicine_page)
        self.content_area.addWidget(self.history_page)
        self.content_area.addWidget(QLabel("Submit & Recheck Page"))  # Placeholder
        self.content_area.addWidget(QLabel("BLA BLA BLA Page"))       # Placeholder

        main_content.addWidget(sidebar_frame, 1)
        main_content.addLayout(content_with_search, 4)

        # Add top bar and main content to the main layout
        main_layout.addLayout(top_bar)
        main_layout.addLayout(main_content)

        self.setLayout(main_layout)

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

    def search_patient(self):
        try:
            self.visit_id = self.search_input.text().strip()  # Set the visit ID
            print(f"Search for VisitID: {self.visit_id}")  # Debugging line
            if not self.visit_id:
                show_error("Please enter a VisitID to search.")
                return

            # Search for the patient by visit ID
            patient = search_patient_by_visitID(self.visit_id)
            print(f"Patient Data: {patient}")  # Debugging line

            if patient:
                # Set patient data in PatientDataPage
                self.patient_data_page.set_patient_data(
                    patient_id=patient["PatientID"],
                    first_name=patient["FirstName"],
                    last_name=patient["LastName"],
                    dob=patient["DateOfBirth"],
                    cnic=patient["CNIC"],
                    contact=patient["ContactNumber"],
                    gender=patient["Gender"],
                    email=patient["Email"],
                    address=patient["Address"],
                    reg_date=patient["DateRegistered"]
                )
                self.show_patient_data()  # Switch to the PatientDataPage

                # Update the visit_id in MedicinePage and DiagnosisPage
                self.medicine_page.update_visit_id(self.visit_id)
                self.diagnosis_page.set_visit_id(self.visit_id)  # Update visit_id in DiagnosisPage
                self.history_page.set_visit_id(self.visit_id)

                print(f"visit_id set in MedicinePage and DiagnosisPage: {self.visit_id}")  # Debugging
            else:
                show_error("No patient found with the provided VisitID.")
        except Exception as e:
            print(f"Error in search_patient: {e}")
            show_error(f"An error occurred while searching for the patient: {e}")

    def show_patient_data(self):
        self.content_area.setCurrentWidget(self.patient_data_page)

    def show_diagnosis(self):
        self.content_area.setCurrentWidget(self.diagnosis_page)

    def show_medicine(self):
        self.content_area.setCurrentWidget(self.medicine_page)

    def show_history(self):
        self.content_area.setCurrentWidget(self.history_page)

    def show_submit(self):
        self.content_area.setCurrentIndex(4)

    def show_bla_bla(self):
        self.content_area.setCurrentIndex(5)

if __name__ == '__main__':
    app = QApplication([])
    window = DoctorScreen()
    window.show()
    app.exec_()
