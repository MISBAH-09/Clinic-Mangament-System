from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QPushButton, QComboBox, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont

class ViewPatientScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("View Patients")
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

        search_patient_button = QPushButton("Search Patient")
        search_patient_button.setStyleSheet(
            "background-color: #2196F3; color: white; padding: 5px 10px; border-radius: 5px;"
        )
        search_patient_button.clicked.connect(self.search_patient)

        # filter_layout.addWidget(department_dropdown)
        filter_layout.addWidget(refresh_button)
        filter_layout.addWidget(search_patient_button)

        # Table for patient data
        self.table = QTableWidget()
        self.table.setColumnCount(10)  # Updated for 10 columns
        self.table.setHorizontalHeaderLabels(
            ["PatientID", "FirstName", "LastName", "CNIC", "DateOfBirth", "Gender", "ContactNumber", "Email", "Address", "DateRegistered"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Load initial data
        self.load_patient_data()

        # Add components to layout
        layout.addLayout(filter_layout)
        layout.addWidget(QLabel("Search Records"))
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_patient_data(self):
        """Load patient data from the database into the table."""
        from ReceptionBackend import view_patient_data  # Import the backend method

        patients = view_patient_data()

        if patients:
            self.table.setRowCount(len(patients))
            for row_idx, patient in enumerate(patients):
                for col_idx, cell_data in enumerate(patient):
                    # Convert data to string and set it in the table
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
        else:
            # Clear the table if no data is fetched or an error occurs
            self.table.setRowCount(0)
            QMessageBox.warning(self, "Load Error", "Failed to load patient data.")

    def refresh_table(self):
        """Refresh the patient data in the table."""
        print("Refreshing table data...")
        self.load_patient_data()

    from PyQt5.QtWidgets import QInputDialog

    def search_patient(self):
        """Search for a patient by CNIC."""
        # Prompt the user to enter the CNIC
        cnic, ok = QInputDialog.getText(self, "Search Patient", "Enter CNIC:")

        if ok and cnic:
            from ReceptionBackend import search_patient_by_cnic  # Import the backend function

            # Call the backend function to fetch the patient details
            patient = search_patient_by_cnic(cnic)

            if patient:
                # Clear the table and display only the searched patient's data
                self.table.setRowCount(1)
                for col_idx, cell_data in enumerate(patient):
                    self.table.setItem(0, col_idx, QTableWidgetItem(str(cell_data)))
            else:
                # Display a message if no patient is found
                QMessageBox.information(self, "No Results", f"No patient found with CNIC: {cnic}")
        else:
            QMessageBox.warning(self, "Input Error", "CNIC input was canceled or invalid.")

