#!/usr/bin/python

import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon, QKeySequence, QStandardItemModel
from PySide2.QtCore import Slot

@Slot()
def say_hello():
    print("Button clicked, Hello!")

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Memory Wizard")

        self.form_widget = FormWidget(self) 
        self.setCentralWidget(self.form_widget) 
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(" MemWizard started.")

        #tb = self.addToolBar("File")

        #Create Toolbar
        #toolBar = QToolBar()
        #self.addToolBar(toolBar)

        #Toolbar options
        fileMenu = self.menuBar().addMenu("File")
        optionMenu = self.menuBar().addMenu("Options")


class FormWidget(QWidget):

    def __init__(self, parent):        
        super(FormWidget, self).__init__(parent)

        #Top layout containing the other two
        self.topLayout = QHBoxLayout(self)

        #Layout for the components in the left or the right
        self.leftLayout = QVBoxLayout(self)
        self.rightLayout = QGridLayout(self)

        self.rightLayout.setSpacing(0)
        self.rightLayout.setContentsMargins(0,0,0,0)

        ###################################################
        ############ components on the left ###############
        ###################################################
        #ROP content
        #ROP text
        self.ropLabel = QLabel("ROP Gadgets")
        self.leftLayout.addWidget(self.ropLabel)
        #Rop Table
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['addr', 'mnemonic', 'mode'])
        self.tableROP = QTableView()
        self.tableROP.setModel(model)

        self.leftLayout.addWidget(self.tableROP)

        self.tableROP.doubleClicked.connect(self.on_click)

        #JOP content
        #JOP text
        self.jopLabel = QLabel("JOP Gadgets")
        self.leftLayout.addWidget(self.jopLabel)

        self.tableJOP = QTableView()
        self.tableJOP.setModel(model)
        self.leftLayout.addWidget(self.tableJOP)

        '''https://doc.qt.io/qtforpython/tutorials/datavisualize/add_tableview.html'''

        ###################################################
        ############ components on the right ##############
        ###################################################

        self.otherLabel = QLabel("Other Options:")

        self.cb1 = QCheckBox("Set base address?")
        self.baseValue = QLineEdit()

        self.archLabel = QLabel("Architecture")
        self.listWidget = QComboBox() 
        
        self.rightLayout.addWidget(self.otherLabel,0,0)
        self.rightLayout.addWidget(self.cb1,1,0)
        self.rightLayout.addWidget(self.baseValue,2,0)
        self.rightLayout.addWidget(self.archLabel,3,0)
        self.rightLayout.addWidget(self.listWidget,4,0)

        ###################################################

        #Register the left&right layouts in the top one
        self.topLayout.addLayout(self.leftLayout)
        self.topLayout.addLayout(self.rightLayout)

        #The final window layout is the top one
        self.setLayout(self.topLayout)

    @Slot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

class MemWizardGUI:
    def __init__(self):
        # Create the Qt Application
        app = QApplication(sys.argv)
        # Create and show the form
        form = MainWindow()
        form.show()
        # Run the main Qt loop
        sys.exit(app.exec_())

    