from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QTextEdit, QDateEdit, QComboBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import datetime

class PatientDataPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.visit_id = None
        self.initUI()

    def set_visit_id(self, visit_id):
        self.visit_id = visit_id  # Store the visit ID

    def initUI(self):
        layout = QVBoxLayout(self)
        form_layout = QGridLayout()
        form_layout.setContentsMargins(10, 0, 10, 0)
        form_layout.setVerticalSpacing(10)

        label_style = "font-size: 14px; color: #333333;"
        input_style = "font-size: 12px; padding: 5px;"

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

        # Date of Birth
        dob_label = QLabel("Date of Birth:")
        dob_label.setStyleSheet(label_style)
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("dd/MM/yyyy")
        self.dob_input.setStyleSheet(input_style)
        self.dob_input.setDate(QDate())  # Set default to empty date
        form_layout.addWidget(dob_label, 1, 0)
        form_layout.addWidget(self.dob_input, 1, 1)

        # CNIC
        cnic_label = QLabel("CNIC:")
        cnic_label.setStyleSheet(label_style)
        self.cnic_input = QLineEdit()
        self.cnic_input.setStyleSheet(input_style)
        form_layout.addWidget(cnic_label, 1, 2)
        form_layout.addWidget(self.cnic_input, 1, 3)

        # Contact Number
        contact_number_label = QLabel("Contact Number:")
        contact_number_label.setStyleSheet(label_style)
        self.contact_number_input = QLineEdit()
        self.contact_number_input.setStyleSheet(input_style)
        form_layout.addWidget(contact_number_label, 2, 0)
        form_layout.addWidget(self.contact_number_input, 2, 1)

        # Gender
        gender_label = QLabel("Gender:")
        gender_label.setStyleSheet(label_style)
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        self.gender_input.setStyleSheet(input_style)
        form_layout.addWidget(gender_label, 2, 2)
        form_layout.addWidget(self.gender_input, 2, 3)

        # Email
        email_label = QLabel("Email:")
        email_label.setStyleSheet(label_style)
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet(input_style)
        form_layout.addWidget(email_label, 3, 0)
        form_layout.addWidget(self.email_input, 3, 1)

        # Date of Registration
        registration_date_label = QLabel("Date of Registration:")
        registration_date_label.setStyleSheet(label_style)
        self.registration_date_input = QDateEdit()
        self.registration_date_input.setCalendarPopup(True)
        self.registration_date_input.setDisplayFormat("dd/MM/yyyy")
        self.registration_date_input.setReadOnly(True)
        self.registration_date_input.setStyleSheet(input_style)
        self.registration_date_input.setDate(QDate())  # Set default to empty date
        form_layout.addWidget(registration_date_label, 3, 2)
        form_layout.addWidget(self.registration_date_input, 3, 3)

        # Address
        address_label = QLabel("Address:")
        address_label.setStyleSheet(label_style)
        self.address_input = QTextEdit()
        self.address_input.setFixedHeight(100)
        self.address_input.setStyleSheet(input_style)
        form_layout.addWidget(address_label, 4, 0)
        form_layout.addWidget(self.address_input, 4, 1, 1, 3)

        layout.addLayout(form_layout)
        layout.addStretch()

    def set_patient_data(self, patient_id, first_name, last_name, dob, cnic, contact, gender, email, address, reg_date):
        self.first_name_input.setText(first_name)
        self.last_name_input.setText(last_name)

        # # Check if dob and reg_date are datetime objects or properly formatted strings
        # if isinstance(dob, (datetime.date, datetime)):
        #     dob = dob.strftime("%Y-%m-%d")
        # if isinstance(reg_date, (datetime.date, datetime)):
        #     reg_date = reg_date.strftime("%Y-%m-%d")

        # # Set Date of Birth and Date Registered as QDate objects
        # self.dob_input.setDate(QDate.fromString(dob, "yyyy-MM-dd") if dob else QDate())
        # self.registration_date_input.setDate(QDate.fromString(reg_date, "yyyy-MM-dd") if reg_date else QDate())

        self.cnic_input.setText(cnic)
        self.contact_number_input.setText(contact)
        self.gender_input.setCurrentText(gender)
        self.email_input.setText(email)
        self.address_input.setText(address)
