#gui recode

import sys

from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QGridLayout, 
    QCheckBox,
    QSlider,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    )

from PySide6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SecuroPass")

        top = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()

        grid = QGridLayout()
        grid.addLayout(top, 0, 0)
        grid.addLayout(left, 1, 0)
        grid.addLayout(right, 1, 1)

        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)

        top.setContentsMargins(10, 10, 10, 10)                   # Set the margins of the layout
        left.setContentsMargins(10, 10, 10, 10)                   # Set the margins of the layout
        right.setContentsMargins(10, 10, 10, 10)                   # Set the margins of the layout

        top.addWidget(Text("Hi (user), Welcome to SecuroPass"))

        left.addWidget(Checkbox("Use upper case letters"))
        left.addWidget(Checkbox("Use symbols ($, #, /)"))                
        left.addWidget(Checkbox("Use numbers"))
        left.addWidget(Text("Password Length:"))
        left.addWidget(Slider())
        left.addWidget(Text("Include this in my password:\n(When including a phrase, the password generated will include that phrase.)"))
        left.addWidget(Input())

        right.addWidget(Text("Your password will appear here"))

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

class Text(QLabel):
    def __init__(self, text="Text"):
        super(Text, self).__init__()
        
        self.setText(text)
        self.setWordWrap(True)

class Input(QLineEdit):
    def __init__(self):
        super(Input, self).__init__()
        
        self.setPlaceholderText("Type here...")  # Set placeholder text


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()