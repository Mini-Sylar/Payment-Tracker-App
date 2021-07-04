from PyQt5.QtCore import QDate, Qt, QTime, QTimer
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog, QGroupBox, QFormLayout, QLineEdit, \
    QDateEdit, QTimeEdit, QPushButton, QMessageBox


class WindowEmployeeAdd(QDialog):
    def __init__(self):
        super(WindowEmployeeAdd, self).__init__()

        self.setWindowTitle("Add Employee")
        self.set_layout()

    def set_layout(self):
        # Set up basic Stuff here
        vbox = QVBoxLayout()
        group1 = QGroupBox("Employee")
        form1 = QFormLayout()
        group1.setLayout(form1)

        self.namelabel = QLabel("Name")
        self.nameLineEdit = QLineEdit("")
        self.nameLineEdit.setPlaceholderText("Enter Employee Name")
        form1.setWidget(0, QFormLayout.LabelRole, self.namelabel)
        form1.setWidget(0, QFormLayout.FieldRole, self.nameLineEdit)

        datelabel = QLabel("Date Started")
        self.dateLineEdit = QDateEdit()
        self.dateLineEdit.setDate(QDate(2021, 1, 1))
        self.dateLineEdit.setCalendarPopup(True)
        form1.setWidget(1, QFormLayout.LabelRole, datelabel)
        form1.setWidget(1, QFormLayout.FieldRole, self.dateLineEdit)

        self.timestartlabel = QLabel("Time Started")
        self.timestartLineEdit = QTimeEdit()
        self.timestartLineEdit.setTime(QTime(7, 0, 0))
        # Set time constrain
        self.timestartLineEdit.timeChanged.connect(self.connect_start_end)
        form1.setWidget(2, QFormLayout.LabelRole, self.timestartlabel)
        form1.setWidget(2, QFormLayout.FieldRole, self.timestartLineEdit)

        timeendedlabel = QLabel("Time Ended")
        self.timeendeLineEdit = QTimeEdit()
        self.timeendeLineEdit.setTime(QTime(self.timestartLineEdit.time()))
        # connect min time of endtime as starttime
        self.timeendeLineEdit.timeChanged.connect(self.set_min_time)  # you can use lambda function to get 1 line
        form1.setWidget(3, QFormLayout.LabelRole, timeendedlabel)
        form1.setWidget(3, QFormLayout.FieldRole, self.timeendeLineEdit)

        ##Group 2 (Employer)
        group2 = QGroupBox("Employer")
        form2 = QFormLayout()
        group2.setLayout(form2)
        # Add items to form
        amountlabel = QLabel("Amount Paid Per Hour")
        self.amountLine = QLineEdit("$5.00")
        self.amountLine.setEnabled(False)

        form2.setWidget(0, QFormLayout.LabelRole, amountlabel)
        form2.setWidget(0, QFormLayout.FieldRole, self.amountLine)

        ##ADD BUTTON
        self.addbtn = QPushButton("Add Emmployee")
        self.addbtn.clicked.connect(self.saved_messagebox)

        ## ADD ITEMS TO LAYOUT
        vbox.addWidget(group1)
        vbox.addWidget(group2)
        vbox.addWidget(self.addbtn, 0, Qt.AlignHCenter)
        self.setLayout(vbox)

    def connect_start_end(self):
        self.timeendeLineEdit.setTime(self.timestartLineEdit.time())

    def set_min_time(self):
        self.timeendeLineEdit.setMinimumTime(self.timestartLineEdit.time())

    def saved_messagebox(self):
        if self.nameLineEdit.text() != "":
            QMessageBox.information(self, "Information", "Details Saved Successfully")
            self.accept()
        elif self.nameLineEdit.text() == "":
            QMessageBox.warning(self, "Warning", "All Boxes Must be Filled")
