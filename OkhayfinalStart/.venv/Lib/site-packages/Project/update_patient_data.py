from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QComboBox, QPushButton, QSpacerItem, QSizePolicy, QGridLayout, QFrame
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from ReceptionBackend import show_error
from ReceptionBackend import show_success


class UpdatePatientScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Patient")
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Update Patient")
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

        # Create form layout inside a framed box
        form_frame = QFrame()
        form_frame.setStyleSheet("border: 2px solid #333333; padding: 20px;")
        form_layout = QGridLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setVerticalSpacing(10)

        # Spacer to push form content towards the top
        top_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(top_spacer, 0, 0, 1, 4)

        # Style for labels and input fields
        label_style = "font-size: 16px; color: #333333;"
        input_style = "font-size: 16px; padding: 15px;"

        # Fields (Consistent with AddPatientScreen)
        self.first_name_input = self.create_input_field("First Name:", form_layout, 1, 0, input_style, label_style)
        self.last_name_input = self.create_input_field("Last Name:", form_layout, 1, 2, input_style, label_style)
        self.dob_input = self.create_date_field("Date of Birth:", form_layout, 2, 0, input_style, label_style)
        self.contact_number_input = self.create_input_field("Contact Number:", form_layout, 2, 2, input_style, label_style)
        self.gender_input = self.create_combo_box_field("Gender:", ["Male", "Female", "Other"], form_layout, 3, 0, input_style, label_style)
        self.email_input = self.create_input_field("Email:", form_layout, 3, 2, input_style, label_style)
        self.registration_date_input = self.create_date_field("Date of Registration:", form_layout, 4, 0, input_style, label_style, readonly=True)
        self.address_input = self.create_text_edit_field("Address:", form_layout, 4, 2, input_style, label_style)

        # Spacer to push form content towards the bottom
        bottom_spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(bottom_spacer, 5, 0, 1, 4)

        # Update Button
        update_button = QPushButton("Update Patient")
        update_button.setFont(QFont("Arial", 14, QFont.Bold))
        update_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        update_button.clicked.connect(self.update_patient)
        form_layout.addWidget(update_button, 6, 2)

        # Add form layout to the main layout
        main_layout.addWidget(form_frame)

        # Set the main layout
        self.setLayout(main_layout)

    def create_input_field(self, label_text, form_layout, row, col, input_style, label_style):
        label = QLabel(label_text)
        label.setStyleSheet(label_style)
        input_field = QLineEdit()
        input_field.setStyleSheet(input_style)
        form_layout.addWidget(label, row, col)
        form_layout.addWidget(input_field, row, col + 1)
        return input_field

    def create_date_field(self, label_text, form_layout, row, col, input_style, label_style, readonly=False):
        label = QLabel(label_text)
        label.setStyleSheet(label_style)
        date_field = QDateEdit(QDate.currentDate())
        date_field.setCalendarPopup(True)
        date_field.setDisplayFormat("dd/MM/yyyy")
        date_field.setStyleSheet(input_style)
        if readonly:
            date_field.setReadOnly(True)
        form_layout.addWidget(label, row, col)
        form_layout.addWidget(date_field, row, col + 1)
        return date_field

    def create_combo_box_field(self, label_text, options, form_layout, row, col, input_style, label_style):
        label = QLabel(label_text)
        label.setStyleSheet(label_style)
        combo_box = QComboBox()
        combo_box.addItems(options)
        combo_box.setStyleSheet(input_style)
        form_layout.addWidget(label, row, col)
        form_layout.addWidget(combo_box, row, col + 1)
        return combo_box

    def create_text_edit_field(self, label_text, form_layout, row, col, input_style, label_style):
        label = QLabel(label_text)
        label.setStyleSheet(label_style)
        text_edit = QTextEdit()
        text_edit.setFixedHeight(100)
        text_edit.setStyleSheet(input_style)
        form_layout.addWidget(label, row, col)
        form_layout.addWidget(text_edit, row, col + 1)
        return text_edit

    def search_patient(self):
        try:
            cnic = self.cnic_input.text().strip()
            if not cnic:
                show_error("Please enter a CNIC to search.")
                return

            from ReceptionBackend import search_patient_by_cnic
            patient = search_patient_by_cnic(cnic)
            print("Patient Data:", patient)  # Log patient data

            if patient:
                # Unpack and log each field
                (patient_id, first_name, last_name, cnic, dob, gender, contact, email, address, reg_date) = patient
                print(
                    f"ID: {patient_id}, Name: {first_name} {last_name}, DOB: {dob}, Gender: {gender}, Contact: {contact}, Email: {email}, Address: {address}, Reg Date: {reg_date}")

                # Populate fields in the UI
                self.patient_id = patient_id
                self.first_name_input.setText(first_name)
                self.last_name_input.setText(last_name)
                self.dob_input.setDate(
                    QDate.fromString(dob.strftime("%Y-%m-%d"), "yyyy-MM-dd") if dob else QDate.currentDate())
                self.gender_input.setCurrentText(gender)
                self.contact_number_input.setText(contact)
                self.email_input.setText(email)
                self.address_input.setPlainText(address)
                self.registration_date_input.setDate(
                    QDate.fromString(reg_date.strftime("%Y-%m-%d"), "yyyy-MM-dd") if reg_date else QDate.currentDate())
            else:
                show_error("No patient found with the provided CNIC.")
        except Exception as e:
            print(f"Error in search_patient: {e}")
            show_error("An error occurred while searching for the patient.")

    def update_patient(self):
        if not hasattr(self, 'patient_id'):
            from ReceptionBackend import show_error
            show_error("Please search for a patient before updating.")
            return

        # Gather updated data from the input fields
        patient_id = self.patient_id
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        dob = self.dob_input.date().toString("yyyy-MM-dd")
        gender = self.gender_input.currentText()
        contact_number = self.contact_number_input.text()
        email = self.email_input.text()
        address = self.address_input.toPlainText()
        date_registered = self.registration_date_input.date().toString("yyyy-MM-dd")

        # Call the backend function to update patient details
        from ReceptionBackend import update_patient_data
        success = update_patient_data(patient_id, first_name, last_name, dob, gender, contact_number, email, address,
                                      date_registered)
        if success:
            from ReceptionBackend import show_success
            show_success("Patient details updated successfully.")
        else:
            from ReceptionBackend import show_error
            show_error("Failed to update patient details.")

