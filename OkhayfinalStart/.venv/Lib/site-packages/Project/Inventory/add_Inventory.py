from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGridLayout,
    QFrame, QPushButton, QMessageBox, QScrollArea, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class AddMedicineScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout (Vertical)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # Create a container widget for the medicine forms
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout(self.container_widget)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(10)

        # Title for the screen
        self.medicine_title = QLabel("Add Medicine")
        self.medicine_title.setFont(QFont("Arial", 18, QFont.Bold))
        self.medicine_title.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.medicine_title)

        # Scrollable area to hold all medicine forms
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
        submit_all_button.clicked.connect(self.submit_all_medicines)

        self.submit_button_layout.addWidget(submit_all_button, alignment=Qt.AlignCenter)

        # Add the submit button layout below the scroll area
        main_layout.addLayout(self.submit_button_layout)

        # Set the main layout
        self.setLayout(main_layout)

        # A list to store all medicine forms
        self.medicine_forms = []

        # Add the first medicine form
        self.add_medicine_form()

    def add_medicine_form(self):
        # Create a frame for the medicine form
        medicine_frame = QFrame()
        medicine_frame.setStyleSheet("border: 2px solid #333333; padding: 10px;")
        medicine_layout = QGridLayout(medicine_frame)
        medicine_layout.setContentsMargins(5, 5, 5, 5)
        medicine_layout.setVerticalSpacing(5)
        medicine_layout.setHorizontalSpacing(5)

        # Style for labels and input fields
        label_style = "font-size: 16px; color: #333333;"
        input_style = "font-size: 16px; padding: 5px;"

        # Medicine Name
        medicine_name_label = QLabel("Medicine Name:")
        medicine_name_label.setStyleSheet(label_style)
        medicine_name_input = QLineEdit()
        medicine_name_input.setStyleSheet(input_style)
        medicine_layout.addWidget(medicine_name_label, 1, 0)
        medicine_layout.addWidget(medicine_name_input, 1, 1)

        # Active Ingredient
        active_ingredient_label = QLabel("Active Ingredient:")
        active_ingredient_label.setStyleSheet(label_style)
        active_ingredient_input = QLineEdit()
        active_ingredient_input.setStyleSheet(input_style)
        medicine_layout.addWidget(active_ingredient_label, 1, 2)
        medicine_layout.addWidget(active_ingredient_input, 1, 3)

        # Dosage
        dosage_label = QLabel("Dosage:")
        dosage_label.setStyleSheet(label_style)
        dosage_input = QLineEdit()
        dosage_input.setStyleSheet(input_style)
        medicine_layout.addWidget(dosage_label, 2, 0)
        medicine_layout.addWidget(dosage_input, 2, 1)

        # Drug Type
        drug_type_label = QLabel("Drug Type:")
        drug_type_label.setStyleSheet(label_style)
        drug_type_input = QLineEdit()
        drug_type_input.setStyleSheet(input_style)
        medicine_layout.addWidget(drug_type_label, 2, 2)
        medicine_layout.addWidget(drug_type_input, 2, 3)

        # Add the medicine form to the list of forms
        self.medicine_forms.append({
            'medicine_name': medicine_name_input,
            'active_ingredient': active_ingredient_input,
            'dosage': dosage_input,
            'drug_type': drug_type_input,
            'frame': medicine_frame  # Store the frame to remove it later
        })

        # Add More Button for Medicine
        add_more_button = QPushButton("Add More")
        add_more_button.setFixedWidth(200)
        add_more_button.setFont(QFont("Arial", 12, QFont.Bold))
        add_more_button.setStyleSheet("background-color: #FFC107; color: white; padding: 5px; border-radius: 5px;")
        add_more_button.clicked.connect(self.add_medicine_form)
        medicine_layout.addWidget(add_more_button, 3, 2)

        # Cancel Button for Medicine
        cancel_button = QPushButton("Cancel")
        cancel_button.setFixedWidth(200)
        cancel_button.setFont(QFont("Arial", 12, QFont.Bold))
        cancel_button.setStyleSheet("background-color: #F44336; color: white; padding: 5px; border-radius: 5px;")
        cancel_button.clicked.connect(self.cancel_medicine_form)
        medicine_layout.addWidget(cancel_button, 3, 3)

        # Add medicine frame to layout
        self.container_layout.addWidget(medicine_frame)

    def cancel_medicine_form(self):
        # Remove the most recently added form
        if self.medicine_forms:
            last_form = self.medicine_forms.pop()  # Get the last form added
            last_form['frame'].deleteLater()  # Remove the frame from the layout

    def submit_all_medicines(self):
        # Collect all data from the medicine forms
        medicines_data = []
        for form in self.medicine_forms:
            medicine_name = form['medicine_name'].text()
            active_ingredient = form['active_ingredient'].text()
            dosage = form['dosage'].text()
            drug_type = form['drug_type'].text()

            if medicine_name and active_ingredient and dosage and drug_type:
                medicines_data.append({
                    'medicine_name': medicine_name,
                    'active_ingredient': active_ingredient,
                    'dosage': dosage,
                    'drug_type': drug_type
                })
            else:
                QMessageBox.warning(self, "Error", "Please fill all fields for each medicine.")
                return

        # Submit all medicines
        from Inventory.InventoryBackend import insert_medicine
        try:
            for medicine in medicines_data:
                insert_medicine(
                    medicine_name=medicine['medicine_name'],
                    active_ingredient=medicine['active_ingredient'],
                    dosage=medicine['dosage'],
                    drug_type=medicine['drug_type']
                )
            QMessageBox.information(self, "Submitted", "All medicines submitted successfully.")
            self.clear_all_medicines()
        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", "Failed to submit medicines. Please try again.")

    def clear_all_medicines(self):
        """Clears all input fields."""
        for form in self.medicine_forms:
            form['medicine_name'].clear()
            form['active_ingredient'].clear()
            form['dosage'].clear()
            form['drug_type'].clear()
        self.medicine_forms.clear()  # Clear the list of forms
