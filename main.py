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
    QScrollArea,
    QPushButton,
    )

from PySide6 import QtGui
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SecuroPass")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

        top = QHBoxLayout()
        left = QVBoxLayout()
        bottomleft = QVBoxLayout()
        right = QVBoxLayout()

        top.setContentsMargins(10, 10, 10, 10)                   # Set the margins of the layout
        left.setContentsMargins(10, 10, 10, 10)                   # Set the margins of the layout
        bottomleft.setContentsMargins(10, 10, 10, 10)                   # Set the margins of the layout
        right.setContentsMargins(10, 10, 10, 10)                   # Set the margins of the layout

        grid = QGridLayout()
        grid.addLayout(top, 0, 0, 1, 2)                       # Where 1 is rowspan and 2 is columnspan 
        grid.addLayout(left, 1, 0)
        grid.addLayout(bottomleft, 2, 0)
        grid.addLayout(right, 1, 1, 2, 1)                     # Where 2 is rowspan and 1 is columnspan         

        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)

        top.addWidget(Text("Hi (user), Welcome to SecuroPass"))

        left.addWidget(Checkbox("Use upper case letters"))
        left.addWidget(Checkbox("Use symbols ($, #, /)"))                
        left.addWidget(Checkbox("Use numbers"))
        left.addWidget(Text("Password Length:"))
        left.addWidget(Slider())
        left.addWidget(Text("Include this phrase in my password:\n(When including a phrase, the password generated will include that phrase.)"))
        left.addWidget(Input("Enter a phrase here..."))

        bottomleft.addWidget(Button("Generate Password"))
        bottomleft.addWidget(Input("Password will appear here...",readonly=True))

        right.addWidget(Text("Your saved passwords:"))
        right.addWidget(ScrollArea())
        right.addWidget(Button("Add a password to SecuroVault"))

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
        self.setWordWrap(True)                      # Set the text to wrap

class Input(QLineEdit):
    def __init__(self, text="Text", readonly=False):
        super(Input, self).__init__()
        
        self.setPlaceholderText(text)  # Set placeholder text
        self.setReadOnly(readonly)     # Set the input as read-only

class Button(QPushButton):
    def __init__(self, text="Button"):
        super(Button, self).__init__()

        self.setText(text)                          # Set the text of the button

class ScrollArea(QScrollArea):
    def __init__(self):
        super(ScrollArea, self).__init__()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Set the vertical scrollbar policy
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Set the horizontal scrollbar policy


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()