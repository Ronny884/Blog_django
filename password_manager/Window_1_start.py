from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import time
import os
import msvcrt
from encryption import Encryption
from Window_3_database_selection import MyEventHandler_3


class Window_1_start_functional(QMainWindow):
    """
    Класс содержит в себе функционал стартового окна, где пользователь выбирает из 2 действий:
    создать новую базу паролей или войти в уже существующую
    """
    def __init__(self):
        super(Window_1_start_functional, self).__init__()
        self.window__5 = None
        self.window__7 = None
        self.window__3 = None
        self.window__9 = None
        self.window__10 = None
        self.window__G = None
        self.crypto = Encryption()
        self.window_1 = Ui_Window_1_start()
        self.window_1.setupUi(self)
        self.road_map_list = []

        self.window_1.btn_create_a_new_db.clicked.connect(self.create_a_new_db_func)
        self.window_1.btn_open_saved_db.clicked.connect(self.open_saved_db_func)
        self.window_1.btn_generaton.clicked.connect(self.generate)

    def encryption_before_closing_the_program(self):
        """
        Функция вызывает методы шифрования при выходе из программы через нажатие на крестик
        """
        for window in [self.window__5, self.window__7, self.window__9, self.window__10]:
            if window.need_and_name[0] is True:
                # print(window.need_and_name[1], window.need_and_name[2])
                self.crypto.encrypt_file(window.need_and_name[1], window.need_and_name[2])

        LOCK_FILE_PATH = f'{os.getcwd()}/file.lock'
        if os.path.exists(LOCK_FILE_PATH):
            os.remove(LOCK_FILE_PATH)

    def generate(self):
        self.window__G.set_default_state('from_start', 'Generation without saving')
        self.window__G.show()
        self.close()

    def show_window_2_no_db(self):
        """
        Функция создаёт всплывающее окно
        """
        self.window_2_no_db = QMessageBox()
        self.window_2_no_db.setWindowTitle('Database not found')
        self.window_2_no_db.setText('No password databases found. Create first base?')
        self.window_2_no_db.setIcon(QMessageBox.Icon.Question)
        self.window_2_no_db.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        self.window_2_no_db.setDetailedText('details')
        self.window_2_no_db.buttonClicked.connect(self.push_ok)
        self.window_2_no_db.exec()

    def push_ok(self, btn):
        if btn.text() == 'OK':
            self.road_map_list.append(1)
            self.window__5.show()
            self.close()

    def create_a_new_db_func(self):
        self.road_map_list.append(1)
        self.window__5.show()
        self.close()

    def open_saved_db_func(self):
        """
        Открываем сохранённые БД. Если не имеется нужной дериктории, создаём её и выдаём
        пользователю окно 2. Если дериктория имеется, но она пуста, также открываем окно 2.
        """
        for file_name in os.listdir(f'{os.getcwd()}/Database'):
            if file_name.endswith('.db'):
                self.road_map_list.append(1)
                self.window__3.show()
                self.window__3.set_default_state()
                self.close()
                return True
        self.show_window_2_no_db()  # открываем окно 2


class Ui_Window_1_start(object):
    def setupUi(self, Window_1_start):
        Window_1_start.setObjectName("Window_1_start")
        Window_1_start.setEnabled(True)
        Window_1_start.resize(1150, 600)
        Window_1_start.setMinimumSize(QtCore.QSize(1150, 600))
        Window_1_start.setMaximumSize(QtCore.QSize(1150, 600))
        Window_1_start.setWindowIcon(QtGui.QIcon("icons/key.ico"))
        Window_1_start.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(192,195,196,1), stop:0 rgba(40,43,43,1), stop:1 rgba(255,255,255,1), stop:1 rgba(255,255,255,1));\n"
"font: 24pt \"HP Simplified\";\n"
"")
        self.centralwidget = QtWidgets.QWidget(parent=Window_1_start)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(810, 20, 331, 61))
        self.label.setMinimumSize(QtCore.QSize(22, 0))
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"font-weight: bold;\n"
"font-size: 27pt;\n"
"font-color: RGB(28,28,28);\n"
"color:  black;")
        self.label.setObjectName("label")
        self.btn_open_saved_db = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_open_saved_db.setGeometry(QtCore.QRect(391, 201, 381, 141))
        self.btn_open_saved_db.setMinimumSize(QtCore.QSize(0, 81))
        self.btn_open_saved_db.setMaximumSize(QtCore.QSize(16777215, 1111))
        self.btn_open_saved_db.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_open_saved_db.setStyleSheet("QPushButton {\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 23pt;\n"
"border: 3px solid rgb(0,0,0);\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}\n"
"")
        self.btn_open_saved_db.setObjectName("open_saved_db")
        self.btn_generaton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_generaton.setGeometry(QtCore.QRect(350, 470, 291, 71))
        self.btn_generaton.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_generaton.setMaximumSize(QtCore.QSize(16777215, 1111))
        self.btn_generaton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_generaton.setStyleSheet("QPushButton {\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 19pt;\n"
"border: 3px solid rgb(0,0,0);\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_generaton.setObjectName("generaton")
        self.btn_create_a_new_db = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_create_a_new_db.setGeometry(QtCore.QRect(460, 360, 411, 91))
        self.btn_create_a_new_db.setMinimumSize(QtCore.QSize(0, 81))
        self.btn_create_a_new_db.setMaximumSize(QtCore.QSize(16777215, 1111))
        self.btn_create_a_new_db.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_create_a_new_db.setStyleSheet("QPushButton {\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 20pt;\n"
"border: 3px solid rgb(0,0,0);\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_create_a_new_db.setObjectName("create_a_new_db")
        Window_1_start.setCentralWidget(self.centralwidget)

        self.retranslateUi(Window_1_start)
        QtCore.QMetaObject.connectSlotsByName(Window_1_start)

    def retranslateUi(self, Window_1_start):
        _translate = QtCore.QCoreApplication.translate
        Window_1_start.setWindowTitle(_translate("Window_1_start", "PasswordManager"))
        self.label.setText(_translate("Window_1_start", "Password Manager"))
        self.btn_open_saved_db.setText(_translate("Window_1_start", "Open saved db"))
        self.btn_generaton.setText(_translate("Window_1_start", "Generation"))
        self.btn_create_a_new_db.setText(_translate("Window_1_start", "Create a new db"))
