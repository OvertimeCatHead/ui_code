import os, sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt


class main_win(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(800, 800)

    def initUI(self):
        self.lay = QtWidgets.QHBoxLayout()

        self.my_listview = QtWidgets.QListView()

        self.my_listview_model = CustomListModel()

        self.my_delegate = CustomDelegate()

        for i in range(5):
            it = item()
            it.slt = False
            it.txt = 'This is {}'.format(str(i))
            self.my_listview_model.insertData(it)

        self.my_listview.setModel(self.my_listview_model)
        self.my_listview.setItemDelegate(self.my_delegate)
        self.my_listview.setMouseTracking(True)
        self.lay.addWidget(self.my_listview)
        self.setLayout(self.lay)


class CustomListModel(QtCore.QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.data_list = []

    def insertData(self, data):
        self.data_list.append(data)

    def rowCount(self, parent):
        return len(self.data_list)

    def data(self, index, role):
        res = None
        row = index.row()
        if row >= len(self.data_list) or not index.isValid():
            return res
        tmp_data = self.data_list[row]

        if Qt.UserRole + 1:
            res = tmp_data.slt
            return
        elif Qt.UserRole + 2:
            res = tmp_data.txt
            return
        return

    def setData(self, index, value, role):
        res = False
        row = index.row()
        if row >= len(self.data_list) or not index.isValid():
            return res
        tmp_data = self.data_list[row]

        if Qt.UserRole + 1:
            tmp_data.slt = value.toBool()
            res = True
            return res
        elif Qt.UserRole + 2:
            tmp_data.txt = value.toString()
            return res

        self.data_list[row] = tmp_data

        return res


class CustomDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def paint(self, painter, option, index):
        ret = option.SO_FocusRect
        is_slt = index.data(Qt.UserRole + 1).toBool()
        txt = index.data(Qt.UserRole + 2).toString()
        vp = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(vp, index)
        if option.state.testFlag(QtWidgets.QStyle.State_HasFocus):
            vp.state = QtWidgets.QStyle.State_HasFocus
        super().paint(painter, vp, index)

        checboxRec = QtCore.QRect(ret.left() + 10, ret.top() + (ret.height() - 20) // 2, 20, 20)
        pix = QtGui.QPixmap(r"C:\Users\pc\Desktop\tanzi.jpg" if is_slt else r"C:\Users\pc\Desktop\yemao.jpg")
        painter.drawPixmap(checboxRec, pix)

        painter.save()
        font = QtGui.QFont("Microsoft YaHei", 10)
        painter.setFont(font)
        txtRec = QtCore.QRect(ret.left() + 50, ret.top(), ret.width() - 100, ret.height())
        painter.drawText(txtRec, Qt.AlignCenter, txt)
        painter.restore()

        painter.save()

        # 设置字体和颜色
        font = QtGui.QFont("Microsoft YaHei", 10)
        painter.setFont(font)

        txtRec = QtCore.QRect(ret.left() + 50, ret.top(), ret.width() - 100, ret.height())
        painter.drawText(txtRec, Qt.AlignCenter, txt)

        painter.restore()

    def editorEvent(self, event, model, option, index):
        retc = option.rect

        # 对应上面画的checkbox的retc
        checboxRec = QtCore.QRect(retc.left() + 10, retc.top() + (retc.height() - 20) // 2, 20, 20)
        print(model.data(index,Qt.UserRole+1))
        print(model.data(index, Qt.UserRole + 2))
        # 按钮点击事件；
        if checboxRec.contains(event.pos()) and event.type() == QtCore.QEvent.MouseButtonPress:
            value = model.data(index, Qt.UserRole + 1).toBool()
            model.setData(index, not value, Qt.UserRole + 1)
            model.dataChanged(index, index)

        return super().editorEvent(event, model, option, index)


class item():
    def __init__(self):
        super().__init__()
        self.txt = ''
        self.slt = False


app = QtWidgets.QApplication()
starts = main_win()
starts.show()
app.exec_()
