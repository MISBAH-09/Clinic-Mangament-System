from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QPushButton, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont
from StaffBackend import *
from StaffBackend import view_all_staff, search_staff_by_cnic

class ViewStaffScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("View Staff")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("margin-bottom: 10px;")
        layout.addWidget(title)

        # Dropdown and buttons
        filter_layout = QHBoxLayout()

        refresh_button = QPushButton("Refresh")
        refresh_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 5px;")
        refresh_button.clicked.connect(self.refresh_table)

        search_staff_button = QPushButton("Search Staff")
        search_staff_button.setStyleSheet(
            "background-color: #2196F3; color: white; padding: 5px 10px; border-radius: 5px;"
        )
        search_staff_button.clicked.connect(self.search_staff)

        filter_layout.addWidget(refresh_button)
        filter_layout.addWidget(search_staff_button)

        # Table for staff data
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            ["StaffID", "FirstName", "LastName", "CNIC", "JoiningDate", "JobStatus", "Salary", "CredentialUsername", "AddressCity"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Load initial data
        self.load_staff_data()

        # Add components to layout
        layout.addLayout(filter_layout)
        layout.addWidget(QLabel("Search Records"))
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_staff_data(self):
        """Load staff data from the database into the table."""
        print("Loading staff data...")
        staff_list = view_all_staff()

        if staff_list:
            print(f"Staff data loaded: {staff_list}")
            self.table.setRowCount(len(staff_list))
            for row_idx, staff in enumerate(staff_list):
                for col_idx, key in enumerate(staff.keys()):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(staff[key])))
        else:
            # Clear the table if no data is fetched or an error occurs
            self.table.setRowCount(0)
            QMessageBox.warning(self, "Load Error", "Failed to load staff data.")

    def refresh_table(self):
        """Refresh the staff data in the table."""
        print("Refreshing table data...")
        self.load_staff_data()

    def search_staff(self):
        """Search for a staff member by CNIC."""
        # Prompt the user to enter the CNIC
        cnic, ok = QInputDialog.getText(self, "Search staff", "Enter CNIC:")

        if ok and cnic:
            # Call the backend function to fetch the staff details
            staff_member = search_staff_by_cnic(cnic)

            if staff_member:
                # Clear the table and display only the searched staff's data
                self.table.setRowCount(1)
                for col_idx, key in enumerate(staff_member.keys()):
                    self.table.setItem(0, col_idx, QTableWidgetItem(str(staff_member[key])))
            else:
                # Display a message if no staff is found
                QMessageBox.information(self, "No Results", f"No staff found with CNIC: {cnic}")
        else:
            QMessageBox.warning(self, "Input Error", "CNIC input was canceled or invalid.")
