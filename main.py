import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFormLayout, QProgressBar
from PyQt6.QtCore import *


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(608,334,150,100)
        self.setWindowTitle("PomodoroApp")
        
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        
        label = QLabel("Pomodoro", self)
        label.setStyleSheet("""
                                font-family: Arial;
                                font-size: 18px;
                            """)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addRow(label)
        
        barra = QProgressBar(self)
        barra.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout. addRow(barra)
        
        button = QPushButton("Iniciar", self)

        self.layout.addRow(button)
        
        
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # create the main window
    window = MainWindow()

    # start the event loop
    sys.exit(app.exec())
