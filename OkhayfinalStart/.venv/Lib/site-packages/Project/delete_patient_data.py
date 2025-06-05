from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QSpacerItem, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ReceptionBackend import delete_patient_by_cnic


class DeletePatientScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Patient")
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Delete Patient")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Search Bar
        search_layout = QVBoxLayout()
        self.cnic_input = QLineEdit()
        self.cnic_input.setPlaceholderText("Enter CNIC")
        self.cnic_input.setStyleSheet("font-size: 16px; padding: 10px;")
        search_layout.addWidget(QLabel("Search Patient by CNIC:"))
        search_layout.addWidget(self.cnic_input)

        search_button = QPushButton("Search")
        search_button.setFont(QFont("Arial", 14))
        search_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; border-radius: 5px;")
        search_button.clicked.connect(self.search_patient)
        search_layout.addWidget(search_button)

        main_layout.addLayout(search_layout)

        # Frame for displaying patient details
        details_frame = QFrame()
        details_frame.setStyleSheet("border: 2px solid #333333; padding: 20px;")
        details_layout = QGridLayout(details_frame)
        details_layout.setContentsMargins(20, 20, 20, 20)
        details_layout.setVerticalSpacing(10)

        # Spacer to push details content towards the top
        top_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        details_layout.addItem(top_spacer, 0, 0, 1, 2)

        # Patient details label
        self.patient_details_label = QLabel("Patient Details:")
        self.patient_details_label.setStyleSheet("font-size: 16px; color: #333333; font-weight: bold;")
        details_layout.addWidget(self.patient_details_label, 1, 0, 1, 2)

        # Details display
        self.patient_details = QLabel("")
        self.patient_details.setStyleSheet("font-size: 16px; color: #555555;")
        self.patient_details.setWordWrap(True)
        details_layout.addWidget(self.patient_details, 2, 0, 1, 2)

        # Spacer to push details content towards the bottom
        bottom_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        details_layout.addItem(bottom_spacer, 3, 0, 1, 2)

        main_layout.addWidget(details_frame)

        # Delete Button
        delete_button = QPushButton("Delete Patient")
        delete_button.setFont(QFont("Arial", 14, QFont.Bold))
        delete_button.setStyleSheet("background-color: #FF4C4C; color: white; padding: 10px; border-radius: 5px;")
        delete_button.clicked.connect(self.delete_patient)
        main_layout.addWidget(delete_button, alignment=Qt.AlignCenter)

        # Set the main layout
        self.setLayout(main_layout)



    def search_patient(self):
        # Fetch patient details using CNIC
        cnic = self.cnic_input.text().strip()  # Strip any leading/trailing whitespace
        if cnic:
            # Use the backend logic to search for the patient
            from ReceptionBackend import search_patient_by_cnic  # Ensure this is correctly
            patient = search_patient_by_cnic(cnic)
            if patient:
                # Assuming `patient` is a tuple with columns matching the TblPatient table
                self.patient_details.setText(
                    f"Details for CNIC: {cnic}\n"
                    f"Name: {patient[1]} {patient[2]}\n"
                    f"DOB: {patient[3]}\n"
                    f"Gender: {patient[4]}\n"
                    f"Contact: {patient[5]}\n"
                    f"Email: {patient[6]}\n"
                    f"Address: {patient[7]}\n"
                    f"Date Registered: {patient[8]}"
                )
            else:
                self.patient_details.setText("No details found for the provided CNIC.")
        else:
            self.patient_details.setText("Please enter a valid CNIC.")

    def delete_patient(self):
        # Delete patient logic
        cnic = self.cnic_input.text()
        if cnic:
            # Call the backend function to delete the patient
            if delete_patient_by_cnic(cnic):
                self.patient_details.setText(f"Patient with CNIC {cnic} deleted successfully.")
            else:
                self.patient_details.setText(f"Failed to delete patient with CNIC {cnic}.")
        else:
            self.show_message("Error", "No CNIC provided. Unable to delete.", QMessageBox.Critical)

    def show_message(self, title, message, icon):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.exec_()