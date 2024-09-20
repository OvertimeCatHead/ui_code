from PySide2 import QtWidgets,QtCore,QtGui
class my_model(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(my_model, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.resize(1000,500)
        self.main_lay = QtWidgets.QHBoxLayout()
        tv1 = QtWidgets.QTableView()
        tv1.setAlternatingRowColors(True)
        tv1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        tv1.horizontalHeader().setStretchLastSection(True)
        p_model = QtGui.QStandardItemModel(20,5)
        p_model.setHorizontalHeaderLabels(['name','age','class','sex','adress'])
        tv1.setModel(p_model)

        self.main_lay.addWidget(tv1)
        self.setLayout(self.main_lay)
        pass

app = QtWidgets.QApplication()
starts=my_model()
starts.show()
app.exec_()