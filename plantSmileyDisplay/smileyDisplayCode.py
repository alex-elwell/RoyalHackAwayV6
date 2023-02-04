import sys
from PyQt6.QtCore import Qt, QSize

# Import necessary features of QtWidgets from the PyQt6 library
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton, QTabWidget, QGridLayout, QVBoxLayout
from PyQt6.QtWidgets import QToolBar, QStatusBar
from PyQt6.QtGui import QImage, QAction, QIcon, QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My Awesome App")


        # Creates the toolbar
        toolbar = QToolBar("Toolbar Test")
        toolbar.setIconSize(QSize(100,100))
        #toolbar.setOrientation(Qt.vertical)
        self.addToolBar(toolbar)

        # Button created in the toolbar
        leafButton = QAction(QIcon("leafButton.png"),"Plant Status Button", self)
        leafButton.triggered.connect(self.plantStatusWindow)
        toolbar.addAction(leafButton)

        # Shows the purpose of the button
        leafButton.setStatusTip("Show Plant Moisture Status")
        self.setStatusBar(QStatusBar(self))

        # Creates a label with the smiley faces on it
        label = QLabel(self)
        smiley = QPixmap("calmBaseFace.png") # Calm smiley is default smiley
        label.setPixmap(smiley)
        self.setCentralWidget(label)


    # Status section will be visible to the user to see the stats of the plant
    def plantStatusWindow(self, s):
        print("click", s)


app = QApplication(sys.argv)

window = MainWindow()
window.show()
window.showMaximized()
sys.exit(app.exec())



