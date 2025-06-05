import sys
from PyQt5.QtWidgets import QApplication # type: ignore
from mainwindow import Ui_MainWindow  # type: ignore # Import the main window

def main():
    app = QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
