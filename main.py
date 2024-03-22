import sys

from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QGridLayout, 
    QCheckBox,
    QSlider,
    QLabel,
    QSizePolicy,
    QLineEdit,
    )

from PySide6.QtCore import QSize, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SecuroPass")
        self.setFixedSize(QSize(700,500))

        window = QWidget()                                          # Create a central widget
        window.setFixedWidth(350)
        self.setCentralWidget(window)                               # Set the widget as the central widget of the main window

        layout = QGridLayout(window)                                # Set the layout to the window
        layout.setContentsMargins(10, 10, 10, 10)                   # Set the margins of the layout

        layout.addWidget(TopAside(), 0, 0)
        layout.addWidget(LeftAside(), 1, 0)
        layout.addWidget(RightAside(), 1, 1)



class TopAside(QWidget):
    def __init__(self):
        super(TopAside, self).__init__()

        TopAside_layout = QGridLayout(self)

        TopAside_layout.addWidget(Text("Hi (user), Welcome to SecuroPass"), 0, 0)
        self.setStyleSheet (("QWidget{background: rgb(50, 50, 50); color: white;}"))       # Set the background color and text color of the text

class LeftAside(QWidget):
    def __init__(self):
        super(LeftAside, self).__init__()

        self.setFixedSize(QSize(400,300))

        LeftAside_layout = QGridLayout(self)

        LeftAside_layout.addWidget(Checkbox("Use upper case letters"), 0, 0)
        LeftAside_layout.addWidget(Checkbox("Use symbols ($, #, /)"), 1, 0)                
        LeftAside_layout.addWidget(Checkbox("Use numbers"), 2, 0)

        LeftAside_layout.addWidget(Text("Password Length:"), 3, 0)

        LeftAside_layout.addWidget(Slider(), 4, 0)

        LeftAside_layout.addWidget(Text("Include this in my password:\n(When including a phrase, the password generated will include that phrase.)"), 5, 0)

        LeftAside_layout.addWidget(Input(), 6, 0)

        self.setStyleSheet (("QWidget{background: rgb(50, 50, 50); color: white;}"))       # Set the background color and text color of the text

class RightAside(QWidget):
    def __init__(self):
        super(RightAside, self).__init__()

        self.setFixedSize(QSize(400,400))

        RightAside_layout = QGridLayout(self)

        RightAside_layout.addWidget(Text("Your password will appear here"), 0, 0)





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