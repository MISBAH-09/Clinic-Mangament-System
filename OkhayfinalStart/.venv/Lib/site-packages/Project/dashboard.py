import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QScrollArea, QFrame, QSizePolicy, QPushButton
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from DatabaseConnection import DatabaseConnection


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection.get_connection()
        self.setWindowTitle("Clinical Management System Dashboard")
        self.setGeometry(100, 100, 1200, 500)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.add_title()

        # Refresh Button
        self.add_refresh_button()

        # Scrollable area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content.setMinimumSize(1200, 1200)  # Ensure content size is larger than the window

        # Grid layout for scrollable content
        self.scroll_layout = QGridLayout()
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_content.setLayout(self.scroll_layout)

        # Add widgets to the scroll layout
        self.add_dashboard_widgets()

        # Set scrollable content
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

    def add_title(self):
        """Add a styled title to the dashboard."""
        title = QLabel("Clinical Management Dashboard", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: #333333; margin: 20px; text-decoration: underline;"
        )
        self.main_layout.addWidget(title)

    def add_refresh_button(self):
        """Add a refresh button to update dashboard data."""
        refresh_button = QPushButton("Refresh Dashboard")
        refresh_button.setStyleSheet(
            "padding: 10px 20px; font-size: 16px; font-weight: bold; background-color: #4CAF50; color: white; border: none; border-radius: 5px;"
        )
        refresh_button.clicked.connect(self.refresh_dashboard)
        refresh_button.setCursor(Qt.PointingHandCursor)
        self.main_layout.addWidget(refresh_button)

    def add_dashboard_widgets(self):
        """Add widgets to the dashboard using a grid layout."""
        # Clear existing layout
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add updated widgets
        widgets = [
            self.create_text_display("Total Patients", self.fetch_total_patients()),
            self.create_text_display("Total Doctors", self.fetch_total_doctors()),
            self.create_text_display("Total Staff", self.fetch_total_staff()),
            self.create_text_display("Average Daily Visits", self.fetch_average_daily_visits()),
            self.create_bar_chart("Monthly Income", self.fetch_monthly_income()),
            self.create_pie_chart("Gender Distribution", self.fetch_gender_distribution()),
            self.create_bar_chart("Visits of the Week", self.fetch_total_visits_of_week())
        ]

        for i, widget in enumerate(widgets[:-1]):  # Add all widgets except "Visits of the Week"
            row, col = divmod(i, 2)  # 2 columns
            self.scroll_layout.addWidget(widget, row, col)

        # Add "Visits of the Week" widget spanning two columns
        visits_of_week_widget = widgets[-1]  # Last widget
        visits_of_week_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.scroll_layout.addWidget(visits_of_week_widget, len(widgets) // 2, 0, 1, 2)  # Span two columns

        # Set column stretch to balance space
        self.scroll_layout.setColumnStretch(0, 1)
        self.scroll_layout.setColumnStretch(1, 1)

    def refresh_dashboard(self):
        """Refresh the dashboard by reloading data and updating widgets."""
        self.add_dashboard_widgets()

    def create_text_display(self, title, value):
        """Create a text display widget with styling."""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("background-color: #f9f9f9; border: 1px solid #dcdcdc; border-radius: 10px;")
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #555555;")
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: green;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return frame

    def create_pie_chart(self, title, data):
        """Create a pie chart using Matplotlib."""
        fig, ax = plt.subplots()
        if not data:
            data = {'No Data': 100}
        labels, values = data.keys(), data.values()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title(title)

        canvas = FigureCanvas(fig)
        plt.close(fig)  # Close the figure to free up memory
        return self.wrap_chart_in_frame(canvas)

    def create_bar_chart(self, title, data):
        """Create a bar chart using Matplotlib."""
        fig, ax = plt.subplots()
        if not data:
            data = {'No Data': 0}
        labels, values = data.keys(), data.values()
        ax.bar(labels, values, color="#87CEEB")
        ax.set_title(title)
        ax.set_ylabel("Count")

        canvas = FigureCanvas(fig)
        plt.close(fig)  # Close the figure to free up memory
        return self.wrap_chart_in_frame(canvas)

    def wrap_chart_in_frame(self, canvas):
        """Wrap Matplotlib canvas in a styled QFrame."""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("border: 1px solid #dcdcdc; border-radius: 10px; background-color: #ffffff;")
        layout = QVBoxLayout(frame)
        layout.addWidget(canvas)
        return frame

    # Fetching Data Functions (same as provided)
    def fetch_total_patients(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM TblPatients")
        result = cursor.fetchone()
        return str(result[0] if result else 0)

    def fetch_total_doctors(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM TblDoctors")
        result = cursor.fetchone()
        return str(result[0] if result else 0)

    def fetch_total_staff(self):
        cursor = self.db.cursor()
        query = """
            SELECT COUNT(*)
            FROM TblCredentials C
            JOIN TblRoles R ON C.RoleID = R.RoleID
            WHERE R.RoleName IN ('Admin', 'Receptionist')
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return str(result[0] if result else 0)

    def fetch_gender_distribution(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT Gender, COUNT(*) FROM TblPatients GROUP BY Gender")
        data = cursor.fetchall()
        return {row[0]: row[1] for row in data}

    def fetch_monthly_income(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT TOP 4 SalaryID, Amount FROM TblSalary ORDER BY SalaryID DESC")
        data = cursor.fetchall()
        return {f"Month {i+1}": row[1] for i, row in enumerate(data)}

    def fetch_average_daily_visits(self):
        cursor = self.db.cursor()
        query = """
            SELECT AVG(daily_visits) 
            FROM (SELECT COUNT(*) AS daily_visits 
                  FROM TblVisits 
                  GROUP BY VisitDate) AS daily_counts
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return str(int(result[0]) if result and result[0] else 0)

    def fetch_total_visits_of_week(self):
        cursor = self.db.cursor()
        query = """
            SELECT VisitDate, COUNT(*) AS visit_count
            FROM TblVisits
            WHERE VisitDate >= DATEADD(DAY, -7, GETDATE())
            GROUP BY VisitDate
            ORDER BY VisitDate;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        return {row[0].strftime("%Y-%m-%d"): row[1] for row in data}


# Uncomment to run
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = DashboardWindow()
#     window.show()
#     sys.exit(app.exec_())
