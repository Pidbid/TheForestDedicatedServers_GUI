# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2021/02/17 16:14:49
@Author  :   Wicos
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
'''

# here put the import lib
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDesktopWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QTabWidget, QTextBrowser, QTableWidget, QTableWidgetItem, QAbstractItemView, QWidget, QMessageBox, QHBoxLayout, QRadioButton
from PyQt5.QtGui import QFont, QPixmap, QIcon, QCursor
from PyQt5.QtCore import QSize, Qt, pyqtSignal,QProcess
import datetime
import os
import qdarkstyle
from model import start

#nuitka --mingw64 --standalone --show-progress --show-memory --plugin-enable=qt-plugins --output-dir=out main.py

class MyLabel(QLabel):
    mylabelSig = pyqtSignal(str)
    def __int__(self):
        super(MyLabel, self).__init__()

    def mousePressEvent(self, e):    # 单击
        sigContent = self.objectName()
        self.mylabelSig.emit(sigContent)

    def click_fun(self, func):
        self.mylabelSig.connect(func)


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread()
        self.initGui()

    def initGui(self):
        self.resize(800, 500)
        self.setMinimumSize(800, 500)
        self.setMaximumSize(800, 500)
        self.layout = QHBoxLayout(self, spacing=0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setWindowIcon(QIcon('./static/logo.ico'))
        self.move_center()
        self.font()
        self.lable()
        self.log()
        self.tab()
        self.radiobutton()
        # self.win.show()
        self.statusBar().showMessage("Go for your son")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.button()

    def thread(self):
        #start thread
        self.thread_start = start.START()

    def move_center(self):
        screen = QDesktopWidget().screenGeometry()
        form = self.geometry()
        x_move_step = (screen.width() - form.width()) / 2
        y_move_step = (screen.height() - form.height()) / 2
        self.move(int(x_move_step), int(y_move_step))

    def font(self):
        self.font_bigbutton = QFont()
        self.font_bigbutton.setBold(True)
        self.font_bigbutton.setPointSize(20)
        self.font_bigbutton.setWeight(25)
        # radio button fot
        self.font_rbt = QFont()
        self.font_rbt.setBold(True)
        self.font_rbt.setPointSize(15)
        self.font_rbt.setWeight(15)

    def button(self):
        self.btn_start = QPushButton("初始化", self.tab_one)
        self.btn_start.resize(150, 50)
        self.btn_start.setFont(self.font_bigbutton)
        self.btn_start.setIcon(QIcon("./static/start.png"))
        self.btn_start.setIconSize(QSize(25, 25))
        self.btn_start.clicked.connect(self.start_server)
        self.btn_start.move(350, 350)

    def tab(self):
        self.tab_panel = QTabWidget(self)
        self.tab_one = QWidget(self)
        self.tab_two = QWidget(self)
        self.tab_panel.addTab(self.tab_one, "开始")
        self.tab_panel.addTab(self.tab_two, "设置")
        self.tab_panel.resize(520, 440)
        self.tab_panel.move(10, 30)

    def log(self):
        self.log_panel = QTextBrowser(self)
        self.log_panel.resize(250, 415)
        self.log_panel.move(540, 55)

    def lable(self):
        # logo picture
        self.label_icon = QLabel(self)
        self.label_icon.setPixmap(QPixmap("./static/logo.png"))
        self.label_icon.resize(30, 30)
        self.label_icon.move(0, 0)
        # title label
        self.label_title = QLabel(self)
        self.label_title.setText("TFDS-OneKey")
        self.label_title.move(30, 0)
        # close label button
        self.label_close = MyLabel(self)
        self.label_close.setPixmap(QPixmap("./static/close.png"))
        self.label_close.resize(30, 30)
        self.label_close.move(770, 0)
        self.label_close.click_fun(self.close)
        # clear log label
        self.label_clearlog = MyLabel(self)
        self.label_clearlog.setPixmap(QPixmap("./static/clear.png"))
        self.label_clearlog.resize(30, 30)
        self.label_clearlog.move(540, 20)
        self.label_clearlog.click_fun(self.log_clear)
        # minisize label button
        self.label_mini = MyLabel(self)
        self.label_mini.setPixmap(QPixmap("./static/mini.png"))
        self.label_mini.resize(30, 30)
        self.label_mini.move(740, 0)
        self.label_mini.click_fun(self.showMinimized)
        # steamcmd save dir
        #self.label_steamcmd = QLabel(self.tab_one)
        # self.label_steamcmd.setText("Steamcmd:")
        # self.label_steamcmd.move(300,100)

    def radiobutton(self):
        # use pre setting
        self.rbt_preset = QRadioButton("预设", self.tab_one)
        self.rbt_preset.setFont(self.font_rbt)
        self.rbt_preset.setChecked(True)
        self.rbt_preset.move(250, 370)
        # uses setting
        self.rbt_customset = QRadioButton("自定义", self.tab_one)
        self.rbt_customset.setFont(self.font_rbt)
        self.rbt_customset.setCheckable(False)
        self.rbt_customset.move(130, 370)

    def closeEvent(self, event):
        result = QMessageBox.question(
            self, "注意：", "您真的要关闭TFDS吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def log_add(self, data):
        self.log_panel.append(data)

    def log_clear(self):
        self.log_panel.clear()

    def start_server(self):
        self.thread_start.start()
        self.thread_start.trg.connect(self.log_add)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
