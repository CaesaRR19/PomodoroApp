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
from pygame import init, mixer, time


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QTimer(self)
        self.setGeometry(608, 334, 150, 100)
        self.setWindowTitle("PomodoroApp")
        init()
        mixer.init()
        self.sound = mixer.Sound("assets\\bell.wav")
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
        self.change_event = True
        self.disconnect_pomodoro = False
        self.show()

    def start_pomodoro(self):
        self.change_event = True
        self.timer.setInterval(500)
        self.label_state.setText("Work Time!")
        self.button_start.setEnabled(False)
        if self.disconnect_pomodoro:
            self.timer.timeout.disconnect(self.start_pbar)
        self.timer.timeout.connect(self.start_pbar)
        self.timer.start()

    def start_pbar(self):
        if self.current_value < 100:
            self.current_value += 1
            self.pbar.setValue(self.current_value)
        else:
            self.sound.play()
            time.delay(int(self.sound.get_length() * 500))
            self.pbar.reset()
            self.current_value = 0
            self.timer.stop()
            if self.change_event:
                self.start_rest()
            else:
                self.start_pomodoro()

    def start_rest(self):
        self.change_event = not self.change_event
        self.disconnect_pomodoro = True
        self.timer.setInterval(100)
        self.label_state.setText("Rest Time!")
        self.timer.timeout.disconnect(self.start_pbar)
        self.timer.timeout.connect(self.start_pbar)
        self.timer.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())
