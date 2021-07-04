from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog, QGroupBox, QFormLayout, QLineEdit, \
    QDateEdit, QTimeEdit, QPushButton, QMessageBox

class WindowEmployeeUpdate(QDialog):
    def __init__(self):
        super(WindowEmployeeUpdate, self).__init__()

        self.setWindowTitle("Update Employee Details")
        self.set_layout()

    def set_layout(self):
        #Set up basic Stuff here
        vbox=QVBoxLayout()
        group1 = QGroupBox("Employee Update")
        form1 = QFormLayout()
        group1.setLayout(form1)
        #Set Nane
        self.namelabel=QLabel("Name")
        self.nameLineEdit=QLineEdit("")
        self.nameLineEdit.setEnabled(False)
        form1.setWidget(0, QFormLayout.LabelRole,self.namelabel)
        form1.setWidget(0, QFormLayout.FieldRole, self.nameLineEdit)

        #Set Date Label
        self.datelabel = QLabel("Date Started")
        self.dateLineEdit = QDateEdit()
        self.dateLineEdit.setDate(QDate(2021,1,1))
        self.dateLineEdit.setCalendarPopup(True)
        form1.setWidget(1, QFormLayout.LabelRole, self.datelabel)
        form1.setWidget(1, QFormLayout.FieldRole, self.dateLineEdit)

        # set Time Started
        self.timestartlabel = QLabel("Time Started")
        self.updatestartLineEdit = QTimeEdit()
        # Set time constrain
        self.updatestartLineEdit.timeChanged.connect(self.connect_start_end)
        #Add to form Widget
        form1.setWidget(2, QFormLayout.LabelRole, self.timestartlabel)
        form1.setWidget(2, QFormLayout.FieldRole, self.updatestartLineEdit)
        # set Time Ended
        self.timeendedlabel = QLabel("Time Ended")
        self.updateendeLineEdit = QTimeEdit()
        # connect min time of endtime as starttime
        self.updateendeLineEdit.timeChanged.connect(self.connect_min_time) #you can use lambda function to get 1 line
        # Add to form Widget
        form1.setWidget(3, QFormLayout.LabelRole, self.timeendedlabel)
        form1.setWidget(3, QFormLayout.FieldRole, self.updateendeLineEdit)

        ##ADD BUTTON
        self.updatebtn=QPushButton("Update Employee")
        self.updatebtn.clicked.connect(self.saved_messagebox)

        ## ADD ITEMS TO LAYOUT
        vbox.addWidget(group1)
        vbox.addWidget(self.updatebtn, 0, Qt.AlignHCenter)
        self.setLayout(vbox)

    def connect_start_end(self):
        self.updateendeLineEdit.setTime(self.updatestartLineEdit.time())

    def connect_min_time(self):
        self.updateendeLineEdit.setMinimumTime(self.updateendeLineEdit.time())

    def saved_messagebox(self):
        if self.nameLineEdit.text()!="":
            QMessageBox.information(self, "Information", "Details Updated Successfully")
            self.accept()
        elif self.nameLineEdit.text() == "":
            QMessageBox.warning(self,"Warning","All Boxes Must be Filled")





