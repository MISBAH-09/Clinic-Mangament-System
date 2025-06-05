from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QGridLayout, QFrame, QScrollArea, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class UpdateInventoryScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Inventory")
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # Create a widget to hold the main layout
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(5)

        # Title
        title = QLabel("Update Inventory")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)

        # Search Bar
        search_layout = QVBoxLayout()

        # Add Medicine ID field
        self.medicine_id_input = QLineEdit()
        self.medicine_id_input.setPlaceholderText("Enter Medicine ID")
        self.medicine_id_input.setStyleSheet("font-size: 16px; padding: 10px;")
        search_layout.addWidget(QLabel("Search Medicine by ID:"))
        search_layout.addWidget(self.medicine_id_input)

        # Add Medicine Name field
        self.medicine_name_input = QLineEdit()
        self.medicine_name_input.setPlaceholderText("Enter Medicine Name")
        self.medicine_name_input.setStyleSheet("font-size: 16px; padding: 10px;")
        search_layout.addWidget(QLabel("Or by Name:"))
        search_layout.addWidget(self.medicine_name_input)

        # Search Button
        search_button = QPushButton("Search")
        search_button.setFont(QFont("Arial", 14))
        search_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; border-radius: 5px;")
        search_button.clicked.connect(self.search_medicine)
        search_layout.addWidget(search_button)

        container_layout.addLayout(search_layout)

        # Create form layout inside a framed box
        form_frame = QFrame()
        form_frame.setStyleSheet("border: 2px solid #333333; padding: 20px;")
        form_layout = QGridLayout(form_frame)
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setVerticalSpacing(10)

        # Add a spacer to push form content towards the top
        top_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        form_layout.addItem(top_spacer, 0, 0, 1, 4)

        # Style for labels and input fields
        label_style = "font-size: 16px; color: #333333;"
        input_style = "font-size: 16px; padding: 10px;"

        # Medicine Name
        medicine_name_label = QLabel("Medicine Name:")
        medicine_name_label.setStyleSheet(label_style)
        self.medicine_name_update_input = QLineEdit()
        self.medicine_name_update_input.setStyleSheet(input_style)
        form_layout.addWidget(medicine_name_label, 1, 0)
        form_layout.addWidget(self.medicine_name_update_input, 1, 1)

        # Active Ingredient
        active_ingredient_label = QLabel("Active Ingredient:")
        active_ingredient_label.setStyleSheet(label_style)
        self.active_ingredient_input = QLineEdit()
        self.active_ingredient_input.setStyleSheet(input_style)
        form_layout.addWidget(active_ingredient_label, 1, 2)
        form_layout.addWidget(self.active_ingredient_input, 1, 3)

        # Dosage
        dosage_label = QLabel("Dosage:")
        dosage_label.setStyleSheet(label_style)
        self.dosage_input = QLineEdit()
        self.dosage_input.setStyleSheet(input_style)
        form_layout.addWidget(dosage_label, 2, 0)
        form_layout.addWidget(self.dosage_input, 2, 1)

        # Drug Type
        drug_type_label = QLabel("Drug Type:")
        drug_type_label.setStyleSheet(label_style)
        self.drug_type_input = QLineEdit()
        self.drug_type_input.setStyleSheet(input_style)
        form_layout.addWidget(drug_type_label, 2, 2)
        form_layout.addWidget(self.drug_type_input, 2, 3)

        # Update Button for Inventory
        update_inventory_button = QPushButton("Update")
        update_inventory_button.setFont(QFont("Arial", 12, QFont.Bold))
        update_inventory_button.setFixedWidth(200)
        update_inventory_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border-radius: 5px;")
        update_inventory_button.clicked.connect(self.update_inventory_form)
        form_layout.addWidget(update_inventory_button, 3, 3, Qt.AlignRight)

        # Add form layout to the container layout
        container_layout.addWidget(form_frame)

        # Create a scroll area and set the container widget as its child
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container_widget)

        # Add scroll area to the main layout
        main_layout.addWidget(scroll_area)

        # Set the main layout
        self.setLayout(main_layout)

    def search_medicine(self):
        # Get inputs
        medicine_id = self.medicine_id_input.text().strip()
        medicine_name = self.medicine_name_input.text().strip()

        # Validate inputs
        if medicine_id or medicine_name:
            try:
                # Search medicine by ID and/or name
                from Inventory.InventoryBackend import search_medicine_for_update
                medicine = search_medicine_for_update(medicine_id, medicine_name)

                if medicine:
                    # Populate the fields with fetched data
                    self.medicine_name_update_input.setText(medicine[1])  # Medicine Name
                    self.active_ingredient_input.setText(medicine[2])  # Active Ingredient
                    self.dosage_input.setText(medicine[3])  # Dosage
                    self.drug_type_input.setText(medicine[4])  # Drug Type
                else:
                    QMessageBox.warning(self, "Not Found", "No details found for the provided Medicine ID or Name.")
                    self.clear_fields()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while searching for the medicine: {e}")
                self.clear_fields()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter at least one of Medicine ID or Name to search.")
            self.clear_fields()

    def clear_fields(self):
        self.medicine_name_update_input.clear()
        self.active_ingredient_input.clear()
        self.dosage_input.clear()
        self.drug_type_input.clear()

    def update_inventory_form(self):
        id = self.medicine_id_input.text().strip()
        name = self.medicine_name_update_input.text().strip()
        active_ingredient = self.active_ingredient_input.text().strip()
        dosage = self.dosage_input.text().strip()
        drug_type = self.drug_type_input.text().strip()

        if name and active_ingredient and dosage and drug_type:
            from Inventory.InventoryBackend import update_medicine_inventory
            try:
                update_medicine_inventory(id, name, active_ingredient, dosage, drug_type)
                QMessageBox.information(self, "Updated", "Inventory details updated successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while updating the inventory: {e}")
