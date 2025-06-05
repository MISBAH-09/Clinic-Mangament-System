import sys

sys.path.append('E:\HMS')
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QLabel, QComboBox, QHeaderView
from model import *


class MedicineForm(QWidget):
    def _init_(self):
        super()._init_()

        self.setWindowTitle("Medicine Form")
        self.layout = QVBoxLayout()

        # Create the table to display medicine data
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Medicine Name", "Active Ingredient", "Dosage", "Drug Type"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Create the Add More button
        self.add_more_button = QPushButton("Add More")
        self.add_more_button.clicked.connect(self.add_row)

        # Create the Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)

        # Add table and buttons to the layout
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.add_more_button)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

        # Add the first row by default
        self.add_row()

    def add_row(self):
        """Adds a new row to the table for medicine input."""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Create input fields for the new row
        name_field = QLineEdit()
        ingredient_field = QLineEdit()
        dosage_field = QLineEdit()
        drug_type_field = QComboBox()
        drug_type_field.addItems(["Tablet", "Syrup", "Injection", "Tube", "Other"])

        # Add cancel button to remove the row
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(lambda: self.remove_row(row_position))

        # Add widgets to the table
        self.table.setCellWidget(row_position, 0, name_field)
        self.table.setCellWidget(row_position, 1, ingredient_field)
        self.table.setCellWidget(row_position, 2, dosage_field)
        self.table.setCellWidget(row_position, 3, drug_type_field)
        self.table.setCellWidget(row_position, 4, cancel_button)

    def remove_row(self, row_position):
        """Removes a row from the table."""
        self.table.removeRow(row_position)

    def submit_form(self):
        """Handles the form submission."""
        for row in range(self.table.rowCount()):
            name_field = self.table.cellWidget(row, 0).text()
            ingredient_field = self.table.cellWidget(row, 1).text()
            dosage_field = self.table.cellWidget(row, 2).text()
            drug_type_field = self.table.cellWidget(row, 3).currentText()

            if name_field and ingredient_field and dosage_field and drug_type_field:
                try:
                    MedicinesCRUD.add_medicine(name_field, ingredient_field, dosage_field, drug_type_field)
                except Exception as e:
                    print(f"Failed to add medicine for row {row + 1}: {e}")