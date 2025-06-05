from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QDateEdit, QComboBox, QPushButton, QSpacerItem, \
    QSizePolicy, QGridLayout, QFrame, QStackedWidget, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
import datetime
from PyQt5.QtCore import QDate

class UpdateDoctorScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Doctor")
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Update Doctor")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Search by CNIC layout
        search_layout = QHBoxLayout()

        # CNIC input field
        self.cnic_input = QLineEdit(self)
        self.cnic_input.setPlaceholderText("Enter CNIC")
        self.cnic_input.setStyleSheet("font-size: 16px; padding: 5px;")

        # Search button
        search_button = QPushButton("Search")
        search_button.setStyleSheet("background-color: #2196F3; color: white; padding: 5px 10px; border-radius: 5px;")
        search_button.clicked.connect(self.search_doctor)

        search_layout.addWidget(self.cnic_input)
        search_layout.addWidget(search_button)

        main_layout.addLayout(search_layout)

        # Navigation Buttons
        button_layout = QHBoxLayout()
        self.personal_data_button = QPushButton("Update Personal Data")
        self.salary_button = QPushButton("Update Salary")
        self.address_button = QPushButton("Update Address")
        self.credentials_button = QPushButton("Update Credentials")

        # Connect buttons to switch forms
        self.personal_data_button.clicked.connect(lambda: self.switch_form(0))  # Index 0 for Personal Data Form
        self.salary_button.clicked.connect(lambda: self.switch_form(1))  # Index 1 for Salary Form
        self.address_button.clicked.connect(lambda: self.switch_form(2))  # Index 2 for Address Form
        self.credentials_button.clicked.connect(lambda: self.switch_form(3))  # Index 3 for Credentials Form

        button_layout.addWidget(self.personal_data_button)
        button_layout.addWidget(self.salary_button)
        button_layout.addWidget(self.address_button)
        button_layout.addWidget(self.credentials_button)

        main_layout.addLayout(button_layout)

        # Stacked Widget to hold different forms
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_personal_data_form())
        self.stacked_widget.addWidget(self.create_salary_form())
        self.stacked_widget.addWidget(self.create_address_form())
        self.stacked_widget.addWidget(self.create_credentials_form())

        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def switch_form(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def create_personal_data_form(self):
        widget = QWidget()
        form_layout = QGridLayout(widget)

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
        # Change this to avoid conflict
        self.cnic_personal_input = QLineEdit()
        self.cnic_personal_input.setStyleSheet(input_style)
        form_layout.addWidget(cnic_label, 1, 0)
        form_layout.addWidget(self.cnic_personal_input, 1, 1)

        # Joining Date
        joining_date_label = QLabel("Joining Date:")
        joining_date_label.setStyleSheet(label_style)
        self.joining_date_input = QDateEdit(QDate.currentDate())
        self.joining_date_input.setCalendarPopup(True)
        self.joining_date_input.setDisplayFormat("dd/MM/yyyy")
        self.joining_date_input.setStyleSheet(input_style)
        form_layout.addWidget(joining_date_label, 1, 2)
        form_layout.addWidget(self.joining_date_input, 1, 3)

        # Job Status
        job_status_label = QLabel("Job Status:")
        job_status_label.setStyleSheet(label_style)
        self.job_status_input = QLineEdit()
        self.job_status_input.setStyleSheet(input_style)
        form_layout.addWidget(job_status_label, 2, 0)
        form_layout.addWidget(self.job_status_input, 2, 1)

        # License Number
        license_no_label = QLabel("License Number:")
        license_no_label.setStyleSheet(label_style)
        self.license_no_input = QLineEdit()
        self.license_no_input.setStyleSheet(input_style)
        form_layout.addWidget(license_no_label, 2, 2)
        form_layout.addWidget(self.license_no_input, 2, 3)

        # # Specialization
        # role_label = QLabel("Specialization:")
        # role_label.setStyleSheet(label_style)
        # self.role_input = QComboBox()
        # self.role_input.addItems(["Doctor", "Surgeon", "Specialist"])
        # self.role_input.setStyleSheet(input_style)
        # form_layout.addWidget(role_label, 3, 0)
        # form_layout.addWidget(self.role_input, 3, 1)

        # Update Button
        update_button = QPushButton("Update Data")
        update_button.setFont(QFont("Arial", 14, QFont.Bold))
        update_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        update_button.clicked.connect(self.update_personal_data)
        form_layout.addWidget(update_button, 4, 2)

        return widget

    def create_salary_form(self):
        widget = QWidget()
        form_layout = QGridLayout(widget)

        label_style = "font-size: 16px; color: #333333;"
        input_style = "font-size: 16px; padding: 15px;"

        salary_amount_label = QLabel("Salary Amount:")
        salary_amount_label.setStyleSheet(label_style)
        self.salary_amount_input = QLineEdit()
        self.salary_amount_input.setStyleSheet(input_style)
        form_layout.addWidget(salary_amount_label, 0, 0)
        form_layout.addWidget(self.salary_amount_input, 0, 1)

        # Update Button
        update_button = QPushButton("Update Salary")
        update_button.setFont(QFont("Arial", 14, QFont.Bold))
        update_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        update_button.clicked.connect(self.update_salary)
        form_layout.addWidget(update_button, 1, 0)

        return widget

    def create_address_form(self):
        widget = QWidget()
        form_layout = QGridLayout(widget)

        label_style = "font-size: 16px; color: #333333;"
        input_style = "font-size: 16px; padding: 15px;"

        postal_code_label = QLabel("Postal Code:")
        postal_code_label.setStyleSheet(label_style)
        self.postal_code_input = QLineEdit()
        self.postal_code_input.setStyleSheet(input_style)
        form_layout.addWidget(postal_code_label, 0, 0)
        form_layout.addWidget(self.postal_code_input, 0, 1)

        city_label = QLabel("City:")
        city_label.setStyleSheet(label_style)
        self.city_input = QLineEdit()
        self.city_input.setStyleSheet(input_style)
        form_layout.addWidget(city_label, 0, 2)
        form_layout.addWidget(self.city_input, 0, 3)

        street_label = QLabel("Street:")
        street_label.setStyleSheet(label_style)
        self.street_input = QLineEdit()
        self.street_input.setStyleSheet(input_style)
        form_layout.addWidget(street_label, 1, 0)
        form_layout.addWidget(self.street_input, 1, 1)

        state_label = QLabel("State:")
        state_label.setStyleSheet(label_style)
        self.state_input = QLineEdit()
        self.state_input.setStyleSheet(input_style)
        form_layout.addWidget(state_label, 1, 2)
        form_layout.addWidget(self.state_input, 1, 3)

        country_label = QLabel("Country:")
        country_label.setStyleSheet(label_style)
        self.country_input = QLineEdit()
        self.country_input.setStyleSheet(input_style)
        form_layout.addWidget(country_label, 2, 0)
        form_layout.addWidget(self.country_input, 2, 1)

        # Update Button
        update_button = QPushButton("Update Address")
        update_button.setFont(QFont("Arial", 14, QFont.Bold))
        update_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        update_button.clicked.connect(self.update_address)
        form_layout.addWidget(update_button, 3, 0)

        return widget

    def create_credentials_form(self):
        widget = QWidget()
        form_layout = QGridLayout(widget)

        label_style = "font-size: 16px; color: #333333;"
        input_style = "font-size: 16px; padding: 15px;"

        username_label = QLabel("Username:")
        username_label.setStyleSheet(label_style)
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(input_style)
        form_layout.addWidget(username_label, 0, 0)
        form_layout.addWidget(self.username_input, 0, 1)

        password_label = QLabel("Password:")
        password_label.setStyleSheet(label_style)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(input_style)
        form_layout.addWidget(password_label, 0, 2)
        form_layout.addWidget(self.password_input, 0, 3)

        # Update Button
        update_button = QPushButton("Update Credentials")
        update_button.setFont(QFont("Arial", 14, QFont.Bold))
        update_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        update_button.clicked.connect(self.update_credentials)
        form_layout.addWidget(update_button, 1, 2)

        return widget

    from PyQt5.QtCore import QDate

    def search_doctor(self):
        """Search for doctor by CNIC and populate all fields."""
        try:
            cnic = self.cnic_input.text()
            if not cnic:
                QMessageBox.warning(self, "Input Error", "Please enter a CNIC.")
                return

            # Call the backend function to fetch data
            from Doctorsdata.DoctorsBackend import search_doctor_by_name
            doctor_data = search_doctor_by_name(cnic)

            if doctor_data:
                # Populate Personal Data
                self.first_name_input.setText(doctor_data["FirstName"])
                self.last_name_input.setText(doctor_data["LastName"])
                self.cnic_input.setText(doctor_data["CNIC"])
                self.license_no_input.setText(doctor_data["LicenseNo"])

                # Handle the joining date to ensure it's in the correct format
                if isinstance(doctor_data["JoiningDate"], datetime.date):
                    joining_date_str = doctor_data["JoiningDate"].strftime("%Y-%m-%d")
                    self.joining_date_input.setDate(QDate.fromString(joining_date_str, "yyyy-MM-dd"))
                else:
                    self.joining_date_input.setText(
                        doctor_data["JoiningDate"])  # Assuming it's already a string in the correct format

                self.job_status_input.setText(doctor_data["JobStatus"])

                # Populate Salary
                self.salary_amount_input.setText(str(doctor_data["Amount"]))

                # Populate Address
                self.city_input.setText(doctor_data["city"])
                self.street_input.setText(doctor_data["street"])
                self.state_input.setText(doctor_data["state"])
                self.postal_code_input.setText(doctor_data["postal_code"])
                self.country_input.setText(doctor_data["country"])

                # Populate Credentials
                self.username_input.setText(doctor_data["Username"])
                self.password_input.setText(doctor_data["PasswordHash"])

                QMessageBox.information(self, "Search Successful", "Doctor data loaded successfully.")
            else:
                QMessageBox.warning(self, "Search Failed", f"No doctor found with CNIC: {cnic}")
        except Exception as e:
            # Handle unexpected errors
            QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{str(e)}")
            print(f"Error during search: {e}")

    def update_personal_data(self):
        cnic = self.cnic_input.text()
        if not cnic:
            print("CNIC is required to update personal data.")
            return

        # Collect data
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        license_no = self.license_no_input.text()
        joining_date = self.joining_date_input.date().toString("yyyy-MM-dd")
        job_status = self.job_status_input.text()

        # Call backend function
        from Doctorsdata.DoctorsBackend import update_personal_data
        success = update_personal_data(
            cnic=cnic,
            first_name=first_name,
            last_name=last_name,
            license_no=license_no,
            joining_date=joining_date,
            job_status=job_status,
        )

        if success:
            print("Personal data updated successfully.")
            QMessageBox.information(self, "Update Successful", "Personal data has been updated successfully!")
        else:
            print("Failed to update personal data.")
            QMessageBox.warning(self, "Update Failed", "Failed to update personal data. Please try again.")

    def update_salary(self):
        cnic = self.cnic_input.text()
        if not cnic:
            print("CNIC is required to update salary.")
            return

        # Collect data
        salary_amount = self.salary_amount_input.text()

        # Call backend function
        from Doctorsdata.DoctorsBackend import update_salary
        success = update_salary(cnic=cnic, amount=salary_amount)

        if success:
            print("Salary updated successfully.")
            QMessageBox.information(self, "Update Successful", "Salary has been updated successfully!")
        else:
            print("Failed to update salary.")
            QMessageBox.warning(self, "Update Failed", "Failed to update salary. Please try again.")

    def update_address(self):
        cnic = self.cnic_input.text()
        if not cnic:
            print("CNIC is required to update address.")
            return

        # Collect data
        city = self.city_input.text()
        street = self.street_input.text()
        state = self.state_input.text()
        postal_code = self.postal_code_input.text()
        country = self.country_input.text()

        # Call backend function
        from Doctorsdata.DoctorsBackend import update_address
        success = update_address(
            cnic=cnic,
            city=city,
            street=street,
            state=state,
            postal_code=postal_code,
            country=country,
        )

        if success:
            print("Address updated successfully.")
            QMessageBox.information(self, "Update Successful", "Address has been updated successfully!")
        else:
            print("Failed to update address.")
            QMessageBox.warning(self, "Update Failed", "Failed to update address. Please try again.")

    def update_credentials(self):
        cnic = self.cnic_input.text()
        if not cnic:
            print("CNIC is required to update credentials.")
            return

        # Collect data
        username = self.username_input.text()
        password = self.password_input.text()

        # Call backend function
        from Doctorsdata.DoctorsBackend import update_credentials
        success = update_credentials(cnic=cnic, username=username, password=password)

        if success:
            print("Credentials updated successfully.")
            QMessageBox.information(self, "Update Successful", "Credentials have been updated successfully!")
        else:
            print("Failed to update credentials.")
            QMessageBox.warning(self, "Update Failed", "Failed to update credentials. Please try again.")
