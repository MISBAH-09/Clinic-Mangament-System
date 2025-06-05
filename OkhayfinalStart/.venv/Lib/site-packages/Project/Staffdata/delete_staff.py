from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QSpacerItem, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont



class DeleteStaffScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Staff")
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Delete Staff")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Search Bar
        search_layout = QVBoxLayout()
        self.cnic_input = QLineEdit()
        self.cnic_input.setPlaceholderText("Enter CNIC")
        self.cnic_input.setStyleSheet("font-size: 16px; padding: 10px;")
        search_layout.addWidget(QLabel("Search Staff by CNIC:"))
        search_layout.addWidget(self.cnic_input)

        search_button = QPushButton("Search")
        search_button.setFont(QFont("Arial", 14))
        search_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px; border-radius: 5px;")
        search_button.clicked.connect(self.search_staff)
        search_layout.addWidget(search_button)

        main_layout.addLayout(search_layout)

        # Frame for displaying staff details
        details_frame = QFrame()
        details_frame.setStyleSheet("border: 2px solid #333333; padding: 20px;")
        details_layout = QGridLayout(details_frame)
        details_layout.setContentsMargins(20, 20, 20, 20)
        details_layout.setVerticalSpacing(10)

        # Spacer to push details content towards the top
        top_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        details_layout.addItem(top_spacer, 0, 0, 1, 2)

        # Staff details label
        self.staff_details_label = QLabel("Staff Details:")
        self.staff_details_label.setStyleSheet("font-size: 16px; color: #333333; font-weight: bold;")
        details_layout.addWidget(self.staff_details_label, 1, 0, 1, 2)

        # Details display
        self.staff_details = QLabel("")
        self.staff_details.setStyleSheet("font-size: 16px; color: #555555;")
        self.staff_details.setWordWrap(True)
        details_layout.addWidget(self.staff_details, 2, 0, 1, 2)

        # Spacer to push details content towards the bottom
        bottom_spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        details_layout.addItem(bottom_spacer, 3, 0, 1, 2)

        main_layout.addWidget(details_frame)

        # Delete Button
        delete_button = QPushButton("Delete Staff")
        delete_button.setFont(QFont("Arial", 14, QFont.Bold))
        delete_button.setStyleSheet("background-color: #FF4C4C; color: white; padding: 10px; border-radius: 5px;")
        delete_button.clicked.connect(self.delete_staff)
        main_layout.addWidget(delete_button, alignment=Qt.AlignCenter)

        # Set the main layout
        self.setLayout(main_layout)

    def search_staff(self):
        # Fetch staff details using CNIC
        cnic = self.cnic_input.text().strip()  # Strip any leading/trailing whitespace
        # if cnic:
        #     # Use the backend logic to search for the staff member
        #     from ReceptionBackend import search_staff_by_cnic  # Ensure this is correctly
        #     staff = search_staff_by_cnic(cnic)
        #     if staff:
        #         # Assuming `staff` is a tuple with columns matching the TblStaff table
        #         self.staff_details.setText(
        #             f"Details for CNIC: {cnic}\n"
        #             f"Name: {staff[1]} {staff[2]}\n"
        #             f"DOB: {staff[3]}\n"
        #             f"Gender: {staff[4]}\n"
        #             f"Contact: {staff[5]}\n"
        #             f"Email: {staff[6]}\n"
        #             f"Address: {staff[7]}\n"
        #             f"Date Joined: {staff[8]}"
        #         )
        #     else:
        #         self.staff_details.setText("No details found for the provided CNIC.")
        # else:
        #     self.staff_details.setText("Please enter a valid CNIC.")

    def delete_staff(self):
        # Delete staff logic
        cnic = self.cnic_input.text()
        if cnic:
            # Call the backend function to delete the staff member
            if delete_staff_by_cnic(cnic):
                self.staff_details.setText(f"Staff member with CNIC {cnic} deleted successfully.")
            else:
                self.staff_details.setText(f"Failed to delete staff member with CNIC {cnic}.")
        else:
            self.show_message("Error", "No CNIC provided. Unable to delete.", QMessageBox.Critical)

    def show_message(self, title, message, icon):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.exec_()
