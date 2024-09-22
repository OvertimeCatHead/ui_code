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
        super(StudentFrame,self).__init__()
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
        self.m_testNumber = 1001

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

    def add(self, name):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        studet = Student()
        studet.set_id(int(self.m_testNumber))
        studet.set_name(str(name))
        self.m_studentList.append(studet)
        self.layoutChanged.emit()
        self.m_testNumber += 1
        self.endInsertRows()


    def get_data(self, index):
        print(self.m_studentList)
        if self.rowCount() == 0:
            self.add()
        return self.m_studentList[index]


class StudentItemDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, studentListViewModel):
        super().__init__()
        self.m_studentListViewModel = StudentListViewModel()
        self.m_studentFrame = StudentFrame()

    def paint(self, painter, option, index):
        '''
        image_path = index.data(Qt.DisplayRole)
        if image_path:
            pixmap = QPixmap(image_path)
            # 缩放图片到指定区域
            scaled_pixmap = pixmap.scaled(option.rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(option.rect, scaled_pixmap)
        '''
        print(dir(index))
        print(index.data(Qt.DisplayRole))

        if index.column() == 0:
            stu = self.m_studentListViewModel.get_data(index.row())
            print(stu.m_id,stu.m_name)
            if stu:
                self.m_studentFrame.set_name(stu.name())
                self.m_studentFrame.resize(option.rect.width(),option.rect.height())
                if option.state & QtWidgets.QStyle.State_Selected:
                    self.m_studentFrame.set_slted(True)
                else:
                    self.m_studentFrame.set_slted(False)
            pixmap = QtGui.QPixmap(stu.m_name)
            painter.drawPixmap(option.rect, pixmap)

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

        self.btn = QtWidgets.QPushButton('add')
        self.btn.clicked.connect(self.clk)
        self.lay.addWidget(self.my_listview)
        self.lay.addWidget(self.btn)
        self.setLayout(self.lay)

    def clk(self):

        self.m_studentListViewModel.add(name=r'C:\Users\pc\Desktop\tanzi.jpg')

app = QtWidgets.QApplication()
starts = main_win()
starts.show()
app.exec_()
