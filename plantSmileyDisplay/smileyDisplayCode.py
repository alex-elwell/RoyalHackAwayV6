import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6 import QtWidgets, QtCore
# Import necessary features of QtWidgets from the PyQt6 library
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton, QTabWidget, QGridLayout, QVBoxLayout
from PyQt6.QtWidgets import QToolBar, QStatusBar, QDialog, QProgressBar
from PyQt6.QtGui import QImage, QAction, QIcon, QPixmap
import time

# Allows for APIs to be imported into the program
import requests
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.current_moisture = None
        self.current_moisture
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
        '''
        self.addToolBar(toolbar)


        # Button created in the toolbar
        leafButton = QAction(QIcon("leafButton.png"),"Plant Status Button", self)
        self.setCentralWidget(self.defaultSmiley())
        leafButton.triggered.connect(self.buttonSwitch)
        toolbar.addAction(leafButton)

        # Shows the purpose of the button
        leafButton.setStatusTip("Show Plant Moisture Status")
        self.setStatusBar(QStatusBar(self))


    def dataRetrieve(self):
        # Gets the url of the API
        response = requests.get("https://63df75c7a76cfd410582cf50.mockapi.io/api/v1/plants/1/sensor_measurements")
        print(response.status_code)
        print(response.json())

        # Checks if the connection to the API is successful
        if response.status_code == 200:
            data = response.text
            if 'moisture' in data:
                print(response.json()[0]['moisture'])
                moistureList = []
                moistureList.clear()
                # print(len(response.json()))
                # Adds all of the moisture values to a list
                for i in range(0, len(response.json())):
                    moistureList.append(response.json()[i]['moisture'])

                self.current_moisture = moistureList[len(moistureList) - 1]

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

        # The current Moisture used will be used to create necessary smiley face
        self.dataRetrieve()

        layout = QVBoxLayout()
        # Creates a label with the smiley faces on it
        self.x = 1
        label = QLabel(self)
        widget = QWidget()
        smiley = QPixmap("calmBaseFace.png") # Calm smiley is default smiley
        # These water values will be moisture data that are used in the progress bars
        if self.current_moisture < 30:
            smiley = QPixmap("scaredFace.png")
        elif self.current_moisture > 75:
            smiley = QPixmap("happyFace.png")
        else:
            smiley = QPixmap("calmBaseFace.png")
        label.setPixmap(smiley)
        layout.addWidget(label)
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()
        return label



    # Status section will be visible to the user to see the stats of the plant
    def plantStatusWindow(self):
        # The current Moisture used will be used to create necessary smiley face
        self.dataRetrieve()

        layout = QVBoxLayout()
        self.x = 2
        print("click")
        widget = QWidget(self)

        #Creating progress bars for each plant
        # Plant 1 - Only one used as only one moisture record obtained from API
        pbar = QProgressBar(self)
        pbar.setValue(self.current_moisture) # Value can be set based on the moisture input
        layout.addWidget(pbar)

        # Plant 2
        pbar2 = QProgressBar(self)
        pbar2.setValue(0)  # Value can be set based on the moisture input
        layout.addWidget(pbar2)

        # Plant 3
        pbar3 = QProgressBar(self)
        pbar3.setValue(0)  # Value can be set based on the moisture input
        layout.addWidget(pbar3)

        #widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()



if __name__ == "__main__":

    # Calls API data retrieve method
    app = QApplication(sys.argv)
    #widget = QtWidgets.QStackedWidget()
    window = MainWindow()

    window.show()
    #window.showMaximized()
    sys.exit(app.exec())



