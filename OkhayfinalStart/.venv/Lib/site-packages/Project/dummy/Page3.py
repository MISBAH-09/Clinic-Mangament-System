from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton

class Page3(QWidget):
    def __init__(self, submit_data_callback):
        super().__init__()
        self.submit_data_callback = submit_data_callback
        self.med_dropdown = QComboBox()
        self.med_dropdown.addItems(['Med1', 'Med2', 'Med3'])
        self.test_dropdown = QComboBox()
        self.test_dropdown.addItems(['Test1', 'Test2', 'Test3'])
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.med_dropdown)
        layout.addWidget(self.test_dropdown)
        btn_submit = QPushButton('Submit', self)
        btn_submit.clicked.connect(self.submit_data)
        layout.addWidget(btn_submit)

    def submit_data(self):
        # Store selected medication and test, and submit data
        selected_medication = self.med_dropdown.currentText()
        selected_test = self.test_dropdown.currentText()
        self.submit_data_callback(selected_medication, selected_test)
