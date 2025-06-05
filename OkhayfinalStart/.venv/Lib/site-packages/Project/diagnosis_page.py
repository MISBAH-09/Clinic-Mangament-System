from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget, QLabel,
    QPushButton, QHBoxLayout, QGroupBox, QScrollArea, QMainWindow, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
# from diagnosisBackend import get_symptoms, get_diagnosis  # Import the backend functions
from DoctorScreenBackend import get_symptoms, create_symptom_record, create_diagnosis_record, get_diagnosis, fetch_diagnosis_ids, fetch_symptom_ids


class DiagnosisPage(QWidget):
    def __init__(self):
        super().__init__()
        self.symptoms = get_symptoms()  # Fetch all symptoms from the DB
        self.diagnosis = get_diagnosis()
        self.selected_symptoms = []  # Track selected symptoms
        self.selected_diagnosis = []  # Track selected diagnosis
        self.visit_id = None  # Store the visit ID
        self.initUI()  # Initialize the UI

    def set_visit_id(self, visit_id):
        self.visit_id = visit_id  # Store the visit ID
        print(f"DiagnosisPage received Visit ID: {self.visit_id}")

    def initUI(self):
        self.setWindowTitle('Symptoms and Diagnosis Selector')

        main_layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        # Symptoms section
        symptoms_layout = QHBoxLayout()
        left_symptoms_layout = QVBoxLayout()

        # Label for symptoms
        self.symptoms_label = QLabel("Symptoms:", self)
        self.symptoms_label.setFont(QFont('Arial', 14, QFont.Bold))
        left_symptoms_layout.addWidget(self.symptoms_label)

        # Searchable dropdown for symptoms
        self.symptoms_input = QLineEdit(self)
        self.symptoms_input.setPlaceholderText('Enter symptoms')
        self.symptoms_input.textChanged.connect(self.update_symptoms_dropdown)
        self.symptoms_input.setStyleSheet("border: 1px solid black;")
        left_symptoms_layout.addWidget(self.symptoms_input)

        self.symptoms_list = QListWidget(self)
        self.symptoms_list.setSelectionMode(QListWidget.MultiSelection)
        self.symptoms_list.itemSelectionChanged.connect(self.update_symptoms_display)
        self.symptoms_list.setStyleSheet("border: 1px solid black;")
        left_symptoms_layout.addWidget(self.symptoms_list)

        symptoms_layout.addLayout(left_symptoms_layout)

        # Right side for selected symptoms
        self.selected_symptoms_group = QGroupBox("Selected Symptoms")
        self.selected_symptoms_group.setFont(QFont('Arial', 12, QFont.Bold))
        self.selected_symptoms_group.setStyleSheet("border: 1px solid black;")
        self.symptoms_display = QVBoxLayout()
        self.selected_symptoms_group.setLayout(self.symptoms_display)
        symptoms_layout.addWidget(self.selected_symptoms_group)

        symptoms_layout.setStretch(0, 1)
        symptoms_layout.setStretch(1, 1)
        layout.addLayout(symptoms_layout)

        # Diagnosis section
        diagnosis_layout = QHBoxLayout()
        left_diagnosis_layout = QVBoxLayout()

        # Label for diagnosis
        self.diagnosis_label = QLabel("Diagnosis:", self)
        self.diagnosis_label.setFont(QFont('Arial', 14, QFont.Bold))
        left_diagnosis_layout.addWidget(self.diagnosis_label)

        # Searchable dropdown for diagnosis
        self.diagnosis_input = QLineEdit(self)
        self.diagnosis_input.setPlaceholderText('Enter diagnosis')
        self.diagnosis_input.textChanged.connect(self.update_diagnosis_dropdown)
        self.diagnosis_input.setStyleSheet("border: 1px solid black;")
        left_diagnosis_layout.addWidget(self.diagnosis_input)

        self.diagnosis_list = QListWidget(self)
        self.diagnosis_list.setSelectionMode(QListWidget.MultiSelection)
        self.diagnosis_list.itemSelectionChanged.connect(self.update_diagnosis_display)
        self.diagnosis_list.setStyleSheet("border: 1px solid black;")
        left_diagnosis_layout.addWidget(self.diagnosis_list)

        diagnosis_layout.addLayout(left_diagnosis_layout)

        # Right side for selected diagnosis
        self.selected_diagnosis_group = QGroupBox("Selected Diagnosis")
        self.selected_diagnosis_group.setFont(QFont('Arial', 12, QFont.Bold))
        self.selected_diagnosis_group.setStyleSheet("border: 1px solid black;")
        self.diagnosis_display = QVBoxLayout()
        self.selected_diagnosis_group.setLayout(self.diagnosis_display)
        diagnosis_layout.addWidget(self.selected_diagnosis_group)

        diagnosis_layout.setStretch(0, 1)
        diagnosis_layout.setStretch(1, 1)
        layout.addLayout(diagnosis_layout)

        # Add Print button
        self.print_button = QPushButton("Print Selected")
        self.print_button.setFont(QFont('Arial', 12, QFont.Bold))
        self.print_button.clicked.connect(self.print_selected_items)
        layout.addWidget(self.print_button)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def update_symptoms_dropdown(self):
        text = self.symptoms_input.text().lower()
        self.symptoms_list.clear()
        filtered_symptoms = [symptoms for symptoms in self.symptoms if symptoms.lower().startswith(text)]
        self.symptoms_list.addItems(filtered_symptoms)

    def update_diagnosis_dropdown(self):
        text = self.diagnosis_input.text().lower()
        self.diagnosis_list.clear()
        filtered_diagnosis = [diagnosis for diagnosis in self.diagnosis if diagnosis.lower().startswith(text)]
        self.diagnosis_list.addItems(filtered_diagnosis)

    def update_symptoms_display(self):
        selected_symptoms = [item.text() for item in self.symptoms_list.selectedItems()]
        for symptoms in selected_symptoms:
            if symptoms not in self.selected_symptoms:
                self.selected_symptoms.append(symptoms)
                symptoms_layout = QHBoxLayout()
                symptoms_label = QLabel(symptoms)
                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(lambda _, sym=symptoms: self.remove_symptoms(sym))
                symptoms_layout.addWidget(symptoms_label)
                symptoms_layout.addWidget(remove_button)
                self.symptoms_display.addLayout(symptoms_layout)

    def update_diagnosis_display(self):
        selected_diagnosis = [item.text() for item in self.diagnosis_list.selectedItems()]
        for diagnosis in selected_diagnosis:
            if diagnosis not in self.selected_diagnosis:
                self.selected_diagnosis.append(diagnosis)
                diagnosis_layout = QHBoxLayout()
                diagnosis_label = QLabel(diagnosis)
                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(lambda _, diag=diagnosis: self.remove_diagnosis(diag))
                diagnosis_layout.addWidget(diagnosis_label)
                diagnosis_layout.addWidget(remove_button)
                self.diagnosis_display.addLayout(diagnosis_layout)

    def print_selected_items(self):
        # Print visit_id
        print(f"in diagnosis bVisit ID: {self.visit_id}")

        # Print selected diagnosis
        print("Selected Diagnosis:")
        for diagnosis in self.selected_diagnosis:
            print(diagnosis)

        # Print selected symptoms
        print("Selected Symptoms:")
        for symptoms in self.selected_symptoms:
            print(symptoms)

        # Send selected symptoms to backend
        self.send_selected_symptoms_to_backend()
        self.send_selected_diagnosis_to_backend()

    def send_selected_symptoms_to_backend(self):
        try:
            if not self.visit_id:
                print("Visit ID is not set.")
                return

            # Fetch symptom IDs from selected symptoms
            selected_symptom_ids = fetch_symptom_ids(self.selected_symptoms)
            if not selected_symptom_ids:
                print("No symptoms selected to send.")
                return

            print("Selected Symptom IDs:", selected_symptom_ids)
            print(f"Processing symptoms for Visit ID: {self.visit_id}")

            # Create records for each selected symptom
            for symptom_id in selected_symptom_ids:
                try:
                    create_symptom_record(self.visit_id, symptom_id)  # Pass visit_id and symptom_id
                    print(f"Symptom record created for Symptom ID: {symptom_id}")
                except Exception as e:
                    print(f"Error creating symptom record for Symptom ID {symptom_id}: {e}")
        except Exception as e:
            print(f"An error occurred while sending selected symptoms to the backend: {e}")

    def send_selected_diagnosis_to_backend(self):
        try:
            if not self.visit_id:
                print("Visit ID is not set.")
                return

            # Fetch diagnosis IDs from selected diagnoses
            selected_diagnosis_ids = fetch_diagnosis_ids(self.selected_diagnosis)
            if not selected_diagnosis_ids:
                print("No diagnoses selected to send.")
                return

            print("Selected Diagnosis IDs:", selected_diagnosis_ids)
            print(f"Processing diagnoses for Visit ID: {self.visit_id}")

            # Create records for each selected diagnosis
            for diagnosis_id in selected_diagnosis_ids:
                try:
                    create_diagnosis_record(self.visit_id, diagnosis_id)  # Pass visit_id and diagnosis_id
                    print(f"Diagnosis record created for Diagnosis ID: {diagnosis_id}")
                except Exception as e:
                    print(f"Error creating diagnosis record for Diagnosis ID {diagnosis_id}: {e}")
        except Exception as e:
            print(f"An error occurred while sending selected diagnoses to the backend: {e}")

    def remove_symptoms(self, symptom):
        self.selected_symptoms.remove(symptom)
        self.update_symptoms_list_display()

    def remove_diagnosis(self, diagnosis):
        self.selected_diagnosis.remove(diagnosis)
        self.update_diagnosis_list_display()

    def update_symptoms_list_display(self):
        # Clear previous symptom display widgets
        for i in reversed(range(self.symptoms_display.count())):
            widget_to_remove = self.symptoms_display.itemAt(i).layout()
            if widget_to_remove:
                while widget_to_remove.count():
                    widget_to_remove.itemAt(0).widget().setParent(None)

        # Add updated list of selected symptoms
        for symptom in self.selected_symptoms:
            symptom_layout = QHBoxLayout()
            symptom_label = QLabel(symptom)
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda _, sym=symptom: self.remove_symptoms(sym))
            symptom_layout.addWidget(symptom_label)
            symptom_layout.addWidget(remove_button)
            self.symptoms_display.addLayout(symptom_layout)

    def update_diagnosis_list_display(self):
        # Clear previous diagnosis display widgets
        for i in reversed(range(self.diagnosis_display.count())):
            widget_to_remove = self.diagnosis_display.itemAt(i).layout()
            if widget_to_remove:
                while widget_to_remove.count():
                    widget_to_remove.itemAt(0).widget().setParent(None)

        # Add updated list of selected diagnosis
        for diagnosis in self.selected_diagnosis:
            diagnosis_layout = QHBoxLayout()
            diagnosis_label = QLabel(diagnosis)
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda _, diag=diagnosis: self.remove_diagnosis(diag))
            diagnosis_layout.addWidget(diagnosis_label)
            diagnosis_layout.addWidget(remove_button)
            self.diagnosis_display.addLayout(diagnosis_layout)







# DiagnosisPage.py

# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget, QLabel,
#     QPushButton, QHBoxLayout, QGroupBox, QScrollArea, QMainWindow, QMessageBox
# )
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QFont
# from DoctorScreenBackend import (
#     get_symptoms, create_symptom_record, create_diagnosis_record,
#     get_diagnosis, fetch_diagnosis_ids, fetch_symptom_ids
# )

# class DiagnosisPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.symptoms = get_symptoms()  # Fetch all symptoms from the DB
#         self.diagnosis = get_diagnosis()
#         self.selected_symptoms = []  # Track selected symptoms
#         self.selected_diagnosis = []  # Track selected diagnosis
#         self.visit_id = None  # Store the visit ID
#         self.initUI()  # Initialize the UI

#     def set_visit_id(self, visit_id):
#         self.visit_id = visit_id  # Store the visit ID
#         print(f"DiagnosisPage received Visit ID: {self.visit_id}")

#     def initUI(self):
#         self.setWindowTitle('Symptoms and Diagnosis Selector')

#         main_layout = QVBoxLayout()
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)

#         content_widget = QWidget()
#         layout = QVBoxLayout(content_widget)

#         # Symptoms section
#         symptoms_layout = QHBoxLayout()
#         left_symptoms_layout = QVBoxLayout()

#         # Label for symptoms
#         self.symptoms_label = QLabel("Symptoms:", self)
#         self.symptoms_label.setFont(QFont('Arial', 14, QFont.Bold))
#         left_symptoms_layout.addWidget(self.symptoms_label)

#         # Searchable dropdown for symptoms
#         self.symptoms_input = QLineEdit(self)
#         self.symptoms_input.setPlaceholderText('Enter symptoms')
#         self.symptoms_input.textChanged.connect(self.update_symptoms_dropdown)
#         self.symptoms_input.setStyleSheet("border: 1px solid black;")
#         left_symptoms_layout.addWidget(self.symptoms_input)

#         self.symptoms_list = QListWidget(self)
#         self.symptoms_list.setSelectionMode(QListWidget.MultiSelection)
#         self.symptoms_list.itemSelectionChanged.connect(self.update_symptoms_display)
#         self.symptoms_list.setStyleSheet("border: 1px solid black;")
#         left_symptoms_layout.addWidget(self.symptoms_list)

#         symptoms_layout.addLayout(left_symptoms_layout)

#         # Right side for selected symptoms
#         self.selected_symptoms_group = QGroupBox("Selected Symptoms")
#         self.selected_symptoms_group.setFont(QFont('Arial', 12, QFont.Bold))
#         self.selected_symptoms_group.setStyleSheet("border: 1px solid black;")
#         self.symptoms_display = QVBoxLayout()
#         self.selected_symptoms_group.setLayout(self.symptoms_display)
#         symptoms_layout.addWidget(self.selected_symptoms_group)

#         symptoms_layout.setStretch(0, 1)
#         symptoms_layout.setStretch(1, 1)
#         layout.addLayout(symptoms_layout)

#         # Diagnosis section
#         diagnosis_layout = QHBoxLayout()
#         left_diagnosis_layout = QVBoxLayout()

#         # Label for diagnosis
#         self.diagnosis_label = QLabel("Diagnosis:", self)
#         self.diagnosis_label.setFont(QFont('Arial', 14, QFont.Bold))
#         left_diagnosis_layout.addWidget(self.diagnosis_label)

#         # Searchable dropdown for diagnosis
#         self.diagnosis_input = QLineEdit(self)
#         self.diagnosis_input.setPlaceholderText('Enter diagnosis')
#         self.diagnosis_input.textChanged.connect(self.update_diagnosis_dropdown)
#         self.diagnosis_input.setStyleSheet("border: 1px solid black;")
#         left_diagnosis_layout.addWidget(self.diagnosis_input)

#         self.diagnosis_list = QListWidget(self)
#         self.diagnosis_list.setSelectionMode(QListWidget.MultiSelection)
#         self.diagnosis_list.itemSelectionChanged.connect(self.update_diagnosis_display)
#         self.diagnosis_list.setStyleSheet("border: 1px solid black;")
#         left_diagnosis_layout.addWidget(self.diagnosis_list)

#         diagnosis_layout.addLayout(left_diagnosis_layout)

#         # Right side for selected diagnosis
#         self.selected_diagnosis_group = QGroupBox("Selected Diagnosis")
#         self.selected_diagnosis_group.setFont(QFont('Arial', 12, QFont.Bold))
#         self.selected_diagnosis_group.setStyleSheet("border: 1px solid black;")
#         self.diagnosis_display = QVBoxLayout()
#         self.selected_diagnosis_group.setLayout(self.diagnosis_display)
#         diagnosis_layout.addWidget(self.selected_diagnosis_group)

#         diagnosis_layout.setStretch(0, 1)
#         diagnosis_layout.setStretch(1, 1)
#         layout.addLayout(diagnosis_layout)

#         # Add Print button
#         self.print_button = QPushButton("Print Selected")
#         self.print_button.setFont(QFont('Arial', 12, QFont.Bold))
#         self.print_button.clicked.connect(self.print_selected_items)
#         layout.addWidget(self.print_button)

#         scroll.setWidget(content_widget)
#         main_layout.addWidget(scroll)
#         self.setLayout(main_layout)

#         # Populate lists with data
#         self.symptoms_list.addItems(self.symptoms)
#         self.diagnosis_list.addItems(self.diagnosis)

#     def update_symptoms_dropdown(self):
#         text = self.symptoms_input.text().lower()
#         self.symptoms_list.clear()
#         filtered_symptoms = [symptom for symptom in self.symptoms if symptom.lower().startswith(text)]
#         self.symptoms_list.addItems(filtered_symptoms)

#     def update_diagnosis_dropdown(self):
#         text = self.diagnosis_input.text().lower()
#         self.diagnosis_list.clear()
#         filtered_diagnosis = [diag for diag in self.diagnosis if diag.lower().startswith(text)]
#         self.diagnosis_list.addItems(filtered_diagnosis)

#     def update_symptoms_display(self):
#         selected_symptoms = [item.text() for item in self.symptoms_list.selectedItems()]
#         for symptom in selected_symptoms:
#             if symptom not in self.selected_symptoms:
#                 self.selected_symptoms.append(symptom)
#                 symptom_layout = QHBoxLayout()
#                 symptom_label = QLabel(symptom)
#                 remove_button = QPushButton("Remove")
#                 remove_button.clicked.connect(lambda _, sym=symptom: self.remove_symptom(sym))
#                 symptom_layout.addWidget(symptom_label)
#                 symptom_layout.addWidget(remove_button)
#                 self.symptoms_display.addLayout(symptom_layout)

#     def update_diagnosis_display(self):
#         selected_diagnosis = [item.text() for item in self.diagnosis_list.selectedItems()]
#         for diag in selected_diagnosis:
#             if diag not in self.selected_diagnosis:
#                 self.selected_diagnosis.append(diag)
#                 diagnosis_layout = QHBoxLayout()
#                 diagnosis_label = QLabel(diag)
#                 remove_button = QPushButton("Remove")
#                 remove_button.clicked.connect(lambda _, d=diag: self.remove_diagnosis(d))
#                 diagnosis_layout.addWidget(diagnosis_label)
#                 diagnosis_layout.addWidget(remove_button)
#                 self.diagnosis_display.addLayout(diagnosis_layout)

#     def print_selected_items(self):
#         # Print visit_id
#         print(f"Visit ID: {self.visit_id}")

#         # Print selected diagnosis
#         print("Selected Diagnosis:")
#         for diag in self.selected_diagnosis:
#             print(diag)

#         # Print selected symptoms
#         print("Selected Symptoms:")
#         for sym in self.selected_symptoms:
#             print(sym)

#         # Send selected symptoms to backend
#         self.send_selected_symptoms_to_backend()
#         self.send_selected_diagnosis_to_backend()

#     def send_selected_symptoms_to_backend(self):
#         try:
#             if not self.visit_id:
#                 print("Visit ID is not set.")
#                 return

#             # Fetch symptom IDs from selected symptoms
#             selected_symptom_ids = fetch_symptom_ids(self.selected_symptoms)
#             if not selected_symptom_ids:
#                 print("No symptoms selected to send.")
#                 return

#             print("Selected Symptom IDs:", selected_symptom_ids)
#             print(f"Processing symptoms for Visit ID: {self.visit_id}")

#             # Create records for each selected symptom
#             for symptom_id in selected_symptom_ids:
#                 try:
#                     create_symptom_record(self.visit_id, symptom_id)  # Pass visit_id and symptom_id
#                     print(f"Symptom record created for Symptom ID: {symptom_id}")
#                 except Exception as e:
#                     print(f"Error creating symptom record for Symptom ID {symptom_id}: {e}")
#         except Exception as e:
#             print(f"An error occurred while sending selected symptoms to the backend: {e}")

#     def send_selected_diagnosis_to_backend(self):
#         try:
#             if not self.visit_id:
#                 print("Visit ID is not set.")
#                 return

#             # Fetch diagnosis IDs from selected diagnoses
#             selected_diagnosis_ids = fetch_diagnosis_ids(self.selected_diagnosis)
#             if not selected_diagnosis_ids:
#                 print("No diagnoses selected to send.")
#                 return

#             print("Selected Diagnosis IDs:", selected_diagnosis_ids)
#             print(f"Processing diagnoses for Visit ID: {self.visit_id}")

#             # Create records for each selected diagnosis
#             for diagnosis_id in selected_diagnosis_ids:
#                 try:
#                     create_diagnosis_record(self.visit_id, diagnosis_id)  # Pass visit_id and diagnosis_id
#                     print(f"Diagnosis record created for Diagnosis ID: {diagnosis_id}")
#                 except Exception as e:
#                     print(f"Error creating diagnosis record for Diagnosis ID {diagnosis_id}: {e}")
#         except Exception as e:
#             print(f"An error occurred while sending selected diagnoses to the backend: {e}")

#     def remove_symptom(self, symptom):
#         if symptom in self.selected_symptoms:
#             self.selected_symptoms.remove(symptom)
#             self.update_symptoms_display()

#     def remove_diagnosis(self, diagnosis):
#         if diagnosis in self.selected_diagnosis:
#             self.selected_diagnosis.remove(diagnosis)
#             self.update_diagnosis_display()

#     def update_symptoms_display(self):
#         # Clear existing symptom displays
#         while self.symptoms_display.count():
#             layout = self.symptoms_display.takeAt(0)
#             if layout:
#                 while layout.count():
#                     widget = layout.takeAt(0).widget()
#                     if widget:
#                         widget.deleteLater()

#         # Re-add selected symptoms
#         for sym in self.selected_symptoms:
#             symptom_layout = QHBoxLayout()
#             symptom_label = QLabel(sym)
#             remove_button = QPushButton("Remove")
#             remove_button.clicked.connect(lambda _, s=sym: self.remove_symptom(s))
#             symptom_layout.addWidget(symptom_label)
#             symptom_layout.addWidget(remove_button)
#             self.symptoms_display.addLayout(symptom_layout)

#     def update_diagnosis_display(self):
#         # Clear existing diagnosis displays
#         while self.diagnosis_display.count():
#             layout = self.diagnosis_display.takeAt(0)
#             if layout:
#                 while layout.count():
#                     widget = layout.takeAt(0).widget()
#                     if widget:
#                         widget.deleteLater()

#         # Re-add selected diagnoses
#         for diag in self.selected_diagnosis:
#             diagnosis_layout = QHBoxLayout()
#             diagnosis_label = QLabel(diag)
#             remove_button = QPushButton("Remove")
#             remove_button.clicked.connect(lambda _, d=diag: self.remove_diagnosis(d))
#             diagnosis_layout.addWidget(diagnosis_label)
#             diagnosis_layout.addWidget(remove_button)
#             self.diagnosis_display.addLayout(diagnosis_layout)

# if __name__ == '__main__':
#     app = QApplication([])
#     window = DiagnosisPage()
#     window.show()
#     app.exec_()
