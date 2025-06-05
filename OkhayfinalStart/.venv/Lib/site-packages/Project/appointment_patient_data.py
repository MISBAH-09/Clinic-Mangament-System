import re

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QSpacerItem, QSizePolicy, QGridLayout, QFrame, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ReceptionBackend import *

class ManageVisitScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Patient Visit")
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Manage Patient Visit")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create form layout inside a framed box
        form_frame = QFrame()
        form_frame.setStyleSheet("border: 2px solid #333333; padding: 20px;")
        form_layout = QGridLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setVerticalSpacing(10)

        # Add a spacer to push form content towards the top
        top_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(top_spacer, 0, 0, 1, 4)

        # Style for labels and input fields
        label_style = "font-size: 16px; color: #333333;"
        input_style = "font-size: 16px; padding: 15px;"

        # CNIC Input for Search
        cnic_label = QLabel("CNIC:")
        cnic_label.setStyleSheet("font-size: 16px; color: #333333;")
        self.cnic_input = QLineEdit()
        self.cnic_input.setStyleSheet("font-size: 16px; padding: 15px;")
        self.cnic_input.setMaxLength(15)  # To limit the length to CNIC format
        self.cnic_input.textChanged.connect(self.format_cnic)  # Connect the textChanged signal
        form_layout.addWidget(cnic_label, 1, 0)
        form_layout.addWidget(self.cnic_input, 1, 1)

        # Search Button
        search_button = QPushButton("Search")
        search_button.setFont(QFont("Arial", 14, QFont.Bold))
        search_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 5px;")
        search_button.clicked.connect(self.search_patient)
        form_layout.addWidget(search_button, 1, 2)

        # Patient Details (Read-only fields)
        self.patient_details_label = QLabel("Patient Details:")
        self.patient_details_label.setStyleSheet("font-size: 16px; color: #333333; font-weight: bold;")
        # details_layout.addWidget(self.patient_details_label, 1, 0, 1, 2)
        form_layout.addWidget(self.patient_details_label, 2, 0, 1, 2)

        # Details display
        self.patient_details = QLabel("")
        self.patient_details.setStyleSheet("font-size: 16px; color: #555555;")
        self.patient_details.setWordWrap(True)
        form_layout.addWidget(self.patient_details, 3, 0, 1, 2)

        # Referred Doctor
        referred_doctor_label = QLabel("Select Doctor:")
        referred_doctor_label.setStyleSheet(label_style)
        self.referred_doctor_input = QComboBox()
        self.populate_doctor_dropdown()  # Populate dropdown with doctor names
        self.referred_doctor_input.setStyleSheet(input_style)
        form_layout.addWidget(referred_doctor_label, 4, 0)
        form_layout.addWidget(self.referred_doctor_input, 4, 1)

        # Consultancy Fees
        consultancy_fees_label = QLabel("Consultancy Fees:")
        consultancy_fees_label.setStyleSheet(label_style)
        self.consultancy_fees_input = QLineEdit()
        self.consultancy_fees_input.setStyleSheet(input_style)
        form_layout.addWidget(consultancy_fees_label, 5, 0)
        form_layout.addWidget(self.consultancy_fees_input, 5, 1)

        # Submit Button
        submit_button = QPushButton("Generate Visit")
        submit_button.setFont(QFont("Arial", 14, QFont.Bold))
        submit_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        submit_button.clicked.connect(self.generate_visit)
        form_layout.addWidget(submit_button, 6, 1)

        # Add form layout to the scroll area
        scroll_area.setWidget(form_frame)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        # Set the main layout
        self.setLayout(main_layout)

    def format_cnic(self):
        cnic = self.cnic_input.text()

        # Remove any non-numeric characters
        cnic = ''.join([char for char in cnic if char.isdigit()])

        # Add hyphens after every 5th digit
        formatted_cnic = ''
        for i in range(len(cnic)):
            formatted_cnic += cnic[i]
            if i == 4 or i == 11:  # After 5th and 12th digits, add a hyphen
                formatted_cnic += '-'

        # Update the text in the QLineEdit with the formatted CNIC
        self.cnic_input.setText(formatted_cnic)

        # Set the cursor position at the end of the text
        cursor_position = len(formatted_cnic)
        self.cnic_input.setCursorPosition(cursor_position)


    def search_patient(self):
        # Fetch patient details using CNIC
        cnic = self.cnic_input.text()

        if not self.is_valid_cnic(cnic):
            self.show_error("Invalid CNIC format. Please enter a valid CNIC (#####-#######-#).")
            return
        # Strip any leading/trailing whitespace
        if cnic:
            # Use the backend logic to search for the patient
            from ReceptionBackend import search_patient_by_cnic  # Ensure this is correctly
            patient = search_patient_by_cnic(cnic)
            if patient:
                # Assuming `patient` is a tuple with columns matching the TblPatient table
                self.patient_details.setText(
                    f"Details for CNIC: {cnic}\n"
                    f"FirstName: {patient[1]}\n "
                    f"LastName: {patient[2]}\n"
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

    def is_valid_cnic(self, cnic):
        """Validate CNIC format (#####-#######-#)."""
        pattern = r"^\d{5}-\d{7}-\d{1}$"
        return bool(re.match(pattern, cnic))

    def generate_visit(self):
        """
        Generates a new visit for the selected patient and saves it in the database.
        """
        try:
            # Get input values
            cnic = self.cnic_input.text().strip()
            referred_doctor_name = self.referred_doctor_input.currentText().strip()
            consultancy_fees = self.consultancy_fees_input.text().strip()

            # Validate input
            if not cnic or not referred_doctor_name or not consultancy_fees:
                show_error("Please fill in all required fields.")
                return

            if not consultancy_fees.isdigit():
                show_error("Consultancy fees must be a numeric value.")
                return

            consultancy_fees = float(consultancy_fees)

            # Fetch Patient ID
            patient = search_patient_by_cnic(cnic)  # Returns tuple
            if not patient:
                show_error("No patient found for the provided CNIC.")
                return

            patient_id = patient[0]  # Accessing PatientID from tuple

            # Fetch Doctor ID
            doctors = all_doctors()  # Returns a list of dictionaries
            doctor = next((doc for doc in doctors if f"{doc['FirstName']} {doc['LastName']}" == referred_doctor_name),
                          None)
            if not doctor:
                show_error("Selected doctor could not be found.")
                return

            doctor_id = doctor["DoctorID"]

            # Save visit data
            visit_success = save_visit_data(patient_id, doctor_id, consultancy_fees)
            if visit_success:
                show_success("Visit generated successfully!")
                self.clear_form()
            else:
                show_error("Failed to generate visit.")

        except Exception as e:
            print(f"Error in generate_visit: {e}")
            show_error(f"An unexpected error occurred: {str(e)}")

    def clear_form(self):
        """Clears the form inputs."""
        self.cnic_input.clear()
        self.patient_details_label.setText("Patient Details: ")
        self.referred_doctor_input.setCurrentIndex(0)
        self.consultancy_fees_input.clear()

    def populate_doctor_dropdown(self):
        """Populates the referred doctor dropdown with all available doctors."""
        print("Populating doctor dropdown...")
        doctors = all_doctors()  # Ensure this returns a list of dictionaries

        if doctors:
            doctor_names = [f"{doctor['FirstName']} {doctor['LastName']}" for doctor in doctors]
            self.referred_doctor_input.addItems(doctor_names)
        else:
            show_error("Failed to fetch doctors.")
