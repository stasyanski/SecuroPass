# securopass.py includes the gui and the logic of the application

# --- Importing the required modules ---

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGridLayout,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QWidget,
    QSlider,
    QDialog,
    QLabel,
    )

from PySide6.QtGui import ( 
    QKeySequence,
    QKeyEvent,
    )

from PySide6.QtCore import Qt
from PySide6 import QtGui
import sys

import random


# --- CONSTANTS ---
WINDOW_SIZE             = (490, 400)
DIALOG_SIZE             = (250, 90)                                               
MAX_PASS_LEN            = 48                                                      
DEFAULT_PASS_LEN        = 16
DEFAULT_CHECKBOX_STATE  = True
PHRASE_MAX_LEN          = 32                                                  

# --- Preferences values ---
class Preferences:                                                     # Class to store the user preferences, rather than using global variables, much better practice
    def __init__(self):
        self.uppercase  = DEFAULT_CHECKBOX_STATE
        self.symbols    = DEFAULT_CHECKBOX_STATE
        self.numbers    = DEFAULT_CHECKBOX_STATE
        self.length     = DEFAULT_PASS_LEN
        self.phrase     = None

# --- MainWindow, layout and all widgets ---
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.pref = Preferences()                                            # Assign the pref to self.pref, otherwise it would be a local variable and not accessible outside of the __init__ function
        self.securo_pass = SecuroPass(self.pref)                             # Create an instance of the SecuroPass class and assign it to self.securo_pass
        self.dialog = Dialog()                                               # Create an instance of the Dialog class and assign it to self.dialog

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

        self.checkbox_uppercase = Checkbox("Use upper case letters")          # Create an instance of the Checkbox class and assign it to self.checkbox_uppercase
        self.left.addWidget(self.checkbox_uppercase)                          # Add the self.checkbox_uppercase to the left panel of the gui

        self.checkbox_symbols = Checkbox("Use symbols $, #, / etc.")             
        self.left.addWidget(self.checkbox_symbols)                            

        self.checkbox_numbers = Checkbox("Use numbers")                       
        self.left.addWidget(self.checkbox_numbers)                            

        # --- Password length realtime value ---
        self.slider_text = Text(f"Password Length:  {self.pref.length}")        # Set the text of the slider and assign it to self.slider_text
        self.left.addWidget(self.slider_text)                                   # Add the slider text to the left panel 

        # --- Password length slider ---
        self.slider = (Slider())                                                # Create an instance of the Slider class
        self.left.addWidget(self.slider)                                        # Add the slider to the left panel  
    
        # --- User information about phrase in password --- 
        self.left.addWidget(Text("Include this phrase in my password:"))
        self.input_phrase = (Input("Enter a phrase here..."))                     
        self.left.addWidget(self.input_phrase)
        self.left.addWidget(Text("Max 32 characters, spaces not allowed."))

        # --- Bottomleft add widgets - the bottom left panel of the gui ---
        self.gen_button = (Button("Generate Password"))                          
        self.bottom_left.addWidget(self.gen_button)
        self.password_label = (Input("Password will appear here...", readonly=True, context_menu=False))
        self.bottom_left.addWidget(self.password_label)

        # --- Right add widgets - the right panel of the gui ---
        self.right.addWidget(Text("SecuroVault Saved Passwords:"))
        self.right.addWidget(ScrollArea())

        self.add_password = (Button("Add a password to SecuroVault"))
        self.right.addWidget(self.add_password)
    
    
    
    # --- Signals and slots ---
    def setup_signals(self):
        self.checkbox_uppercase.stateChanged.connect(self.update_uppercase)     # Connect the checkbox_uppercase to the update_uppercase function, acting as a signal
        self.checkbox_symbols.stateChanged.connect(self.update_symbols)         
        self.checkbox_numbers.stateChanged.connect(self.update_numbers)
        self.slider.valueChanged.connect(self.update_length)                    # Connect the slider to the update_length function, acting as a signal
        self.input_phrase.textChanged.connect(self.update_phrase)
        self.gen_button.clicked.connect(self.generate_password)
        self.add_password.clicked.connect(self.dialog.exec)                     # Executes dialog window class on press                
    
    # --- Updates ---
    def update_uppercase(self):
        self.pref.uppercase = self.checkbox_uppercase.isChecked()               # Update the uppercase preference to the state of the checkbox

    def update_symbols(self):
        self.pref.symbols = self.checkbox_symbols.isChecked()

    def update_numbers(self):
        self.pref.numbers = self.checkbox_numbers.isChecked()
    
    def update_length(self):
        self.pref.length = self.slider.value()
        self.slider_text.setText(f"Password Length:  {self.pref.length}")       # Update the text of the slider to reflect the user's choice

    def update_phrase(self):
        self.pref.phrase =  self.input_phrase.text()

    def generate_password(self):
        password = self.securo_pass.generate_password()
        self.password_label.setText(password)    




# --- Other widgets ---

class Checkbox(QCheckBox):
    def __init__(self, text="Text"):
        super(Checkbox, self).__init__()

        self.setText(text)                                  
        self.setChecked(DEFAULT_CHECKBOX_STATE)                               

class Slider(QSlider):
    def __init__(self):
        super(Slider, self).__init__()
        
        self.setMinimum(1)
        self.setMaximum(MAX_PASS_LEN)                       
        self.setSliderPosition(DEFAULT_PASS_LEN)            
        self.setOrientation(Qt.Horizontal)                  

class Text(QLabel):
    def __init__(self, text="Text", align=Qt.AlignLeft):    # Align the text to the left (default value), unless a value is specified 
        super(Text, self).__init__()
        
        self.setText(text)
        self.setWordWrap(True)                              
        self.setAlignment(align)                            

class Input(QLineEdit):                                     
    def __init__(self, text="Text", readonly=False, context_menu=True):
        super(Input, self).__init__()
        
        self.setPlaceholderText(text)                       
        self.setReadOnly(readonly)                          # Password will be printed here so it is read only
        self.setMaxLength(PHRASE_MAX_LEN)                   
        self.context_menu = context_menu                    
    
    def keyPressEvent(self, event: QKeyEvent) -> None:      # Function to return none input if key event is key space
        if event.key() == Qt.Key_Space:
            return
        if event.matches(QKeySequence.Paste):               # Return none if key sequence is ctrl+v
            return
        super(Input,self).keyPressEvent(event)

    def dropEvent(self, event):
        if self.context_menu == True:
            return
        super(Input, self).dropEvent(event)

    def dragEnterEvent(self, event):
        if self.context_menu == True:
            return
        super(Input, self).dragEnterEvent(event)
        
    def contextMenuEvent(self, event):
        if self.context_menu == True:
            return
        super(Input, self).contextMenuEvent(event)

class Button(QPushButton):
    def __init__(self, text="Button"):
        super(Button, self).__init__()

        self.setText(text)                                          # Set the text of the button (retrieve text from keyword argument)

class ScrollArea(QScrollArea):
    def __init__(self):
        super(ScrollArea, self).__init__()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)       # Set the vertical scrollbar policy to be always visible

class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()

        self.setWindowTitle("Add a password")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.input = Input("Username, website, service...")
        self.layout.addWidget(self.input)

        self.input = Input("Enter a password here...")
        self.layout.addWidget(self.input)

        self.add_button = Button("Add Password")
        self.layout.addWidget(self.add_button)




# --- SecuroPass logic ---

class SecuroPass:
    def __init__(self, pref):
        self.pref = pref
        self.banks = {
            'uppercase': "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz",
            'lowercase': "aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz",
            'symbols': "!@#$%^&*()_+-=[]{}|;:,.<>?/!@#$%^&*()_+-=[]{}|;:,.<>?/",
            'numbers': "012345678901234567890123456789"
        }

    def generate_password(self):
        if self.pref.uppercase is True:
            self.bank = self.banks['uppercase']
        else:
            self.bank = self.banks['lowercase']

        if self.pref.symbols is True:
            self.bank += self.banks['symbols']

        if self.pref.numbers is True:
            self.bank += self.banks['numbers']

        password = "".join(random.sample(self.bank, self.pref.length))           # random.sample returns a list of unique elements from the bank, join together to form and return a string

        if self.pref.phrase:
            password = self.pref.phrase + '_' + password                    # Concatenate phrase with password, use _ to separate them visually
            password = password[0:self.pref.length]                         # Respect the user preferred length
        return password
        

    def save_password(self):
        pass

    def load_passwords(self):
        pass

    def add_password(self):
        pass


# --- Mainloop ---

if __name__ == "__main__":
    app = QApplication(sys.argv)                            # Create an application object, an instance of the QApplication class, QApplication manages the GUI application, sys.argv is needed as it is a Python list containing the command line args passed to the app, ensures proper functionality               
    window = MainWindow()                                   # Create an instance of the MainWindow class (the main window of the application, as the class defines it at the top of the script)           
    window.show()                                           # Makes the main window visible        
    app.exec()                                              # Start the pyside event loop, infinite loop which waits for user input