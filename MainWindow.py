import json
import os.path
import sys

import xlsxwriter
from PyQt5.QtCore import QTime, QTimer, Qt, QCoreApplication, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox, QLabel, QToolBar, QTabWidget, \
    QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QAbstractItemView, QFileDialog, QApplication
from qt_material import apply_stylesheet

from Windows.AddEmployee import WindowEmployeeAdd
from Windows.UpdateEmployee import WindowEmployeeUpdate

import ToolbarIcons

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setObjectName("ManageEmployeeObject")

        self.setWindowTitle("Manage Employee")
        self.setGeometry(100, 100, 700, 600)
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

        self.create_menu()
        self.create_statusbar()
        self.create_toolbar()
        self.manageIcons()
        self.create_tabs()

    def create_menu(self):
        # create menu bar
        main_menu = self.menuBar()
        fileMenu = main_menu.addMenu("File")
        # Add actions here
        newAction = QAction("New", self)  # This will open the Add Employee Window
        newAction.setShortcut("Ctrl+N")
        newAction.triggered.connect(self.newEmployeeWindow)
        fileMenu.addAction(newAction)

        openAction = QAction("Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.read_json)
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()

        self.saveAction = QAction("Save", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.write_json)
        fileMenu.addAction(self.saveAction)
        self.saveAction.setEnabled(False)

        self.saveasAction = QAction("Export", self)
        self.saveasAction.triggered.connect(self.exporter)
        self.saveasAction.setShortcut("Ctrl+Alt+S")
        self.saveasAction.setEnabled(False)
        fileMenu.addAction(self.saveasAction)

        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(lambda :self.close())
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
        self.tabtoolBar.setIconSize(QSize(24, 24))
        self.tabtoolBar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # replace with Icons
        self.toolActionNew = QAction("New")  # For demonstration Purposes
        self.toolActionNew.triggered.connect(self.newEmployeeWindow)
        self.tabtoolBar.addAction(self.toolActionNew)
        self.tabtoolBar.addSeparator()

        self.toolActionOpen = QAction("Open")  # For demonstration Purposes # replace with Icon
        self.toolActionOpen.triggered.connect(self.read_json)
        self.tabtoolBar.addAction(self.toolActionOpen)
        self.tabtoolBar.addSeparator()

        self.toolActionSave = QAction("Save")  # For demonstration Purposes
        self.toolActionSave.triggered.connect(self.write_json)
        self.toolActionSave.setEnabled(False)
        self.tabtoolBar.addAction(self.toolActionSave)
        self.tabtoolBar.addSeparator()

        self.toolActionExport = QAction("Export")  # For demonstration Purposes
        self.toolActionExport.triggered.connect(self.exporter)
        self.toolActionExport.setEnabled(False)
        self.tabtoolBar.addAction(self.toolActionExport)
        self.tabtoolBar.addSeparator()

    def create_tabs(self):
        # add tab widget to central Window
        self.tabs = QTabWidget(self.centralwidget)
        self.tabs.setObjectName("MyTabs")
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
        self.saveAction.setEnabled(True)
        self.saveasAction.setEnabled(True)
        self.toolActionSave.setEnabled(True)
        self.toolActionExport.setEnabled(True)
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

    def manageIcons(self):
        newIcon = QIcon()
        openIcon = QIcon()
        saveIcon = QIcon()
        exportIcon = QIcon()
        newIcon.addFile(u":/main/doc_plus_icon&32.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolActionNew.setIcon(newIcon)
        openIcon.addFile(u":/main/folder_open_icon&32.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolActionOpen.setIcon(openIcon)
        saveIcon.addFile(u":/main/save_icon&32.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolActionSave.setIcon(saveIcon)
        exportIcon.addFile(u":/main/doc_export_icon&32.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolActionExport.setIcon(exportIcon)

    def add_atab(self,tabname):
        # Create a tab as a widget so you can place anything on it
        self.tabNew = QWidget(self.tabs)
        # Create a layout and add said tab
        self.tab_layout = QVBoxLayout(self.tabNew)
        self.tab_layout.setObjectName("tabLayout")
        # Create a table
        self.table = QTableWidget(self)
        self.table.setObjectName("AddEmployeeTable")
        self.saveAction.setEnabled(True)
        self.saveasAction.setEnabled(True)
        self.toolActionSave.setEnabled(True)
        self.toolActionExport.setEnabled(True)
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

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # create a button
        self.updateButton = QPushButton("Update")
        self.updateButton.clicked.connect(self.UpdateEmployeeWindow)
        # Add Widgets to the tab layout you have created
        self.tab_layout.addWidget(self.table)
        self.tab_layout.addWidget(self.updateButton, 0, Qt.AlignHCenter)
        # Add the tab widget as a new tab to the main QTabWidget
        self.tabs.addTab(self.tabNew, str(tabname))
        self.tabNew.setObjectName(str(tabname))
        self.tabs.setCurrentIndex(self.tabs.indexOf(self.tabNew))

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
            getTimeMins = (self.gettimeEnded.minute() - self.gettimeStarted.minute())  # change if you can

            self.totaltimeworked = str(getTimeHours) + "hour(s) " + str(getTimeMins) + "mins"
            # Total Amount Paid
            self.final_amount = (self.gettimeStarted.secsTo(self.gettimeEnded) / 3600) * 5.00
            self.tableUpdater()  # pass # call the function that updates the table here
        self.updateAvailable = None

    def tableUpdater(self):
        # Find the child in the CurrentWidget(which is self.tab) and find the child in that current widget
        self.whichtable = self.tabs.currentWidget().findChild(QTableWidget)
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
        try:
            self.write_json()
        except AttributeError:
            print("There is no table")
        super().closeEvent(event)

    def write_json(self):
        mydict = {"Name": [self.tabs.tabText(self.tabs.currentIndex())]}
        column = 0
        date, timestarted, timeended, totaltimeworked, amount_perhour, amount_paid = [], [], [], [], [], []
        # Start adding stuff here
        for row in range(self.table.rowCount()):
            _item = self.table.item(row, column)
            if _item:
                column = 0
                item = self.table.item(row, column).text()
                column = 1
                item2 = self.table.item(row, column).text()
                column = 2
                item3 = self.table.item(row, column).text()
                column = 3
                item4 = self.table.item(row, column).text()
                column = 4
                item5 = self.table.item(row, column).text()
                column = 5
                item6 = self.table.item(row, column).text()

                date.append(item)
                timestarted.append(item2)
                timeended.append(item3)
                totaltimeworked.append(item4)
                amount_perhour.append(item5)
                amount_paid.append(item6)

                mydict[self.table.item(0, 0).text()] = date[1:]
                mydict[self.table.item(0, 1).text()] = timestarted[1:]
                mydict[self.table.item(0, 2).text()] = timeended[1:]
                mydict[self.table.item(0, 3).text()] = totaltimeworked[1:]
                mydict[self.table.item(0, 4).text()] = amount_perhour[1:]
                mydict[self.table.item(0, 5).text()] = amount_paid[1:]

        # Setting Up json
        json_object = json.dumps(mydict, indent=4)
        filename = self.tabs.tabText(self.tabs.currentIndex()).replace(" ", "") + "-data.json"
        finalpath = os.path.join('SavedData', filename)

        outfile = open(finalpath,"w")
        outfile.write(json_object)
        outfile.close()

    def read_json(self, json_name=None):
        if not json_name:
            json_name = QFileDialog.getOpenFileName(self, 'Open Json', '', ".json(*.json)")
        if json_name[0]:
            try:
                with open(json_name[0]) as f:
                    data = json.load(f)
                while True:
                    if self.tabs.tabText(self.tabs.currentIndex()) == data["Name"][0]:
                        column_count = (len(data['Date']))
                        self.table.setRowCount(column_count + 1)
                        # fill Specific Columns
                        for row in range(self.table.rowCount()):  # add items from array to QTableWidget
                            row = 1
                            for column in range(column_count):
                                item_date = (list(data["Date"])[column])
                                item_timestarted = (list(data["Time Started"])[column])
                                item_timeended = (list(data["Time Ended"])[column])
                                item_totaltime = (list(data["Total Time Worked"])[column])
                                item_amountper = (list(data["Amount Per Hour"])[column])
                                item_amountpaid = (list(data["Amount Paid"])[column])

                                self.table.setItem(row, 0, QTableWidgetItem(item_date))
                                self.table.setItem(row, 1, QTableWidgetItem(item_timestarted))
                                self.table.setItem(row, 2, QTableWidgetItem(item_timeended))
                                self.table.setItem(row, 3, QTableWidgetItem(item_totaltime))
                                self.table.setItem(row, 4, QTableWidgetItem(item_amountper))
                                self.table.setItem(row, 5, QTableWidgetItem(item_amountpaid))
                                row += 1
                        break
                    else:
                        # Else create a tab with a table and re run loop
                        self.add_atab(data["Name"][0])

            except AttributeError as e:
                print(e)


app = QApplication(sys.argv)

QCoreApplication.setApplicationName("Simple Payment Tracker")
QCoreApplication.setOrganizationDomain("Terence")
QCoreApplication.setApplicationName("Simple Payment Tracker")

# setup stylesheet
apply_stylesheet(app, theme='dark_teal.xml')

window = MainWindow()
window.show()
sys.exit(app.exec_())
