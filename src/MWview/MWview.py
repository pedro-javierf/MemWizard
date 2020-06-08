#!/usr/bin/python

import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon, QKeySequence, QStandardItemModel, QColor
from PySide2.QtCore import Slot, Qt

@Slot()
def say_hello():
    print("Button clicked, Hello!")

class MainWindow(QMainWindow):
    def __init__(self, MWengine, parent=None):
        super(MainWindow, self).__init__()
        self.engine = MWengine
        self.setWindowTitle("Memory Wizard")

        self.form_widget = FormWidget(self,self.engine) 
        self.setCentralWidget(self.form_widget) #if uncommented the status bar disapears
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(" MemWizard started.")

        #Toolbar options
        fileMenu = self.menuBar().addMenu("File")

        openAction = QAction('Open', self)
        openAction.triggered.connect(self.loadFileDialog)
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        optionMenu = self.menuBar().addMenu("Export")

        defineAction = QAction('Export as DEFINE .h file', self)
        otherAction = QAction('Export as payload (binary) [TODO]', self)
        optionMenu.addAction(defineAction)
        optionMenu.addAction(otherAction)

        otherMenu = self.menuBar().addMenu("Other")

        themeAction = QAction('Switch Theme', self)
        otherMenu.addAction(themeAction)
        

        #to add other submenus: http://zetcode.com/gui/pyqt5/menustoolbars/

    @Slot()
    def loadFileDialog(self):
        fname = QFileDialog.getOpenFileName(self)
        self.engine.loadFile(fname)


class FormWidget(QWidget):

    def __init__(self, parent,MWengine):        
        super(FormWidget, self).__init__(parent)

        #top layer containing the buttons layer(s) + the console layer
        self.topLayout = QVBoxLayout(self)

        #second layer layout containing the vertical ones
        self.layer2Layout = QHBoxLayout(self)
        self.consoleLayout = QHBoxLayout(self) #the type of layout doesn't matter as it's only going to have 1 component

        #Layout for the components in the left or the right
        self.leftLayout = QVBoxLayout(self)
        self.rightLayout = QVBoxLayout(self)

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

        self.splitter1 = QSplitter(Qt.Horizontal)

        self.cb1 = QCheckBox("Set base address?")
        self.cb1.stateChanged.connect(self.toggleBaseBox)
        self.baseValue = QLineEdit()
        self.baseValue.setEnabled(False)

        self.archLabel = QLabel("Architecture")
        self.listWidget = QComboBox() 
        self.listWidget.insertSeparator(-1) #separator in all the entries 
        
        self.analButton = QPushButton("Run Analysis")
        #self.analButton.setCheckable(True)
        self.analButton.clicked.connect(self.analysis)
        

        self.rightLayout.addWidget(self.otherLabel)
        self.rightLayout.addWidget(self.splitter1)
        self.rightLayout.addWidget(self.cb1)
        self.rightLayout.addWidget(self.baseValue)
        self.rightLayout.addWidget(self.archLabel)
        self.rightLayout.addWidget(self.listWidget)
        self.rightLayout.addWidget(self.analButton)

        ###################################################
        ######### console #################################
        ###################################################
        
        console = QTextEdit()
        console.setStyleSheet("background-color: rgb(0, 44, 66);")
        console.setTextColor(QColor(255, 255, 255))
        console.setText("MW Console")
        self.consoleLayout.addWidget(console)

        #Register the left&right layouts in the top one
        self.layer2Layout.addLayout(self.leftLayout)
        self.rightLayout.setAlignment(Qt.AlignTop)
        self.layer2Layout.addLayout(self.rightLayout)

        #elements
        self.topLayout.addLayout(self.layer2Layout)

        #console
        self.topLayout.addLayout(self.consoleLayout)

        #The final window layout is the top one
        self.setLayout(self.topLayout)

    @Slot()
    def analysis(self):
        print("analysis")

    @Slot()
    def toggleBaseBox(self,state):
        if state > 0:
            self.baseValue.setEnabled(True)
        else:
            self.baseValue.setEnabled(False)

class MemWizardGUI:
    def __init__(self, engine):
        # Create the Qt Application
        app = QApplication(sys.argv)
        # Create and show the form
        form = MainWindow(engine)
        form.show()
        # Run the main Qt loop
        sys.exit(app.exec_())

    