from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QComboBox, QPushButton, \
    QSpacerItem, QSizePolicy, QGridLayout, QFrame, QScrollArea, QMessageBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from ReceptionBackend import submit_patient_data, show_error, all_doctors
import re


class AddPatientScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Patient")
        self.initUI()
        self.doctorMapping = {}

        # Assuming you have a method to load doctor data from the database
        # self.load_doctor_data()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Add Patient")
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

        # First Name
        first_name_label = QLabel("First Name:")
        first_name_label.setStyleSheet(label_style)
        self.first_name_input = QLineEdit()
        self.first_name_input.setStyleSheet(input_style)
        form_layout.addWidget(first_name_label, 1, 0)
        form_layout.addWidget(self.first_name_input, 1, 1)

        # Last Name
        last_name_label = QLabel("Last Name:")
        last_name_label.setStyleSheet(label_style)
        self.last_name_input = QLineEdit()
        self.last_name_input.setStyleSheet(input_style)
        form_layout.addWidget(last_name_label, 1, 2)
        form_layout.addWidget(self.last_name_input, 1, 3)

        # Date of Birth
        dob_label = QLabel("Date of Birth:")
        dob_label.setStyleSheet(label_style)
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("dd/MM/yyyy")
        self.dob_input.setStyleSheet(input_style)
        form_layout.addWidget(dob_label, 2, 0)
        form_layout.addWidget(self.dob_input, 2, 1)

        # CNIC
        cnic_label = QLabel("CNIC:")
        cnic_label.setStyleSheet("font-size: 16px; color: #333333;")
        self.cnic_input = QLineEdit()
        self.cnic_input.setStyleSheet("font-size: 16px; padding: 15px;")
        self.cnic_input.setMaxLength(15)  # To limit the length to CNIC format
        self.cnic_input.textChanged.connect(self.format_cnic)  # Connect the textChanged signal
        form_layout.addWidget(cnic_label, 2, 2)
        form_layout.addWidget(self.cnic_input, 2, 3)

        # Contact Number
        contact_number_label = QLabel("Contact Number:")
        contact_number_label.setStyleSheet(label_style)
        self.contact_number_input = QLineEdit()
        self.contact_number_input.setStyleSheet(input_style)
        form_layout.addWidget(contact_number_label, 3, 0)
        form_layout.addWidget(self.contact_number_input, 3, 1)

        # Gender
        gender_label = QLabel("Gender:")
        gender_label.setStyleSheet(label_style)
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        self.gender_input.setStyleSheet(input_style)
        form_layout.addWidget(gender_label, 3, 2)
        form_layout.addWidget(self.gender_input, 3, 3)

        # Email
        email_label = QLabel("Email:")
        email_label.setStyleSheet(label_style)
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet(input_style)
        form_layout.addWidget(email_label, 4, 0)
        form_layout.addWidget(self.email_input, 4, 1)

        # Date of Registration
        registration_date_label = QLabel("Date of Registration:")
        registration_date_label.setStyleSheet(label_style)
        self.registration_date_input = QDateEdit(QDate.currentDate())
        self.registration_date_input.setCalendarPopup(True)
        self.registration_date_input.setDisplayFormat("dd/MM/yyyy")
        self.registration_date_input.setReadOnly(True)
        self.registration_date_input.setStyleSheet(input_style)
        form_layout.addWidget(registration_date_label, 4, 2)
        form_layout.addWidget(self.registration_date_input, 4, 3)

        # Address
        address_label = QLabel("Address:")
        address_label.setStyleSheet(label_style)
        self.address_input = QTextEdit()
        self.address_input.setFixedHeight(100)
        self.address_input.setStyleSheet(input_style)
        form_layout.addWidget(address_label, 5, 0)
        form_layout.addWidget(self.address_input, 5, 1, 1, 3)

        # Referred Doctor
        referred_doctor_label = QLabel("Referred Doctor:")
        referred_doctor_label.setStyleSheet(label_style)
        self.referred_doctor_input = QComboBox()
        self.populate_doctor_dropdown()  # Populate dropdown with doctor names
        self.referred_doctor_input.setStyleSheet(input_style)
        form_layout.addWidget(referred_doctor_label, 6, 0)
        form_layout.addWidget(self.referred_doctor_input, 6, 1)

        # Consultancy Fees
        consultancy_fees_label = QLabel("Consultancy Fees:")
        consultancy_fees_label.setStyleSheet(label_style)
        self.consultancy_fees_input = QLineEdit()
        self.consultancy_fees_input.setStyleSheet(input_style)
        form_layout.addWidget(consultancy_fees_label, 6, 2)
        form_layout.addWidget(self.consultancy_fees_input, 6, 3)

        # Add a spacer to push form content towards the bottom
        bottom_spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(bottom_spacer, 7, 0, 1, 4)

        # Submit Button
        submit_button = QPushButton("Submit")
        submit_button.setFont(QFont("Arial", 14, QFont.Bold))
        submit_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        submit_button.clicked.connect(self.submit_form)
        form_layout.addWidget(submit_button, 8, 2)

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

    def submit_form(self):
        try:
            # Collect form data
            first_name = self.first_name_input.text()
            last_name = self.last_name_input.text()
            dob = self.dob_input.date().toString("yyyy-MM-dd")
            cnic = self.cnic_input.text()
            contact_number = self.contact_number_input.text()
            gender = self.gender_input.currentText()
            email = self.email_input.text()
            registration_date = self.registration_date_input.date().toString("yyyy-MM-dd")
            address = self.address_input.toPlainText()
            doctor_name = self.referred_doctor_input.currentText()

            # Validate CNIC format
            if not self.is_valid_cnic(cnic):
                self.show_error("Invalid CNIC format. Please enter a valid CNIC (#####-#######-#).")
                return

            if not self.is_valid_email(email):
                self.show_error("Invalid email format. Please enter a valid email address.")
                return



            # Get consultancy fees
            try:
                consultancy_fees = float(self.consultancy_fees_input.text())
                if consultancy_fees <= 0:
                    raise ValueError("Consultancy fees must be greater than zero.")
            except ValueError:
                self.show_error("Please enter a valid consultancy fee.")
                return

            # Submit patient data
            success = submit_patient_data(
                first_name=first_name,
                last_name=last_name,
                cnic=cnic,
                dob=dob,
                gender=gender,
                contact_number=contact_number,
                email=email,
                address=address,
                date_registered=registration_date,
                referred_doctor=doctor_name,
                consultancy_fees=consultancy_fees
            )

            if success:
                self.show_success("Patient data submitted successfully!")
                self.clear_form()
            else:
                self.show_error("Failed to submit patient data.")

        except Exception as e:
            print(f"Error in submit_form: {e}")
            self.show_error(f"An error occurred during form submission: {e}")

    def is_valid_cnic(self, cnic):
        """Validate CNIC format (#####-#######-#)."""
        pattern = r"^\d{5}-\d{7}-\d{1}$"
        return bool(re.match(pattern, cnic))

    def is_valid_email(self, email):
        """Validate email format using a regular expression."""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email))

    def show_error(self, message):
        """Show error message box."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

    def show_success(self, message):
        """Show success message box."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Success")
        msg.exec_()

    def clear_form(self):
        """Clears the form inputs."""
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.dob_input.setDate(QDate.currentDate())
        self.cnic_input.clear()
        self.contact_number_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.email_input.clear()
        self.address_input.clear()
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