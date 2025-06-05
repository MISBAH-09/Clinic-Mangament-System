from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QPushButton, QScrollArea, QFrame, QVBoxLayout, QLineEdit
)
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QFont

class MedicinePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Medicine Selection
        medicine_label = QLabel("Select Medicines:")
        medicine_label.setFont(QFont("Arial", 14))
        self.medicine_dropdown = QComboBox()
        self.medicine_dropdown.setEditable(True)
        self.medicine_items = ["Paracetamol", "Ibuprofen", "Antibiotics"]  # Example medicines
        self.medicine_model = QStringListModel(self.medicine_items)
        self.medicine_dropdown.setModel(self.medicine_model)
        self.medicine_dropdown.setInsertPolicy(QComboBox.NoInsert)
        self.medicine_dropdown.setCurrentText('')  # Ensure dropdown is empty by default
        self.medicine_dropdown.lineEdit().textChanged.connect(self.filter_medicines)
        layout.addWidget(medicine_label)
        layout.addWidget(self.medicine_dropdown)
        
        # Test Selection
        test_label = QLabel("Select Tests:")
        test_label.setFont(QFont("Arial", 14))
        self.test_dropdown = QComboBox()
        self.test_dropdown.setEditable(True)
        self.test_items = ["Blood Test", "X-Ray", "MRI"]  # Example tests
        self.test_model = QStringListModel(self.test_items)
        self.test_dropdown.setModel(self.test_model)
        self.test_dropdown.setInsertPolicy(QComboBox.NoInsert)
        self.test_dropdown.setCurrentText('')  # Ensure dropdown is empty by default
        self.test_dropdown.lineEdit().textChanged.connect(self.filter_tests)
        layout.addWidget(test_label)
        layout.addWidget(self.test_dropdown)
        
        # Selected Medicines Display
        selected_medicines_label = QLabel("Selected Medicines:")
        selected_medicines_label.setFont(QFont("Arial", 12))
        layout.addWidget(selected_medicines_label)
        self.medicine_display_area = self.create_scrollable_area()
        layout.addWidget(self.medicine_display_area)
        
        # Selected Tests Display
        selected_tests_label = QLabel("Selected Tests:")
        selected_tests_label.setFont(QFont("Arial", 12))
        layout.addWidget(selected_tests_label)
        self.test_display_area = self.create_scrollable_area()
        layout.addWidget(self.test_display_area)
        
        layout.addStretch()
        self.setLayout(layout)

    def create_scrollable_area(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QFrame()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        return scroll_area

    def filter_medicines(self, text):
        if text == "":
            self.medicine_dropdown.clear()
            self.medicine_dropdown.setCurrentText('')
        else:
            filtered_items = [item for item in self.medicine_items if text.lower() in item.lower()]
            self.medicine_model.setStringList(filtered_items)
            self.medicine_dropdown.showPopup()

    def filter_tests(self, text):
        if text == "":
            self.test_dropdown.clear()
            self.test_dropdown.setCurrentText('')
        else:
            filtered_items = [item for item in self.test_items if text.lower() in item.lower()]
            self.test_model.setStringList(filtered_items)
            self.test_dropdown.showPopup()

    def add_medicine(self):
        selected_medicine = self.medicine_dropdown.currentText()
        if selected_medicine and not self.is_item_already_added(self.medicine_display_area, selected_medicine):
            self.add_item_to_display(self.medicine_display_area, selected_medicine)

    def add_test(self):
        selected_test = self.test_dropdown.currentText()
        if selected_test and not self.is_item_already_added(self.test_display_area, selected_test):
            self.add_item_to_display(self.test_display_area, selected_test)

    def is_item_already_added(self, display_area, item_text):
        scroll_content = display_area.widget()
        for i in range(scroll_content.layout().count()):
            item_widget = scroll_content.layout().itemAt(i).widget()
            if item_widget and item_widget.layout().itemAt(0).widget().text() == item_text:
                return True
        return False

    def add_item_to_display(self, display_area, item_text):
        scroll_content = display_area.widget()
        layout = scroll_content.layout()

        # Create a horizontal layout for the item and its remove button
        item_layout = QHBoxLayout()
        item_label = QLabel(item_text)
        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet("color: red; font-size: 10pt;")
        remove_button.clicked.connect(lambda: self.remove_item(item_layout, display_area))
        item_layout.addWidget(item_label)
        item_layout.addWidget(remove_button)
        item_layout.setAlignment(Qt.AlignLeft)

        # Add the horizontal layout to the scroll area's content
        item_widget = QWidget()
        item_widget.setLayout(item_layout)
        layout.addWidget(item_widget)

    def remove_item(self, item_layout, display_area):
        scroll_content = display_area.widget()
        layout = scroll_content.layout()
        for i in range(layout.count()):
            if layout.itemAt(i).layout() == item_layout:
                widget_to_remove = layout.itemAt(i).widget()
                if widget_to_remove:
                    widget_to_remove.deleteLater()
                layout.removeItem(layout.itemAt(i))
                break
