from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QPushButton, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont

class ViewInventoryScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("View Medicine")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("margin-bottom: 10px;")
        layout.addWidget(title)

        # Dropdown and buttons
        filter_layout = QHBoxLayout()

        refresh_button = QPushButton("Refresh")
        refresh_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 5px;")
        refresh_button.clicked.connect(self.refresh_table)

        search_medicine_button = QPushButton("Search Patient")
        search_medicine_button.setStyleSheet(
            "background-color: #2196F3; color: white; padding: 5px 10px; border-radius: 5px;"
        )
        search_medicine_button.clicked.connect(self.search_medicine)
        filter_layout.addWidget(refresh_button)
        filter_layout.addWidget(search_medicine_button)

        # Table layout for medicine data
        table_layout = QHBoxLayout()

        # Table for medicine data (all five columns)
        self.medicine_table = QTableWidget()
        self.medicine_table.setColumnCount(5)
        self.medicine_table.setHorizontalHeaderLabels(["Medicine ID", "Medicine Name", "Active Ingredient", "Dosage", "Dosage Type"])
        self.medicine_table.horizontalHeader().setStretchLastSection(True)
        self.medicine_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.medicine_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.load_medicine_data()

        # Add tables to the table layout
        table_layout.addWidget(QLabel("Medicine Records"))
        table_layout.addWidget(self.medicine_table)

        # Add components to layout
        layout.addLayout(filter_layout)
        layout.addLayout(table_layout)

        self.setLayout(layout)

    def load_medicine_data(self):
        """Load medicine data from the database into the table."""
        print("Loading medicine data...")
        try:
            from Inventory.InventoryBackend import view_medicines  # Import the backend method
            medicines = view_medicines()
            print(f"Medicine data fetched: {medicines}")

            if medicines:
                self.medicine_table.setRowCount(len(medicines))  # Set row count based on the fetched data
                for row_idx, medicine in enumerate(medicines):  # Iterate through the fetched data
                    print(f"Populating row {row_idx} with data: {medicine}")
                    # Set each column of the row with the respective data
                    self.medicine_table.setItem(row_idx, 0, QTableWidgetItem(str(medicine["MedicineID"])))  # MedicineID
                    self.medicine_table.setItem(row_idx, 1, QTableWidgetItem(str(medicine["MedicineName"])))  # MedicineName
                    self.medicine_table.setItem(row_idx, 2, QTableWidgetItem(str(medicine["ActiveIngredient"])))  # ActiveIngredient
                    self.medicine_table.setItem(row_idx, 3, QTableWidgetItem(str(medicine["Dosage"])))  # Dosage
                    self.medicine_table.setItem(row_idx, 4, QTableWidgetItem(str(medicine["DrugType"])))  # DosageType
            else:
                self.medicine_table.setRowCount(0)
                QMessageBox.warning(self, "Load Error", "Failed to load medicine data.")
        except Exception as e:
            print(f"Error loading medicine data: {e}")
            QMessageBox.warning(self, "Error", f"Error loading medicine data: {e}")

    def refresh_table(self):
        """Refresh the medicine data in the table."""
        print("Refreshing table data...")
        self.load_medicine_data()

    def search_medicine(self):
        """Search for a medicine by its name."""
        try:
            # Prompt the user to enter the medicine name
            medicine_name, ok = QInputDialog.getText(self, "Search Medicine", "Enter Medicine Name:")

            if ok and medicine_name:
                from Inventory.InventoryBackend import search_medicine_by_name  # Import the backend function

                # Call the backend function to fetch the medicine details
                medicine = search_medicine_by_name(medicine_name)

                if medicine:
                    # Clear the table and display only the searched medicine's data
                    self.medicine_table.setRowCount(1)
                    for col_idx, key in enumerate(medicine):
                        self.medicine_table.setItem(0, col_idx, QTableWidgetItem(str(medicine[key])))
                else:
                    # Display a message if no medicine is found
                    QMessageBox.information(self, "No Results", f"No medicine found with the name: {medicine_name}")
            else:
                QMessageBox.warning(self, "Input Error", "Medicine Name input was canceled or invalid.")
        except Exception as e:
            print(f"Error during search: {e}")
            QMessageBox.warning(self, "Search Error", f"An error occurred while searching for the medicine: {e}")
