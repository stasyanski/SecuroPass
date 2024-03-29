# securopass.py includes the gui and the logic of the application

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

# --- CONSTANTS ---
WINDOW_SIZE = (490, 400)                                               
MAX_PASS_LEN = 48                                                      
DEFAULT_PASS_LEN = 16                                                  

# --- Preferences values ---
class Preferences:                                                     # Class to store the user preferences, rather than using global variables, much better practice
    def __init__(self):
        self.uppercase = True
        self.symbols = True
        self.numbers = True
        self.length = DEFAULT_PASS_LEN
        self.phrase = None
pref = Preferences()

# --- MainWindow, layout and all widgets ---
class MainWindow(QMainWindow):

    def __init__(self, pref):
        super(MainWindow, self).__init__()
        
        self.pref = pref                                                # Assign the pref to self.pref, otherwise it would be a local variable and not accessible outside of the __init__ function

        self.setWindowTitle("SecuroPass")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.setFixedSize(*WINDOW_SIZE)                                 # Hardcoded size of the window, * unpacks the tuple

        self.setup_layouts()
        self.setup_widgets()
        self.setup_signals()

    def setup_layouts(self):
        self.top = QHBoxLayout()
        self.left = QVBoxLayout()
        self.bottom_left = QVBoxLayout()
        self.right = QVBoxLayout()

        self.top.setContentsMargins(10, 10, 10, 10)                          # Set the margins of the layout
        self.left.setContentsMargins(10, 10, 10, 10)                         
        self.bottom_left.setContentsMargins(10, 10, 10, 10)                   
        self.right.setContentsMargins(10, 10, 10, 10)                        

        self.grid = QGridLayout()
        self.grid.addLayout(self.top, 0, 0, 1, 2)                                 # Where 1 is rowspan and 2 is columnspan 
        self.grid.addLayout(self.left, 1, 0)                                      # Where 1 is row and 0 is column          
        self.grid.addLayout(self.bottom_left, 2, 0)                               # Where 2 is row and 0 is column
        self.grid.addLayout(self.right, 1, 1, 2, 1)                               # Where 2 is rowspan and 1 is columnspan         

        self.widget = QWidget()                                              # Setting a central widget, acting as a container / parent for everything else (like a frame in tkinter)
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)                                   # Set the central widget of the window, assigning the central widget as parent       

    def setup_widgets(self):
        # --- Top add widgets - the greeting text ---
        self.top.addWidget(Text("Hi (user), welcome to SecuroPass, free-and-open-source software to generate and manage your passwords.", align=Qt.AlignCenter))

        # --- Left add widgets - the left panel of the gui ---
        self.left.addWidget(Text("SecuroGen Password Generator:"))
        self.left.addWidget(Checkbox("Use upper case letters"))
        self.left.addWidget(Checkbox("Use symbols ($, #, /)"))                
        self.left.addWidget(Checkbox("Use numbers"))

        # --- Password length realtime value ---
        self.slider_text = Text((f"Password Length:  {self.pref.length}"))      # Set the text of the slider and assign it to self.slider_text
        self.left.addWidget(self.slider_text)                                   # Add the slider text to the left panel 

        # --- Password length slider ---
        self.slider = Slider()                                                  # Create an instance of the Slider class
        self.left.addWidget(self.slider)                                        # Add the slider to the left panel  
    
        # --- User information about phrase in password --- 
        self.left.addWidget(Text("Include this phrase in my password:\n(When including a phrase, the password generated will include that phrase.)"))
        self.left.addWidget(Input("Enter a phrase here..."))

        # --- Bottomleft add widgets - the bottom left panel of the gui ---
        self.bottom_left.addWidget(Button("Generate Password"))
        self.bottom_left.addWidget(Input("Password will appear here...", readonly=True))

        # --- Right add widgets - the right panel of the gui ---
        self.right.addWidget(Text("SecuroVault Saved Passwords:"))
        self.right.addWidget(ScrollArea())
        self.right.addWidget(Button("Add a password to SecuroVault"))
    
    def setup_signals(self):
        self.slider.valueChanged.connect(self.update_length)                    # Connect the slider to the update_length function, acting as a signal
    
    # --- Signals and slots ---
    def update_length(self):
        self.pref.length = self.slider.value()
        self.slider_text.setText(f"Password Length:  {self.pref.length}")

# --- Other widgets ---

class Checkbox(QCheckBox):
    def __init__(self, text="Text"):
        super(Checkbox, self).__init__()

        self.setText(text)                                  
        self.setChecked(True)                               

class Slider(QSlider):
    def __init__(self):
        super(Slider, self).__init__()
        
        self.setMinimum(1)
        self.setMaximum(MAX_PASS_LEN)                       # Maximum value of a password is constant
        self.setSliderPosition(DEFAULT_PASS_LEN)            # Default value of the slider
        self.setOrientation(Qt.Horizontal)                  # Set the slider

class Text(QLabel):
    def __init__(self, text="Text", align=Qt.AlignLeft):    # Align the text to the left (default value), unless a value is specified 
        super(Text, self).__init__()
        
        self.setText(text)
        self.setWordWrap(True)                              
        self.setAlignment(align)                            

class Input(QLineEdit):
    def __init__(self, text="Text", readonly=False):
        super(Input, self).__init__()
        
        self.setPlaceholderText(text)                       
        self.setReadOnly(readonly)                          # Password will be printed here so it is read only

class Button(QPushButton):
    def __init__(self, text="Button"):
        super(Button, self).__init__()

        self.setText(text)                                  # Set the text of the button (retrieve text from keyword argument)

class ScrollArea(QScrollArea):
    def __init__(self):
        super(ScrollArea, self).__init__()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)       # Set the vertical scrollbar policy to be always visible


# --- Mainloop ---

if __name__ == "__main__":
    app = QApplication(sys.argv)                            # Create an application object, an instance of the QApplication class, QApplication manages the GUI application, sys.argv is needed as it is a Python list containing the command line args passed to the app, ensures proper functionality               
    window = MainWindow(pref)                               # Create an instance of the MainWindow class (the main window of the application, as the class defines it at the top of the script)           
    window.show()                                           # Makes the main window visible        
    app.exec()                                              # Start the pyside event loop, infinite loop which waits for user input