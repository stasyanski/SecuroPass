# Main.py includes the required GUI code

# --- Importing the required modules ---

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

# --- MainWindow and layouts ---

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SecuroPass")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.setFixedSize(490, 390)                                     # Hardcoded size of the window, slightly poor practice however, it is a simple, small, lightweight application, and according to survey, most computers have a minimum res of 640px

        top = QHBoxLayout()
        left = QVBoxLayout()
        bottomleft = QVBoxLayout()
        right = QVBoxLayout()

        top.setContentsMargins(10, 10, 10, 10)                          # Set the margins of the layout
        left.setContentsMargins(10, 10, 10, 10)                         # Set the margins of the layout
        bottomleft.setContentsMargins(10, 10, 10, 10)                   # Set the margins of the layout
        right.setContentsMargins(10, 10, 10, 10)                        # Set the margins of the layout

        grid = QGridLayout()
        grid.addLayout(top, 0, 0, 1, 2)                                 # Where 1 is rowspan and 2 is columnspan 
        grid.addLayout(left, 1, 0)                                      # Where 1 is row and 0 is column          
        grid.addLayout(bottomleft, 2, 0)                                # Where 2 is row and 0 is column
        grid.addLayout(right, 1, 1, 2, 1)                               # Where 2 is rowspan and 1 is columnspan         

        widget = QWidget()                                              # Setting a central widget, acting as a container / parent for everything else (like a frame in tkinter)
        widget.setLayout(grid)
        self.setCentralWidget(widget)                                   # Set the central widget of the window, assigning the central widget as parent       

        # Top add widgets - the greeting text
        top.addWidget(Text("Hi (user), Welcome to SecuroPass", align=Qt.AlignCenter))

        # Left add widgets - the left panel of the gui
        left.addWidget(Text("SecuroGen Password Generator:"))
        left.addWidget(Checkbox("Use upper case letters"))
        left.addWidget(Checkbox("Use symbols ($, #, /)"))                
        left.addWidget(Checkbox("Use numbers"))
        left.addWidget(Text("Password Length:"))
        left.addWidget(Slider())
        left.addWidget(Text("Include this phrase in my password:\n(When including a phrase, the password generated will include that phrase.)"))
        left.addWidget(Input("Enter a phrase here..."))

        # Bottomleft add widgets - the bottom left panel of the gui
        bottomleft.addWidget(Button("Generate Password"))
        bottomleft.addWidget(Input("Password will appear here...", readonly=True))

        # Right add widgets - the right panel of the gui
        right.addWidget(Text("SecuroVault Saved Passwords:"))
        right.addWidget(ScrollArea())
        right.addWidget(Button("Add a password to SecuroVault"))

# --- Other widgets ---

class Checkbox(QCheckBox):
    def __init__(self, text="Text"):
        super(Checkbox, self).__init__()

        self.setText(text)                                  # Set the text of the checkbox
        self.setChecked(True)                               # Set the checkbox as checked by default

class Slider(QSlider):
    def __init__(self):
        super(Slider, self).__init__()

        self.setMinimum(1)
        self.setMaximum(256)                                # Maximum value of a password is 256
        self.setSliderPosition(16)                          # Default value of the slider
        self.setOrientation(Qt.Horizontal)                  # Set the slider

class Text(QLabel):
    def __init__(self, text="Text", align=Qt.AlignLeft):    # Align the text to the left (default value), unless a value is specified 
        super(Text, self).__init__()
        
        self.setText(text)
        self.setWordWrap(True)                              # Set the text to wrap
        self.setAlignment(align)                            # Align the text to the center (horizontally and vertically

class Input(QLineEdit):
    def __init__(self, text="Text", readonly=False):
        super(Input, self).__init__()
        
        self.setPlaceholderText(text)                       # Set placeholder text
        self.setReadOnly(readonly)                          # Set the input as read-only (password will be printed here)

class Button(QPushButton):
    def __init__(self, text="Button"):
        super(Button, self).__init__()

        self.setText(text)                                  # Set the text of the button (retrieve text from keyword argument)

class ScrollArea(QScrollArea):
    def __init__(self):
        super(ScrollArea, self).__init__()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)       # Set the vertical scrollbar policy


# --- Mainloop ---

if __name__ == "__main__":
    app = QApplication(sys.argv)                            # Create an application object, an instance of the QApplication class, QApplication manages the GUI application, sys.argv is needed as it is a Python list containing the command line args passed to the app, ensures proper functionality               
    window = MainWindow()                                   # Create an instance of the MainWindow class (the main window of the application, as the class defines it at the top of the script)           
    window.show()                                           # Makes the main window visible        
    app.exec()                                              # Start the pyside event loop, infinite loop which waits for user input