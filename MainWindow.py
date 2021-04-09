import sys

import xlsxwriter
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime, QTimer, Qt, QSettings, QCoreApplication, QObject
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox, QLabel, QToolBar, QTabWidget, \
    QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QAbstractItemView, QFileDialog, QApplication

import TableSaver
from AddEmployee import WindowEmployeeAdd
from UpdateEmployee import WindowEmployeeUpdate
from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setObjectName("ManageEmployeeObject")

        # self.settings = QSettings("__settings.ini", QSettings.IniFormat)
        # print(self.settings.fileName())

        self.setWindowTitle("Manage Employee")
        self.setGeometry(100, 100, 690, 600)
        # self.setFixedSize(690,600)
        self.windowAvailable = None  # set available Window to None
        self.updateAvailable = None
        # To add Items to Central Widget Create a Widget and set the CentralWidget to it
        self.centralwidget = QWidget(self)
        self.vbox = QVBoxLayout(self.centralwidget)
        self.vbox.setObjectName("Vbox!")
        self.centralwidget.setLayout(self.vbox)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setObjectName("CentralWidget")
        # Settings

        self.settings = QSettings("__settings.ini", QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)

        self.create_menu()
        self.create_statusbar()
        self.create_toolbar()
        self.create_tabs()


    def create_menu(self):
        # create menu bar
        main_menu = self.menuBar()
        fileMenu = main_menu.addMenu("File")
        ## Add actions here
        newAction = QAction("New", self)  # This will open the Add Employee Window
        newAction.setShortcut("Ctrl+N")
        newAction.triggered.connect(self.newEmployeeWindow)
        fileMenu.addAction(newAction)

        openAction = QAction("Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.read_settings)
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()

        self.saveasAction = QAction("Save As", self)
        self.saveasAction.triggered.connect(self.exporter)
        self.saveasAction.setShortcut("Ctrl+S")
        self.saveasAction.setEnabled(False)
        fileMenu.addAction(self.saveasAction)

        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # Menu 2
        editMenu = main_menu.addMenu("Edit")
        # add Action Here
        copyAction = QAction("Copy", self)
        copyAction.setShortcut("Ctrl+C")
        editMenu.addAction(copyAction)
        editMenu.addSeparator()

        # Menu 3
        helpMenu = main_menu.addMenu("Help")
        aboutAction = QAction("About", self)
        aboutAction.triggered.connect(self.helpMessage)
        helpMenu.addAction(aboutAction)

    def create_statusbar(self):
        statusbar = self.statusBar()
        # SETUP TIMER #
        self.timerlabel = QLabel()
        self.timer = QTimer()
        self.timer.timeout.connect(self.time_statusbar)
        self.timer.start(1000)
        # Insert Widgets
        statusbar.insertPermanentWidget(0, self.timerlabel)

    def time_statusbar(self):
        self.current_time = QTime.currentTime()
        self.label_time = self.current_time.toString("h:mm AP")
        self.timerlabel.setText(self.label_time)

    def create_toolbar(self):  # Employee Tabs
        self.tabtoolBar = QToolBar("Employee Tabs")
        self.addToolBar(Qt.TopToolBarArea, self.tabtoolBar)

        # replace with Icons
        self.toolActionNew = QAction("New")  # For demonstration Purposes
        self.toolActionNew.triggered.connect(self.newEmployeeWindow)
        self.tabtoolBar.addAction(self.toolActionNew)
        self.tabtoolBar.addSeparator()

        self.toolActionOpen = QAction("Open")  # For demonstration Purposes # replace with Icon
        self.tabtoolBar.addAction(self.toolActionOpen)
        self.tabtoolBar.addSeparator()

        self.toolActionSave = QAction("Save")  # For demonstration Purposes
        self.tabtoolBar.addAction(self.toolActionSave)
        self.tabtoolBar.addSeparator()

    def create_tabs(self):
        # add tab widget to central Window
        self.tabs = QTabWidget(self.centralwidget)
        self.tabs.setObjectName("MyTabs")
        print("Main TabName is ", self.tabs.objectName())
        self.vbox.addWidget(self.tabs)

    def addNewTab(self):
        # Create a tab as a widget so you can place anything on it
        self.tabNew = QWidget(self.tabs)
        # Create a layout and add said tab
        self.tab_layout = QVBoxLayout(self.tabNew)
        self.tab_layout.setObjectName("tabLayout")
        # Create a table
        self.table = QTableWidget(self)
        self.table.setObjectName("AddEmployeeTable")
        self.saveasAction.setEnabled(True)
        # Set properties for table for demo process
        self.table.setRowCount(2)  # for demonstration purposes
        self.table.setColumnCount(6)  # For Demonstration Purposes
        self.table.setColumnWidth(3, 110)  # For Demonstration Purposes
        self.table.setColumnWidth(4, 120)  # For Demonstration Purposes

        # Column
        self.table.setItem(0, 0, QTableWidgetItem("Date"))
        self.table.setItem(0, 1, QTableWidgetItem("Time Started"))
        self.table.setItem(0, 2, QTableWidgetItem("Time Ended"))
        self.table.setItem(0, 3, QTableWidgetItem("Total Time Worked"))
        self.table.setItem(0, 4, QTableWidgetItem("Amount Per Hour"))
        self.table.setItem(0, 5, QTableWidgetItem("Amount Paid"))

        # Rows after clicking new Employee
        self.table.setItem(1, 0, QTableWidgetItem(self.dateSetAdd))
        self.table.setItem(1, 1, QTableWidgetItem(self.timeStarted))
        self.table.setItem(1, 2, QTableWidgetItem(self.timeEnded))
        self.table.setItem(1, 3, QTableWidgetItem(str(self.totaltimeworked_add)))
        self.table.setItem(1, 4, QTableWidgetItem("$5.00"))
        self.table.setItem(1, 5, QTableWidgetItem('${:,.2f}'.format(self.final_amount_add)))
        # Set trigger no Edit Trigger to prevent editing
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # create a button
        self.updateButton = QPushButton("Update")
        self.updateButton.clicked.connect(self.UpdateEmployeeWindow)
        # Add Widgets to the tab layout you have created
        self.tab_layout.addWidget(self.table)
        self.tab_layout.addWidget(self.updateButton, 0, Qt.AlignHCenter)
        # Add the tab widget as a new tab to the main QTabWidget
        self.tabs.addTab(self.tabNew, self.windowAvailable.nameLineEdit.text())
        self.tabNew.setObjectName(self.windowAvailable.nameLineEdit.text())
        print("Tab name is ", self.tabNew.objectName())

    def newEmployeeWindow(self):
        if self.windowAvailable is None:
            self.windowAvailable = WindowEmployeeAdd()
            self.windowAvailable.setGeometry(self.x(), self.y(), 400, 400)
        if self.windowAvailable.exec_():
            ## Set the data and Time Now
            self.dateSetAdd = self.windowAvailable.dateLineEdit.date().toString()
            self.timeStarted = self.windowAvailable.timestartLineEdit.time().toString("h:mm AP")
            self.timeEnded = self.windowAvailable.timeendeLineEdit.time().toString("h:mm AP")
            # Total Time Worked
            self.gettimeStarted_add = self.windowAvailable.timestartLineEdit.time()
            self.gettimeEnded_add = self.windowAvailable.timeendeLineEdit.time()
            # get time here
            getTimeHours = int(self.gettimeStarted_add.secsTo(self.gettimeEnded_add) / 3600)
            getTimeMins = (self.gettimeEnded_add.minute() - self.gettimeStarted_add.minute())  ## change if you can
            # Put Everything Together
            self.totaltimeworked_add = str(getTimeHours) + "hour(s) " + str(getTimeMins) + "mins"
            self.final_amount_add = (self.gettimeStarted_add.secsTo(self.gettimeEnded_add) / 3600) * 5.00
            # Check if condition from Add Employee has been fulfilled, it has the accept...if accepted add new tab
            self.addNewTab()
        self.windowAvailable = None

    def UpdateEmployeeWindow(self):
        if self.updateAvailable is None:
            self.updateAvailable = WindowEmployeeUpdate()
            self.updateAvailable.setGeometry(self.x(), self.y(), 400, 400)
            self.index = self.tabs.currentIndex()
            # Set the new stuff here
            self.updateAvailable.nameLineEdit.setText(self.tabs.tabText(self.index))
            self.updateAvailable.updatestartLineEdit.setTime(self.gettimeEnded_add)
            self.updateAvailable.updateendeLineEdit.setTime(self.updateAvailable.updatestartLineEdit.time())

        if self.updateAvailable.exec_():
            # Update New Table
            self.setDateUpdate = self.updateAvailable.dateLineEdit.date().toString()
            self.timeStarted = self.updateAvailable.updatestartLineEdit.time().toString("h:mm AP")
            self.timeEnded = self.updateAvailable.updateendeLineEdit.time().toString("h:mm AP")
            # Perform New Calculations here
            self.gettimeStarted = self.updateAvailable.updatestartLineEdit.time()
            self.gettimeEnded = self.updateAvailable.updateendeLineEdit.time()

            getTimeHours = int(self.gettimeStarted.secsTo(self.gettimeEnded) / 3600)
            getTimeMins = (self.gettimeEnded.minute() - self.gettimeStarted.minute())  ## change if you can

            self.totaltimeworked = str(getTimeHours) + "hour(s) " + str(getTimeMins) + "mins"
            # Total Amount Paid
            self.final_amount = (self.gettimeStarted.secsTo(self.gettimeEnded) / 3600) * 5.00
            print("Mins to is:", int(self.gettimeStarted.secsTo(self.gettimeEnded) / 60))
            self.tableUpdater()  # pass # call the function that updates the table here
        self.updateAvailable = None

    def tableUpdater(self):
        # Find the child in the CurrentWidget(which is self.tab) and find the child in that current widget
        self.whichtable = self.tabs.currentWidget().findChild(QTableWidget)
        # print("Which Table is ",whichtable)
        for row in range(self.whichtable.rowCount()):
            row_number = self.whichtable.rowCount()
            self.whichtable.insertRow(row_number)
            self.whichtable.setItem(row_number, 0, QTableWidgetItem(self.setDateUpdate))  # Date
            self.whichtable.setItem(row_number, 1, QTableWidgetItem(self.timeStarted))  # Time Started
            self.whichtable.setItem(row_number, 2, QTableWidgetItem(self.timeEnded))  # Time Ended
            self.whichtable.setItem(row_number, 3,
                                    QTableWidgetItem(str(self.totaltimeworked)))  # Total Time Worked
            self.whichtable.setItem(row_number, 4, QTableWidgetItem("$5.00"))  # Amount Paid Per Hour
            self.whichtable.setItem(row_number, 5,
                                    QTableWidgetItem('${:,.2f}'.format(self.final_amount)))  # Total Amount Paid
            break



    def helpMessage(self):
        QMessageBox.about(self, "About", "DSC Challenge GUI v.1.0.0 \nBy Terence Quashie")

    def exporter(self, filename=None):
        if not filename:
            filename = QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
        if filename[0]:
            wb = xlsxwriter.Workbook(filename[0])
            self.sb = wb.add_worksheet()
            self.sb.set_column('A:F', 20)
            self.export()
            wb.close()
            print("file saved successfully")

    def export(self):
        row = 0
        col = 0
        for i in range(self.table.columnCount()):
            for x in range(self.table.rowCount()):
                try:
                    text = str(self.table.item(row, col).text())
                    self.sb.write(row, col, text)
                    row += 1
                except AttributeError:
                    row += 1
            row = 0
            col += 1

    def closeEvent(self, event):
        self.write_settings()

        super().closeEvent(event)


    def read_settings(self):
        with TableSaver.settingsContext("data.ini") as m:
            for children in self.findChildren(QtWidgets.QWidget):
                if children.objectName():
                    m.read(children)


    def write_settings(self):
        self.settings.beginGroup(self.tabNew.objectName())
        self.settings.setValue("ObjectName",self.tabNew.objectName())
        self.settings.endGroup()
        with TableSaver.settingsContext("data.ini") as m:
            for children in self.findChildren(QtWidgets.QWidget):
                if children.objectName():
                    m.write(children)


app = QApplication(sys.argv)

QCoreApplication.setApplicationName("Ugo")
QCoreApplication.setOrganizationDomain("Ugo")
QCoreApplication.setApplicationName("Ugo")

# setup stylesheet
apply_stylesheet(app, theme='dark_teal.xml')

window = MainWindow()
window.show()
sys.exit(app.exec_())
