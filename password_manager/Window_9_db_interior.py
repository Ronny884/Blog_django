from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer, QCoreApplication
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QToolTip, QListWidgetItem
import pyperclip
from data import Data
from encryption import Encryption


class Window_9_db_interior_functional(QMainWindow):
    def __init__(self):
        super(Window_9_db_interior_functional, self).__init__()
        self.window_9 = Ui_Window_9_db_interior()
        self.window_9.setupUi(self)
        self.db = Data()
        self.crypto = Encryption()
        self.working_db_name = None
        self.password_for_encryption = None
        self.window__1 = None
        self.window__3 = None
        self.window__7 = None
        self.window__10 = None
        self.need_and_name = False, None, None

        self.set_default_state()
        self.window_9.search_line.textChanged.connect(self.search_note)
        self.window_9.notes_list.itemClicked.connect(self.handle_note_item_click)
        self.window_9.categories_list.itemClicked.connect(self.handle_category_item_click)
        self.window_9.btn_add_new_note.clicked.connect(self.add_new_note)
        self.window_9.btn_return_to_start.clicked.connect(self.return_to_start)
        self.window_9.btn_back_to_db_list.clicked.connect(self.back_to_db_list)
        self.window_9.btn_copy_password.clicked.connect(self.copy_password)
        self.window_9.btn_copy_login.clicked.connect(self.copy_login)
        self.window_9.btn_open_a_note.clicked.connect(self.open_a_note)

    def set_default_state(self):
        '''
        Вызывается в некоторых случаях при выходе из окна 9 и входе в него из другого окна
        (кроме случая, когда в окне 7 нажата Again)
        '''
        self.window_9.search_line.setText('')
        self.category_selected = False
        self.window_9.groupBox_for_note.hide()
        self.window_9.categories_list.clear()
        if self.working_db_name is not None:
            try:
                self.filling_in_the_list_of_notes(None)
                self.category_list = list(set(self.db.select_all_categories(self.working_db_name)))
                if ''.join(self.category_list) != '':
                    self.window_9.groupBox_categories.setTitle(" Categories:")
                    self.window_9.search_line.setPlaceholderText(" search in all categories")
                    item = QListWidgetItem('  Ignore categories')
                    item.setForeground(QColor("black"))
                    self.window_9.categories_list.addItem(item)
                    for category_name in self.category_list:
                        if category_name != '':
                            self.window_9.categories_list.addItem('  ' + category_name)
                else:
                    self.window_9.search_line.setPlaceholderText(" enter a note name for search")
                    self.window_9.groupBox_categories.setTitle(" No categories")

            except:
                # если при самом начале работы с БД произошли неполадки и какая-либо функция получения данных из БД
                # вернула False (например, если каким-то образом оказалась изменена структура БД), то на этапе
                # обновления окна следует оповестить пользователя и вернуться к окну списка баз
                self.window_db_error('There were problems opening the database', self.back_to_db_list())

    def showEvent(self, event):
        self.need_and_name = True, self.working_db_name, self.password_for_encryption

    def window_db_error(self, text, func):
        self.error_window = QMessageBox()
        self.error_window.setWindowTitle('DataBaseError')
        self.error_window.setText(text)
        self.error_window.setIcon(QMessageBox.Icon.Warning)
        self.error_window.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.error_window.buttonClicked.connect(func)
        self.error_window.exec()

    def open_a_note(self):
        try:
            self.window__1.road_map_list.append(9)
            self.need_and_name = False, None, None
            self.window__10.set_default_state()
            self.window__10.show()
            self.close()
        except:
            self.set_default_state()

    def filling_in_the_list_of_notes(self, category_parametr):
        self.window_9.notes_list.clear()
        self.window_9.notes_list.setFont(QFont("MS Shell Dlg 2", 20))
        self.note_name_list = self.db.select_notes_with_or_without_category(self.working_db_name, category_parametr)
        for note_name in self.note_name_list:
            self.window_9.notes_list.addItem(' ' + note_name)

    def search_note(self):
        try:
            self.window_9.notes_list.clear()
            text = self.window_9.search_line.text()
            for note_name in self.note_name_list:
                if text.strip().lower() in note_name.lower():
                    self.window_9.notes_list.addItem(' ' + note_name)
        except:
            self.set_default_state()

    def handle_note_item_click(self, item, name=None):
        try:
            if name is None:
                self.chosen_note_name = item.text().strip()
            else:
                self.chosen_note_name = name

            self.chosen_note_id = self.db.select_parameter_for_copy(self.working_db_name, self.chosen_note_name, 'id')
            if len(self.chosen_note_name) > 12:
                self.short_chosen_note_name = self.chosen_note_name[0:10] + '... '
                self.window_9.groupBox_for_note.setTitle(' ' + self.short_chosen_note_name + ':')
            else:
                self.window_9.groupBox_for_note.setTitle(' ' + self.chosen_note_name + ':')
            self.window_9.groupBox_for_note.show()
        except:
            self.set_default_state()

    def handle_category_item_click(self, item):
        try:
            self.window_9.search_line.setText('')
            self.window_9.groupBox_for_note.hide()
            self.chosen_category_name = item.text().strip()
            if self.chosen_category_name == 'Ignore categories':
                self.window_9.search_line.setPlaceholderText(" search in all categories")
                self.filling_in_the_list_of_notes(None)
                self.category_selected = False
            else:
                self.window_9.search_line.setPlaceholderText(f' search in "{self.chosen_category_name}"')
                self.filling_in_the_list_of_notes(self.chosen_category_name)
                self.category_selected = True
        except:
            self.set_default_state()

    def add_chosen_db_name(self, name):
        '''
        Данная функция вызывается из другого модуля
        '''
        self.window_9.label_db_name.setText(name)

    def add_new_note(self):
        '''
        Перенаправляет в окно 7, в котором должна появиться кнопка Again. set_default_state окна 9 вызывать не нужно,
        поскольку нам не требуется обнуление всех параметров после добавления заметки
        '''
        self.window__1.road_map_list.append(9)
        self.need_and_name = False, None, None
        self.window__7.set_default_state()
        self.window__7.show()
        self.close()

    def return_to_start(self):
        self.set_default_state()
        self.window__1.road_map_list.append(9)
        self.crypto.encrypt_file(self.need_and_name[1], self.need_and_name[2])
        self.need_and_name = False, None, None
        self.window__1.show()
        self.close()

    def back_to_db_list(self):
        self.set_default_state()
        self.window__1.road_map_list.append(9)
        self.crypto.encrypt_file(self.need_and_name[1], self.need_and_name[2])
        self.need_and_name = False, None, None
        self.window__3.set_default_state()
        self.window__3.show()
        self.close()

    def copy_password(self):
        try:
            pyperclip.copy(self.db.select_parameter_for_copy(self.working_db_name, self.chosen_note_name, 'password'))
            self.copy_information('Copied', self.window_9.btn_copy_password)
        except:
            self.set_default_state()

    def copy_login(self):
        try:
            login = self.db.select_parameter_for_copy(self.working_db_name, self.chosen_note_name, 'login')
            if login == '':
                self.copy_information('Login not found', self.window_9.btn_copy_login)
            else:
                pyperclip.copy(login)
                self.copy_information('Copied', self.window_9.btn_copy_login)
        except:
            self.set_default_state()

    def copy_information(self, text, btn):
        QCoreApplication.processEvents()
        tooltip = QToolTip
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor())
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor())
        tooltip.setFont(QFont("Arial", 10))
        tooltip.setPalette(palette)
        tooltip.showText(btn.mapToGlobal(btn.rect().bottomLeft()), text, btn)
        QTimer.singleShot(2000, tooltip.hideText)


class Ui_Window_9_db_interior(object):
    def setupUi(self, Window_9_db_interior):
        Window_9_db_interior.setObjectName("Window_9_db_interior")
        Window_9_db_interior.setEnabled(True)
        Window_9_db_interior.setWindowIcon(QtGui.QIcon("icons/key.ico"))
        Window_9_db_interior.resize(1150, 600)
        Window_9_db_interior.setMinimumSize(QtCore.QSize(1150, 600))
        Window_9_db_interior.setMaximumSize(QtCore.QSize(1150, 600))
        Window_9_db_interior.setStyleSheet("background-color: rgb(185, 185, 185);\n"
"")
        Window_9_db_interior.setIconSize(QtCore.QSize(25, 25))
        Window_9_db_interior.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(parent=Window_9_db_interior)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_return_to_start = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_return_to_start.setGeometry(QtCore.QRect(700, 510, 151, 41))
        self.btn_return_to_start.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_return_to_start.setStyleSheet("QPushButton {\n"
"background-color: rgba(0, 0, 0, 50);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 14pt;\n"
"\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_return_to_start.setObjectName("btn_return_to_start")
        self.search_line = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.search_line.setGeometry(QtCore.QRect(331, 61, 521, 41))
        self.search_line.setToolTip("")
        self.search_line.setStyleSheet("background-color: rgb(244, 244, 244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 20pt;\n"
"border-radius: 10px;")
        self.search_line.setText("")
        self.search_line.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.VisualMoveStyle)
        self.search_line.setObjectName("search_line")
        self.btn_search = QtWidgets.QToolButton(parent=self.centralwidget)
        self.btn_search.setGeometry(QtCore.QRect(860, 60, 41, 41))
        self.btn_search.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('icons/search.png'), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_search.setIcon(icon)
        self.btn_search.setIconSize(QtCore.QSize(35, 35))
        self.btn_search.setObjectName("btn_search")
        self.notes_list = QtWidgets.QListWidget(parent=self.centralwidget)
        self.notes_list.setGeometry(QtCore.QRect(330, 120, 521, 371))
        self.notes_list.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.notes_list.setStyleSheet("background-color: rgba(0, 0, 0, 40);\n"
"color: rgb(70,70,70);\n"
"border-radius: 10px;")
        self.notes_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.notes_list.setObjectName("notes_list")
        self.btn_back_to_db_list = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_back_to_db_list.setGeometry(QtCore.QRect(460, 510, 221, 41))
        self.btn_back_to_db_list.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_back_to_db_list.setStyleSheet("QPushButton {\n"
"background-color: rgba(0, 0, 0, 50);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 14pt;\n"
"\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_back_to_db_list.setObjectName("btn_back_to_db_list")
        self.btn_add_new_note = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_add_new_note.setGeometry(QtCore.QRect(50, 510, 391, 61))
        self.btn_add_new_note.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_add_new_note.setStyleSheet("QPushButton {\n"
"background-color: rgba(0, 0, 0, 50);\n"
"font: \"MS Shell Dlg 2\";\n"
"font-size: 18pt;\n"
"border-radius: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_add_new_note.setObjectName("btn_add_new_note")
        self.groupBox_for_note = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_for_note.setGeometry(QtCore.QRect(870, 120, 231, 371))
        self.groupBox_for_note.setStyleSheet("background-color: rgba(0, 0, 0, 20);\n"
"border-radius: 10px;\n"
"font-size: 20pt;")
        self.groupBox_for_note.setObjectName("groupBox_for_note")
        self.btn_open_a_note = QtWidgets.QPushButton(parent=self.groupBox_for_note)
        self.btn_open_a_note.setGeometry(QtCore.QRect(20, 240, 191, 111))
        self.btn_open_a_note.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_open_a_note.setStyleSheet("QPushButton {\n"
"background-color: rgba(0, 0, 0, 50);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 18pt;\n"
"\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_open_a_note.setObjectName("btn_open_a_note")
        self.btn_copy_login = QtWidgets.QPushButton(parent=self.groupBox_for_note)
        self.btn_copy_login.setGeometry(QtCore.QRect(20, 150, 191, 71))
        self.btn_copy_login.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_copy_login.setStyleSheet("QPushButton {\n"
"background-color: rgba(0, 0, 0, 50);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 14pt;\n"
"\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_copy_login.setObjectName("btn_copy_login")
        self.btn_copy_password = QtWidgets.QPushButton(parent=self.groupBox_for_note)
        self.btn_copy_password.setGeometry(QtCore.QRect(20, 60, 191, 71))
        self.btn_copy_password.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_copy_password.setStyleSheet("QPushButton {\n"
"background-color: rgba(0, 0, 0, 50);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 14pt;\n"
"\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_copy_password.setObjectName("btn_copy_password")
        self.groupBox_categories = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_categories.setGeometry(QtCore.QRect(50, 120, 261, 371))
        self.groupBox_categories.setStyleSheet("background-color: rgba(0, 0, 0, 20);\n"
"border-radius: 10px;\n"
"font-size: 20pt;")
        self.groupBox_categories.setObjectName("groupBox_categories")
        self.categories_list = QtWidgets.QListWidget(parent=self.groupBox_categories)
        self.categories_list.setGeometry(QtCore.QRect(20, 60, 221, 291))
        self.categories_list.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.categories_list.setStyleSheet("background-color: rgba(0, 0, 0, 40);\n"
"border-radius: 10px;\n"
"color: rgb(60,60,60);\n"
"font-size: 17pt;")
        self.categories_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.categories_list.setObjectName("categories_list")
        self.label_db_name = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_db_name.setGeometry(QtCore.QRect(20, 20, 371, 31))
        self.label_db_name.setStyleSheet("font: \"MS Shell Dlg 2\";\n"
"font-size: 18pt;\n"
"font: bold;")
        self.label_db_name.setObjectName("label_db_name")
        Window_9_db_interior.setCentralWidget(self.centralwidget)

        self.retranslateUi(Window_9_db_interior)
        QtCore.QMetaObject.connectSlotsByName(Window_9_db_interior)

    def retranslateUi(self, Window_9_db_interior):
        _translate = QtCore.QCoreApplication.translate
        Window_9_db_interior.setWindowTitle(_translate("Window_9_db_interior", "PasswordManager"))
        self.btn_return_to_start.setText(_translate("Window_9_db_interior", "Return to start"))
        self.search_line.setPlaceholderText(_translate("Window_9_db_interior", " search in all categories"))
        self.btn_search.setText(_translate("Window_9_db_interior", "..."))
        self.btn_back_to_db_list.setText(_translate("Window_9_db_interior", "Back to database list"))
        self.btn_add_new_note.setText(_translate("Window_9_db_interior", "Add a new note"))
        self.groupBox_for_note.setTitle(_translate("Window_9_db_interior", " For note:"))
        self.btn_open_a_note.setText(_translate("Window_9_db_interior", "Open a note"))
        self.btn_copy_login.setText(_translate("Window_9_db_interior", "Copy login"))
        self.btn_copy_password.setText(_translate("Window_9_db_interior", "Copy password"))
        self.groupBox_categories.setTitle(_translate("Window_9_db_interior", " Categories:"))
        self.label_db_name.setText(_translate("Window_9_db_interior", "TextLabel"))


