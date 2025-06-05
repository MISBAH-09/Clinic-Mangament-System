from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QStackedWidget, QLineEdit, QTextEdit # type: ignore
from PyQt5.QtCore import Qt # type: ignore
from PyQt5.QtGui import QFont # type: ignore
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView




class AdminScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clinic Admin Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Top bar with doctor's name and logout button
        top_bar = QHBoxLayout()
        doctor_name_label = QLabel("Dr. John Doe")
        doctor_name_label.setFont(QFont("Arial", 16))
        doctor_name_label.setStyleSheet("padding: 10px;")

        logout_button = QPushButton("Logout")
        logout_button.setFont(QFont("Arial", 12))
        logout_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")
        logout_button.clicked.connect(self.logout)

        top_bar.addWidget(doctor_name_label, alignment=Qt.AlignLeft)
        top_bar.addWidget(logout_button, alignment=Qt.AlignRight)

        # Search bar
        search_bar = QHBoxLayout()
        search_label = QLabel("Enter Patient ID:")
        search_label.setFont(QFont("Arial", 14))
        self.search_input = QLineEdit()
        self.search_input.setMaximumWidth(300)
        self.search_input.setFont(QFont("Arial", 12))
        search_button = QPushButton("Search")
        search_button.setFont(QFont("Arial", 12))
        search_button.setMaximumWidth(150)
        search_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 5px;")
        search_button.clicked.connect(self.search_patient)

        search_bar.addWidget(search_label)
        search_bar.addWidget(self.search_input)
        search_bar.addWidget(search_button)

        # Sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)  # Remove layout margins
        sidebar_layout.setSpacing(5)  # Remove spacing between buttons

        sidebar_buttons = {
            "Dashboard": self.show_dashboard,
            "Patients": self.show_patients,
            "Doctors/Staff": self.show_doctors,
            "Billing": self.show_billing,
            "Reports": self.show_reports,
            "Inventory": self.show_inventory,
        }

        for text, action in sidebar_buttons.items():
            btn = QPushButton(text)
            btn.setFont(QFont("Arial", 14))
            btn.setStyleSheet("padding: 5px;")  # Add consistent padding for the buttons
            btn.clicked.connect(action)
            sidebar_layout.addWidget(btn)

        # Center the sidebar in the frame
        centered_layout = QVBoxLayout()
        centered_layout.addStretch()  # Add stretchable space above
        centered_layout.addLayout(sidebar_layout)  # Add the sidebar layout
        centered_layout.addStretch()  # Add stretchable space below

        sidebar_frame = QFrame()
        sidebar_frame.setLayout(centered_layout)
        sidebar_frame.setStyleSheet("background-color: #d3d3d3; padding: 5px;")

        # Content area setup
        self.stacked_widget = QStackedWidget()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.create_label_page("Dashboard Overview"))
        self.stacked_widget.addWidget(self.create_patients_page())  # Patients page
        self.stacked_widget.addWidget(self.create_doctors_staff_page())  # Doctors/Staff page
        self.stacked_widget.addWidget(self.create_billing_page())  # Billing page
        self.stacked_widget.addWidget(self.create_reports_page())  # Reports page
        self.stacked_widget.addWidget(self.create_inventory_page())  # Inventory page

        # Main content area
        main_content = QHBoxLayout()
        main_content.addWidget(sidebar_frame, 1)
        main_content.addWidget(self.stacked_widget, 4)

        # Add top bar, search bar, and main content to the main layout
        main_layout.addLayout(top_bar)
        main_layout.addLayout(search_bar)
        main_layout.addLayout(main_content)

        self.setLayout(main_layout)

    def logout(self):
            # Emit a signal or directly call a method in the parent to go back to login screen
            self.parent().showLoginPage()

    def search_patient(self):
        # Perform patient search logic here
        patient_id = self.search_input.text()
        print(f"Searching for patient ID: {patient_id}")

    def create_label_page(self, text):
        """Creates a placeholder page with a label."""
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(text)
        label.setStyleSheet("font-size: 24px; margin: 20px;")
        layout.addWidget(label)
        layout.addStretch()
        return page

    from PyQt5.QtWidgets import QPushButton

    def create_patients_page(self):
        """Creates the Patients page with a button to add a new patient."""
        page = QWidget()
        self.patients_layout = QVBoxLayout(page)

        # Section header
        label = QLabel("Patients")
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        self.patients_layout.addWidget(label)

        # Add buttons
        self.add_patient_button = QPushButton("Add New Patient")
        self.add_patient_button.clicked.connect(self.toggle_add_new_patient_form)
        self.patients_layout.addWidget(self.add_patient_button)

        # Placeholder for the "View Patient Records" button
        self.add_view_button = QPushButton("View Patient Records")
        self.add_view_button.clicked.connect(self.toggle_view_patient_records)
        self.patients_layout.addWidget(self.add_view_button)

        # self.patients_layout.addWidget(self.create_button_with_pointer("View Patient Records"))
        self.patients_layout.addWidget(self.create_button_with_pointer("Edit/Update Patient Information"))
        self.patients_layout.addWidget(self.create_button_with_pointer("Delete Patient"))

        # Placeholder for the "Add New Patient" form
        self.add_patient_form = self.create_add_new_patient_page()
        self.add_patient_form.setVisible(False)  # Initially hidden
        self.patients_layout.addWidget(self.add_patient_form)

        # Placeholder for the "View Patient Information" form
        self.view_patient_info = self.create_view_patient_page()
        self.view_patient_info.setVisible(False)  # Initially hidden
        self.patients_layout.addWidget(self.view_patient_info)

        self.patients_layout.addStretch()
        return page

    def toggle_add_new_patient_form(self):
        """Shows or hides the 'Add New Patient' form."""
        if self.add_patient_form.isVisible():
            self.add_patient_form.setVisible(False)
            self.add_patient_button.setText("Add New Patient")
        else:
            self.add_patient_form.setVisible(True)
            self.add_patient_button.setText("Close Add Patient Form")

    def toggle_view_patient_records(self):
        """Shows or hides the 'View Patient Information' form."""
        if self.view_patient_info.isVisible():
            self.view_patient_info.setVisible(False)
            self.add_view_button.setText("View Patient Information")
        else:
            self.view_patient_info.setVisible(True)
            self.add_view_button.setText("Close View Patient Form")

    def create_doctors_staff_page(self):
        """Creates the Doctors/Staff page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Doctors & Staff")
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(label)

        # Add any other content here (buttons, tables, etc.)
        layout.addStretch()
        return page

    def create_billing_page(self):
        """Creates the Billing page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Billing")
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(label)

        # Add other elements for the billing page here (buttons, tables, etc.)
        layout.addStretch()
        return page

    def create_reports_page(self):
        """Creates the Reports page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Reports")
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(label)

        # Add other elements for the reports page here (e.g., buttons, tables, etc.)
        layout.addStretch()
        return page

    def create_inventory_page(self):
        """Creates the Inventory page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel("Inventory")
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(label)

        # Add other elements for the inventory page (e.g., buttons, tables, etc.)
        layout.addStretch()
        return page

    def create_button_with_pointer(self, text, action=None):
        """Creates a QPushButton with a pointer cursor and optional action."""
        button = QPushButton(text)
        button.setCursor(Qt.PointingHandCursor)  # Set pointer cursor
        if action:
            button.clicked.connect(action)
        return button

    def open_add_new_patient_page(self):
        try:
            print("Button clicked. Opening Add New Patient page...")
            add_patient_page = self.create_add_new_patient_page()
            self.stacked_widget.addWidget(add_patient_page)
            self.stacked_widget.setCurrentWidget(add_patient_page)
        except Exception as e:
            print(f"Error: {e}")

    def create_add_new_patient_page(self):
        """Creates the Add New Patient form page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Form layout using QGridLayout
        form_layout = QGridLayout()
        form_layout.setContentsMargins(10, 0, 10, 0)
        form_layout.setVerticalSpacing(10)

        # Styles for labels and input fields
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
        self.registration_date_input = QDateEdit(QDate.currentDate())
        self.registration_date_input.setCalendarPopup(True)
        self.registration_date_input.setDisplayFormat("dd/MM/yyyy")
        self.registration_date_input.setReadOnly(True)
        self.registration_date_input.setStyleSheet(input_style)
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

        return page

    def create_view_patient_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Dropdown and buttons
        filter_layout = QHBoxLayout()
        department_dropdown = QComboBox()
        department_dropdown.addItems(["Operative Dentistry", "Orthodontics", "Pediatrics"])
        refresh_button = QPushButton("Refresh")
        refresh_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 5px;")
        search_patient_button = QPushButton("Search Patient")
        search_patient_button.setStyleSheet(
            "background-color: #2196F3; color: white; padding: 5px 10px; border-radius: 5px;")

        filter_layout.addWidget(department_dropdown)
        filter_layout.addWidget(refresh_button)
        filter_layout.addWidget(search_patient_button)

        # Table
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(
            ["Name", "MR No.", "Gender", "Age", "Department Name", "Send Status", "CheckedOut By", "Referral Date"])
        table.horizontalHeader().setStretchLastSection(True)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Example data
        patients = [
            ["zainab iftikhar", "24-0012502", "Female", "32", "Operative Dentistry", "--", "--", "10/7/2024 2:09 PM"],
            ["emaan imran", "24-0012501", "Female", "23", "Operative Dentistry", "--", "--", "10/7/2024 1:26 PM"],
            ["raheela nadeem", "24-0012496", "Female", "32", "Operative Dentistry", "--", "--", "10/7/2024 11:22 AM"],
        ]

        table.setRowCount(len(patients))
        for row_idx, row_data in enumerate(patients):
            for col_idx, cell_data in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(cell_data))

        # Add components to layout
        layout.addLayout(filter_layout)
        layout.addWidget(QLabel("Search Records"))
        layout.addWidget(table)

        page.setLayout(layout)
        return page

    # Button actions for switching pages
    def show_dashboard(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_patients(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_doctors(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_billing(self):
        self.stacked_widget.setCurrentIndex(3)

    def show_reports(self):
        self.stacked_widget.setCurrentIndex(4)

    def show_inventory(self):
        self.stacked_widget.setCurrentIndex(5)
