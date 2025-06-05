from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class DeleteMedicineScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Inventory")
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()

        # Left side for Deleting Medicine
        left_layout = QVBoxLayout()

        # Medicine Section Title
        title_medicine = QLabel("Delete Medicine")
        title_medicine.setFont(QFont("Arial", 20, QFont.Bold))
        title_medicine.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title_medicine)

        # Search Bar for Medicine
        self.medicine_name_input = QLineEdit()
        self.medicine_name_input.setPlaceholderText("Enter Medicine Name")
        self.medicine_name_input.setStyleSheet("font-size: 16px; padding: 10px;")
        search_layout_medicine = QHBoxLayout()
        search_layout_medicine.addWidget(QLabel("Search:"))
        search_layout_medicine.addWidget(self.medicine_name_input)
        search_button_medicine = QPushButton("Search")
        search_button_medicine.setFont(QFont("Arial", 14))
        search_button_medicine.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; border-radius: 5px;")
        search_button_medicine.clicked.connect(self.search_medicine)
        search_layout_medicine.addWidget(search_button_medicine)
        left_layout.addLayout(search_layout_medicine)

        # Frame for displaying medicine details
        details_frame_medicine = QFrame()
        details_frame_medicine.setStyleSheet("border: 2px solid #333333; padding: 10px;")
        details_layout_medicine = QGridLayout(details_frame_medicine)
        details_layout_medicine.setContentsMargins(10, 10, 10, 10)

        # Medicine details compact display
        details_layout_medicine.addWidget(QLabel("Medicine Details:"), 0, 0, 1, 1, Qt.AlignLeft)
        self.medicine_details = QLabel("")
        self.medicine_details.setStyleSheet("font-size: 14px; color: #555555;")
        self.medicine_details.setWordWrap(True)
        details_layout_medicine.addWidget(self.medicine_details, 0, 1, 1, 2)

        left_layout.addWidget(details_frame_medicine)

        # Delete Button for Medicine
        delete_button_medicine = QPushButton("Delete Medicine")
        delete_button_medicine.setFont(QFont("Arial", 14, QFont.Bold))
        delete_button_medicine.setStyleSheet("background-color: #FF4C4C; color: white; padding: 10px; border-radius: 5px;")
        delete_button_medicine.clicked.connect(self.delete_medicine)
        left_layout.addWidget(delete_button_medicine, alignment=Qt.AlignCenter)

        main_layout.addLayout(left_layout)

        # Set the main layout
        self.setLayout(main_layout)

    def search_medicine(self):
        # Fetch medicine details using name
        medicine_name = self.medicine_name_input.text().strip()
        if medicine_name:
            try:
                # Use the backend logic to search for the medicine
                from Inventory.InventoryBackend import search_medicine_for_delete
                medicine = search_medicine_for_delete(medicine_name)

                # Check if the result is valid and not None
                if medicine:
                    # Assuming `medicine` is a tuple with columns matching the TblMedicines table
                    self.medicine_details.setText(
                        f"Details for Medicine: {medicine_name}\n"
                        f"Name: {medicine[1]}\n"
                        f"Active Ingredient: {medicine[2]}\n"
                        f"Dosage: {medicine[3]}\n"
                        f"Drug Type: {medicine[4]}"
                    )
                else:
                    self.medicine_details.setText("No details found for the provided medicine name.")

            except Exception as e:
                self.show_message("Error", f"An error occurred while searching medicine: {e}", QMessageBox.Critical)
        else:
            self.medicine_details.setText("Please enter a valid medicine name.")

    def delete_medicine(self):
        # Fetch the medicine name from the input
        medicine_name = self.medicine_name_input.text().strip()

        if medicine_name:
            # Call the backend function to delete the medicine
            from Inventory.InventoryBackend import delete_medicine_by_name
            if delete_medicine_by_name(medicine_name):
                self.medicine_details.setText(f"Medicine with name '{medicine_name}' deleted successfully.")
            else:
                self.medicine_details.setText(f"Failed to delete medicine with name '{medicine_name}'.")
        else:
            self.show_message("Error", "No medicine name provided. Unable to delete.", QMessageBox.Critical)

    def show_message(self, title, message, icon):
        """Helper method to show message boxes"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec_()
