from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QScrollArea, QGroupBox, QFormLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from DoctorScreenBackend import (
    get_patient_and_doctor_info,
    get_medicines_by_visit,
    get_tests_by_visit,
    get_diagnoses_by_visit,
    get_symptoms_by_visit
)


class HistoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.visit_id = None

    def set_visit_id(self, visit_id):
        """
        Set the visit ID and update the UI with the relevant data.
        """
        self.visit_id = visit_id
        print(f"HistoryPage received Visit ID: {self.visit_id}")
        self.update_data()

    def initUI(self):
        """
        Initialize the user interface for the HistoryPage.
        """
        self.layout = QVBoxLayout(self)

        # Create a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create a widget to hold all the content
        self.content_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.content_widget)

        # Patient and Doctor Information
        self.info_group = QGroupBox("Patient & Doctor Information")
        self.info_layout = QFormLayout(self.info_group)
        self.doctor_name_label = QLabel()
        self.patient_name_label = QLabel()
        self.age_label = QLabel()
        self.gender_label = QLabel()
        self.contact_label = QLabel()

        self.info_layout.addRow("Doctor:", self.doctor_name_label)
        self.info_layout.addRow("Patient Name:", self.patient_name_label)
        self.info_layout.addRow("Age:", self.age_label)
        self.info_layout.addRow("Gender:", self.gender_label)
        self.info_layout.addRow("Contact:", self.contact_label)

        # Symptoms
        self.symptoms_group = QGroupBox("Symptoms")
        self.symptoms_layout = QVBoxLayout(self.symptoms_group)
        self.symptoms_content = QLabel()
        self.symptoms_layout.addWidget(self.symptoms_content)

        # Diagnoses
        self.diagnoses_group = QGroupBox("Diagnoses")
        self.diagnoses_layout = QVBoxLayout(self.diagnoses_group)
        self.diagnoses_content = QLabel()
        self.diagnoses_layout.addWidget(self.diagnoses_content)

        # Medicines
        self.medicines_group = QGroupBox("Prescribed Medicines")
        self.medicines_layout = QVBoxLayout(self.medicines_group)
        self.medicines_content = QLabel()
        self.medicines_layout.addWidget(self.medicines_content)

        # Tests
        self.tests_group = QGroupBox("Prescribed Tests")
        self.tests_layout = QVBoxLayout(self.tests_group)
        self.tests_content = QLabel()
        self.tests_layout.addWidget(self.tests_content)

        # Add all sections to the content layout
        self.scroll_layout.addWidget(self.info_group)
        self.scroll_layout.addWidget(self.symptoms_group)
        self.scroll_layout.addWidget(self.diagnoses_group)
        self.scroll_layout.addWidget(self.medicines_group)
        self.scroll_layout.addWidget(self.tests_group)

        # Set the content widget as the scroll area's widget
        self.scroll_area.setWidget(self.content_widget)

        # Add the scroll area to the main layout
        self.layout.addWidget(self.scroll_area)

    def update_data(self):
        """
        Fetch and display data for the provided visit ID.
        """
        if not self.visit_id:
            return

        # Fetch and display patient and doctor info
        patient_and_doctor_info = get_patient_and_doctor_info(self.visit_id)
        if patient_and_doctor_info:
            doctor_name, patient_name, age, gender, contact = patient_and_doctor_info
            self.doctor_name_label.setText(doctor_name)
            self.patient_name_label.setText(patient_name)
            self.age_label.setText(f"{age} years")
            self.gender_label.setText(gender)
            self.contact_label.setText(contact)
        else:
            self.doctor_name_label.setText("Not Found")
            self.patient_name_label.setText("Not Found")
            self.age_label.setText("N/A")
            self.gender_label.setText("N/A")
            self.contact_label.setText("N/A")

        # Fetch and display symptoms
        symptoms = get_symptoms_by_visit(self.visit_id)
        if symptoms:
            symptoms_list = ", ".join(symptom[0] for symptom in symptoms)
            self.symptoms_content.setText(symptoms_list)
        else:
            self.symptoms_content.setText("No symptoms recorded.")

        # Fetch and display diagnoses
        diagnoses = get_diagnoses_by_visit(self.visit_id)
        if diagnoses:
            diagnoses_list = ", ".join(diagnosis[0] for diagnosis in diagnoses)
            self.diagnoses_content.setText(diagnoses_list)
        else:
            self.diagnoses_content.setText("No diagnoses recorded.")

        # Fetch and display medicines
        medicines = get_medicines_by_visit(self.visit_id)
        if medicines:
            medicines_list = "\n".join(f"{medicine[0]} - {medicine[1]} ({medicine[2]} days)"
                                       for medicine in medicines)
            self.medicines_content.setText(medicines_list)
        else:
            self.medicines_content.setText("No medicines prescribed.")

        # Fetch and display tests
        tests = get_tests_by_visit(self.visit_id)
        if tests:
            tests_list = "\n".join(f"{test[0]} - {test[1]}" for test in tests)
            self.tests_content.setText(tests_list)
        else:
            self.tests_content.setText("No tests prescribed.")
