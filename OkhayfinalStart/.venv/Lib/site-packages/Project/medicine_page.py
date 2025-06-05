from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget, QLabel, QPushButton, QHBoxLayout, QGroupBox
from PyQt5.QtCore import Qt
from DoctorScreenBackend import create_prescription, create_test_prescription, get_medicines, get_test, fetch_medicine_ids ,fetch_test_ids # Import the backend functions


class MedicinePage(QWidget):
    def __init__(self):
        super().__init__()
        self.visit_id = None  # Default value for visit_id
        self.medicines = get_medicines()  # Fetch all medicines from the DB
        self.tests = get_test()
        self.selected_medicines = []  # Track selected medicines
        self.selected_tests = []  # Track selected tests
        self.initUI()  # Initialize the UI

    def update_visit_id(self, visit_id):
        self.visit_id = visit_id  # Update the visit ID
        print(f"Updated VisitID: {self.visit_id}")

    def initUI(self):
        self.setWindowTitle('Medicine and Test Selector')

        layout = QVBoxLayout()

        # Label for Medicines
        self.medicine_label = QLabel("Medicines:", self)
        layout.addWidget(self.medicine_label)

        # Searchable dropdown for Medicines
        self.medicine_input = QLineEdit(self)
        self.medicine_input.setPlaceholderText('Enter Medicine')
        self.medicine_input.textChanged.connect(self.update_medicine_dropdown)
        layout.addWidget(self.medicine_input)

        self.medicine_list = QListWidget(self)
        self.medicine_list.setSelectionMode(QListWidget.MultiSelection)
        self.medicine_list.itemSelectionChanged.connect(self.update_medicine_display)
        layout.addWidget(self.medicine_list)

        # Label for Tests
        self.tests_label = QLabel("Tests:", self)
        layout.addWidget(self.tests_label)

        # Searchable dropdown for Tests
        self.test_input = QLineEdit(self)
        self.test_input.setPlaceholderText('Enter Test')
        self.test_input.textChanged.connect(self.update_test_dropdown)
        layout.addWidget(self.test_input)

        self.test_list = QListWidget(self)
        self.test_list.setSelectionMode(QListWidget.MultiSelection)
        self.test_list.itemSelectionChanged.connect(self.update_test_display)
        layout.addWidget(self.test_list)

        # Group boxes for selected items
        self.selected_medicines_group = QGroupBox("Selected Medicines")
        self.medicine_display = QVBoxLayout()
        self.selected_medicines_group.setLayout(self.medicine_display)

        self.selected_tests_group = QGroupBox("Selected Tests")
        self.test_display = QVBoxLayout()
        self.selected_tests_group.setLayout(self.test_display)

        layout.addWidget(self.selected_medicines_group)
        layout.addWidget(self.selected_tests_group)

        # Print button
        self.print_button = QPushButton("Print Selected Items")
        self.print_button.clicked.connect(self.print_selected_items)
        layout.addWidget(self.print_button)

        self.medicine_list.addItems(self.medicines)  # Add all medicines to the list
        self.test_list.addItems(self.tests)  # Add all tests to the list

        self.setLayout(layout)

    def update_medicine_dropdown(self):
        text = self.medicine_input.text().lower()
        self.medicine_list.clear()

        # Filter medicines based on the search text
        filtered_medicines = [medicine for medicine in self.medicines if medicine.lower().startswith(text)]
        self.medicine_list.addItems(filtered_medicines)

    def update_test_dropdown(self):
        text = self.test_input.text().lower()
        self.test_list.clear()

        # Filter tests based on the search text
        filtered_tests = [test for test in self.tests if test.lower().startswith(text)]
        self.test_list.addItems(filtered_tests)

    def update_medicine_display(self):
        selected_medicines = [item.text() for item in self.medicine_list.selectedItems()]

        for medicine in selected_medicines:
            if medicine not in self.selected_medicines:
                self.selected_medicines.append(medicine)
                medicine_layout = QHBoxLayout()
                medicine_label = QLabel(medicine)
                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(lambda _, med=medicine: self.remove_medicine(med))
                medicine_layout.addWidget(medicine_label)
                medicine_layout.addWidget(remove_button)
                self.medicine_display.addLayout(medicine_layout)

    def update_test_display(self):
        selected_tests = [item.text() for item in self.test_list.selectedItems()]

        for test in selected_tests:
            if test not in self.selected_tests:
                self.selected_tests.append(test)
                test_layout = QHBoxLayout()
                test_label = QLabel(test)
                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(lambda _, tst=test: self.remove_test(tst))
                test_layout.addWidget(test_label)
                test_layout.addWidget(remove_button)
                self.test_display.addLayout(test_layout)

    def remove_medicine(self, medicine):
        self.selected_medicines.remove(medicine)
        self.update_medicine_list_display()

    def remove_test(self, test):
        self.selected_tests.remove(test)
        self.update_test_list_display()

    def update_medicine_list_display(self):
        # Clear previous medicine display widgets
        for i in reversed(range(self.medicine_display.count())):
            widget_to_remove = self.medicine_display.itemAt(i).layout()
            if widget_to_remove:
                while widget_to_remove.count():
                    widget_to_remove.itemAt(0).widget().setParent(None)

        # Add updated list of selected medicines
        for medicine in self.selected_medicines:
            medicine_layout = QHBoxLayout()
            medicine_label = QLabel(medicine)
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda _, med=medicine: self.remove_medicine(med))
            medicine_layout.addWidget(medicine_label)
            medicine_layout.addWidget(remove_button)
            self.medicine_display.addLayout(medicine_layout)

    def update_test_list_display(self):
        # Clear previous test display widgets
        for i in reversed(range(self.test_display.count())):
            widget_to_remove = self.test_display.itemAt(i).layout()
            if widget_to_remove:
                while widget_to_remove.count():
                    widget_to_remove.itemAt(0).widget().setParent(None)

        # Add updated list of selected tests
        for test in self.selected_tests:
            test_layout = QHBoxLayout()
            test_label = QLabel(test)
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda _, tst=test: self.remove_test(tst))
            test_layout.addWidget(test_label)
            test_layout.addWidget(remove_button)
            self.test_display.addLayout(test_layout)

    def print_selected_items(self):
        # Print selected medicines
        print("Selected Medicines:")
        for medicine in self.selected_medicines:
            print(medicine)

        # Print selected tests
        print("Selected Tests:")
        for test in self.selected_tests:
            print(test)

        # Send selected medicines to backend
        self.send_selected_medicines_to_backend()
        self.send_selected_tests_to_backend()

    def send_selected_medicines_to_backend(self):
        try:
            # Fetch medicine IDs from selected medicines
            selected_medicine_ids = fetch_medicine_ids(self.selected_medicines)
            if not selected_medicine_ids:
                print("No medicines selected to send.")
                return
            
            print("Selected Medicine IDs:", selected_medicine_ids)
            
            # Get visit ID
            if self.visit_id is None:
                print("Visit ID is not set.")
                return
            print(f"Processing prescriptions for Visit ID: {self.visit_id}")
            
            # Create prescriptions for each selected medicine
            for medicine_id in selected_medicine_ids:
                try:
                    create_prescription(self.visit_id, medicine_id)  # Pass visit_id and medicine_id
                    print(f"Prescription created for Medicine ID: {medicine_id}")
                except Exception as e:
                    print(f"Error creating prescription for Medicine ID {medicine_id}: {e}")
        except Exception as e:
            print(f"An error occurred while sending selected medicines to the backend: {e}")



    def send_selected_tests_to_backend(self):
        try:
            # Fetch test IDs from selected tests
            selected_test_ids = fetch_test_ids(self.selected_tests)
            if not selected_test_ids:
                print("No tests selected to send.")
                return
            
            print("Selected Test IDs:", selected_test_ids)
            
            # Get visit ID
            if self.visit_id is None:
                print("Visit ID is not set.")
                return
            print(f"Processing tests for Visit ID: {self.visit_id}")
            
            # Process each selected test ID
            for test_id in selected_test_ids:
                try:
                    create_test_prescription(self.visit_id, test_id)  # Pass visit_id and test_id
                    print(f"Test prescription created for Test ID: {test_id}")
                except Exception as e:
                    print(f"Error processing test ID {test_id}: {e}")
        except Exception as e:
            print(f"An error occurred while sending selected tests to the backend: {e}")



    def go_to_next_page(self): 
        # Logic to switch to the next page 
        parent = self.parentWidget() 
        if parent: 
            parent.show_history()
if __name__ == '__main__':
    app = QApplication([])
    window = MedicinePage()
    window.show()
    app.exec_()
    
