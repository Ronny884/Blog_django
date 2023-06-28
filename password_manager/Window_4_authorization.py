from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit
import os
import os.path
import time
from data import Data
from encryption import Encryption


class Window_4_authorization_functional(QMainWindow):
    def __init__(self):
        super(Window_4_authorization_functional, self).__init__()
        self.window_4 = Ui_Window_4_authorization()
        self.window_4.setupUi(self)
        self.db = Data()
        self.crypto = Encryption()
        self.window__1 = None
        self.window__3 = None
        self.window__9 = None

        self.set_default_state()
        self.window_4.btn_return_to_start.clicked.connect(self.return_to_start)
        self.window_4.btn_Again.clicked.connect(self.again)
        self.window_4.btn_Enter.clicked.connect(self.enter_password)
        self.window_4.btn_eye.clicked.connect(self.show_or_hide_password_text)

    def set_default_state(self):
        self.attempts = 4
        self.eye_state = False
        self.window_4.line_enter_master_password.setEchoMode(QLineEdit.EchoMode.Normal)
        self.window_4.btn_Enter.show()
        self.window_4.line_enter_master_password.setText('')
        self.set_style_sheet("background-color: rgb(244, 244, 244);\n"
                             "font: \"MS Shell Dlg 2\";;\n"
                             "font-size: 20pt;\n"
                             "border-radius: 10px;")
        self.window_4.label_db_name.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                                  "color: rgb(72,72,72);\n"
                                                  "font: \"MS Shell Dlg 2\";\n"
                                                  "font-size: 16pt;\n")

    def set_style_sheet(self, style_sheet):
        self.window_4.line_enter_master_password.setStyleSheet(style_sheet)

    def enter_password(self):
        verifiable_password = self.window_4.line_enter_master_password.text()
        db_name = self.window__3.chosen_name
        if os.path.isfile(f'{os.getcwd()}/Database/{db_name}.db'):
            if db_name in self.window__3.db_without_salt:
                self.error_window_show('There is no decryption file for this database', 'The "Alpha" folder should'
                                              ' contain a file for decrypting the selected '
                                              'database. Its name must match the name of the database, for example, '
                                              f'for the "{db_name}" database, the name would be '
                                              f'"{db_name}.bin". In this case, '
                                              'this file could have been deleted, moved, or renamed, which could cause '
                                              'the program to work incorrectly. Check its presence and the correctness '
                                              'of the name.')
                return False

            decrypt = self.crypto.decrypt_file(db_name, verifiable_password)
            if decrypt:
                self.window__9.password_for_encryption = verifiable_password  # соль для дальнейшей зашифровки
                self.set_default_state()
                self.window__1.road_map_list.append(4)
                self.window__9.working_db_name = db_name
                self.window__9.set_default_state()
                # в себе название БД, с которой идёт работа
                self.window__9.add_chosen_db_name(db_name)
                self.window__9.show()
                self.close()
            else:
                self.attempts -= 1
                if self.attempts == 0:
                    self.add_chosen_db_name('You have no more login attempts left')
                    self.window_4.line_enter_master_password.setText(' :(')
                    self.window_4.btn_Enter.hide()
                    QCoreApplication.processEvents()  # дожидается, пока выпонится вся асинхронная поебень
                    time.sleep(3)
                    exit()

                self.add_chosen_db_name(f'Wrong password. You have attempts left: {self.attempts}')
                self.window_4.label_db_name.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                                          "color: rgb(255, 0, 0);\n"
                                                          "font: \"MS Shell Dlg 2\";\n"
                                                          "font-size: 16pt;\n")
                self.set_style_sheet("background-color: rgb(255, 235, 235);\n"
                                     "font: \"MS Shell Dlg 2\";;\n"
                                     "border: 1px solid rgb(255,0,0);\n"
                                     "font-size: 20pt;\n"
                                     "border-radius: 10px;")
        else:
            self.error_window_show('The database was not found in the required directory "Database"', 'This can happen '
                                              'if the database has been moved or removed from the'
                                              ' specified directory while in this window. Check the file in other'
                                              ' directories and, if found, move it to the "Database" directory.'
                                              'It could also happen if the file was renamed. In this case, just try '
                                              'logging in again by clicking OK.')

    def error_window_show(self, text, details):
        self.error_window = QMessageBox()
        self.error_window.setWindowTitle('FoundError')
        self.error_window.setText(text)
        self.error_window.setIcon(QMessageBox.Icon.Warning)
        self.error_window.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.error_window.setDetailedText(details)
        self.error_window.buttonClicked.connect(self.again)
        self.error_window.exec()

    def return_to_start(self):
        self.window__1.road_map_list.append(4)
        self.set_default_state()
        self.window__1.show()
        self.hide()

    def again(self):
        if self.window__1.road_map_list[-1] == 3:
            self.window__1.road_map_list.append(4)
            self.set_default_state()
            self.window__3.set_default_state()
            self.window__3.show()
            self.close()

    def show_or_hide_password_text(self):
        if self.eye_state == False:
            self.window_4.line_enter_master_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_state = True
        else:
            self.window_4.line_enter_master_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_state = False

    def add_chosen_db_name(self, name):
        '''
        Данная функция вызывается из другого модуля
        '''
        self.window_4.label_db_name.setText(name)


class Ui_Window_4_authorization(object):
    def setupUi(self, Window_4_authorization):
        Window_4_authorization.setObjectName("Window_4_authorization")
        Window_4_authorization.setWindowIcon(QtGui.QIcon("icons/key.ico"))
        Window_4_authorization.setEnabled(True)
        Window_4_authorization.resize(1150, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Window_4_authorization.sizePolicy().hasHeightForWidth())
        Window_4_authorization.setSizePolicy(sizePolicy)
        Window_4_authorization.setMinimumSize(QtCore.QSize(1150, 600))
        Window_4_authorization.setMaximumSize(QtCore.QSize(1150, 600))
        Window_4_authorization.setStyleSheet("background-color: rgb(185, 185, 185);\n"
                                             "")
        Window_4_authorization.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(parent=Window_4_authorization)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(450, 80, 300, 41))
        self.label.setMinimumSize(QtCore.QSize(300, 0))
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                 "\n"
                                 "font: \"MS Shell Dlg 2\";\n"
                                 "font-weight: bold;\n"
                                 "font-size: 28pt;\n"
                                 "font-color: RGB(28,28,28);\n"
                                 "color:  black;")
        self.label.setObjectName("label")
        self.btn_return_to_start = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_return_to_start.setGeometry(QtCore.QRect(950, 530, 181, 51))
        self.btn_return_to_start.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_return_to_start.setStyleSheet("QPushButton {\n"
                                               "background-color: rgba(0, 0, 0, 50);\n"
                                               "font: \"MS Shell Dlg 2\";\n"
                                               "\n"
                                               "font-size: 16pt;\n"
                                               "\n"
                                               "border-radius: 10px;\n"
                                               "}\n"
                                               "\n"
                                               "QPushButton:hover {\n"
                                               "background-color: rgba(225,225,225,200);\n"
                                               "}")
        self.btn_return_to_start.setObjectName("btn_return_to_start")
        self.line_enter_master_password = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.line_enter_master_password.setGeometry(QtCore.QRect(180, 200, 781, 51))
        self.line_enter_master_password.setToolTip("")
        self.line_enter_master_password.setStyleSheet("background-color: rgb(244, 244, 244);\n"
                                                      "font: \"MS Shell Dlg 2\";;\n"
                                                      "\n"
                                                      "\n"
                                                      "font-size: 20pt;\n"
                                                      "border-radius: 10px;")
        self.line_enter_master_password.setText("")
        self.line_enter_master_password.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.VisualMoveStyle)
        self.line_enter_master_password.setObjectName("line_enter_master_password")
        self.btn_Enter = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_Enter.setGeometry(QtCore.QRect(480, 270, 181, 51))
        self.btn_Enter.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_Enter.setStyleSheet("QPushButton {\n"
                                     "background-color: rgba(0, 0, 0, 50);\n"
                                     "font: \"MS Shell Dlg 2\";\n"
                                     "\n"
                                     "font-size: 20pt;\n"
                                     "\n"
                                     "border-radius: 10px;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover {\n"
                                     "background-color: rgba(225,225,225,200);\n"
                                     "}")
        self.btn_Enter.setObjectName("btn_Enter")
        self.btn_eye = QtWidgets.QToolButton(parent=self.centralwidget)
        self.btn_eye.setGeometry(QtCore.QRect(970, 200, 51, 51))
        self.btn_eye.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_eye.setStyleSheet("QToolButton {\n"
                                   "background-color: rgba(0, 0, 0, 0);\n"
                                   "font: \"MS Shell Dlg 2\";\n"
                                   "\n"
                                   "\n"
                                   "\n"
                                   "border-radius: 25px;\n"
                                   "}\n"
                                   "\n"
                                   "QToolButton:hover {\n"
                                   "background-color: rgba(225,225,225,200);\n"
                                   "}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('icons/eye.png'), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_eye.setIcon(icon)
        self.btn_eye.setIconSize(QtCore.QSize(40, 40))
        self.btn_eye.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.btn_eye.setObjectName("btn_eye")
        self.btn_Again = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_Again.setGeometry(QtCore.QRect(800, 530, 131, 51))
        self.btn_Again.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_Again.setStyleSheet("QPushButton {\n"
                                     "background-color: rgba(0, 0, 0, 50);\n"
                                     "font: \"MS Shell Dlg 2\";\n"
                                     "\n"
                                     "font-size: 16pt;\n"
                                     "\n"
                                     "border-radius: 10px;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover {\n"
                                     "background-color: rgba(225,225,225,200);\n"
                                     "}")
        self.btn_Again.setObjectName("btn_Again")
        self.label_db_name = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_db_name.setGeometry(QtCore.QRect(180, 160, 591, 31))
        self.label_db_name.setMinimumSize(QtCore.QSize(100, 0))
        self.label_db_name.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                         "color: rgb(72, 72, 72);\n"
                                         "\n"
                                         "font: \"MS Shell Dlg 2\";\n"
                                         "font-size: 16pt;\n"
                                         "\n"
                                         "\n"
                                         "")
        self.label_db_name.setObjectName("label_db_name")
        Window_4_authorization.setCentralWidget(self.centralwidget)

        self.retranslateUi(Window_4_authorization)
        QtCore.QMetaObject.connectSlotsByName(Window_4_authorization)

    def retranslateUi(self, Window_4_authorization):
        _translate = QtCore.QCoreApplication.translate
        Window_4_authorization.setWindowTitle(_translate("Window_4_authorization", "PasswordManager"))
        self.label.setText(_translate("Window_4_authorization", "Authorization"))
        self.btn_return_to_start.setText(_translate("Window_4_authorization", "Return to start"))
        self.line_enter_master_password.setPlaceholderText(
            _translate("Window_4_authorization", " enter master password"))
        self.btn_Enter.setText(_translate("Window_4_authorization", "Enter"))
        self.btn_eye.setText(_translate("Window_4_authorization", "..."))
        self.btn_Again.setText(_translate("Window_4_authorization", "Again"))
        self.label_db_name.setText(_translate("Window_4_authorization", ""))


