from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QComboBox, QPushButton, QSpacerItem, \
    QSizePolicy, QGridLayout, QFrame, QMessageBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from StaffBackend import *
import traceback

class AddStaffScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Doctor")
        self.initUI()
        self.loadRoles()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Add Staff")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Create form layout inside a framed box
        form_frame = QFrame()
        form_frame.setStyleSheet("border: 2px solid #333333; padding: 20px;")
        form_layout = QGridLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setVerticalSpacing(10)

        # Style for labels and input fields
        label_style = "font-size: 16px; color: #333333;"
        input_style = "font-size: 16px; padding: 15px;"

        # First Name
        first_name_label = QLabel("First Name:")
        first_name_label.setStyleSheet(label_style)
        self.first_name_input = QLineEdit()
        self.first_name_input.setStyleSheet(input_style)
        form_layout.addWidget(first_name_label, 0, 0)
        form_layout.addWidget(self.first_name_input, 0, 1)

        # Last Name
        last_name_label = QLabel("Last Name:")
        last_name_label.setStyleSheet(label_style)
        self.last_name_input = QLineEdit()
        self.last_name_input.setStyleSheet(input_style)
        form_layout.addWidget(last_name_label, 0, 2)
        form_layout.addWidget(self.last_name_input, 0, 3)

        # CNIC
        cnic_label = QLabel("CNIC:")
        cnic_label.setStyleSheet(label_style)
        self.cnic_input = QLineEdit()
        self.cnic_input.setStyleSheet(input_style)
        form_layout.addWidget(cnic_label, 1, 0)
        form_layout.addWidget(self.cnic_input, 1, 1)

        # Username
        username_label = QLabel("Username:")
        username_label.setStyleSheet(label_style)
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(input_style)
        form_layout.addWidget(username_label, 1, 2)
        form_layout.addWidget(self.username_input, 1, 3)

        # Password
        password_label = QLabel("Password:")
        password_label.setStyleSheet(label_style)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(input_style)
        form_layout.addWidget(password_label, 2, 0)
        form_layout.addWidget(self.password_input, 2, 1)

       # Role 
        role_label = QLabel("Role:") 
        role_label.setStyleSheet(label_style)
        self.role_input = QComboBox()
        self.role_input.addItem("Loading...") # Placeholder while roles load 
        self.role_input.setStyleSheet(input_style)
        form_layout.addWidget(role_label, 2, 2) 
        form_layout.addWidget(self.role_input, 2, 3)

        # Joining Date
        joining_date_label = QLabel("Joining Date:")
        joining_date_label.setStyleSheet(label_style)
        self.joining_date_input = QDateEdit(QDate.currentDate())
        self.joining_date_input.setCalendarPopup(True)
        self.joining_date_input.setDisplayFormat("dd/MM/yyyy")
        self.joining_date_input.setStyleSheet(input_style)
        form_layout.addWidget(joining_date_label, 3, 0)
        form_layout.addWidget(self.joining_date_input, 3, 1)

        # Salary Amount
        salary_amount_label = QLabel("Salary Amount:")
        salary_amount_label.setStyleSheet(label_style)
        self.salary_amount_input = QLineEdit()
        self.salary_amount_input.setStyleSheet(input_style)
        form_layout.addWidget(salary_amount_label, 3, 2)
        form_layout.addWidget(self.salary_amount_input, 3, 3)

        # City
        city_label = QLabel("City:")
        city_label.setStyleSheet(label_style)
        self.city_input = QLineEdit()
        self.city_input.setStyleSheet(input_style)
        form_layout.addWidget(city_label, 4, 0)
        form_layout.addWidget(self.city_input, 4, 1)

        # Street
        street_label = QLabel("Street:")
        street_label.setStyleSheet(label_style)
        self.street_input = QLineEdit()
        self.street_input.setStyleSheet(input_style)
        form_layout.addWidget(street_label, 4, 2)
        form_layout.addWidget(self.street_input, 4, 3)

        # State
        state_label = QLabel("State:")
        state_label.setStyleSheet(label_style)
        self.state_input = QLineEdit()
        self.state_input.setStyleSheet(input_style)
        form_layout.addWidget(state_label, 5, 0)
        form_layout.addWidget(self.state_input, 5, 1)

        # Postal Code
        postal_code_label = QLabel("Postal Code:")
        postal_code_label.setStyleSheet(label_style)
        self.postal_code_input = QLineEdit()
        self.postal_code_input.setStyleSheet(input_style)
        form_layout.addWidget(postal_code_label, 5, 2)
        form_layout.addWidget(self.postal_code_input, 5, 3)

        # Country
        country_label = QLabel("Country:")
        country_label.setStyleSheet(label_style)
        self.country_input = QLineEdit()
        self.country_input.setStyleSheet(input_style)
        form_layout.addWidget(country_label, 6, 0)
        form_layout.addWidget(self.country_input, 6, 1)

        # Add a spacer to push form content towards the bottom
        bottom_spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(bottom_spacer, 8, 0, 1, 4)

        # Submit Button
        submit_button = QPushButton("Submit")
        submit_button.setFont(QFont("Arial", 14, QFont.Bold))
        submit_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        submit_button.clicked.connect(self.submit_form)
        form_layout.addWidget(submit_button, 9, 2)

        # Add form layout to the main layout
        main_layout.addWidget(form_frame)

        # Set the main layout
        self.setLayout(main_layout)

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def loadRoles(self):
        try: 
            role_names = get_distinct_role_names()
            self.role_input.clear() 
            self.role_input.addItems(role_names)
        except Exception as e: 
            error_message = f"An error occurred while loading roles: {str(e)}" 
            show_error(error_message) 
            print(traceback.format_exc())

    def closeEvent(self, event):
        # Confirm before closing the window
        reply = QMessageBox.question(self, 'Confirm Close', 'Are you sure you want to exit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()  # Close the window
        else:
            event.ignore()  # Ignore the close event (prevent closing)



    def validate_form(self):
        if not self.first_name_input.text().strip():
            return "First Name is required."
        if not self.last_name_input.text().strip():
            return "Last Name is required."
        if not self.cnic_input.text().strip():
            return "CNIC is required."
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
            username = self.username_input.text()
            password_hash = self.password_input.text()
            role_name = self.role_input.currentText()  # Use role_name to match the backend function
            joining_date = self.joining_date_input.date().toString("yyyy-MM-dd")
            # job_status = self.job_status_input.text()
            salary_amount = self.salary_amount_input.text()
            city = self.city_input.text()
            street = self.street_input.text()
            state = self.state_input.text()
            postal_code = self.postal_code_input.text()
            country = self.country_input.text()

            # Call the backend function to submit the data
            success = execute_staff_transaction(
                first_name=first_name,
                last_name=last_name,
                cnic=cnic,
                username=username,
                password_hash=password_hash,
                joining_date=joining_date,
                role_name=role_name,  # Pass role_name correctly
                salary_amount=salary_amount,
                city=city,
                street=street,
                state=state,
                postal_code=postal_code,
                country=country
            )

            if success:
                self.show_message("Success", "Staff data submitted successfully!")
                self.clear_form()
            else:
                self.show_message("Error", "Failed to submit Staff data. Please try again.")

        except Exception as e:
            print(f"Error: {str(e)}")  # Log the error for debugging
            self.show_message("Error", "An error occurred while submitting the data. Please try again.")

    def clear_form(self):
        # Reset the form fields after successful submission
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.cnic_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.role_input.setCurrentIndex(0)
        self.joining_date_input.setDate(QDate.currentDate())
        self.salary_amount_input.clear()
        self.city_input.clear()
        self.street_input.clear()
        self.state_input.clear()
        self.postal_code_input.clear()
        self.country_input.clear()