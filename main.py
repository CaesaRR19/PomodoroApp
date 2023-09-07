"""El sys es usado para que el programa funcione correctamente.
"""
import sys

# pylint: disable=E0611
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QFormLayout,
    QProgressBar,
)
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QTimer
from pygame import init, mixer, time


class MainWindow(QWidget):
    """Clase principal de la aplicación Pomodoro.
    Esta clase representa la ventana principal de la aplicación Pomodoro.
    Proporciona una interfaz gráfica de usuario para gestionar las sesiones de trabajo y descanso.

    Args:
        *args: Argumentos posicionales adicionales.
        **kwargs: Argumentos de palabras clave adicionales.

    Attributes:
        timer (QTimer): Un temporizador utilizado para controlar el tiempo de trabajo y descanso.
        current_value (int): Valor actual de la barra de progreso.
        change_event (bool): Indica si la aplicación está en estado de trabajo o descanso.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QTimer(self)
        self.setFixedSize(200, 140)
        self.setWindowTitle("PAPP")

        # Icono del programa:
        self.setWindowIcon(QtGui.QIcon("assets\\pomodoro.ico"))

        # Layout:
        layout = QFormLayout()
        self.setLayout(layout)

        # Titulo del window:
        label_title = QLabel("Pomodoro", self)
        label_title.setStyleSheet(
            """
                                font-family: Arial;
                                font-size: 18px;
                            """
        )
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(label_title)

        # Titulo de estado, nos dice si es hora de descansar o trabajar.
        self.label_state = QLabel("", self)
        self.label_state.setStyleSheet(
            """
                                font-family: Arial;
                                font-size: 14px;
                            """
        )
        self.label_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addRow(self.label_state)

        # Barra de progreso:
        self.pbar = QProgressBar(self)
        self.pbar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_value = 0
        layout.addRow(self.pbar)

        # Botón de inicio:
        self.button_start = QPushButton("Start", self)

        # Botón de parar:
        self.button_stop = QPushButton("Stop", self)
        self.button_stop.setEnabled(False)

        layout.addRow(self.button_start, self.button_stop)

        # Credito
        label_credits = QLabel("Made by César Ramos <3", self)
        label_credits.setStyleSheet(
            """
                                font-family: Arial;
                                font-size: 10px;
                            """
        )
        layout.addRow(label_credits)

        self.button_start.clicked.connect(self.start_pomodoro)
        self.button_stop.clicked.connect(self.stop_pomodoro)
        # self.timer.start()
        self.change_event = True

        self.show()

    def start_pomodoro(self):
        """Inicia el pomodoro, y se debe ejecutar cada 15 segundos."""
        self.button_stop.setEnabled(True)
        self.change_event = True
        self.timer.setInterval(150)
        self.label_state.setText("Work Time!")
        self.button_start.setEnabled(False)
        try:
            self.timer.timeout.disconnect(self.start_pbar)
        except TypeError as error:
            print("Error: ", error)
        finally:
            self.timer.timeout.connect(self.start_pbar)
            self.timer.start()

    def start_pbar(self):
        """Agrega el conteo de la barra de progreso, va intercambiando entre start_rest
        y start_pomodoro
        """
        if self.current_value < 100:
            self.current_value += 1
            self.pbar.setValue(self.current_value)
        else:
            self.pbar.reset()
            self.current_value = 0
            self.play_sound()
            self.timer.stop()
            if self.change_event:
                self.start_rest()
            else:
                self.start_pomodoro()

    def start_rest(self):
        """Inicia el modo de descanso, se ejecuta cada tres segundos."""
        self.change_event = not self.change_event
        self.timer.setInterval(30)
        self.label_state.setText("Rest Time!")
        self.timer.timeout.disconnect(self.start_pbar)
        self.timer.timeout.connect(self.start_pbar)
        self.timer.start()

    def stop_pomodoro(self):
        """Detiene tanto el modo de trabajo, como el modo de descanso.
        Es como si abrieramos la aplicación de nuevo.
        """
        self.timer.stop()
        try:
            self.timer.timeout.disconnect(self.start_pbar)
            self.timer.timeout.disconnect(self.start_pomodoro)
            self.timer.timeout.disconnect(self.start_rest)
        except TypeError:
            self.button_stop.setEnabled(False)
            self.button_start.setEnabled(True)
            self.current_value = 0
            self.pbar.reset()

    def play_sound(self):
        """Genera un sonido de campana. Detiene el programa por un segundo."""
        init()
        mixer.init()
        sound = mixer.Sound("assets\\bell.wav")
        sound.play()
        time.delay(int(sound.get_length() * 500))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())
