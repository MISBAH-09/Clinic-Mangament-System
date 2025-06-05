from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QComboBox, QPushButton, QSpacerItem, QSizePolicy, QGridLayout, QFrame, QMessageBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

class AddDoctorScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Doctor")
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Add Doctor")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

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

        # CNIC
        cnic_label = QLabel("CNIC:")
        cnic_label.setStyleSheet(label_style)
        self.cnic_input = QLineEdit()
        self.cnic_input.setStyleSheet(input_style)
        form_layout.addWidget(cnic_label, 2, 0)
        form_layout.addWidget(self.cnic_input, 2, 1)

        # License Number
        license_no_label = QLabel("License Number:")
        license_no_label.setStyleSheet(label_style)
        self.license_no_input = QLineEdit()
        self.license_no_input.setStyleSheet(input_style)
        form_layout.addWidget(license_no_label, 2, 2)
        form_layout.addWidget(self.license_no_input, 2, 3)

        # Username
        username_label = QLabel("Username:")
        username_label.setStyleSheet(label_style)
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(input_style)
        form_layout.addWidget(username_label, 3, 0)
        form_layout.addWidget(self.username_input, 3, 1)

        # Password
        password_label = QLabel("Password:")
        password_label.setStyleSheet(label_style)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(input_style)
        form_layout.addWidget(password_label, 3, 2)
        form_layout.addWidget(self.password_input, 3, 3)

        # Role
        role_label = QLabel("Role:")
        role_label.setStyleSheet(label_style)
        self.role_input = QComboBox()
        self.role_input.addItem("Doctor")  # Placeholder while roles load
        self.role_input.setStyleSheet(input_style)
        form_layout.addWidget(role_label, 4, 0)
        form_layout.addWidget(self.role_input, 4, 1)

        # Joining Date
        joining_date_label = QLabel("Joining Date:")
        joining_date_label.setStyleSheet(label_style)
        self.joining_date_input = QDateEdit(QDate.currentDate())
        self.joining_date_input.setCalendarPopup(True)
        self.joining_date_input.setDisplayFormat("dd/MM/yyyy")
        self.joining_date_input.setStyleSheet(input_style)
        form_layout.addWidget(joining_date_label, 4, 2)
        form_layout.addWidget(self.joining_date_input, 4, 3)

        # Salary Amount
        salary_amount_label = QLabel("Salary Amount:")
        salary_amount_label.setStyleSheet(label_style)
        self.salary_amount_input = QLineEdit()
        self.salary_amount_input.setStyleSheet(input_style)
        form_layout.addWidget(salary_amount_label, 5, 0)
        form_layout.addWidget(self.salary_amount_input, 5, 1)

        # City
        city_label = QLabel("City:")
        city_label.setStyleSheet(label_style)
        self.city_input = QLineEdit()
        self.city_input.setStyleSheet(input_style)
        form_layout.addWidget(city_label, 5, 2)
        form_layout.addWidget(self.city_input, 5, 3)

        # Street
        street_label = QLabel("Street:")
        street_label.setStyleSheet(label_style)
        self.street_input = QLineEdit()
        self.street_input.setStyleSheet(input_style)
        form_layout.addWidget(street_label, 6, 0)
        form_layout.addWidget(self.street_input, 6, 1)

        # State
        state_label = QLabel("State:")
        state_label.setStyleSheet(label_style)
        self.state_input = QLineEdit()
        self.state_input.setStyleSheet(input_style)
        form_layout.addWidget(state_label, 6, 2)
        form_layout.addWidget(self.state_input, 6, 3)

        # Postal Code
        postal_code_label = QLabel("Postal Code:")
        postal_code_label.setStyleSheet(label_style)
        self.postal_code_input = QLineEdit()
        self.postal_code_input.setStyleSheet(input_style)
        form_layout.addWidget(postal_code_label, 7, 0)
        form_layout.addWidget(self.postal_code_input, 7, 1)

        # Country
        country_label = QLabel("Country:")
        country_label.setStyleSheet(label_style)
        self.country_input = QLineEdit()
        self.country_input.setStyleSheet(input_style)
        form_layout.addWidget(country_label, 7, 2)
        form_layout.addWidget(self.country_input, 7, 3)

        # Add a spacer to push form content towards the bottom
        bottom_spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(bottom_spacer, 9, 0, 1, 4)

        # Submit Button
        submit_button = QPushButton("Submit")
        submit_button.setFont(QFont("Arial", 14, QFont.Bold))
        submit_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        submit_button.clicked.connect(self.submit_form)
        form_layout.addWidget(submit_button, 10, 2)

        # Add form layout to the main layout
        main_layout.addWidget(form_frame)

        # Set the main layout
        self.setLayout(main_layout)

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def closeEvent(self, event):
        # Confirm before closing the window
        reply = QMessageBox.question(self, 'Confirm Close', 'Are you sure you want to exit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()  # Close the window
        else:
            event.ignore()  # Ignore the close event (prevent closing)

    # def load_roles(self):
    #     from Doctorsdata.DoctorsBackend import fetch_roles  # Import the backend function
    #     try:
    #         self.role_input.clear()  # Clear existing items before loading new ones
    #         self.role_input.addItem("Loading...")  # Show "Loading..." while fetching roles
    #
    #         roles = fetch_roles()  # Fetch the roles from the backend
    #         self.role_input.clear()  # Clear "Loading..." placeholder
    #
    #         if roles:
    #             # If roles are found, add them to the combo box
    #             self.role_input.addItems(roles)
    #         else:
    #             # If no roles are found, show a message in the combo box
    #             self.role_input.addItem("No roles available")
    #
    #     except Exception as e:
    #         # In case of any error while fetching roles, show an error in the combo box
    #         print(f"Error fetching roles: {str(e)}")
    #         self.role_input.clear()
    #         self.role_input.addItem("Error loading roles")

    def validate_form(self):
        if not self.first_name_input.text().strip():
            return "First Name is required."
        if not self.last_name_input.text().strip():
            return "Last Name is required."
        if not self.cnic_input.text().strip():
            return "CNIC is required."
        if not self.license_no_input.text().strip():
            return "License Number is required."
        if not self.username_input.text().strip():
            return "Username is required."
        if not self.password_input.text().strip():
            return "Password is required."
        # if self.role_input.currentText() in ["Loading...", "No roles available", "Error loading roles"]:
        #     return "Please select a valid role."
        if not self.salary_amount_input.text().strip():
            return "Salary Amount is required."
        if not self.city_input.text().strip():
            return "City is required."
        # Additional validation rules can be added as needed
        return None

    def submit_form(self):
        try:
            # Validate form data
            validation_error = self.validate_form()
            if validation_error:
                self.show_message("Validation Error", validation_error)
                return

            # Collect the form data
            first_name = self.first_name_input.text()
            last_name = self.last_name_input.text()
            cnic = self.cnic_input.text()
            license_no = self.license_no_input.text()
            username = self.username_input.text()
            password_hash = self.password_input.text()
            joining_date = self.joining_date_input.date().toString("yyyy-MM-dd")
            salary_amount = self.salary_amount_input.text()
            city = self.city_input.text()
            street = self.street_input.text()
            state = self.state_input.text()
            postal_code = self.postal_code_input.text()
            country = self.country_input.text()

            # Call the backend function to submit the data
            from Doctorsdata.DoctorsBackend import execute_transaction  # Import the backend function
            success = execute_transaction(
                first_name=first_name,
                last_name=last_name,
                cnic=cnic,
                license_no=license_no,
                username=username,
                password_hash=password_hash,
                joining_date=joining_date,
                salary_amount=salary_amount,
                city=city,
                street=street,
                state=state,
                postal_code=postal_code,
                country=country
            )

            if success:
                self.show_message("Success", "Doctor data submitted successfully!")
                self.clear_form()
            else:
                self.show_message("Error", "Failed to submit doctor data. Please try again.")
                print("Error: Backend transaction failed.")

        except Exception as e:
            print(f"Error during submission: {str(e)}")  # Log error for debugging
            self.show_message("Error", "An error occurred while submitting the data. Please try again.")

    def clear_form(self):
        # Reset the form fields after successful submission
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.cnic_input.clear()
        self.license_no_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.role_input.setCurrentIndex(0)
        self.joining_date_input.setDate(QDate.currentDate())
        # self.job_status_input.clear()  # Clear the job status field
        self.salary_amount_input.clear()
        self.city_input.clear()
        self.street_input.clear()
        self.state_input.clear()
        self.postal_code_input.clear()
        self.country_input.clear()