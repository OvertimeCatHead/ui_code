import os,sys
from PySide2 import QtWidgets,QtCore,QtGui

class my_list_model(QtCore.QAbstractListModel):
    def __init__(self,item_list,parent=None):
        super().__init__()
        self.item_list=item_list
    def data(self, index, role) :
        print(index,role)
        if not index.isValid() :
            print('a')
            return None
        if not index.row()>=self.rowCount():
            print('c')
        if role==QtGui.Qt.DisplayRole or role==QtGui.Qt.EditRole:
            print('b')
            return self.item_list[index.row()]
        return None

    def setData(self, index, value, role):
        pass

    def rowCount(self, parent=None) :
        return len(self.item_list)

    def headerData(self, section, orientation, role):
        if role!= QtGui.Qt.DisplayRole:
            return
        if orientation==QtGui.Qt.Horizontal:
            return 'col'
        else:
            return 'row'


    def insertRow(self, row, parent=None):
        pass
    def removeRow(self, row, parent=None):
        pass






class my_model(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(my_model, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.resize(1000,500)
        self.main_lay = QtWidgets.QHBoxLayout()
        ll = QtWidgets.QListView()
        ll.setIconSize(QtCore.QSize(30,30))
        ll.setGridSize(QtCore.QSize(32,35))
        # tv1.setAlternatingRowColors(True)
        # tv1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # tv1.horizontalHeader().setStretchLastSection(True)
        p_model = my_list_model(['a','b'])
        # p_model.setHorizontalHeaderLabels(['name','age','class','sex','adress'])
        ll.setModel(p_model)

        self.main_lay.addWidget(ll)
        self.setLayout(self.main_lay)
        pass


app = QtWidgets.QApplication()
starts=my_model()
starts.show()
app.exec_()