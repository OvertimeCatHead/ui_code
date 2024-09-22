import os, sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt


class Student():
    def __init__(self):
        super().__init__()
        self.m_id = 0
        self.m_name = ''

    def set_id(self, id):
        self.m_id = id

    def set_name(self, name):
        self.m_name = name

    def id(self):
        return self.m_id

    def name(self):
        return self.m_name


class StudentFrame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(StudentFrame, self).__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.line_name = QtWidgets.QLineEdit()
        self.layout.addWidget(self.line_name)

    def set_name(self, name):
        self.line_name.setText(name)

    def set_slted(self, slted):
        if slted:
            self.setStyleSheet("#StudentFrame{border:2px solid red;}");
        else:
            self.setStyleSheet("#StudentFrame{border:none;}");


class StudentListViewModel(QtCore.QAbstractListModel):
    m_studentList = []

    def __init__(self):
        super().__init__()

    def rowCount(self, parent=None):
        return len(self.m_studentList)

    def columnCount(self):
        return 1

    def data(self, index, role):
        student = self.m_studentList[index.row()]
        if not student:
            return None
        if role == Qt.UserRole:
            return student.id()
        elif role == Qt.UserRole + 1:
            return student.name()
        elif role == Qt.SizeHintRole:
            return QtCore.QSize(0, 100)
        return None

    def add(self, name, img):
        print(name, img)
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        studet = Student()
        studet.set_id(name)
        studet.set_name(img)
        self.m_studentList.append(studet)
        self.layoutChanged.emit()
        self.endInsertRows()

    def get_data(self, index):
        if self.rowCount() == 0:
            self.add()
        return self.m_studentList[index]


class StudentItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, studentListViewModel):
        super().__init__()
        self.m_studentListViewModel = StudentListViewModel()
        self.m_studentFrame = StudentFrame()

    def paint(self, painter, option, index):
        opc = option.rect
        if index.column() == 0:
            stu = self.m_studentListViewModel.get_data(index.row())
            print(stu.m_id, stu.m_name)
            if stu:
                self.m_studentFrame.set_name(stu.name())
                self.m_studentFrame.resize(opc.width(), opc.height())
                if option.state & QtWidgets.QStyle.State_Selected:
                    self.m_studentFrame.set_slted(True)
                else:
                    self.m_studentFrame.set_slted(False)
            pixmap = QtGui.QPixmap(stu.m_name)
            img_rec = QtCore.QRect(opc.x() + 2, opc.y() - 2, 94, 94)
            painter.drawPixmap(img_rec, pixmap)
            print(opc,img_rec)
            txt_rec = QtCore.QRect(2+94+2+5, opc.y()+94/2-10, 94, 94)
            print(txt_rec)
            painter.drawText(txt_rec, stu.m_id)

        super().paint(painter, option, index)


class main_win(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(800, 800)

    def initUI(self):
        self.lay = QtWidgets.QHBoxLayout()

        self.my_listview = QtWidgets.QListView()

        self.m_studentListViewModel = StudentListViewModel()
        self.m_studentItemDelegate = StudentItemDelegate(self.m_studentListViewModel)

        self.my_listview.setModel(self.m_studentListViewModel)
        self.my_listview.setItemDelegate(self.m_studentItemDelegate)

        self.add_datas()
        self.btn = QtWidgets.QPushButton('add')
        # self.btn.clicked.connect(self.clk)
        self.lay.addWidget(self.my_listview)
        self.lay.addWidget(self.btn)
        self.setLayout(self.lay)

    def add_datas(self):
        dic = {}
        for i in range(12000):
            self.m_studentListViewModel.add(str(i), r'C:\Users\pc\Desktop\tanzi.jpg')

    # def clk(self):
    #     for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    #               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
    #         if i in self.dic:
    #             print(i,self.dic)
    #             if i not in self.dic:
    #                 continue
    #             self.m_studentListViewModel.add(i, self.dic[1])
    #             self.dic.pop(i)


app = QtWidgets.QApplication()
starts = main_win()
starts.show()
app.exec_()
