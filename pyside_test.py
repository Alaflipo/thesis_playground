from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt, QSize
import sys 

window_titles = [
    "My App",
    "My App",
    "Still My App",
    "Still My App",
    "What on earth",
    "What on earth",
    "This is surprising",
    "This is surprising",
    "Something went wrong",
]

class MouseEventWindow(QMainWindow): 
    def __init__(self): 
        super().__init__()
        self.setMouseTracking(True)
        self.label = QLabel("Click in this label")
        self.label.setMouseTracking(True)
        self.setCentralWidget(self.label)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            # handle the left-button press in here
            self.label.setText("mousePressEvent LEFT")

        elif e.button() == Qt.MouseButton.MiddleButton:
            # handle the middle-button press in here.
            self.label.setText("mousePressEvent MIDDLE")

        elif e.button() == Qt.MouseButton.RightButton:
            # handle the right-button press in here.
            self.label.setText("mousePressEvent RIGHT")

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("mouseReleaseEvent LEFT")

        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("mouseReleaseEvent MIDDLE")

        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("mouseReleaseEvent RIGHT")

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("mouseDoubleClickEvent LEFT")

        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("mouseDoubleClickEvent MIDDLE")

        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("mouseDoubleClickEvent RIGHT")

class TestWindow(QMainWindow): 

    def __init__(self):
        super().__init__()
        self.setWindowTitle(window_titles[0])

        self.button_is_checked = False 
        self.amount_clicked = 0 

        self.setFixedSize(QSize(400,300))

        # button!
        self.button = QPushButton('Push me please!')
        self.button.clicked.connect(self.button_click)

        # window!
        self.windowTitleChanged.connect(self.window_title_changed)

        # label! 
        self.label = QLabel()

        # line edit! 
        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        # put it all in one layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
    
    def button_click(self): 
        print("button was clicked!")
        self.amount_clicked += 1
        self.setWindowTitle(window_titles[self.amount_clicked])

    def window_title_changed(self, windowname): 
        print(f"New window title: {windowname}")

        if windowname == window_titles[len(window_titles) - 1]: 
            self.button.setEnabled(False)

    def was_button_toggled(self, checked): 
        self.button_is_checked = checked
        print("Button checked?", self.button_is_checked)


def main():
    app = QApplication(sys.argv)
    window_select = 0
    if (len(sys.argv) > 1): 
        window_select = int(sys.argv[1])

    windows = [TestWindow(), MouseEventWindow()]
    windows[window_select].show()

    app.exec()

if __name__ == "__main__": 
    main()

