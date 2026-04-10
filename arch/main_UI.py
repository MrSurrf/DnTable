from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDockWidget
from design import Ui_MainWindow

class MapTerminal(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.resize(720,1280)
        self.setFixedSize(720,1280)

        # Запретить табы между доками
        self.setDockOptions(
            QMainWindow.DockOption.AnimatedDocks           
        )


def main():
    app = QApplication()
    window = MapTerminal()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()