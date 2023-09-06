import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QFormLayout,
    QProgressBar,
)
from PyQt6.QtCore import Qt, QTimer


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QTimer(self)
        self.setGeometry(608, 334, 150, 100)
        self.setWindowTitle("PomodoroApp")

        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.label_title = QLabel("Pomodoro", self)
        self.label_title.setStyleSheet(
            """
                                font-family: Arial;
                                font-size: 18px;
                            """
        )
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addRow(self.label_title)

        self.label_state = QLabel("", self)
        self.label_state.setStyleSheet(
            """
                                font-family: Arial;
                                font-size: 14px;
                            """
        )
        self.label_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addRow(self.label_state)

        self.pbar = QProgressBar(self)
        self.pbar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_value = 0
        self.layout.addRow(self.pbar)

        self.button_start = QPushButton("Start", self)
        self.button_stop = QPushButton("Stop", self)
        self.button_stop.setEnabled(False)

        self.layout.addRow(self.button_start, self.button_stop)

        self.button_start.clicked.connect(self.start_pomodoro)
        self.timer.start()

        self.show()

    def start_pomodoro(self):
        self.label_state.setText("Work Time!")
        self.button_start.setEnabled(False)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.grow_pbar)
        self.timer.start()

    def grow_pbar(self):
        if self.current_value < self.pbar.maximum():
            self.current_value += 1
            self.pbar.setValue(self.current_value)
        elif self.current_value == 100:
            self.current_value = 0
            self.pbar.reset()
            self.timer.stop()
            self.start_rest()

    def start_rest(self):
        self.label_state.setText("Rest Time!")
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.grow_pbar)
        self.timer.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # create the main window
    window = MainWindow()

    # start the event loop
    sys.exit(app.exec())
