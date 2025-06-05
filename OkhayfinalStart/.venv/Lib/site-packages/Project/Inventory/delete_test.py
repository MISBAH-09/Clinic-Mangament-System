from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class DeleteTestScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Test")
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Test Section Title
        title_test = QLabel("Delete Test")
        title_test.setFont(QFont("Arial", 20, QFont.Bold))
        title_test.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_test)

        # Search Bar for Test
        self.test_name_input = QLineEdit()
        self.test_name_input.setPlaceholderText("Enter Test Name")
        self.test_name_input.setStyleSheet("font-size: 16px; padding: 10px;")
        search_layout_test = QHBoxLayout()
        search_layout_test.addWidget(QLabel("Search:"))
        search_layout_test.addWidget(self.test_name_input)
        search_button_test = QPushButton("Search")
        search_button_test.setFont(QFont("Arial", 14))
        search_button_test.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; border-radius: 5px;")
        search_button_test.clicked.connect(self.search_test)
        search_layout_test.addWidget(search_button_test)
        main_layout.addLayout(search_layout_test)

        # Frame for displaying test details
        details_frame_test = QFrame()
        details_frame_test.setStyleSheet("border: 2px solid #333333; padding: 10px;")
        details_layout_test = QGridLayout(details_frame_test)
        details_layout_test.setContentsMargins(10, 10, 10, 10)

        # Test details compact display
        details_layout_test.addWidget(QLabel("Test Details:"), 0, 0, 1, 1, Qt.AlignLeft)
        self.test_details = QLabel("")
        self.test_details.setStyleSheet("font-size: 14px; color: #555555;")
        self.test_details.setWordWrap(True)
        details_layout_test.addWidget(self.test_details, 0, 1, 1, 2)

        main_layout.addWidget(details_frame_test)

        # Delete Button for Test
        delete_button_test = QPushButton("Delete Test")
        delete_button_test.setFont(QFont("Arial", 14, QFont.Bold))
        delete_button_test.setStyleSheet("background-color: #FF4C4C; color: white; padding: 10px; border-radius: 5px;")
        delete_button_test.clicked.connect(self.delete_test)
        main_layout.addWidget(delete_button_test, alignment=Qt.AlignCenter)

        # Set the main layout
        self.setLayout(main_layout)

    def search_test(self):
        # Fetch test details using name
        test_name = self.test_name_input.text().strip()
        if test_name:
            # Use the backend logic to search for the test
            from Inventory.InventoryBackend import search_test_for_delete
            test = search_test_for_delete(test_name)
            if test:
                # Assuming `test` is a tuple with columns matching the TblTests table
                self.test_details.setText(
                    f"Details for Test: {test_name}\n"
                    f"Name: {test[1]}"
                )
            else:
                self.test_details.setText("No details found for the provided test name.")
        else:
            self.test_details.setText("Please enter a valid test name.")

    def delete_test(self):
        # Delete test logic
        test_name = self.test_name_input.text().strip()
        if test_name:
            # Call the backend function to delete the test
            from Inventory.InventoryBackend import delete_test_by_name
            if delete_test_by_name(test_name):
                self.test_details.setText(f"Test with name {test_name} deleted successfully.")
            else:
                self.test_details.setText(f"Failed to delete test with name {test_name}.")
        else:
            QMessageBox.critical(self, "Error", "No test name provided. Unable to delete.")
