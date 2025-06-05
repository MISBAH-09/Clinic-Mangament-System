from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QPushButton, QComboBox, QMessageBox, QInputDialog
)

from PyQt5.QtGui import QFont

class ViewDoctorScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("View Doctor")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("margin-bottom: 10px;")
        layout.addWidget(title)

        # Dropdown and buttons
        filter_layout = QHBoxLayout()

        # department_dropdown = QComboBox()
        # department_dropdown.addItems(["Operative Dentistry", "Orthodontics", "Pediatrics"])

        refresh_button = QPushButton("Refresh")
        refresh_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 5px;")
        refresh_button.clicked.connect(self.refresh_table)

        search_doctor_button = QPushButton("Search doctor")
        search_doctor_button.setStyleSheet(
            "background-color: #2196F3; color: white; padding: 5px 10px; border-radius: 5px;"
        )
        search_doctor_button.clicked.connect(self.search_doctor)

        # filter_layout.addWidget(department_dropdown)
        filter_layout.addWidget(refresh_button)
        filter_layout.addWidget(search_doctor_button)

        # Table for patient data
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(
            ["DoctorID", "FirstName", "LastName", "CNIC", "LicenseNo", "JoiningDate", "JobStatus", "Salary", "Credential", "Address"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Load initial data
        self.load_doctor_data()

        # Add components to layout
        layout.addLayout(filter_layout)
        layout.addWidget(QLabel("Search Records"))
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_doctor_data(self):
        """Load doctor data from the database into the table."""
        from Doctorsdata.DoctorsBackend import view_all_doctors  # Import the backend method

        doctors = view_all_doctors()

        if doctors:
            self.table.setRowCount(len(doctors))
            for row_idx, doctor in enumerate(doctors):
                for col_idx, key in enumerate(doctor):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(doctor[key])))

        else:
            # Clear the table if no data is fetched or an error occurs
            self.table.setRowCount(0)
            QMessageBox.warning(self, "Load Error", "Failed to load doctor data.")

    def refresh_table(self):
        """Refresh the patient data in the table."""
        # Logic to refresh table (replace with actual implementation)
        print("Refreshing table data...")
        self.load_doctor_data()


    def search_doctor(self):
        """Search for a doctor by CNIC."""
        # Prompt the user to enter the CNIC
        cnic, ok = QInputDialog.getText(self, "Search Patient", "Enter CNIC:")

        if ok and cnic:
            from Doctorsdata.DoctorsBackend import search_doctor_by_cnic  # Import the backend function

            # Call the backend function to fetch the patient details
            doctor = search_doctor_by_cnic(cnic)

            if doctor:
                # Clear the table and display only the searched patient's data
                self.table.setRowCount(1)
                for col_idx, key in enumerate(doctor):
                    self.table.setItem(0, col_idx, QTableWidgetItem(str(doctor[key])))
            else:
                # Display a message if no patient is found
                QMessageBox.information(self, "No Results", f"No patient found with CNIC: {cnic}")
        else:
            QMessageBox.warning(self, "Input Error", "CNIC input was canceled or invalid.")