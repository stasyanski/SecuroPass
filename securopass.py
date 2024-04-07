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

from cryptography.fernet import Fernet
from json import JSONDecodeError
from PySide6.QtCore import Qt
from PySide6 import QtGui

import os
import sys
import json
import random


# --- CONSTANTS ---
WINDOW_SIZE             = (490, 400)
DIALOG_SIZE             = (260, 160)                                               
MAX_PASS_LEN            = 48
PHRASE_MAX_LEN          = 32                                                     
DEFAULT_PASS_LEN        = 16
SCROLLAREA_WIDTH        = 175
PASSWORD_DIALOG_SIZE    = (260, 50) 
DEFAULT_CHECKBOX_STATE  = True                                            

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
        self.top.addWidget(Text("Welcome to SecuroPass, free-and-open-source software to generate and manage your passwords.", align=Qt.AlignCenter, wrap=True))

        # --- Left add widgets - the left panel of the gui ---
        self.left.addWidget(Text("SecuroGen Password Generator:", align=Qt.AlignLeft, wrap=False))

        self.checkbox_uppercase = Checkbox("Use upper case letters")          # Create an instance of the Checkbox class and assign it to self.checkbox_uppercase
        self.left.addWidget(self.checkbox_uppercase)                          # Add the self.checkbox_uppercase to the left panel of the gui

        self.checkbox_symbols = Checkbox("Use symbols $, #, / etc.")             
        self.left.addWidget(self.checkbox_symbols)                            

        self.checkbox_numbers = Checkbox("Use numbers")                       
        self.left.addWidget(self.checkbox_numbers)                            

        # --- Password length realtime value ---
        self.slider_text = Text(f"Password Length:  {self.pref.length}", align=Qt.AlignLeft, wrap=False)        # Set the text of the slider and assign it to self.slider_text
        self.left.addWidget(self.slider_text)                                   # Add the slider text to the left panel 

        # --- Password length slider ---
        self.slider = (Slider())                                                # Create an instance of the Slider class
        self.left.addWidget(self.slider)                                        # Add the slider to the left panel  
    
        # --- User information about phrase in password --- 
        self.left.addWidget(Text("Include this phrase in my password:", align=Qt.AlignLeft, wrap=False))
        self.input_phrase = Input("Enter a phrase here...", readonly=False, max_len=PHRASE_MAX_LEN)                    
        self.left.addWidget(self.input_phrase)
        self.left.addWidget(Text("Max 32 characters, spaces not allowed.", align=Qt.AlignLeft, wrap=False))

        # --- Bottomleft add widgets - the bottom left panel of the gui ---
        self.gen_button = Button("Generate Password")                          
        self.bottom_left.addWidget(self.gen_button)
        self.password_label = Input("Password will appear here...", readonly=True, max_len=MAX_PASS_LEN)
        self.bottom_left.addWidget(self.password_label)

        # --- Right add widgets - the right panel of the gui ---
        self.right.addWidget(Text("SecuroVault Saved Passwords:", align=Qt.AlignLeft, wrap=False))

        self.scroll_area = ScrollArea()
        self.right.addWidget(self.scroll_area)

        self.add_password = (Button("Add a password to SecuroVault"))
        self.right.addWidget(self.add_password)
    
    
    

    # --- Signals and slots ---
    def setup_signals(self):
        self.input_phrase.textChanged.connect(self.sanitize_input)

        self.checkbox_uppercase.stateChanged.connect(self.update_uppercase)     # Connect the checkbox_uppercase to the update_uppercase function, acting as a signal
        self.checkbox_symbols.stateChanged.connect(self.update_symbols)         
        self.checkbox_numbers.stateChanged.connect(self.update_numbers)
        self.slider.valueChanged.connect(self.update_length)                    # Connect the slider to the update_length function, acting as a signal
        self.input_phrase.textChanged.connect(self.update_phrase)
        self.gen_button.clicked.connect(self.generate_password)
        self.add_password.clicked.connect(self.dialog.exec)                     # Executes dialog window class on press
        self.dialog.save_password.clicked.connect(lambda: self.securo_pass.encrypt_to_json(self.dialog.input_user.text(), self.dialog.input_pass.text()))                                                                            # Pass user and password to encrypt and store in json                   
        self.dialog.save_password.clicked.connect(self.dialog.close)                    # Close the dialog window after saving the password
        self.dialog.save_password.clicked.connect(self.scroll_area.new_json_data)       # Update the scroll area with the new password
    
    # --- Updates ---
    def sanitize_input(self):
        self.current_text = self.input_phrase.text()
        self.sanitized_text = self.current_text.replace(" ", "")    # Replace spaces with nothing, not allow to store password with space
        self.input_phrase.setText(self.sanitized_text)   

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
    def __init__(self, text):
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
    def __init__(self, text, align, wrap):    # Align the text to the left (default value), unless a value is specified 
        super(Text, self).__init__()
        
        self.setText(text)                             
        self.setAlignment(align)  
        self.setWordWrap(wrap)                          # Wrap the text if it exceeds the width of the label                          

class Input(QLineEdit):                                         
    def __init__(self, text, readonly, max_len):
        super(Input, self).__init__()
        
        self.setPlaceholderText(text)                       
        self.setReadOnly(readonly)                          # Password will be printed here so it is read only
        self.setMaxLength(max_len)                   


    """
    from PySide6.QtGui import ( 
        QKeySequence,
        QKeyEvent,
        )
    """
    
    """
    def keyPressEvent(self, event: QKeyEvent) -> None:          # Function to return none input if key event is key space
        if self.space_allowed==False:
            if event.key() == Qt.Key_Space:
                return
            if event.matches(QKeySequence.Paste):               # Return none if key sequence is ctrl+v
                return
        super(Input,self).keyPressEvent(event)
    """
    
    """
    def dropEvent(self, event):
        if self.context_menu == False:
            return
        super(Input, self).dropEvent(event)

    def dragEnterEvent(self, event):
        if self.context_menu == False:                            No longer used context menu code
            return
        super(Input, self).dragEnterEvent(event)
        
    def contextMenuEvent(self, event):
        if self.context_menu == False:
            return
        super(Input, self).contextMenuEvent(event)
    """

class Button(QPushButton):
    def __init__(self, text):
        super(Button, self).__init__()

        self.setText(text)                                          # Set the text of the button (retrieve text from keyword argument)
        
class ScrollArea(QScrollArea):
    def __init__(self):
        super(ScrollArea, self).__init__()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Set the vertical scrollbar policy to be always visible

        self.scroll_widget = QWidget()                         
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)

        self.load_json_data()

        self.setWidget(self.scroll_widget)

    def load_json_data(self):
        try:
            with open('sp.json', 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}

        buttonList = []
        x=0
        for item in data:
            button = QPushButton(item)
            button.setFixedWidth(SCROLLAREA_WIDTH)
            buttonList.append(('Button'+str(x), button))
            self.scroll_layout.addWidget(button)
            x+=1

        """
        for button_name, button in buttonList:
            button.clicked.connect(self.)
        """
        

    def new_json_data(self):
        self.scroll_widget.deleteLater()
        self.scroll_widget = QWidget()                         
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)

        self.load_json_data()
        
        self.setWidget(self.scroll_widget)

class Dialog(QDialog):
    def sanitize_input(self):
        self.current_text = self.input_pass.text()
        self.sanitized_text = self.current_text.replace(" ", "")    # Replace spaces with nothing, not allow to store password with space
        self.input_pass.setText(self.sanitized_text)
    
    def __init__(self):
        super(Dialog, self).__init__()

        self.setWindowTitle("Add a password")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.setFixedSize(*DIALOG_SIZE)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        
        self.layout.addWidget(Text("What's this password linked to?", align=Qt.AlignLeft, wrap=False))
        self.input_user = Input("Username, website, service...", readonly=False, max_len=PHRASE_MAX_LEN)
        self.layout.addWidget(self.input_user)

        self.layout.addWidget(Text("Add a password to SecuroVault:", align=Qt.AlignLeft, wrap=False))
        self.input_pass = Input("Enter a password here...", readonly=False, max_len=MAX_PASS_LEN)
        self.input_pass.textChanged.connect(self.sanitize_input)
        self.layout.addWidget(self.input_pass)

        self.save_password = Button("Add Password")
        self.layout.addWidget(self.save_password)

class PasswordDialog(QDialog):
    def __init__(self):
        super(PasswordDialog, self).__init__()

        self.setWindowTitle("Show Password")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.setFixedSize(*PASSWORD_DIALOG_SIZE)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.show_password = Input("Password will appear here...", readonly=True, max_len=MAX_PASS_LEN)
        self.layout.addWidget(self.show_password)





# --- SecuroPass logic ---

class SecuroPass():
    def __init__(self, pref):
        self.pref = pref
        self.banks = {
            'uppercase': "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz",
            'lowercase': "aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz",
            'symbols': "!@#$%^&*()_+-=[]{}|;:,.<>?/!@#$%^&*()_+-=[]{}|;:,.<>?/",
            'numbers': "012345678901234567890123456789"
        }
        self.key = None
        self.cipher_suite = None

    def generate_password(self):
        if self.pref.uppercase is True:
            self.bank = self.banks['uppercase']
        else:
            self.bank = self.banks['lowercase']

        if self.pref.symbols is True:
            self.bank += self.banks['symbols']

        if self.pref.numbers is True:
            self.bank += self.banks['numbers']

        password = "".join(random.sample(self.bank, self.pref.length))

        if self.pref.phrase:
            password = self.pref.phrase + '_' + password
            password = password[0:self.pref.length]
        return password

    def encrypt_to_json(self, user, password: str) -> None:
        self.key = Fernet.generate_key()
        os.environ[user] = self.key.decode()
        self.cipher = Fernet(self.key)
        
        encrypted_password = self.cipher.encrypt(password.encode()).decode()

        try:
            with open('sp.json', 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            data = {}

        data[user] = encrypted_password

        with open('sp.json', 'w') as f:
            json.dump(data, f)

    def decrypt_from_json(self, user) -> str:
        self.key = os.environ.get(user).encode()
        self.cipher = Fernet(self.key)

        with open('sp.json', 'r') as f:
            data = json.load(f)
            encrypted_password = data.get(user)
        
        if encrypted_password:
            password = self.cipher.decrypt(encrypted_password.encode()).decode()
            return password
        else:
            return None
    
    def delete_from_json(self, user) -> None:
        pass





# --- Mainloop ---

if __name__ == "__main__":
    app = QApplication(sys.argv)                            # Create an application object, an instance of the QApplication class, QApplication manages the GUI application, sys.argv is needed as it is a Python list containing the command line args passed to the app, ensures proper functionality               
    window = MainWindow()                                   # Create an instance of the MainWindow class (the main window of the application, as the class defines it at the top of the script)           
    window.show()                                           # Makes the main window visible        
    app.exec()                                              # Start the pyside event loop, infinite loop which waits for user input