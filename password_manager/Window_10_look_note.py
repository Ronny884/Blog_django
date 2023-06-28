from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMessageBox
import pyperclip
from data import Data


class Window_10_look_note_functional(QMainWindow):
    def __init__(self):
        super(Window_10_look_note_functional, self).__init__()
        self.window_10 = Ui_Window_10_look_note()
        self.window_10.setupUi(self)
        self.db = Data()
        self.window__1 = None
        self.window__7 = None
        self.window__9 = None
        self.need_and_name = False, None, None

        self.window_10.btn_OK.clicked.connect(self.push_btn_OK)
        self.window_10.btn_Edit_note.clicked.connect(self.edit_note)
        self.window_10.btn_Delete_note.clicked.connect(self.delete_note)

        self.window_10.btn_copy_username.clicked.connect(self.copy_username)
        self.window_10.btn_copy_password.clicked.connect(self.copy_password)
        self.window_10.btn_copy_login.clicked.connect(self.copy_login)
        self.window_10.btn_copy_passphrase.clicked.connect(self.copy_passphrase)
        self.window_10.btn_copy_phone_number.clicked.connect(self.copy_phone_number)
        self.window_10.btn_copy_url.clicked.connect(self.copy_url)

    def set_default_state(self):
        try:
            if self.window__1 is None or self.window__1.road_map_list[-1] == 9:
                self.main_note_name = self.window__9.chosen_note_name
            elif self.window__1.road_map_list[-1] == 7:
                self.main_note_name = self.db.get_name_by_id(self.window__9.working_db_name,
                                                             self.window__9.chosen_note_id)

            self.window_10.lbl_note_name.setText(self.main_note_name)
            self.window_10.lbl_password.setText(' ' +
                                                self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                                  self.main_note_name,
                                                                                  'password'))
            self.window_10.lbl_login.setText(' ' +
                                             self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                               self.main_note_name,
                                                                               'login'))
            self.show_or_hide_copy_btn(self.window_10.lbl_login, self.window_10.btn_copy_login,
                                       self.window_10.lbl_copy_login)

            self.window_10.lbl_username.setText(' ' +
                                                self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                                  self.main_note_name,
                                                                                  'username'))
            self.show_or_hide_copy_btn(self.window_10.lbl_username, self.window_10.btn_copy_username,
                                       self.window_10.lbl_copy_username)

            self.window_10.lbl_passphrase.setText(' ' +
                                                  self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                                    self.main_note_name,
                                                                                    'passphrase'))
            self.show_or_hide_copy_btn(self.window_10.lbl_passphrase, self.window_10.btn_copy_passphrase,
                                       self.window_10.lbl_copy_passphrase)

            self.window_10.lbl_phone_number.setText(' ' +
                                                    self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                                      self.main_note_name,
                                                                                      'phone_number'))
            self.show_or_hide_copy_btn(self.window_10.lbl_phone_number, self.window_10.btn_copy_phone_number,
                                       self.window_10.lbl_copy_phone_number)

            self.window_10.lbl_url.setText(' ' +
                                           self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                             self.main_note_name,
                                                                             'url'))
            self.show_or_hide_copy_btn(self.window_10.lbl_url, self.window_10.btn_copy_url,
                                       self.window_10.lbl_copy_url)

            self.window_10.lbl_category.setText(' ' +
                                                self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                                  self.main_note_name,
                                                                                  'category'))
        except:
            self.window__9.set_default_state()
            self.window__9.show()
            self.close()

    def showEvent(self, event):
        self.need_and_name = True, self.window__9.working_db_name, self.window__9.password_for_encryption

    def show_or_hide_copy_btn(self, field, btn, lbl):
        if field.text().strip() == '':
            btn.hide()
            lbl.show()
        else:
            btn.show()
            lbl.hide()

    def copy_username(self):
        pyperclip.copy(self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                           self.main_note_name,
                                                                           'username'))
        self.window__9.copy_information('Copied', self.window_10.btn_copy_username)

    def copy_password(self):
        pyperclip.copy(self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                           self.main_note_name,
                                                                           'password'))
        self.window__9.copy_information('Copied', self.window_10.btn_copy_password)

    def copy_login(self):
        pyperclip.copy(self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                           self.main_note_name,
                                                                           'login'))
        self.window__9.copy_information('Copied', self.window_10.btn_copy_login)

    def copy_passphrase(self):
        pyperclip.copy(self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                           self.main_note_name,
                                                                           'passphrase'))
        self.window__9.copy_information('Copied', self.window_10.btn_copy_passphrase)

    def copy_phone_number(self):
        pyperclip.copy(self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                           self.main_note_name,
                                                                           'phone_number'))
        self.window__9.copy_information('Copied', self.window_10.btn_copy_phone_number)

    def copy_url(self):
        pyperclip.copy(self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                           self.main_note_name,
                                                                           'url'))
        self.window__9.copy_information('Copied', self.window_10.btn_copy_url)

    def push_btn_OK(self):
        if self.window__1.road_map_list[-1] == 9 or \
                (self.window__1.road_map_list[-1] == 7 and self.window__7.window_9_in_previous_state is True):
            self.window__1.road_map_list.append(10)
            self.need_and_name = False, None, None
            # self.window__9.set_default_state()
            self.window__9.show()
            self.close()
        elif self.window__1.road_map_list[-1] == 7 and self.window__7.window_9_in_previous_state is False:
            self.window__1.road_map_list.append(10)
            self.need_and_name = False, None, None
            self.window__9.set_default_state()
            self.window__9.handle_note_item_click(item=None, name=self.main_note_name)
            self.window__9.show()
            self.close()

    def delete_note(self):
        self.window_11 = QMessageBox()
        self.window_11.setWindowTitle('Deleting a note')
        self.window_11.setText('Are you sure you want to completely delete this note?')
        self.window_11.setIcon(QMessageBox.Icon.Question)
        self.window_11.setStandardButtons(
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        self.window_11.buttonClicked.connect(self.push_ok)
        self.window_11.exec()

    def push_ok(self, btn):
        if btn.text() == 'OK':
            self.db.delete_note(self.window__9.working_db_name, self.main_note_name)
            self.window__1.road_map_list.append(10)
            self.need_and_name = False, None, None
            self.window__9.set_default_state()
            self.window__9.show()
            self.close()

    def edit_note(self):
        self.window__1.road_map_list.append(10)
        self.need_and_name = False, None, None
        self.window__7.set_default_state()
        self.window__7.show()
        self.hide()


class Ui_Window_10_look_note(object):
    def setupUi(self, Window_10_look_note):
        Window_10_look_note.setObjectName("Window_10_look_note")
        Window_10_look_note.setEnabled(True)
        Window_10_look_note.setWindowIcon(QtGui.QIcon("icons/key.ico"))
        Window_10_look_note.resize(1150, 600)
        Window_10_look_note.setMinimumSize(QtCore.QSize(1150, 600))
        Window_10_look_note.setMaximumSize(QtCore.QSize(1150, 600))
        Window_10_look_note.setStyleSheet("background-color: rgb(185, 185, 185);\n"
"")
        Window_10_look_note.setIconSize(QtCore.QSize(50, 50))
        Window_10_look_note.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(parent=Window_10_look_note)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 90, 191, 431))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 41))
        self.label_3.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 15pt;\n"
"font-color: RGB(28,28,28);\n"
"color: rgb(72, 72, 72);")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 41))
        self.label_4.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 15pt;\n"
"font-color: RGB(28,28,28);\n"
"color: rgb(72, 72, 72);")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 41))
        self.label_5.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 15pt;\n"
"font-color: RGB(28,28,28);\n"
"color: rgb(72, 72, 72);")
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 41))
        self.label_6.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 15pt;\n"
"font-color: RGB(28,28,28);\n"
"color: rgb(72, 72, 72);")
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 41))
        self.label_7.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 15pt;\n"
"font-color: RGB(28,28,28);\n"
"color: rgb(72, 72, 72);")
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 41))
        self.label_8.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 15pt;\n"
"font-color: RGB(28,28,28);\n"
"color: rgb(72, 72, 72);")
        self.label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 41))
        self.label_9.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 15pt;\n"
"font-color: RGB(28,28,28);\n"
"color: rgb(72, 72, 72);")
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.btn_Edit_note = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_Edit_note.setGeometry(QtCore.QRect(560, 520, 181, 41))
        self.btn_Edit_note.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_Edit_note.setStyleSheet("QPushButton {\n"
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
        self.btn_Edit_note.setObjectName("btn_Edit_note")
        self.btn_OK = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_OK.setGeometry(QtCore.QRect(410, 520, 131, 41))
        self.btn_OK.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_OK.setStyleSheet("QPushButton {\n"
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
        self.btn_OK.setObjectName("btn_Again")
        self.lbl_note_name = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_note_name.setGeometry(QtCore.QRect(210, 30, 771, 41))
        self.lbl_note_name.setMinimumSize(QtCore.QSize(300, 0))
        self.lbl_note_name.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"\n"
"font: \"MS Shell Dlg 2\";\n"
"font-weight: bold;\n"
"font-size: 20pt;\n"
"font-color: RGB(28,28,28);\n"
"color:  black;")
        self.lbl_note_name.setObjectName("lbl_note_name")
        self.btn_Delete_note = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_Delete_note.setGeometry(QtCore.QRect(760, 520, 181, 41))
        self.btn_Delete_note.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_Delete_note.setStyleSheet("QPushButton {\n"
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
        self.btn_Delete_note.setObjectName("btn_Delete_note")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(940, 90, 41, 371))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_copy_username = QtWidgets.QToolButton(parent=self.widget)
        self.btn_copy_username.setMaximumSize(QtCore.QSize(16777215, 41))
        self.btn_copy_username.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_copy_username.setStyleSheet("QToolButton {\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"\n"
"\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('icons/copy.png'), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_copy_username.setIcon(icon)
        self.btn_copy_username.setIconSize(QtCore.QSize(60, 60))
        self.btn_copy_username.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.btn_copy_username.setObjectName("btn_copy_username")
        self.verticalLayout_3.addWidget(self.btn_copy_username)
        self.btn_copy_password = QtWidgets.QToolButton(parent=self.widget)
        self.lbl_copy_username = QtWidgets.QLabel(parent=self.widget)
        self.lbl_copy_username.setMaximumSize(QtCore.QSize(16777215, 41))
        self.verticalLayout_3.addWidget(self.lbl_copy_username)
        self.btn_copy_password.setMaximumSize(QtCore.QSize(16777215, 41))
        self.btn_copy_password.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_copy_password.setStyleSheet("QToolButton {\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"\n"
"\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_copy_password.setIcon(icon)
        self.btn_copy_password.setIconSize(QtCore.QSize(60, 60))
        self.btn_copy_password.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.btn_copy_password.setObjectName("btn_copy_password")
        self.verticalLayout_3.addWidget(self.btn_copy_password)
        self.btn_copy_login = QtWidgets.QToolButton(parent=self.widget)
        self.lbl_copy_login = QtWidgets.QLabel(parent=self.widget)
        self.btn_copy_login.setMaximumSize(QtCore.QSize(16777215, 41))
        self.lbl_copy_login.setMaximumSize(QtCore.QSize(16777215, 41))
        # self.btn_copy_login.setMinimumSize(QtCore.QSize(41, 41))
        self.btn_copy_login.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_copy_login.setStyleSheet("QToolButton {\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"\n"
"\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_copy_login.setIcon(icon)
        self.btn_copy_login.setIconSize(QtCore.QSize(60, 60))
        self.btn_copy_login.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.btn_copy_login.setObjectName("btn_copy_login")
        self.verticalLayout_3.addWidget(self.btn_copy_login)
        self.verticalLayout_3.addWidget(self.lbl_copy_login)
        self.btn_copy_passphrase = QtWidgets.QToolButton(parent=self.widget)
        self.btn_copy_passphrase.setMaximumSize(QtCore.QSize(16777215, 41))
        self.lbl_copy_passphrase = QtWidgets.QLabel(parent=self.widget)
        self.lbl_copy_passphrase.setMaximumSize(QtCore.QSize(16777215, 41))
        self.verticalLayout_3.addWidget(self.lbl_copy_passphrase)
        self.btn_copy_passphrase.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_copy_passphrase.setStyleSheet("QToolButton {\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"\n"
"\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_copy_passphrase.setIcon(icon)
        self.btn_copy_passphrase.setIconSize(QtCore.QSize(60, 60))
        self.btn_copy_passphrase.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.btn_copy_passphrase.setObjectName("btn_copy_passphrase")
        self.verticalLayout_3.addWidget(self.btn_copy_passphrase)
        self.btn_copy_phone_number = QtWidgets.QToolButton(parent=self.widget)
        self.btn_copy_phone_number.setMaximumSize(QtCore.QSize(16777215, 41))
        self.lbl_copy_phone_number = QtWidgets.QLabel(parent=self.widget)
        self.lbl_copy_phone_number.setMaximumSize(QtCore.QSize(16777215, 41))
        self.verticalLayout_3.addWidget(self.lbl_copy_phone_number)
        self.btn_copy_phone_number.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_copy_phone_number.setStyleSheet("QToolButton {\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"\n"
"\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_copy_phone_number.setIcon(icon)
        self.btn_copy_phone_number.setIconSize(QtCore.QSize(60, 60))
        self.btn_copy_phone_number.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.btn_copy_phone_number.setObjectName("btn_copy_phone_number")
        self.verticalLayout_3.addWidget(self.btn_copy_phone_number)
        self.btn_copy_url = QtWidgets.QToolButton(parent=self.widget)
        self.btn_copy_url.setMaximumSize(QtCore.QSize(16777215, 41))
        self.lbl_copy_url = QtWidgets.QLabel(parent=self.widget)
        self.lbl_copy_url.setMaximumSize(QtCore.QSize(16777215, 41))
        self.verticalLayout_3.addWidget(self.lbl_copy_url)
        self.btn_copy_url.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_copy_url.setStyleSheet("QToolButton {\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"\n"
"\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_copy_url.setIcon(icon)
        self.btn_copy_url.setIconSize(QtCore.QSize(60, 60))
        self.btn_copy_url.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.btn_copy_url.setObjectName("btn_copy_url")
        self.verticalLayout_3.addWidget(self.btn_copy_url)
        self.widget1 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(210, 90, 731, 431))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_username = QtWidgets.QLabel(parent=self.widget1)
        self.lbl_username.setMaximumSize(QtCore.QSize(7777, 41))
        self.lbl_username.setStyleSheet("background-color: rgb(244,244,244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 15pt;\n"
"border-radius: 10px;\n"
"")
        self.lbl_username.setObjectName("lbl_username")
        self.verticalLayout.addWidget(self.lbl_username)
        self.lbl_password = QtWidgets.QLabel(parent=self.widget1)
        self.lbl_password.setMaximumSize(QtCore.QSize(16777215, 41))
        self.lbl_password.setStyleSheet("background-color: rgb(244, 244, 244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 15pt;\n"
"border-radius: 10px;\n"
"")
        self.lbl_password.setText("")
        self.lbl_password.setObjectName("lbl_password")
        self.verticalLayout.addWidget(self.lbl_password)
        self.lbl_login = QtWidgets.QLabel(parent=self.widget1)
        self.lbl_login.setMaximumSize(QtCore.QSize(16777215, 41))
        self.lbl_login.setStyleSheet("background-color: rgb(244, 244, 244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 15pt;\n"
"border-radius: 10px;\n"
"")
        self.lbl_login.setText("")
        self.lbl_login.setObjectName("lbl_login")
        self.verticalLayout.addWidget(self.lbl_login)
        self.lbl_passphrase = QtWidgets.QLabel(parent=self.widget1)
        self.lbl_passphrase.setMaximumSize(QtCore.QSize(16777215, 41))
        self.lbl_passphrase.setStyleSheet("background-color: rgb(244, 244, 244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 15pt;\n"
"border-radius: 10px;\n"
"")
        self.lbl_passphrase.setText("")
        self.lbl_passphrase.setObjectName("lbl_passphrase")
        self.verticalLayout.addWidget(self.lbl_passphrase)
        self.lbl_phone_number = QtWidgets.QLabel(parent=self.widget1)
        self.lbl_phone_number.setMaximumSize(QtCore.QSize(16777215, 41))
        self.lbl_phone_number.setStyleSheet("background-color: rgb(244, 244, 244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 15pt;\n"
"border-radius: 10px;\n"
"")
        self.lbl_phone_number.setText("")
        self.lbl_phone_number.setObjectName("lbl_phone_number")
        self.verticalLayout.addWidget(self.lbl_phone_number)
        self.lbl_url = QtWidgets.QLabel(parent=self.widget1)
        self.lbl_url.setMaximumSize(QtCore.QSize(16777215, 41))
        self.lbl_url.setStyleSheet("background-color: rgb(244, 244, 244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 15pt;\n"
"border-radius: 10px;\n"
"")
        self.lbl_url.setText("")
        self.lbl_url.setObjectName("lbl_url")
        self.verticalLayout.addWidget(self.lbl_url)
        self.lbl_category = QtWidgets.QLabel(parent=self.widget1)
        self.lbl_category.setMaximumSize(QtCore.QSize(16777215, 41))
        self.lbl_category.setStyleSheet("background-color: rgb(244, 244, 244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 15pt;\n"
"border-radius: 10px;\n"
"")
        self.lbl_category.setText("")
        self.lbl_category.setObjectName("lbl_category")
        self.verticalLayout.addWidget(self.lbl_category)
        Window_10_look_note.setCentralWidget(self.centralwidget)

        self.retranslateUi(Window_10_look_note)
        QtCore.QMetaObject.connectSlotsByName(Window_10_look_note)

    def retranslateUi(self, Window_10_look_note):
        _translate = QtCore.QCoreApplication.translate
        Window_10_look_note.setWindowTitle(_translate("Window_10_look_note", "PasswordManager"))
        self.label_3.setText(_translate("Window_10_look_note", "Username:"))
        self.label_4.setText(_translate("Window_10_look_note", "Password:"))
        self.label_5.setText(_translate("Window_10_look_note", "Login:"))
        self.label_6.setText(_translate("Window_10_look_note", "Passphrase:"))
        self.label_7.setText(_translate("Window_10_look_note", "Phone number:"))
        self.label_8.setText(_translate("Window_10_look_note", "URL:"))
        self.label_9.setText(_translate("Window_10_look_note", "Category:"))
        self.btn_Edit_note.setText(_translate("Window_10_look_note", "Edit note"))
        self.btn_OK.setText(_translate("Window_10_look_note", "OK"))
        self.btn_Delete_note.setText(_translate("Window_10_look_note", "Delete note"))
        self.btn_copy_username.setText(_translate("Window_10_look_note", "..."))
        self.btn_copy_password.setText(_translate("Window_10_look_note", "..."))
        self.btn_copy_login.setText(_translate("Window_10_look_note", "..."))
        self.btn_copy_passphrase.setText(_translate("Window_10_look_note", "..."))
        self.btn_copy_phone_number.setText(_translate("Window_10_look_note", "..."))
        self.btn_copy_url.setText(_translate("Window_10_look_note", "..."))

