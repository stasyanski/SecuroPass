import sys

from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QGridLayout, 
    QCheckBox,
    QSlider,
    QLabel,
    QSizePolicy
    )

from PySide6.QtCore import QSize, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SecuroPass")
        self.setFixedSize(QSize(700,500))

        widget = QWidget()                                          # Create a central widget
        widget.setFixedWidth(350)
        self.setCentralWidget(widget)                               # Set the widget as the central widget of the main window

        layout = QGridLayout(widget)                                # Set the layout to the widget
        layout.setContentsMargins(10, 10, 10, 10)                   # Set the margins of the layout

        layout.addWidget(Checkbox("Use upper case letters"), 0, 0)
        layout.addWidget(Checkbox("Use symbols ($, #, /)"), 1, 0)   # Where 0,0 1,0 are the row and column, using grid layout                
        layout.addWidget(Checkbox("Use numbers"), 2, 0)

        layout.addWidget(Text("Password Length"), 3, 0)

        layout.addWidget(Slider(), 4, 0)


class Checkbox(QCheckBox):
    def __init__(self, text="Text"):
        super(Checkbox, self).__init__()

        self.setText(text)                          # Set the text of the checkbox
        self.setChecked(True)                       # Set the checkbox as checked

class Slider(QSlider):
    def __init__(self):
        super(Slider, self).__init__()

        self.setMinimum(1)
        self.setMaximum(256)                        # Maximum value of a password is 256
        self.setSliderPosition(16)
        self.setOrientation(Qt.Horizontal)          # Set the slider
        self.setFixedWidth(330)

class Text(QLabel):
    def __init__(self, text="Text"):
        super(Text, self).__init__()
        self.setText(text)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # By default QLabel will expand to fill the available space, set size policy sets width and height to a fixed size, acting like a normal widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()