from PyQt5.QtWidgets import ( # type: ignore
    QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QTextEdit, QDateEdit, QComboBox, QSpacerItem, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, QDate # type: ignore
from PyQt5.QtGui import QFont # type: ignore

class ReceptionScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clinic Reception")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Main layout using QVBoxLayout
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Patient Registration")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #333333; margin-bottom: 20px; border: 2px solid #333333; padding: 10px;")
        main_layout.addWidget(title)

        # Create a widget to hold the form layout with a border
        form_frame = QFrame()
        form_frame.setStyleSheet("border: 2px solid #333333; padding: 20px;")
        form_layout = QGridLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setVerticalSpacing(10)

        # Spacer to push form content towards the top
        top_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(top_spacer, 0, 0, 1, 4)

        # Styles for labels and input fields
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
        cnic_label.setStyleSheet(label_style)
        self.cnic_input = QLineEdit()
        self.cnic_input.setStyleSheet(input_style)
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

        # Spacer to push form content towards the top
        bottom_spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(bottom_spacer, 6, 0, 1, 4)

        # Submit Button
        submit_button = QPushButton("Submit")
        submit_button.setFont(QFont("Arial", 14, QFont.Bold))
        submit_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        submit_button.clicked.connect(self.submit_form)
        form_layout.addWidget(submit_button, 7, 2)

        # Logout Button
        logout_button = QPushButton("Logout")
        logout_button.setFont(QFont("Arial", 14, QFont.Bold))
        logout_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")
        logout_button.clicked.connect(self.logout)
        form_layout.addWidget(logout_button, 7, 3)

        # Add form frame to the main layout
        main_layout.addWidget(form_frame)
        self.setLayout(main_layout)

    def submit_form(self):
        # Collect the form data
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        dob = self.dob_input.date()  # Get the QDate object
        cnic = self.cnic_input.text()
        contact_number = self.contact_number_input.text()
        gender = self.gender_input.currentText()
        email = self.email_input.text()
        address = self.address_input.toPlainText()
        registration_date = self.registration_date_input.date().toString("yyyy-MM-dd")

        # Calculate age from DOB (if required)
        current_date = QDate.currentDate()
        age = dob.daysTo(current_date) // 365  # Approximate age calculation based on days

        # Call the backend function to submit the data
        from ReceptionBackend import submit_patient_data  # Import the backend function
        try:
            # Pass the form fields directly to submit_patient_data function
            success = submit_patient_data(
                first_name=first_name,
                last_name=last_name,
                cnic=cnic,
                dob=dob.toString("yyyy-MM-dd"),  # Convert QDate to string
                gender=gender,
                contact_number=contact_number,
                email=email,
                address=address,
                date_registered=registration_date  # Use registration_date instead of 'age' if not required
            )
        except Exception as e:
            print(f"Error: {str(e)}")
            success = False

        # Feedback to the user
        if success:
            print("Patient data submitted successfully!")
            self.clear_form()
        else:
            print("Failed to submit patient data. Please try again.")

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

    def logout(self):
        # Hide the current widget (ReceptionScreen)
        self.hide()
        # Show the parent widget's login page
        self.parent().showLoginPage()

