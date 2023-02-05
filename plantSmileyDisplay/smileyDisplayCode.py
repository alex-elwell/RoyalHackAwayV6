import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6 import QtWidgets, QtCore
# Import necessary features of QtWidgets from the PyQt6 library
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton, QTabWidget, QGridLayout, QVBoxLayout
from PyQt6.QtWidgets import QToolBar, QStatusBar, QDialog, QProgressBar
from PyQt6.QtGui import QImage, QAction, QIcon, QPixmap
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.x = 0 # Will be used to identify button input
        self.setWindowTitle("Plant Display")
        layout = QVBoxLayout()
        self.testWaterValue = 0
        self.setStyleSheet("background-color: green;")

        # Creates the toolbar
        toolbar = QToolBar("Toolbar Test")
        toolbar.setIconSize(QSize(100,100))
        '''
        toolbar.setOrientation(QtCore.Qt.Vertical)
        self.addToolBar(QtCore.Qt.RightToolBarArea,toolbar)
        '''

        # Button created in the toolbar
        leafButton = QAction(QIcon("leafButton.png"),"Plant Status Button", self)
        self.setCentralWidget(self.defaultSmiley())
        leafButton.triggered.connect(self.buttonSwitch)
        toolbar.addAction(leafButton)

        # Shows the purpose of the button
        leafButton.setStatusTip("Show Plant Moisture Status")
        self.setStatusBar(QStatusBar(self))

    def buttonSwitch(self, labelval):
        # If statements check what the label is

        if self.x == 2:
            print("2")
            self.defaultSmiley()
        elif self.x == 1:
            print("1")
            self.plantStatusWindow()
        else:
            print("Error")

    def defaultSmiley(self):
        layout = QVBoxLayout()
        # Creates a label with the smiley faces on it
        self.x = 1
        label = QLabel(self)
        widget = QWidget()
        smiley = QPixmap("calmBaseFace.png") # Calm smiley is default smiley

        # These water values will be moisture data that are used in the progress bars
        # Will need to be changed to compare values from API
        self.testWaterValue += 1
        if self.testWaterValue < 30:
            smiley = QPixmap("scaredFace.png")
        elif self.testWaterValue > 75:
            smiley = QPixmap("happyFace.png")
        label.setPixmap(smiley)
        layout.addWidget(label)
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()
        return label



    # Status section will be visible to the user to see the stats of the plant
    def plantStatusWindow(self):
        layout = QVBoxLayout()
        self.x = 2
        print("click")
        widget = QWidget(self)

        #Creating progress bars for each plant
        # Plant 1
        pbar = QProgressBar(self)
        pbar.setValue(50) # Value can be set based on the moisture input
        layout.addWidget(pbar)

        # Plant 2
        pbar2 = QProgressBar(self)
        pbar2.setValue(20)  # Value can be set based on the moisture input
        layout.addWidget(pbar2)

        # Plant 3
        pbar3 = QProgressBar(self)
        pbar3.setValue(75)  # Value can be set based on the moisture input
        layout.addWidget(pbar3)

        #widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    #widget = QtWidgets.QStackedWidget()
    window = MainWindow()

    window.show()
    #window.showMaximized()
    sys.exit(app.exec())



