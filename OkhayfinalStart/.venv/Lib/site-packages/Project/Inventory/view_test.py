from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QPushButton, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont

class ViewTestScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        # self.load_test_data()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("View Test")
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

        search_doctor_button = QPushButton("Search Tests")
        search_doctor_button.setStyleSheet(
            "background-color: #2196F3; color: white; padding: 5px 10px; border-radius: 5px;"
        )
        search_doctor_button.clicked.connect(self.search_test)

        # filter_layout.addWidget(department_dropdown)
        filter_layout.addWidget(refresh_button)
        filter_layout.addWidget(search_doctor_button)

        # Table for patient data
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(
            ["Test-ID", "Test-Name"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Load initial data
        self.load_test_data()

        # Add components to layout
        layout.addLayout(filter_layout)
        layout.addWidget(QLabel("Search Records"))
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_test_data(self):
        """Load test data from the database into the table."""
        print("Loading test data...")
        try:
            from Inventory.InventoryBackend import view_tests  # Import the backend method
            tests = view_tests()
            print(f"Test data fetched: {tests}")

            if tests:
                self.table.setRowCount(len(tests))  # Set row count based on the fetched data
                for row_idx, test in enumerate(tests):  # Iterate through the fetched test data
                    print(f"Populating row {row_idx} with data: {test}")
                    # Set each column of the row with the respective data from the dictionary
                    self.table.setItem(row_idx, 0, QTableWidgetItem(str(test["TestID"])))  # TestID
                    self.table.setItem(row_idx, 1, QTableWidgetItem(str(test["TestName"])))  # TestName
            else:
                self.table.setRowCount(0)
                QMessageBox.warning(self, "Load Error", "Failed to load test data.")
        except Exception as e:
            print(f"Error loading test data: {e}")
            QMessageBox.warning(self, "Error", f"Error loading test data: {e}")

    def refresh_table(self):
        """Refresh the patient data in the table."""
        # Logic to refresh table (replace with actual implementation)
        print("Refreshing table data...")
        self.load_test_data()

    def search_test(self):
        """Search for a Test by TestName."""
        try:
            # Prompt the user to enter the TestName
            test_name, ok = QInputDialog.getText(self, "Search Test", "Enter TestName:")

            if ok and test_name:
                from Inventory.InventoryBackend import search_test_by_name  # Import the backend function

                # Call the backend function to fetch the test details
                test = search_test_by_name(test_name)

                if test:
                    # Clear the table and display only the searched test's data
                    self.table.setRowCount(1)
                    for col_idx, key in enumerate(test):
                        self.table.setItem(0, col_idx, QTableWidgetItem(str(test[key])))
                else:
                    # Display a message if no test is found
                    QMessageBox.information(self, "No Results", f"No test found with the name: {test_name}")
            else:
                QMessageBox.warning(self, "Input Error", "Test Name input was canceled or invalid.")
        except Exception as e:
            print(f"Error during search: {e}")
            QMessageBox.warning(self, "Search Error", f"An error occurred while searching for the test: {e}")

