from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from Inventory.add_Inventory import AddMedicineScreen
from Inventory.add_test import AddTestScreen
from Inventory.delete_inventory import DeleteMedicineScreen
from Inventory.delete_test import DeleteTestScreen
from Inventory.update_inventory import UpdateInventoryScreen
from Inventory.view_inventory import ViewInventoryScreen
from Inventory.view_test import ViewTestScreen


# Other parts of the InventoryScreen class
class InventoryScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Main Layout
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Inventory Registration")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("color: #333333; margin-bottom: 20px;")
        main_layout.addWidget(title)

        # Button Panel for Navigation
        self.button_panel = QVBoxLayout()

        add_medicine_button = QPushButton("Add Medicines")
        add_medicine_button.setFont(QFont("Arial", 14))
        add_medicine_button.clicked.connect(self.show_add_medicine_screen)
        self.button_panel.addWidget(add_medicine_button)

        add_test_button = QPushButton("Add Tests")
        add_test_button.setFont(QFont("Arial", 14))
        add_test_button.clicked.connect(self.show_add_test_screen)
        self.button_panel.addWidget(add_test_button)

        delete_medicine_button = QPushButton("Delete Medicines")
        delete_medicine_button.setFont(QFont("Arial", 14))
        delete_medicine_button.clicked.connect(self.show_delete_medicine_screen)
        self.button_panel.addWidget(delete_medicine_button)

        delete_test_button = QPushButton("Delete Tests")
        delete_test_button.setFont(QFont("Arial", 14))
        delete_test_button.clicked.connect(self.show_delete_test_screen)
        self.button_panel.addWidget(delete_test_button)

        update_Inventory_button = QPushButton("Update Medicines")
        update_Inventory_button.setFont(QFont("Arial", 14))
        update_Inventory_button.clicked.connect(self.show_update_Inventory_screen)
        self.button_panel.addWidget(update_Inventory_button)

        view_Inventory_button = QPushButton("View Medicines")  # New button
        view_Inventory_button.setFont(QFont("Arial", 14))
        view_Inventory_button.clicked.connect(self.show_view_Inventory_screen)
        self.button_panel.addWidget(view_Inventory_button)

        view_test_button = QPushButton("View Tests") # New button
        view_test_button.setFont(QFont("Arial", 14))
        view_test_button.clicked.connect(self.show_view_test_screen)
        self.button_panel.addWidget(view_test_button)

        main_layout.addLayout(self.button_panel)

        # Stacked Widget to hold different screens
        self.stacked_widget = QStackedWidget()
        self.add_medicine_screen = AddMedicineScreen(self)
        self.add_test_screen = AddTestScreen(self)  # Initialize new screen
        self.delete_medicine_screen = DeleteMedicineScreen(self)
        self.delete_test_screen = DeleteTestScreen(self)  # Initialize new screen
        self.update_Inventory_screen = UpdateInventoryScreen(self)  # Corrected variable name
        self.view_Inventory_screen = ViewInventoryScreen(self)  # Initialize new screen
        self.view_test_screen = ViewTestScreen(self) # Initialize new screen

        # Add screens to the stacked widget
        self.stacked_widget.addWidget(self.add_medicine_screen)
        self.stacked_widget.addWidget(self.add_test_screen)  # Corrected variable name from add_inventory_screen to add_test_screen
        self.stacked_widget.addWidget(self.delete_medicine_screen)
        self.stacked_widget.addWidget((self.delete_test_screen))
        self.stacked_widget.addWidget(self.update_Inventory_screen)  # Corrected variable name
        self.stacked_widget.addWidget(self.view_Inventory_screen)  # Add to stacked widget
        self.stacked_widget.addWidget(self.view_test_screen)

        # Add stacked widget to the main layout
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def show_add_medicine_screen(self):
        """Switch to the Add Inventory screen."""
        self.stacked_widget.setCurrentWidget(self.add_medicine_screen)

    def show_add_test_screen(self):
        """Switch to the Add Test screen."""
        self.stacked_widget.setCurrentWidget(self.add_test_screen)  # Corrected variable name from add_inventory_screen to add_test_screen

    def show_delete_medicine_screen(self):
        """Switch to the Delete Inventory screen."""
        self.stacked_widget.setCurrentWidget(self.delete_medicine_screen)

    def show_delete_test_screen(self):
        """Switch to the Delete Inventory screen."""
        self.stacked_widget.setCurrentWidget(self.delete_test_screen)

    def show_update_Inventory_screen(self):
        """Switch to the Update Inventory screen."""
        self.stacked_widget.setCurrentWidget(self.update_Inventory_screen)

    def show_view_Inventory_screen(self):
        """Switch to the View Inventory screen."""
        self.stacked_widget.setCurrentWidget(self.view_Inventory_screen)

    def show_view_test_screen(self):
        """Switch to the View Test Screen."""
        self.stacked_widget.setCurrentWidget(self.view_test_screen)
