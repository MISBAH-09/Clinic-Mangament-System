
import sys
from PyQt5.QtWidgets import ( # type: ignore
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QStackedWidget, QWidget, QLineEdit, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt  # type: ignore # For cursor settings

class AdminDashboard(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clinic Admin Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Main container widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layouts
        main_layout = QHBoxLayout(main_widget)
        sidebar_layout = QVBoxLayout()
        content_layout = QVBoxLayout()

        # Sidebar
        sidebar_buttons = {
            "Dashboard": self.show_dashboard,
            "Appointments": self.show_appointments,
            "Patients": self.show_patients,
            "Doctors/Staff": self.show_doctors,
            "Billing": self.show_billing,
            "Reports": self.show_reports,
            "Inventory": self.show_inventory,
            "Settings": self.show_settings,
        }

        for text, action in sidebar_buttons.items():
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)  # Add pointer cursor to sidebar buttons
            btn.clicked.connect(action)
            sidebar_layout.addWidget(btn)

        # Add stretch before and after the buttons to center them vertically
        sidebar_layout.insertStretch(0)  # Spacer above the buttons
        sidebar_layout.addStretch()  # Spacer below the buttons

        sidebar = QFrame()
        sidebar.setLayout(sidebar_layout)
        sidebar.setStyleSheet("background-color: #d3d3d3; padding: 10px;")

        # Content area
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_label_page("Dashboard Overview"))
        self.stacked_widget.addWidget(self.create_appointments_page())
        self.stacked_widget.addWidget(self.create_patients_page())
        self.stacked_widget.addWidget(self.create_doctors_staff_page())
        self.stacked_widget.addWidget(self.create_billing_page())
        self.stacked_widget.addWidget(self.create_reports_page())
        self.stacked_widget.addWidget(self.create_inventory_page())
        self.stacked_widget.addWidget(self.create_settings_page())

        content_layout.addWidget(self.stacked_widget)
        content_area = QFrame()
        content_area.setLayout(content_layout)

        # Adding layouts to the main layout
        main_layout.addWidget(sidebar, 2)
        main_layout.addWidget(content_area, 8)

    def create_label_page(self, text):
        """Creates a placeholder page with a label."""
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(text)
        label.setStyleSheet("font-size: 24px; margin: 20px;")
        layout.addWidget(label)
        layout.addStretch()
        return page

    def create_appointments_page(self):
        """Creates the Appointments page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title Label
        label = QLabel("Appointments")
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(label)

        # View All Appointments Button
        view_all_btn = QPushButton("View All Appointments")
        view_all_btn.setCursor(Qt.PointingHandCursor)
        view_all_btn.clicked.connect(self.view_all_appointments)  # Connect to handler
        layout.addWidget(view_all_btn)

        # Schedule New Appointment Button
        schedule_btn = QPushButton("Schedule New Appointment")
        schedule_btn.setCursor(Qt.PointingHandCursor)
        schedule_btn.clicked.connect(self.schedule_new_appointment)  # Connect to handler
        layout.addWidget(schedule_btn)

        # Cancel Appointment Button
        cancel_btn = QPushButton("Cancel Appointment")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.cancel_appointment)  # Connect to handler
        layout.addWidget(cancel_btn)

        # Search Input
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by date, doctor, or patient...")
        layout.addWidget(search_input)

        layout.addStretch()  # Add stretch for spacing
        return page
        # button functions

    def view_all_appointments(self):
        """Handles the 'View All Appointments' button click."""
        print("View All Appointments button clicked!")
        # Add logic to display or fetch all appointments

    def schedule_new_appointment(self):
        """Handles the 'Schedule New Appointment' button click."""
        print("Schedule New Appointment button clicked!")
        # Add logic for scheduling a new appointment

    def cancel_appointment(self):
        """Handles the 'Cancel Appointment' button click."""
        print("Cancel Appointment button clicked!")
        # Add logic to cancel an appointment

    def create_patients_page(self):
        """Creates the Patients page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title Label
        label = QLabel("Patients")
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(label)

        # Add New Patient Button
        add_patient_btn = QPushButton("Add New Patient")
        add_patient_btn.setCursor(Qt.PointingHandCursor)
        add_patient_btn.clicked.connect(self.add_new_patient)  # Connect to handler
        layout.addWidget(add_patient_btn)

        # View Patient Records Button
        view_records_btn = QPushButton("View Patient Records")
        view_records_btn.setCursor(Qt.PointingHandCursor)
        view_records_btn.clicked.connect(self.view_patient_records)  # Connect to handler
        layout.addWidget(view_records_btn)

        # Edit/Update Patient Information Button
        edit_patient_btn = QPushButton("Edit/Update Patient Information")
        edit_patient_btn.setCursor(Qt.PointingHandCursor)
        edit_patient_btn.clicked.connect(self.edit_patient_information)  # Connect to handler
        layout.addWidget(edit_patient_btn)

        # Delete Patient Button
        delete_patient_btn = QPushButton("Delete Patient")
        delete_patient_btn.setCursor(Qt.PointingHandCursor)
        delete_patient_btn.clicked.connect(self.delete_patient)  # Connect to handler
        layout.addWidget(delete_patient_btn)

        # Search Input
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by name, age, or ailment...")
        layout.addWidget(search_input)

        layout.addStretch()  # Add stretch for spacing
        return page

    #button function
    def add_new_patient(self):
        """Handles the 'Add New Patient' button click."""
        print("Add New Patient button clicked!")
        # Implement the logic for adding a new patient

    def view_patient_records(self):
        """Handles the 'View Patient Records' button click."""
        print("View Patient Records button clicked!")
        # Implement the logic to view patient records

    def edit_patient_information(self):
        """Handles the 'Edit/Update Patient Information' button click."""
        print("Edit/Update Patient Information button clicked!")
        # Implement the logic to edit patient information

    def delete_patient(self):
        """Handles the 'Delete Patient' button click."""
        print("Delete Patient button clicked!")
        # Implement the logic to delete a patient

    def create_doctors_staff_page(self):
        """Creates the Doctors/Staff page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title Label
        label = QLabel("Doctors/Staff")
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(label)

        # Add Doctor/Staff Button
        add_staff_btn = QPushButton("Add Doctor/Staff")
        add_staff_btn.setCursor(Qt.PointingHandCursor)
        add_staff_btn.clicked.connect(self.add_doctor_staff)  # Connect to handler
        layout.addWidget(add_staff_btn)

        # View Doctor Schedules Button
        view_schedules_btn = QPushButton("View Doctor Schedules")
        view_schedules_btn.setCursor(Qt.PointingHandCursor)
        view_schedules_btn.clicked.connect(self.view_doctor_schedules)  # Connect to handler
        layout.addWidget(view_schedules_btn)

        # Edit Staff Details Button
        edit_staff_btn = QPushButton("Edit Staff Details")
        edit_staff_btn.setCursor(Qt.PointingHandCursor)
        edit_staff_btn.clicked.connect(self.edit_staff_details)  # Connect to handler
        layout.addWidget(edit_staff_btn)

        # Remove Staff Button
        remove_staff_btn = QPushButton("Remove Staff")
        remove_staff_btn.setCursor(Qt.PointingHandCursor)
        remove_staff_btn.clicked.connect(self.remove_staff)  # Connect to handler
        layout.addWidget(remove_staff_btn)

        layout.addStretch()  # Add stretch for spacing
        return page

        # button function

    def add_doctor_staff(self):
        """Handles the 'Add Doctor/Staff' button click."""
        print("Add Doctor/Staff button clicked!")
        # Add logic for adding a doctor or staff

    def view_doctor_schedules(self):
        """Handles the 'View Doctor Schedules' button click."""
        print("View Doctor Schedules button clicked!")
        # Add logic to view doctor schedules

    def edit_staff_details(self):
        """Handles the 'Edit Staff Details' button click."""
        print("Edit Staff Details button clicked!")
        # Add logic to edit staff details

    def remove_staff(self):
        """Handles the 'Remove Staff' button click."""
        print("Remove Staff button clicked!")
        # Add logic to remove a staff member

    def create_billing_page(self):
        """Creates the Billing page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title Label
        label = QLabel("Billing")
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(label)

        # Generate Invoice Button
        generate_invoice_btn = QPushButton("Generate Invoice")
        generate_invoice_btn.setCursor(Qt.PointingHandCursor)
        generate_invoice_btn.clicked.connect(self.generate_invoice)  # Connect to handler
        layout.addWidget(generate_invoice_btn)

        # View Payment History Button
        view_payment_history_btn = QPushButton("View Payment History")
        view_payment_history_btn.setCursor(Qt.PointingHandCursor)
        view_payment_history_btn.clicked.connect(self.view_payment_history)  # Connect to handler
        layout.addWidget(view_payment_history_btn)

        # Record New Payment Button
        record_payment_btn = QPushButton("Record New Payment")
        record_payment_btn.setCursor(Qt.PointingHandCursor)
        record_payment_btn.clicked.connect(self.record_new_payment)  # Connect to handler
        layout.addWidget(record_payment_btn)

        # Summary Section
        summary = QTextEdit("Summary:\n- Pending Payments\n- Completed Payments")
        summary.setReadOnly(True)
        layout.addWidget(summary)

        layout.addStretch()
        return page

    # button functions
    def generate_invoice(self):
        """Handles the 'Generate Invoice' button click."""
        print("Generate Invoice button clicked!")
        # Add logic to generate an invoice

    def view_payment_history(self):
        """Handles the 'View Payment History' button click."""
        print("View Payment History button clicked!")
        # Add logic to view payment history

    def record_new_payment(self):
        """Handles the 'Record New Payment' button click."""
        print("Record New Payment button clicked!")
        # Add logic to record a new payment

    def create_reports_page(self):
        """Creates the Reports page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title Label
        label = QLabel("Reports")
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(label)

        # Generate Patient Reports Button
        generate_patient_reports_btn = QPushButton("Generate Patient Reports")
        generate_patient_reports_btn.setCursor(Qt.PointingHandCursor)
        generate_patient_reports_btn.clicked.connect(self.generate_patient_reports)  # Connect to handler
        layout.addWidget(generate_patient_reports_btn)

        # Generate Appointment Reports Button
        generate_appointment_reports_btn = QPushButton("Generate Appointment Reports")
        generate_appointment_reports_btn.setCursor(Qt.PointingHandCursor)
        generate_appointment_reports_btn.clicked.connect(self.generate_appointment_reports)  # Connect to handler
        layout.addWidget(generate_appointment_reports_btn)

        # Revenue Reports Button
        revenue_reports_btn = QPushButton("Revenue Reports")
        revenue_reports_btn.setCursor(Qt.PointingHandCursor)
        revenue_reports_btn.clicked.connect(self.generate_revenue_reports)  # Connect to handler
        layout.addWidget(revenue_reports_btn)

        layout.addStretch()  # Add stretch for spacing
        return page
    # button function
    def generate_patient_reports(self):
        """Handles the 'Generate Patient Reports' button click."""
        print("Generate Patient Reports button clicked!")
        # Add logic to generate patient reports

    def generate_appointment_reports(self):
        """Handles the 'Generate Appointment Reports' button click."""
        print("Generate Appointment Reports button clicked!")
        # Add logic to generate appointment reports

    def generate_revenue_reports(self):
        """Handles the 'Revenue Reports' button click."""
        print("Revenue Reports button clicked!")
        # Add logic to generate revenue reports

    def create_inventory_page(self):
        """Creates the Inventory page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title Label
        label = QLabel("Inventory")
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(label)

        # Add New Item Button
        add_item_btn = QPushButton("Add New Item")
        add_item_btn.setCursor(Qt.PointingHandCursor)
        add_item_btn.clicked.connect(self.add_new_item)  # Connect to handler
        layout.addWidget(add_item_btn)

        # View Inventory Button
        view_inventory_btn = QPushButton("View Inventory")
        view_inventory_btn.setCursor(Qt.PointingHandCursor)
        view_inventory_btn.clicked.connect(self.view_inventory)  # Connect to handler
        layout.addWidget(view_inventory_btn)

        # Low Stock Alerts Button
        low_stock_alerts_btn = QPushButton("Low Stock Alerts")
        low_stock_alerts_btn.setCursor(Qt.PointingHandCursor)
        low_stock_alerts_btn.clicked.connect(self.low_stock_alerts)  # Connect to handler
        layout.addWidget(low_stock_alerts_btn)

        # Order Supplies Button
        order_supplies_btn = QPushButton("Order Supplies")
        order_supplies_btn.setCursor(Qt.PointingHandCursor)
        order_supplies_btn.clicked.connect(self.order_supplies)  # Connect to handler
        layout.addWidget(order_supplies_btn)

        layout.addStretch()  # Add stretch for spacing
        return page
    # button functions
    def add_new_item(self):
        """Handles the 'Add New Item' button click."""
        print("Add New Item button clicked!")
        # Add logic to add a new inventory item

    def view_inventory(self):
        """Handles the 'View Inventory' button click."""
        print("View Inventory button clicked!")
        # Add logic to view the inventory list

    def low_stock_alerts(self):
        """Handles the 'Low Stock Alerts' button click."""
        print("Low Stock Alerts button clicked!")
        # Add logic to check for low stock alerts

    def order_supplies(self):
        """Handles the 'Order Supplies' button click."""
        print("Order Supplies button clicked!")
        # Add logic to order new supplies

    def create_settings_page(self):
        """Creates the Settings page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title Label
        label = QLabel("Settings")
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(label)

        # User Roles and Permissions Button
        roles_permissions_btn = QPushButton("User Roles and Permissions")
        roles_permissions_btn.setCursor(Qt.PointingHandCursor)
        roles_permissions_btn.clicked.connect(self.manage_user_roles)  # Connect to handler
        layout.addWidget(roles_permissions_btn)

        # Update Clinic Information Button
        update_clinic_btn = QPushButton("Update Clinic Information")
        update_clinic_btn.setCursor(Qt.PointingHandCursor)
        update_clinic_btn.clicked.connect(self.update_clinic_info)  # Connect to handler
        layout.addWidget(update_clinic_btn)

        # Change Password Button
        change_password_btn = QPushButton("Change Password")
        change_password_btn.setCursor(Qt.PointingHandCursor)
        change_password_btn.clicked.connect(self.change_password)  # Connect to handler
        layout.addWidget(change_password_btn)

        # Backup Data Button
        backup_data_btn = QPushButton("Backup Data")
        backup_data_btn.setCursor(Qt.PointingHandCursor)
        backup_data_btn.clicked.connect(self.backup_data)  # Connect to handler
        layout.addWidget(backup_data_btn)

        layout.addStretch()  # Add stretch for spacing
        return page
    # button functions
    def manage_user_roles(self):
        """Handles the 'User Roles and Permissions' button click."""
        print("User Roles and Permissions button clicked!")
        # Add logic to manage user roles and permissions

    def update_clinic_info(self):
        """Handles the 'Update Clinic Information' button click."""
        print("Update Clinic Information button clicked!")
        # Add logic to update clinic information

    def change_password(self):
        """Handles the 'Change Password' button click."""
        print("Change Password button clicked!")
        # Add logic to change the user's password

    def backup_data(self):
        """Handles the 'Backup Data' button click."""
        print("Backup Data button clicked!")
        # Add logic to back up clinic data

    def create_section_page(self, title, buttons, search_placeholder=None):
        """Creates a generic section page with buttons and optional search."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        label = QLabel(title)
        label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(label)

        # Buttons
        for button_text in buttons:
            layout.addWidget(self.create_button_with_pointer(button_text))

        # Search bar if applicable
        if search_placeholder:
            search_input = QLineEdit()
            search_input.setPlaceholderText(search_placeholder)
            layout.addWidget(search_input)

        layout.addStretch()
        return page

    def create_button_with_pointer(self, text):
        """Creates a QPushButton with a pointer cursor."""
        button = QPushButton(text)
        button.setCursor(Qt.PointingHandCursor)  # Set pointer cursor
        return button

    # Button actions
    def show_dashboard(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_appointments(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_patients(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_doctors(self):
        self.stacked_widget.setCurrentIndex(3)

    def show_billing(self):
        self.stacked_widget.setCurrentIndex(4)

    def show_reports(self):
        self.stacked_widget.setCurrentIndex(5)

    def show_inventory(self):
        self.stacked_widget.setCurrentIndex(6)

    def show_settings(self):
        self.stacked_widget.setCurrentIndex(7)
