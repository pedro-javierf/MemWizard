#!/usr/bin/python

import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon, QKeySequence, QStandardItemModel, QColor
from PySide2.QtCore import Slot, Qt, QAbstractTableModel, QModelIndex

AVAILABLE_ARCHS = ['ARM', 'ARM64', 'x86','x86-64','PPC','MIPS']

#https://doc.qt.io/qtforpython/tutorials/datavisualize/add_tableview.html
class CustomTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.load_data(data)
        self.base_addr = 0

    def load_data(self, data): #data is a list(or dictionary) of lists
        self.input_addresses = data[0]
        self.input_gadgetdesc = data[1]
        self.input_others    = data[2]

        self.column_count = 3
        self.row_count = len(self.input_addresses)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("ADDRESS", "GADGET", "MODE")[section]
        else:
            return "{}".format(section)

    #displays data at index
    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        #Actual data display/dispatcher
        if role == Qt.DisplayRole and row>=0:
            if column == 0:
                columnVals = self.input_addresses[row]
                return columnVals
            elif column == 1:
                columnVals = self.input_gadgetdesc[row]
                return columnVals
            elif column == 2:
                columnVals = self.input_others[row]
                return columnVals

        elif role == Qt.BackgroundRole:
            return QColor(Qt.white) #background color

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None

    #Update the whole set of data
    #UNUSED (yet)
    def setData(self, newData):
        self.load_data(newData)

    def applyBaseToDataset(self, base_addr):
        self.base_addr=base_addr
        for i in self.input_addresses:
            i = str(int(i,0) + int(base_addr))

    def removeBaseAddr(self):
        for i in self.input_addresses:
            i = str(int(i,0) - int(self.base_addr))

class MainWindow(QMainWindow):
    def __init__(self, MWengine, parent=None):
        super(MainWindow, self).__init__()
        self.setFixedSize(780, 580)

        self.engine = MWengine
        self.binLoaded = False
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
        self.binLoaded = self.engine.loadFile(fname)


class FormWidget(QWidget):

    def __init__(self, parent, MWengine):        
        super(FormWidget, self).__init__(parent)
        self.parent = parent
        self.engine = MWengine

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

        # Getting the Model
        self.ROPmodel = CustomTableModel(MWengine.getROPData())
        # Set the view's model
        self.tableROP = QTableView()
        self.tableROP.setModel(self.ROPmodel)
        # Configure sizes
        header = self.tableROP.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch) 
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        self.tableROP.resizeRowsToContents()
        #h2 = self.tableROP.verticalHeader()
        #h2.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        #h2.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        #h2.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.leftLayout.addWidget(self.tableROP)

        #JOP content
        #JOP text
        self.jopLabel = QLabel("JOP Gadgets")
        self.leftLayout.addWidget(self.jopLabel)

        self.JOPmodel = CustomTableModel(MWengine.getJOPData())

        self.tableJOP = QTableView()
        self.tableJOP.setModel(self.JOPmodel)
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
        self.baseValue.setText("0") #default value
        self.baseValue.setEnabled(False)

        self.archLabel = QLabel("Architecture")
        self.listWidget = QComboBox()
        self.listWidget.addItems(AVAILABLE_ARCHS)
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
        if(self.parent.binLoaded):
            print("[>] Analysis: "+self.getChosenArch())
            self.engine.runAnalysis()

            #reset model to force view update
            #there is a better way using model.setData()
            self.ROPmodel = CustomTableModel(self.engine.getROPData())
            self.tableROP.setModel(self.ROPmodel)

            #adjust size of the cells
            self.tableROP.resizeRowsToContents()

        else:
            print("[!] Load a binary first!")

    @Slot()
    def toggleBaseBox(self,state):
        if state > 0:
            self.baseValue.setEnabled(True)
            self.ROPmodel.applyBaseToDataset(int(self.baseValue.text()))
        else:
            self.baseValue.setEnabled(False)

    def getChosenArch(self):
        return str(self.listWidget.currentText()) #returns one of the available archs

class MemWizardGUI:
    def __init__(self, engine):
        # Create the Qt Application
        app = QApplication(sys.argv)
        # Create and show the form
        form = MainWindow(engine)
        form.show()
        # Run the main Qt loop
        sys.exit(app.exec_())

    