from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGridLayout,
    QFrame, QPushButton, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class AddTestScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout (Vertical)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # Create a container widget for the test forms
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout(self.container_widget)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(10)

        # Title for the screen
        self.test_title = QLabel("Add Test")
        self.test_title.setFont(QFont("Arial", 18, QFont.Bold))
        self.test_title.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.test_title)

        # Scrollable area to hold all test forms
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.container_widget)

        # Add scroll area to the main layout
        main_layout.addWidget(self.scroll_area)

        # Add a "Submit All" button at the bottom (outside the scrollable area)
        self.submit_button_layout = QHBoxLayout()
        submit_all_button = QPushButton("Submit All")
        submit_all_button.setFixedWidth(200)
        submit_all_button.setFont(QFont("Arial", 12, QFont.Bold))
        submit_all_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border-radius: 5px;")
        submit_all_button.clicked.connect(self.submit_all_tests)

        self.submit_button_layout.addWidget(submit_all_button, alignment=Qt.AlignCenter)

        # Add the submit button layout below the scroll area
        main_layout.addLayout(self.submit_button_layout)

        # Set the main layout
        self.setLayout(main_layout)

        # A list to store all test forms
        self.test_forms = []

        # Add the first test form
        self.add_test_form()

    def add_test_form(self):
        # Create a frame for the test form
        test_frame = QFrame()
        test_frame.setStyleSheet("border: 2px solid #333333; padding: 10px;")
        test_layout = QGridLayout(test_frame)
        test_layout.setContentsMargins(5, 5, 5, 5)
        test_layout.setVerticalSpacing(5)
        test_layout.setHorizontalSpacing(5)

        # Style for labels and input fields
        label_style = "font-size: 16px; color: #333333;"
        input_style = "font-size: 16px; padding: 5px;"

        # Test Name
        test_name_label = QLabel("Test Name:")
        test_name_label.setStyleSheet(label_style)
        test_name_input = QLineEdit()
        test_name_input.setStyleSheet(input_style)
        test_layout.addWidget(test_name_label, 1, 0)
        test_layout.addWidget(test_name_input, 1, 1)

        # # Test Description
        # test_description_label = QLabel("Description:")
        # test_description_label.setStyleSheet(label_style)
        # test_description_input = QLineEdit()
        # test_description_input.setStyleSheet(input_style)
        # test_layout.addWidget(test_description_label, 2, 0)
        # test_layout.addWidget(test_description_input, 2, 1)

        # Add the test form to the list of forms
        self.test_forms.append({
            'test_name': test_name_input,
            # 'description': test_description_input,
            'frame': test_frame  # Store the frame to remove it later
        })

        # Add More Button for Test
        add_more_button = QPushButton("Add More")
        add_more_button.setFixedWidth(200)
        add_more_button.setFont(QFont("Arial", 12, QFont.Bold))
        add_more_button.setStyleSheet("background-color: #FFC107; color: white; padding: 5px; border-radius: 5px;")
        add_more_button.clicked.connect(self.add_test_form)
        test_layout.addWidget(add_more_button, 2, 0)

        # Cancel Button for Test
        cancel_button = QPushButton("Cancel")
        cancel_button.setFixedWidth(200)
        cancel_button.setFont(QFont("Arial", 12, QFont.Bold))
        cancel_button.setStyleSheet("background-color: #F44336; color: white; padding: 5px; border-radius: 5px;")
        cancel_button.clicked.connect(self.cancel_test_form)
        test_layout.addWidget(cancel_button, 2, 1)

        # Add test frame to layout
        self.container_layout.addWidget(test_frame)

    def cancel_test_form(self):
        # Remove the most recently added form
        if self.test_forms:
            last_form = self.test_forms.pop()  # Get the last form added
            last_form['frame'].deleteLater()  # Remove the frame from the layout

    def submit_all_tests(self):
        # Collect all test names from the forms
        test_names = [form['test_name'].text() for form in self.test_forms if form['test_name'].text()]

        if not test_names:
            QMessageBox.warning(self, "Error", "No test names to submit.")
            return

        print("Tests Data to Submit:", test_names)  # Debugging log

        from Inventory.InventoryBackend import insert_tests
        try:
            # Call the backend function
            if insert_tests(test_names):
                QMessageBox.information(self, "Submitted", "All tests submitted successfully.")
                self.clear_all_tests()
            else:
                QMessageBox.warning(self, "Error", "Failed to submit tests. Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            QMessageBox.warning(self, "Error", f"An unexpected error occurred: {str(e)}")

    def clear_all_tests(self):
        """Clears all input fields."""
        for form in self.test_forms:
            form['test_name'].clear()
            # form['description'].clear()
        self.test_forms.clear()  # Clear the list of forms
