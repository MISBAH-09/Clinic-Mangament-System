import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QListWidget, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from Page1 import Page1
from Page2 import Page2
from Page3 import Page3

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.symptoms = []
        self.diagnoses = []
        self.medications = []
        self.tests = []
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QHBoxLayout(self)

        # Sidebar layout (Vertical layout to stack items)
        sidebar_layout = QVBoxLayout()

        # Sidebar widget (ListWidget)
        self.sidebar = QListWidget()
        self.sidebar.addItem("Symptoms")
        self.sidebar.addItem("Diagnosis")
        self.sidebar.addItem("Medication & Test")
        self.sidebar.setStyleSheet("background-color: lightgray; border-right: 2px solid black;")  # Add border and background

        # Add a spacer to center the buttons vertically
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        sidebar_layout.addItem(spacer)

        # Button to navigate to different pages
        self.symptoms_button = QPushButton("Go to Symptoms")
        self.diagnosis_button = QPushButton("Go to Diagnosis")
        self.medication_button = QPushButton("Go to Medication & Test")

        # Style the buttons (borders, padding, etc.)
        self.style_buttons()

        # Add buttons to the sidebar layout
        sidebar_layout.addWidget(self.symptoms_button)
        sidebar_layout.addWidget(self.diagnosis_button)
        sidebar_layout.addWidget(self.medication_button)

        # Add sidebar layout to the main layout
        sidebar_layout.addWidget(self.sidebar)
        main_layout.addLayout(sidebar_layout, 1)  # Sidebar takes 1/4 of the width

        # QStackedWidget
        self.stacked_widget = QStackedWidget(self)

        # Initialize Pages
        self.page1 = Page1(self.goToPage2)
        self.page2 = Page2(self.goToPage3)
        self.page3 = Page3(self.submitData)

        # Add Pages to QStackedWidget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)

        # Add QStackedWidget to the main layout
        main_layout.addWidget(self.stacked_widget, 3)  # Stacked widget takes 3/4 of the width

        # Set the main layout
        self.setLayout(main_layout)
        self.setWindowTitle('Doctor Panel')
        self.show()

        # Connect the buttons to the page change methods
        self.symptoms_button.clicked.connect(lambda: self.changePage(0))
        self.diagnosis_button.clicked.connect(lambda: self.changePage(1))
        self.medication_button.clicked.connect(lambda: self.changePage(2))

    def goToPage2(self, symptom):
        self.symptoms.append(symptom)
        self.stacked_widget.setCurrentWidget(self.page2)

    def goToPage3(self, diagnosis):
        self.diagnoses.append(diagnosis)
        self.stacked_widget.setCurrentWidget(self.page3)

    def submitData(self, medication, test):
        self.medications.append(medication)
        self.tests.append(test)
        # Here, insert the data into the respective tables
        print(f'Symptoms: {self.symptoms}')
        print(f'Diagnoses: {self.diagnoses}')
        print(f'Medications: {self.medications}')
        print(f'Tests: {self.tests}')

    def changePage(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def style_buttons(self):
        """ Apply styling to buttons like borders, padding, etc. """
        button_style = """
        QPushButton {
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 10px 20px;
            background-color: #8BC34A;
            color: white;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #7CB342;
        }
        """
        self.symptoms_button.setStyleSheet(button_style)
        self.diagnosis_button.setStyleSheet(button_style)
        self.medication_button.setStyleSheet(button_style)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
