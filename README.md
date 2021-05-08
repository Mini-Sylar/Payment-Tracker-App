# DSC-CHALLENGE-UG (UI version 1.0)
### University of Ghana
A program to help an employee track how much they are paid after a period of work (UI version)

## Installation
Program depends on the following libraries
- pyqt5
- sys
- xlswriter
- qt_material
- TableSaver (custom module adapted from ellyansec's save modules)

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following libraries.

```bash
pip install PyQt5
pip install XlsxWriter
pip install qt-material
TableSaver Module is included in the files 
```

## Usage

```
- run MainWindow.py 
- add an employee from the file menu to generate an employee tab with a table
- Use the update button to add more entries to the table
- Use the save button to export the items in the table as a spreadsheet
```

## Issues
```
At the moment you cannot recover employee data after closing the program
this issue is being worked on
```

## Screenshots
<div>
<img width="380" src="/Screenshots/Screen1.png" alt="Mainwindow Interface">
<img width="380" src="/Screenshots/Screen2.png" alt="Add Employee">
<img width="380" src="/Screenshots/Screen3.png" alt="Sample Data1">
<img width="380" src="/Screenshots/Screen4.png" alt="Update Employee">
<img width="380" src="/Screenshots/Screen5.png" alt="Sample Data After Update">
<img width="380" src="/Screenshots/Screen6.png" alt="Sample Data After Exporting">
</div>
Sample file is included in Screenshots folder as [Sample Output](Employee1_Data.xls)

## Contributing
Pull requests are welcome. Also a TO DO list will be added to give an idea of what is 
planned


## License
[MIT](https://choosealicense.com/licenses/mit/)
