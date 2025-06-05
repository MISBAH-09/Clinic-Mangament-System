from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton

class Page1(QWidget):
    def __init__(self, go_to_page2_callback):
        super().__init__()
        self.go_to_page2_callback = go_to_page2_callback
        self.symptom_dropdown = QComboBox()
        self.symptom_dropdown.addItems(['Symptom1', 'Symptom2', 'Symptom3'])
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.symptom_dropdown)
        btn_next = QPushButton('Next', self)
        btn_next.clicked.connect(self.go_to_page2)
        layout.addWidget(btn_next)

    def go_to_page2(self):
        # Store selected symptom and navigate to Page 2
        selected_symptom = self.symptom_dropdown.currentText()
        self.go_to_page2_callback(selected_symptom)
