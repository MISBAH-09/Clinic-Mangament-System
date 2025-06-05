from PyQt5.QtWidgets import ( # type: ignore
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QTextEdit, QDateEdit, QComboBox, QSpacerItem, QSizePolicy, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt, QDate # type: ignore
from PyQt5.QtGui import QFont # type: ignore

class DoctorScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Doctor Panel")
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

        # Main content area
        main_content = QHBoxLayout()

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(0, 0, 0, 0)  # Remove layout margins
        sidebar.setSpacing(5)  # Remove spacing between buttons

        sidebar_buttons = {
            "Patient Data": self.show_patient_data,
            "Diagnosis": self.show_diagnosis,
            "Medicine and Test": self.show_medicine,
            "History": self.show_history,
            "Submit & Recheck": self.show_submit,
            "BLA BLA BLA":self.show_bla_bla,
        }

        for text, action in sidebar_buttons.items():
            btn = QPushButton(text)
            btn.setFont(QFont("Arial", 14))
            btn.setStyleSheet("padding: 5px;")  # Add consistent padding for the buttons
            btn.clicked.connect(action)
            sidebar.addWidget(btn)

        # Center the sidebar in the frame
        centered_layout = QVBoxLayout()
        centered_layout.addStretch()  # Add stretchable space above
        centered_layout.addLayout(sidebar)  # Add the sidebar layout
        centered_layout.addStretch()  # Add stretchable space below

        sidebar_frame = QFrame()
        sidebar_frame.setLayout(centered_layout)
        sidebar_frame.setStyleSheet("background-color: #d3d3d3; padding: 5px;")


        # Content area to display data based on sidebar selection
        self.content_area = QStackedWidget()

        # Add placeholder widgets for each section
        self.content_area.addWidget(self.create_patient_data_page())
        self.content_area.addWidget(self.create_diagnosis_page())
        self.content_area.addWidget(self.create_medicine_page())
        self.content_area.addWidget(self.create_history_page())
        self.content_area.addWidget(self.create_submit_page())
        self.content_area.addWidget(self.create_BLA_BLA_page())

        main_content.addWidget(sidebar_frame, 1)
        main_content.addWidget(self.content_area, 4)

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

    def show_patient_data(self):
        self.content_area.setCurrentIndex(0)

    def show_diagnosis(self):
        self.content_area.setCurrentIndex(1)

    def show_medicine(self):
        self.content_area.setCurrentIndex(2)

    def show_history(self):
        self.content_area.setCurrentIndex(3)

    def show_submit(self):
        self.content_area.setCurrentIndex(4)
    def show_bla_bla(self):
        self.content_area.setCurrentIndex(5)

    def create_patient_data_page(self): 
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
    
    def create_diagnosis_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Presenting Complaints
        presenting_label = QLabel("Presenting Complaints:")
        presenting_label.setFont(QFont("Arial", 14))
        self.presenting_input = QTextEdit()
        self.presenting_input.setFixedHeight(100)
        layout.addWidget(presenting_label)
        layout.addWidget(self.presenting_input)

        # History
        history_label = QLabel("History:")
        history_label.setFont(QFont("Arial", 14))
        self.history_input = QTextEdit()
        self.history_input.setFixedHeight(100)
        layout.addWidget(history_label)
        layout.addWidget(self.history_input)

        # Duration
        duration_label = QLabel("Duration:")
        duration_label.setFont(QFont("Arial", 14))
        self.duration_input = QLineEdit()
        layout.addWidget(duration_label)
        layout.addWidget(self.duration_input)

        # Timing Checkboxes
        timing_label = QLabel("Timing:")
        timing_label.setFont(QFont("Arial", 14))
        layout.addWidget(timing_label)
        
        self.timing_occasional = QPushButton("Occasionally")
        self.timing_random = QPushButton("Random")
        for button in [self.timing_occasional, self.timing_random]:
            button.setCheckable(True)
            button.setStyleSheet("padding: 5px;")
            layout.addWidget(button)

        layout.addStretch()
        return page

    from PyQt5.QtWidgets import (
        QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout,
        QPushButton, QScrollArea, QFrame, QVBoxLayout
    )
    from PyQt5.QtGui import QFont
    from PyQt5.QtCore import Qt

    def create_medicine_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Medicine Selection
        medicine_label = QLabel("Select Medicines:")
        medicine_label.setFont(QFont("Arial", 14))
        self.medicine_dropdown = QComboBox()
        self.medicine_dropdown.setEditable(False)  # Dropdown is not editable
        self.medicine_dropdown.addItems(["Paracetamol", "Ibuprofen", "Antibiotics"])  # Example medicines
        self.medicine_dropdown.currentIndexChanged.connect(self.add_medicine)
        layout.addWidget(medicine_label)
        layout.addWidget(self.medicine_dropdown)
        
        # Test Selection
        test_label = QLabel("Select Tests:")
        test_label.setFont(QFont("Arial", 14))
        self.test_dropdown = QComboBox()
        self.test_dropdown.setEditable(False)  # Dropdown is not editable
        self.test_dropdown.addItems(["Blood Test", "X-Ray", "MRI"])  # Example tests
        self.test_dropdown.currentIndexChanged.connect(self.add_test)
        layout.addWidget(test_label)
        layout.addWidget(self.test_dropdown)
        
        # Selected Medicines Display
        selected_medicines_label = QLabel("Selected Medicines:")
        selected_medicines_label.setFont(QFont("Arial", 12))
        layout.addWidget(selected_medicines_label)
        self.medicine_display_area = self.create_scrollable_area()
        layout.addWidget(self.medicine_display_area)
        
        # Selected Tests Display
        selected_tests_label = QLabel("Selected Tests:")
        selected_tests_label.setFont(QFont("Arial", 12))
        layout.addWidget(selected_tests_label)
        self.test_display_area = self.create_scrollable_area()
        layout.addWidget(self.test_display_area)
        
        layout.addStretch()
        return page

    def create_scrollable_area(self):
        scroll_area = QScrollArea() # type: ignore
        scroll_area.setWidgetResizable(True)
        scroll_content = QFrame()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        return scroll_area

    def add_medicine(self):
        selected_medicine = self.medicine_dropdown.currentText()
        if selected_medicine and not self.is_item_already_added(self.medicine_display_area, selected_medicine):
            self.add_item_to_display(self.medicine_display_area, selected_medicine)

    def add_test(self):
        selected_test = self.test_dropdown.currentText()
        if selected_test and not self.is_item_already_added(self.test_display_area, selected_test):
            self.add_item_to_display(self.test_display_area, selected_test)

    def is_item_already_added(self, display_area, item_text):
        scroll_content = display_area.widget()
        for i in range(scroll_content.layout().count()):
            item_widget = scroll_content.layout().itemAt(i).widget()
            if item_widget and item_widget.text() == item_text:
                return True
        return False

    def add_item_to_display(self, display_area, item_text):
        scroll_content = display_area.widget()
        layout = scroll_content.layout()
        
        # Create a horizontal layout for the item and its remove button
        item_layout = QHBoxLayout()
        item_label = QLabel(item_text)
        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet("color: red; font-size: 10pt;")
        remove_button.clicked.connect(lambda: self.remove_item(item_layout, display_area))
        item_layout.addWidget(item_label)
        item_layout.addWidget(remove_button)
        item_layout.setAlignment(Qt.AlignLeft)
        
        # Add the horizontal layout to the scroll area's content
        item_widget = QWidget()
        item_widget.setLayout(item_layout)
        layout.addWidget(item_widget)

    def remove_item(self, item_layout, display_area):
        scroll_content = display_area.widget()
        layout = scroll_content.layout()
        for i in range(layout.count()):
            if layout.itemAt(i).layout() == item_layout:
                widget_to_remove = layout.itemAt(i).widget()
                if widget_to_remove:
                    widget_to_remove.deleteLater()
                layout.removeItem(layout.itemAt(i))
                break



    # def create_diagnosis_page(self):
    #     page = QWidget()
    #     layout = QVBoxLayout(page)
    #     layout.addWidget(QLabel("Diagnosis"))
    #     # Add fields for presenting complaint, duration, etc.
    #     layout.addStretch()
    #     return page

    # def create_medicine_page(self):
    #     page = QWidget()
    #     layout = QVBoxLayout(page)
    #     layout.addWidget(QLabel("Medicine"))
    #     # Add dropdowns for medicines and tests
    #     layout.addStretch()
    #     return page

    def create_history_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("History"))
        # Add history fields
        layout.addStretch()
        return page
    
    def create_submit_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Submit and Recheck Data"))
        # Add fields 
        layout.addStretch()
        return page
    
    def create_BLA_BLA_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("blaa bla"))
        # Add fields 
        layout.addStretch()
        return page
