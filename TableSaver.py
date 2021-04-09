import contextlib

from PyQt5 import QtCore, QtWidgets


class SettingsManager:
    def __init__(self, filename):
        self.m_settings = QtCore.QSettings(filename, QtCore.QSettings.IniFormat)

    @property
    def settings(self):
        return self.m_settings

    def read(self, widget):
        self.settings.beginGroup(widget.objectName())
        if isinstance(widget, QtWidgets.QAbstractItemView):
            selectionMode = self.settings.value(
                "selectionMode", type=QtWidgets.QAbstractItemView.SelectionMode
            )
            widget.setSelectionMode(selectionMode)
        if isinstance(widget, QtWidgets.QListWidget):
            items = self.settings.value("items")
            selecteditems = self.settings.value("selecteditems")
            # In the first reading the initial values must be established
            if items is None:
                self.read_defaults(widget)
            else:
                stream = QtCore.QDataStream(items, QtCore.QIODevice.ReadOnly)
                while not stream.atEnd():
                    it = QtWidgets.QListWidgetItem()
                    stream >> it
                    widget.addItem(it)
                stream = QtCore.QDataStream(
                    selecteditems, QtCore.QIODevice.ReadOnly
                )
                while not stream.atEnd():
                    row = stream.readInt()
                    it = widget.item(row)
                    if it is not None:
                        it.setSelected(True)
        if isinstance(widget, QtWidgets.QTableWidget):
            rowCount = self.settings.value("rowCount", type=int)
            columnCount = self.settings.value("columnCount", type=int)
            widget.setRowCount(rowCount)
            widget.setColumnCount(columnCount)
            items = self.settings.value("items")
            if items is None:
                self.read_defaults(widget)
            else:
                stream = QtCore.QDataStream(items, QtCore.QIODevice.ReadOnly)
                while not stream.atEnd():
                    it = QtWidgets.QTableWidgetItem()
                    i = stream.readInt()
                    j = stream.readInt()
                    stream >> it
                    widget.setItem(i, j, it)
                selecteditems = self.settings.value("selecteditems")
                stream = QtCore.QDataStream(
                    selecteditems, QtCore.QIODevice.ReadOnly
                )
                while not stream.atEnd():
                    i = stream.readInt()
                    j = stream.readInt()
                    it = widget.item(i, j)
                    if it is not None:
                        it.setSelected(True)
        if isinstance(widget,QtWidgets.QTabWidget):
            widget.addTab(self.settings.value("Object"),"Ugo")
        self.settings.endGroup()

    def write(self, widget):
        self.settings.beginGroup(widget.objectName())
        if isinstance(widget, QtWidgets.QAbstractItemView):
            self.settings.setValue("selectionMode", widget.selectionMode())
        if isinstance(widget, QtWidgets.QListWidget):
            items = QtCore.QByteArray()
            stream = QtCore.QDataStream(items, QtCore.QIODevice.WriteOnly)
            for i in range(widget.count()):
                stream << widget.item(i)
            self.settings.setValue("items", items)
            selecteditems = QtCore.QByteArray()
            stream = QtCore.QDataStream(
                selecteditems, QtCore.QIODevice.WriteOnly
            )
            for it in widget.selectedItems():
                stream.writeInt(widget.row(it))

            self.settings.setValue("selecteditems", selecteditems)
        if isinstance(widget, QtWidgets.QTableWidget):
            self.settings.setValue("rowCount", widget.rowCount())
            self.settings.setValue("columnCount", widget.columnCount())
            items = QtCore.QByteArray()
            stream = QtCore.QDataStream(items, QtCore.QIODevice.WriteOnly)
            for i in range(widget.rowCount()):
                for j in range(widget.columnCount()):
                    it = widget.item(i, j)
                    if it is not None:
                        stream.writeInt(i)
                        stream.writeInt(j)
                        stream << it
            self.settings.setValue("items", items)
            selecteditems = QtCore.QByteArray()
            stream = QtCore.QDataStream(
                selecteditems, QtCore.QIODevice.WriteOnly
            )
            for it in widget.selectedItems():
                # print(it.row(), it.column())
                stream.writeInt(it.row())
                stream.writeInt(it.column())
            self.settings.setValue("selecteditems", selecteditems)
        # if isinstance(widget,QtWidgets.QWidget):
        #     self.settings.setValue("Object",widget)
        #     self.settings.setValue("Name", widget.objectName())

        self.settings.endGroup()

    def release(self):
        self.m_settings.sync()

    def read_defaults(self, widget):
        if widget.objectName() == "listwidget_1":
            widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            for i in range(10):
                widget.addItem(QtWidgets.QListWidgetItem(str(i)))
        elif widget.objectName() == "listwidget_2":
            widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            for i in "abcdefghijklmnopqrstuvwxyz":
                widget.addItem(QtWidgets.QListWidgetItem(i))
        elif widget.objectName() == "tablewidget":
            widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            widget.setRowCount(10)
            widget.setColumnCount(10)
            for i in range(widget.rowCount()):
                for j in range(widget.columnCount()):
                    it = QtWidgets.QTableWidgetItem("{}-{}".format(i, j))
                    widget.setItem(i, j, it)


@contextlib.contextmanager
def settingsContext(filename):
    manager = SettingsManager(filename)
    try:
        yield manager
    finally:
        manager.release()
