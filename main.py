from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout
from PySide6.QtCore import QSize
import sys 

from canvas import Canvas
from scenes.scene import BisectorScene, NetworkScene

class MainWindow(QMainWindow): 

    def __init__(self): 
        super().__init__()

        self.window_size = QSize(1280, 700)

        self.setWindowTitle("Network playground")
        self.setMinimumSize(self.window_size)

        self.canvas = BisectorScene(self.window_size, draw_axis=True)
        self.setCentralWidget(self.canvas)
        layout = QHBoxLayout(self.canvas)
        self.setLayout(layout)

        self.canvas.render()

    def update(self): 
        self.canvas()

def create_window() -> QMainWindow: 
    return MainWindow()

def main(): 
    app = QApplication(sys.argv)
    
    window = create_window()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__": 
    main()
