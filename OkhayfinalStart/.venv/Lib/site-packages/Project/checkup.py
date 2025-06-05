from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget, QLabel,
    QPushButton, QHBoxLayout, QGroupBox, QScrollArea, QMainWindow, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from DoctorScreenBackend import (
    get_medicines, get_test, fetch_medicine_ids, fetch_test_ids, get_symptoms,
    get_diagnosis, fetch_diagnosis_ids, fetch_symptom_ids
)

class Checkup:
    def __init__(self):
        # Store selected symptoms, diagnoses, medicines, and tests
        self.selected_symptoms = []
        self.selected_diagnosis = []
        self.selected_medicines = []
        self.selected_tests = []
        self.visit_id = None

    def set_visit_id(self, visit_id):
        self.visit_id = visit_id  # Store the visit ID for this checkup

    def add_symptom(self, symptom):
        if symptom not in self.selected_symptoms:
            self.selected_symptoms.append(symptom)

    def remove_symptom(self, symptom):
        if symptom in self.selected_symptoms:
            self.selected_symptoms.remove(symptom)

    def add_diagnosis(self, diagnosis):
        if diagnosis not in self.selected_diagnosis:
            self.selected_diagnosis.append(diagnosis)

    def remove_diagnosis(self, diagnosis):
        if diagnosis in self.selected_diagnosis:
            self.selected_diagnosis.remove(diagnosis)

    def add_medicine(self, medicine):
        if medicine not in self.selected_medicines:
            self.selected_medicines.append(medicine)

    def remove_medicine(self, medicine):
        if medicine in self.selected_medicines:
            self.selected_medicines.remove(medicine)

    def add_test(self, test):
        if test not in self.selected_tests:
            self.selected_tests.append(test)

    def remove_test(self, test):
        if test in self.selected_tests:
            self.selected_tests.remove(test)

    def get_symptom_ids(self):
        return fetch_symptom_ids(self.selected_symptoms)

    def get_diagnosis_ids(self):
        return fetch_diagnosis_ids(self.selected_diagnosis)

    def get_medicine_ids(self):
        return fetch_medicine_ids(self.selected_medicines)

    def get_test_ids(self):
        return fetch_test_ids(self.selected_tests)

    def print_checkup_summary(self):
        print("Selected Symptoms:", self.selected_symptoms)
        print("Selected Diagnosis:", self.selected_diagnosis)
        print("Selected Medicines:", self.selected_medicines)
        print("Selected Tests:", self.selected_tests)

class CheckupPage(QWidget):
    def __init__(self, checkup):
        super().__init__()
        self.checkup = checkup  # Pass the Checkup instance
        self.medicines = get_medicines()  # Fetch all medicines from the DB
        self.tests = get_test()  # Fetch all tests from the DB
        self.symptoms = get_symptoms()  # Fetch all symptoms from the DB
        self.diagnosis = get_diagnosis()  # Fetch all diagnosis from the DB
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Checkup Page')
        
        # Create a horizontal layout (50-50 split)
        main_layout = QHBoxLayout()

        # Left side: dropdowns for symptoms, diagnosis, medicines, tests
        left_layout = QVBoxLayout()
        
        # Symptoms Section
        self.symptoms_label = QLabel("Symptoms:", self)
        left_layout.addWidget(self.symptoms_label)

        self.symptoms_input = QLineEdit(self)
        self.symptoms_input.setPlaceholderText('Enter Symptom')
        self.symptoms_input.textChanged.connect(self.update_symptom_dropdown)
        left_layout.addWidget(self.symptoms_input)

        self.symptom_list = QListWidget(self)
        self.symptom_list.setSelectionMode(QListWidget.MultiSelection)
        self.symptom_list.itemSelectionChanged.connect(self.update_symptom_display)
        left_layout.addWidget(self.symptom_list)

        # Diagnosis Section
        self.diagnosis_label = QLabel("Diagnosis:", self)
        left_layout.addWidget(self.diagnosis_label)

        self.diagnosis_input = QLineEdit(self)
        self.diagnosis_input.setPlaceholderText('Enter Diagnosis')
        self.diagnosis_input.textChanged.connect(self.update_diagnosis_dropdown)
        left_layout.addWidget(self.diagnosis_input)

        self.diagnosis_list = QListWidget(self)
        self.diagnosis_list.setSelectionMode(QListWidget.MultiSelection)
        self.diagnosis_list.itemSelectionChanged.connect(self.update_diagnosis_display)
        left_layout.addWidget(self.diagnosis_list)

        # Medicines Section
        self.medicine_label = QLabel("Medicines:", self)
        left_layout.addWidget(self.medicine_label)

        self.medicine_input = QLineEdit(self)
        self.medicine_input.setPlaceholderText('Enter Medicine')
        self.medicine_input.textChanged.connect(self.update_medicine_dropdown)
        left_layout.addWidget(self.medicine_input)

        self.medicine_list = QListWidget(self)
        self.medicine_list.setSelectionMode(QListWidget.MultiSelection)
        self.medicine_list.itemSelectionChanged.connect(self.update_medicine_display)
        left_layout.addWidget(self.medicine_list)

        # Tests Section
        self.tests_label = QLabel("Tests:", self)
        left_layout.addWidget(self.tests_label)

        self.test_input = QLineEdit(self)
        self.test_input.setPlaceholderText('Enter Test')
        self.test_input.textChanged.connect(self.update_test_dropdown)
        left_layout.addWidget(self.test_input)

        self.test_list = QListWidget(self)
        self.test_list.setSelectionMode(QListWidget.MultiSelection)
        self.test_list.itemSelectionChanged.connect(self.update_test_display)
        left_layout.addWidget(self.test_list)

        # Add all symptoms, diagnoses, medicines, and tests to the lists
        self.symptom_list.addItems(self.symptoms)
        self.diagnosis_list.addItems(self.diagnosis)
        self.medicine_list.addItems(self.medicines)
        self.test_list.addItems(self.tests)

        # Right side: selected items display
        right_layout = QVBoxLayout()

        # Selected Symptoms, Diagnosis, Medicines, Tests
        self.selected_label = QLabel("Selected Items:", self)
        right_layout.addWidget(self.selected_label)

        # Display selected symptoms, diagnosis, medicines, tests
        self.selected_display = QLabel("", self)
        right_layout.addWidget(self.selected_display)

        # Button to print the summary of selected items
        self.print_button = QPushButton("Print Selected Items")
        self.print_button.clicked.connect(self.print_selected_items)
        right_layout.addWidget(self.print_button)

        # Add both left and right sections to the main layout
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 1)

        # Set the main layout for the page
        self.setLayout(main_layout)

    def update_symptom_dropdown(self):
        text = self.symptoms_input.text().lower()
        self.symptom_list.clear()
        filtered_symptoms = [symptom for symptom in self.symptoms if symptom.lower().startswith(text)]
        self.symptom_list.addItems(filtered_symptoms)

    def update_diagnosis_dropdown(self):
        text = self.diagnosis_input.text().lower()
        self.diagnosis_list.clear()
        filtered_diagnosis = [diagnosis for diagnosis in self.diagnosis if diagnosis.lower().startswith(text)]
        self.diagnosis_list.addItems(filtered_diagnosis)

    def update_medicine_dropdown(self):
        text = self.medicine_input.text().lower()
        self.medicine_list.clear()
        filtered_medicines = [medicine for medicine in self.medicines if medicine.lower().startswith(text)]
        self.medicine_list.addItems(filtered_medicines)

    def update_test_dropdown(self):
        text = self.test_input.text().lower()
        self.test_list.clear()
        filtered_tests = [test for test in self.tests if test.lower().startswith(text)]
        self.test_list.addItems(filtered_tests)

    def update_symptom_display(self):
        selected_symptoms = [item.text() for item in self.symptom_list.selectedItems()]
        for symptom in selected_symptoms:
            self.checkup.add_symptom(symptom)
        self.update_selected_display()

    def update_diagnosis_display(self):
        selected_diagnosis = [item.text() for item in self.diagnosis_list.selectedItems()]
        for diagnosis in selected_diagnosis:
            self.checkup.add_diagnosis(diagnosis)
        self.update_selected_display()

    def update_medicine_display(self):
        selected_medicines = [item.text() for item in self.medicine_list.selectedItems()]
        for medicine in selected_medicines:
            self.checkup.add_medicine(medicine)
        self.update_selected_display()

    def update_test_display(self):
        selected_tests = [item.text() for item in self.test_list.selectedItems()]
        for test in selected_tests:
            self.checkup.add_test(test)
        self.update_selected_display()

    def update_selected_display(self):
        selected_items = (
            f"Symptoms: {', '.join(self.checkup.selected_symptoms)}\n"
            f"Diagnosis: {', '.join(self.checkup.selected_diagnosis)}\n"
            f"Medicines: {', '.join(self.checkup.selected_medicines)}\n"
            f"Tests: {', '.join(self.checkup.selected_tests)}"
        )
        self.selected_display.setText(selected_items)

    def print_selected_items(self):
        self.checkup.print_checkup_summary()

if __name__ == '__main__':
    app = QApplication([])
    checkup = Checkup()
    checkup_page = CheckupPage(checkup)
    checkup_page.show()
    app.exec_()
