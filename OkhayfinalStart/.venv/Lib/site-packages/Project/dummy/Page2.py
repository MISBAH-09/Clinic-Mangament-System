from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton

class Page2(QWidget):
    def __init__(self, go_to_page3_callback):
        super().__init__()
        self.go_to_page3_callback = go_to_page3_callback
        self.diagnosis_dropdown = QComboBox()
        self.diagnosis_dropdown.addItems(['Diagnosis1', 'Diagnosis2', 'Diagnosis3'])
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.diagnosis_dropdown)
        btn_next = QPushButton('Next', self)
        btn_next.clicked.connect(self.go_to_page3)
        layout.addWidget(btn_next)

    def go_to_page3(self):
        # Store selected diagnosis and navigate to Page 3
        selected_diagnosis = self.diagnosis_dropdown.currentText()
        self.go_to_page3_callback(selected_diagnosis)
