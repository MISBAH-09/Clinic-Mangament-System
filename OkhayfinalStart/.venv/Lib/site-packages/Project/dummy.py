import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QStackedWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.symptoms = []
        self.diagnoses = []
        self.medications = []
        self.tests = []

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        self.page1 = QWidget()
        self.page2 = QWidget()
        self.page3 = QWidget()

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)

        self.setupPage1()
        self.setupPage2()
        self.setupPage3()

        self.setLayout(self.layout)
        self.setWindowTitle('Doctor Panel')
        self.show()

    def setupPage1(self):
        layout = QVBoxLayout()
        self.symptom_dropdown = QComboBox()
        self.symptom_dropdown.addItems(['Symptom1', 'Symptom2', 'Symptom3'])
        layout.addWidget(self.symptom_dropdown)
        btn_next = QPushButton('Next', self)
        btn_next.clicked.connect(self.goToPage2)
        layout.addWidget(btn_next)
        self.page1.setLayout(layout)

    def setupPage2(self):
        layout = QVBoxLayout()
        self.diagnosis_dropdown = QComboBox()
        self.diagnosis_dropdown.addItems(['Diagnosis1', 'Diagnosis2', 'Diagnosis3'])
        layout.addWidget(self.diagnosis_dropdown)
        btn_next = QPushButton('Next', self)
        btn_next.clicked.connect(self.goToPage3)
        layout.addWidget(btn_next)
        self.page2.setLayout(layout)

    def setupPage3(self):
        layout = QVBoxLayout()
        self.med_dropdown = QComboBox()
        self.med_dropdown.addItems(['Med1', 'Med2', 'Med3'])
        layout.addWidget(self.med_dropdown)
        self.test_dropdown = QComboBox()
        self.test_dropdown.addItems(['Test1', 'Test2', 'Test3'])
        layout.addWidget(self.test_dropdown)
        btn_submit = QPushButton('Submit', self)
        btn_submit.clicked.connect(self.submitData)
        layout.addWidget(btn_submit)
        self.page3.setLayout(layout)

    def goToPage2(self):
        self.symptoms.append(self.symptom_dropdown.currentText())
        self.stacked_widget.setCurrentWidget(self.page2)

    def goToPage3(self):
        self.diagnoses.append(self.diagnosis_dropdown.currentText())
        self.stacked_widget.setCurrentWidget(self.page3)

    def submitData(self):
        self.medications.append(self.med_dropdown.currentText())
        self.tests.append(self.test_dropdown.currentText())
        # Here, insert the data into the respective tables
        print(f'Symptoms: {self.symptoms}')
        print(f'Diagnoses: {self.diagnoses}')
        print(f'Medications: {self.medications}')
        print(f'Tests: {self.tests}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
