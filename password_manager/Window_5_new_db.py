from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit
from data import Data
import os
from encryption import Encryption


class Window_5_new_db_functional(QMainWindow):
    """
    Класс содержит функционал окна 5, где пользователь вводит название и придумывет
    мастер-пароль для новой БД. Кнопка "Create" появляется только после заполнения полей
    """
    def __init__(self):
        super(Window_5_new_db_functional, self).__init__()
        self.window__1 = None
        self.window__G = None
        self.window__7 = None
        self.window__9 = None
        self.need_and_name = (False, None, None)
        self.window_5 = Ui_Window_5_new_db()
        self.window_5.setupUi(self)
        self.db = Data()
        self.crypto = Encryption()

        self.set_default_state()
        self.window_5.btn_return_to_start.clicked.connect(self.again)
        self.window_5.btn_generate.clicked.connect(self.generate_master_password)
        self.window_5.btn_hide_show.clicked.connect(self.hide_or_show_password)
        self.window_5.btn_create.clicked.connect(self.create_db)
        self.window_5.btn_OK.clicked.connect(self.create_new_note)

        self.window_5.enter_db_name.textChanged.connect(self.tracking_db_name)
        self.window_5.enter_master_password.textChanged.connect(self.tracking_master_password)

    general_state_db_name = False
    general_state_master_password = False
    finish_new_db_name = None

    def set_default_state(self):
        '''
        Функция возвращает параметры окна 5 в начальное состояние
        '''
        self.is_db = False
        self.window_5.enter_master_password.setEchoMode(QLineEdit.EchoMode.Normal)
        self.window_5.btn_return_to_start.setText('Return to start')
        self.window_5.btn_create.hide()
        self.window_5.btn_hide_show.show()
        self.window_5.btn_generate.show()
        self.window_5.enter_master_password.show()
        self.window_5.label.show()
        self.window_5.enter_db_name.show()
        self.window_5.enter_master_password.setText('')
        self.window_5.enter_db_name.setText('')
        self.window_5.btn_OK.hide()
        self.window_5.lbl_successful.hide()
        self.set_border_color(self.window_5.enter_db_name, '(244, 244, 244)')
        self.set_border_color(self.window_5.enter_master_password, '(244, 244, 244)')

    def set_border_color(self, field, color_css):
        field.setStyleSheet(f"background-color: rgb(244, 244, 244);\n"
                                                          f"border: 3px solid rgb{color_css};\n"
                                                          "font-size: 20pt;\n"
                                                          "border-radius: 10px;")

    def tracking_db_name(self):
        '''
        Функция динамически проверяет введённые данные в поле имени БД.
        Если введённое название соответствует всем требованиям (обрамление поля зелёное),
        то она задаёт атрибуту general_state_db_name значение True
        '''
        invalid_folder_chars_db_name = ('!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '[', ']', '{', '}',
                          '|', '\\', '/', '<', '>', '?', ',', '.', ':', ';', '"', "'", '`', '~', ' ', '«', '»', '—')
        invalid_chars_signal = None
        new_db_name_now = self.window_5.enter_db_name.text()
        for i in new_db_name_now:
            if i not in invalid_folder_chars_db_name:
                invalid_chars_signal = True
            else:
                invalid_chars_signal = False
                break

        if len(new_db_name_now) > 2 and invalid_chars_signal == True:
            self.general_state_db_name = True
            self.set_border_color(self.window_5.enter_db_name, '(0,160,0)')
        elif len(new_db_name_now) == 0:
            self.general_state_db_name = False
            self.set_border_color(self.window_5.enter_db_name, '(244, 244, 244)')
        else:
            self.general_state_db_name = False
            self.set_border_color(self.window_5.enter_db_name, '(255,0,0)')
        self.btn_create_state()

    def tracking_master_password(self):
        '''
               Функция динамически проверяет введённые данные в поле мастер-пароля.
               Если введённый пароль соответствует всем требованиям (обрамление поля зелёное),
               то она задаёт атрибуту general_state_master_password значение True
               '''
        invalid_folder_chars_master_password = (' ', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+',
                                                '=', '[', ']', '{', '}', '|', '\\', ';', ':', "'", '"', '<', '>', ',',
                                                '.', '/', '?', '~', '`',
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                                                'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
    'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х',
                                                'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я')
        invalid_chars_signal = None
        master_password_now = self.window_5.enter_master_password.text()
        for i in master_password_now:
            if i not in invalid_folder_chars_master_password:
                invalid_chars_signal = True
            else:
                invalid_chars_signal = False
                break

        if len(master_password_now) > 8 and invalid_chars_signal == True:
            self.general_state_master_password = True
            self.set_border_color(self.window_5.enter_master_password, '(0,160,0)')
        elif len(master_password_now) == 0:
            self.general_state_master_password = False
            self.set_border_color(self.window_5.enter_master_password, '(244, 244, 244)')
        else:
            self.general_state_master_password = False
            self.set_border_color(self.window_5.enter_master_password, '(255,0,0)')
        self.btn_create_state()

    def btn_create_state(self):
        '''
        Функция отслеживает состояние полей ввода и в зависимости от него показывает
        или убирает кнопку Create. Данная кнопка появляется, если оба поля имеют
        зелёное обрамление, т.е. данные в них введены корректно
        '''
        if self.general_state_master_password == True and self.general_state_db_name == True:
            self.window_5.btn_create.show()
        else:
            self.window_5.btn_create.hide()

    def cleen_db_name_field(self):
        self.window_5.enter_db_name.setText('')

    def create_db(self):
        self.finish_master_password = self.window_5.enter_master_password.text()
        self.finish_new_db_name = self.window_5.enter_db_name.text()
        if os.path.isfile(f'{os.getcwd()}/Database/{self.finish_new_db_name}.db'):
            self.window_6_incorrect_name = QMessageBox()
            self.window_6_incorrect_name.setWindowTitle('Incorrect name')
            self.window_6_incorrect_name.setText('A database with the same name already exists. Please enter another name')
            self.window_6_incorrect_name.setIcon(QMessageBox.Icon.Warning)
            self.window_6_incorrect_name.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.window_6_incorrect_name.buttonClicked.connect(self.cleen_db_name_field)
            self.window_6_incorrect_name.exec()
        else:
            self.db.create_new_db(self.finish_new_db_name)
            self.need_and_name = (True, self.finish_new_db_name, self.finish_master_password)
            self.is_db = True
            self.window_5.btn_create.hide()
            self.window_5.enter_master_password.hide()
            self.window_5.enter_db_name.hide()
            self.window_5.btn_generate.hide()
            self.window_5.btn_hide_show.hide()
            self.window_5.label.hide()

            self.window_5.btn_OK.show()
            self.window_5.lbl_successful.show()

    def create_new_note(self):
        self.window__1.road_map_list.append(5)
        self.window__7.set_default_state()
        self.window__7.need_and_name = (True, self.finish_new_db_name, self.finish_master_password)
        self.window__7.password_for_encryption = self.finish_master_password
        self.window__9.password_for_encryption = self.finish_master_password
        self.window__7.show()
        self.set_default_state()
        self.need_and_name = (False, None, None)
        self.close()

    def again(self):
        if self.window__1.road_map_list[-1] in [1, 11]:
            if self.is_db:
                self.crypto.encrypt_file(self.finish_new_db_name, self.finish_master_password)
            self.set_default_state()
            self.window__1.road_map_list.append(5)
            self.window__1.show()
            self.need_and_name = (False, None, None)
            self.close()

    def generate_master_password(self):
        '''
        При уходе в окно генерации пароля не нужно отмечаться в road_map_list
        '''
        self.window__G.set_default_state('password_db', 'Master password for new database')
        self.window__G.show()
        self.close()

    def hide_or_show_password(self):
        '''
        Функция заменяет символы на точки в целях приватности
        '''
        if self.window_5.enter_master_password.echoMode() is QLineEdit.EchoMode.Normal:
            self.window_5.enter_master_password.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.window_5.enter_master_password.setEchoMode(QLineEdit.EchoMode.Normal)


class Ui_Window_5_new_db(object):
    def setupUi(self, Window_5_new_db):
        Window_5_new_db.setObjectName("Window_5_new_db")
        Window_5_new_db.setEnabled(True)
        Window_5_new_db.resize(1150, 600)
        Window_5_new_db.setWindowIcon(QtGui.QIcon("icons/key.ico"))
        Window_5_new_db.setMinimumSize(QtCore.QSize(1150, 600))
        Window_5_new_db.setMaximumSize(QtCore.QSize(1150, 600))
        Window_5_new_db.setStyleSheet("background-color: rgb(185, 185, 185);\n"
"")
        self.centralwidget = QtWidgets.QWidget(parent=Window_5_new_db)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 70, 651, 51))
        self.label.setMinimumSize(QtCore.QSize(300, 0))
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"font-weight: bold;\n"
"font-size: 20pt;\n"
"font-color: RGB(28,28,28);\n"
"color:  black;")
        self.label.setObjectName("label")
        self.btn_create = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_create.setGeometry(QtCore.QRect(470, 390, 201, 81))
        self.btn_create.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_create.setStyleSheet("QPushButton {\n"
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
        self.btn_create.setObjectName("btn_create")
        self.btn_return_to_start = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_return_to_start.setGeometry(QtCore.QRect(970, 530, 161, 51))
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
        self.btn_return_to_start.setObjectName("btn_again")
        self.lbl_successful = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_successful.setGeometry(QtCore.QRect(80, 190, 981, 81))
        self.lbl_successful.setMinimumSize(QtCore.QSize(300, 0))
        self.lbl_successful.setStyleSheet("background-color: rgba(0, 0, 0, 50);\n"
"font: \"MS Shell Dlg 2\";\n"
"border-radius: 10px;\n"
"font-weight: bold;\n"
"font-size: 27pt;\n"
"font-color: RGB(28,28,28);\n"
"")
        self.lbl_successful.setObjectName("lbl_successful")
        self.btn_OK = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_OK.setGeometry(QtCore.QRect(470, 390, 201, 81))
        self.btn_OK.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_OK.setStyleSheet("QPushButton {\n"
"background-color: rgba(0, 0, 0, 50);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 35pt;\n"
"\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_OK.setObjectName("btn_OK")
        self.enter_db_name = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.enter_db_name.setGeometry(QtCore.QRect(180, 170, 781, 51))
        self.enter_db_name.setToolTip("")
        self.enter_db_name.setStyleSheet("background-color: rgb(244, 244, 244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 20pt;\n"
"border-radius: 10px;")
        self.enter_db_name.setText("")
        self.enter_db_name.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.VisualMoveStyle)
        self.enter_db_name.setObjectName("enter_db_name")
        self.enter_master_password = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.enter_master_password.setGeometry(QtCore.QRect(180, 240, 781, 51))
        self.enter_master_password.setToolTip("")
        self.enter_master_password.setStyleSheet("background-color: rgb(244, 244, 244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 20pt;\n"
"border-radius: 10px;")
        self.enter_master_password.setText("")
        self.enter_master_password.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.VisualMoveStyle)
        self.enter_master_password.setObjectName("line_enter_master_password")
        self.btn_hide_show = QtWidgets.QToolButton(parent=self.centralwidget)
        self.btn_hide_show.setGeometry(QtCore.QRect(970, 240, 51, 51))
        self.btn_hide_show.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_hide_show.setStyleSheet("QToolButton {\n"
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
        self.btn_hide_show.setIcon(icon)
        self.btn_hide_show.setIconSize(QtCore.QSize(40, 40))
        self.btn_hide_show.setObjectName("btn_hide_show")
        self.btn_generate = QtWidgets.QToolButton(parent=self.centralwidget)
        self.btn_generate.setGeometry(QtCore.QRect(120, 240, 51, 51))
        self.btn_generate.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_generate.setStyleSheet("QToolButton {\n"
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap('icons/G.png'), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_generate.setIcon(icon1)
        self.btn_generate.setIconSize(QtCore.QSize(30, 30))
        self.btn_generate.setObjectName("btn_generate")
        Window_5_new_db.setCentralWidget(self.centralwidget)

        self.retranslateUi(Window_5_new_db)
        QtCore.QMetaObject.connectSlotsByName(Window_5_new_db)

    def retranslateUi(self, Window_5_new_db):
        _translate = QtCore.QCoreApplication.translate
        Window_5_new_db.setWindowTitle(_translate("Window_5_new_db", "PasswordManager"))
        self.label.setText(_translate("Window_5_new_db", "Create a name and password for the new database"))
        self.btn_create.setText(_translate("Window_5_new_db", "Create "))
        self.btn_return_to_start.setText(_translate("Window_5_new_db", "Return to start"))
        self.lbl_successful.setText(_translate("Window_5_new_db", "   The database was created successfully. Add first entry?"))
        self.btn_OK.setText(_translate("Window_5_new_db", "OK"))
        self.enter_db_name.setPlaceholderText(_translate("Window_5_new_db", " enter database name"))
        self.enter_master_password.setPlaceholderText(_translate("Window_5_new_db", " enter master password"))
        self.btn_hide_show.setText(_translate("Window_5_new_db", "..."))
        self.btn_generate.setText(_translate("Window_5_new_db", "..."))
