from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit
from data import Data
from encryption import Encryption


class Window_7_new_note_functional(QMainWindow):
    """
    Класс содержит функционал окна 7, где пользователь вводит все необходимые данные атомарной заметки
    в базе данных. Поля Password и Name должны быть заполнены обязательно. Кнопка Add появляется только после их
    заполнения. Комбо-бокс имеет также опцию ввода текста. На окно можно придти с окна 5, 9.
    С окна можно перейти на стартовое окно 1, а так же на окно 9, если до этого мы были на нём.
    Если предыдущим окном было 9, то появляется кнопка Again
    """

    def __init__(self):
        super(Window_7_new_note_functional, self).__init__()
        self.window_7 = Ui_Window_7_new_note()
        self.window_7.setupUi(self)
        self.window__1 = None
        self.window__G = None
        self.window__9 = None
        self.window__5 = None
        self.window__10 = None
        self.password_for_encryption = None
        self.need_and_name = (False, None, None)
        self.db = Data()
        self.crypto = Encryption()

        self.set_default_state()
        self.window_7.enter_name.textChanged.connect(self.tracking_note_name)
        self.window_7.enter_password.textChanged.connect(self.tracking_note_password)
        self.window_7.eye_password.clicked.connect(lambda: self.hide_or_show_text(self.window_7.enter_password))
        self.window_7.eye_login.clicked.connect(lambda: self.hide_or_show_text(self.window_7.enter_login))
        self.window_7.eye_passphrase.clicked.connect(lambda: self.hide_or_show_text(self.window_7.enter_passphrase))
        self.window_7.btn_add_or_edit.clicked.connect(self.add_note)
        self.window_7.btn_again.clicked.connect(self.again)
        self.window_7.btn_generate_login.clicked.connect(lambda: self.generate_password_or_login('Login'))
        self.window_7.btn_generate_password.clicked.connect(lambda: self.generate_password_or_login('Password'))
        self.window_7.btn_return_to_start.clicked.connect(self.return_to_start)

    general_state_note_name = False
    general_state_note_password = False

    def set_default_state(self):
        self.window_9_in_previous_state = False

        if self.window__1 is None or self.window__1.road_map_list == [] or self.window__1.road_map_list[-1] == 5:
            self.window_7.label.setText('Adding a new note')
            self.window_7.btn_add_or_edit.setText('Add')
            self.window_7.btn_add_or_edit.hide()
            self.window_7.btn_again.hide()
            self.set_empty_line()
        elif self.window__1.road_map_list[-1] == 9:
            self.need_and_name = (True, self.window__9.working_db_name, self.window__9.password_for_encryption)
            self.password_for_encryption = self.window__9.password_for_encryption
            self.window_7.label.setText('Adding a new note')
            self.window_7.btn_add_or_edit.setText('Add')
            self.window_7.btn_add_or_edit.hide()
            self.window_7.btn_again.show()
            self.window_7.enter_choose_category.clear()
            for category in self.window__9.category_list:
                if category != '':
                    self.window_7.enter_choose_category.addItem(category)
            self.set_empty_line()
        elif self.window__1.road_map_list[-1] == 10:
            self.need_and_name = (True, self.window__9.working_db_name, self.window__9.password_for_encryption)
            self.password_for_encryption = self.window__9.password_for_encryption
            self.window_7.label.setText('Note editing')
            self.window_7.btn_add_or_edit.setText('Edit')
            self.window_7.btn_add_or_edit.show()
            self.window_7.btn_again.show()
            self.window_7.enter_name.setText(self.window__10.main_note_name)
            self.window_7.enter_username.setText(self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                                   self.window__10.main_note_name,
                                                                                   'username'))
            self.window_7.enter_password.setText(self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                                   self.window__10.main_note_name,
                                                                                   'password'))
            self.window_7.enter_login.setText(self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                                self.window__10.main_note_name,
                                                                                'login'))
            self.window_7.enter_passphrase.setText(self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                                     self.window__10.main_note_name,
                                                                                     'passphrase'))
            self.window_7.enter_phone_number.setText(self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                                       self.window__10.main_note_name,
                                                                                       'phone_number'))
            self.window_7.enter_URL.setText(self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                                              self.window__10.main_note_name,
                                                                              'url'))

            self.window_7.enter_choose_category.clear()
            for category in self.window__9.category_list:
                if category != '':
                    self.window_7.enter_choose_category.addItem(category)
            self.window_7.enter_choose_category.setCurrentText(
                self.db.select_parameter_for_copy(self.window__9.working_db_name,
                                                  self.window__10.main_note_name,
                                                  'category'))

        self.password_eye = False
        self.login_eye = False
        self.passphrase_eye = False
        self.question_result = False

        self.set_border_color_and_size(self.window_7.enter_password, '(244,244,244)', '1')
        self.set_border_color_and_size(self.window_7.enter_name, '(244,244,244)', '1')

    def set_empty_line(self):
        self.window_7.enter_name.setText('')
        self.window_7.enter_username.setText('')
        self.window_7.enter_password.setText('')
        self.window_7.enter_login.setText('')
        self.window_7.enter_passphrase.setText('')
        self.window_7.enter_phone_number.setText('')
        self.window_7.enter_URL.setText('')
        self.window_7.enter_choose_category.setCurrentText('')

    def add_note(self):
        if self.window__1.road_map_list[-1] == 5:
            target_db_name = self.window__5.finish_new_db_name
            self.window__9.working_db_name = target_db_name  # если на окно 9 первый раз мы попадаем из окна 7 по ветке
            # создания новой БД, то working_db_name надо определить. При инициализации в окне 9 она идёт как None
        elif self.window__1.road_map_list[-1] == 9 or self.window_7.btn_add_or_edit.text() == 'Edit':
            target_db_name = self.window__9.working_db_name

        name = self.window_7.enter_name.text().strip()
        username = self.window_7.enter_username.text().strip()
        password = self.window_7.enter_password.text()
        login = self.window_7.enter_login.text()
        passphrase = self.window_7.enter_passphrase.text().strip()
        phone_number = self.window_7.enter_phone_number.text().strip()
        URL = self.window_7.enter_URL.text().strip()
        category = self.window_7.enter_choose_category.currentText().strip()

        query_values = [name, username, password, login, passphrase, phone_number, URL, category]
        for i in query_values:
            empty_lines = [' ' * k for k in range(1, 100)]
            if i == '' or i in empty_lines:
                index = query_values.index(i)
                query_values.pop(index)
                query_values.insert(index, None)

        if self.window__1.road_map_list[-1] in [5, 9]:
            if self.db.repition_chek(target_db_name, name):
                self.db.add_new_note_to_target_db(target_db_name, query_values)
                self.window__1.road_map_list.append(7)
                self.window__9.add_chosen_db_name(target_db_name)
                self.window__9.set_default_state()
                self.window__9.show()
                self.need_and_name = False, None, None
                self.close()
            else:
                self.error_window = QMessageBox()
                self.error_window.setWindowTitle('RepitionError')
                self.error_window.setText('A note with the same name already exists. Please, come up with a different '
                                          'name, it is necessary for the correct operation of the program')
                self.error_window.setIcon(QMessageBox.Icon.Warning)
                self.error_window.setStandardButtons(QMessageBox.StandardButton.Ok)
                self.error_window.exec()
                self.window_7.enter_name.setText('')

        else:
            query_values.append(self.window__9.chosen_note_id)
            self.db.update_note(target_db_name, query_values)
            self.window__1.road_map_list.append(7)
            self.window__10.set_default_state()
            self.need_and_name = False, None, None
            self.window__10.show()
            self.close()

    def again(self):
        '''
        Возвращает в окно 9 (сама кнопка появляется только в том случае, если мы пришли с окна 9)
        '''
        if self.window__1.road_map_list[-1] == 9:
            if self.string_checking_and_confirmation():
                # self.set_default_state()
                self.window__1.road_map_list.append(7)
                self.need_and_name = False, None, None
                self.window__9.show()
                self.close()
        elif self.window__1.road_map_list[-1] == 10:
            self.window_8_2 = QMessageBox()
            self.window_8_2.setWindowTitle('Changes will not be saved')
            self.window_8_2.setText('Changes will not be saved when reverting. Would you like to continue?')
            self.window_8_2.setIcon(QMessageBox.Icon.Question)
            self.window_8_2.setStandardButtons(
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            self.window_8_2.buttonClicked.connect(self.push_ok_2)
            self.window_8_2.exec()

    def return_to_start(self):
        if self.string_checking_and_confirmation():
            # self.set_default_state()
            self.window__1.road_map_list.append(7)
            self.crypto.encrypt_file(self.need_and_name[1], self.need_and_name[2])
            self.need_and_name = False, None, None
            self.window__1.show()
            self.close()

    def window_8_question(self):
        self.window_8_1 = QMessageBox()
        self.window_8_1.setWindowTitle('Data will not be saved')
        self.window_8_1.setText('When you return to the beginning or to the previous step, '
                                'the data you entered for this note '
                                'will not be saved. Would you like to continue?')
        self.window_8_1.setIcon(QMessageBox.Icon.Warning)
        self.window_8_1.setStandardButtons(
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        self.window_8_1.buttonClicked.connect(self.push_ok_1)
        self.window_8_1.exec()

    def push_ok_1(self, btn):
        if btn.text() == 'OK':
            self.question_result = True
        else:
            self.question_result = False

    def push_ok_2(self, btn):
        if btn.text() == 'OK':
            self.window__1.road_map_list.append(7)
            self.need_and_name = False, None, None
            self.window_9_in_previous_state = True
            # self.window__10.set_default_state()
            self.window__10.show()
            self.close()

    def string_checking_and_confirmation(self):
        '''
        Функция проверяет, пусты ли все поля одновременно. Если пусты, то возвращает True, разрешая возвращаться
        назад или в начало без дополнительных подтверждений. Если же хоть одно поле не пустое, вызывается
        всплывающее окно 8, при нажатии на котором кнопки ОК переменная question_result принимает True, что также
        является условием для возврата True функцией string_checking
        '''
        if (self.window_7.enter_name.text() == '' and
                self.window_7.enter_username.text() == '' and
                self.window_7.enter_password.text() == '' and
                self.window_7.enter_login.text() == '' and
                self.window_7.enter_passphrase.text() == '' and
                self.window_7.enter_phone_number.text() == '' and
                self.window_7.enter_URL.text() == '' and
                self.window_7.enter_choose_category.currentText() == ''):
            return True
        else:
            self.window_8_question()
            if self.question_result:
                return True

    def set_border_color_and_size(self, field, color_css, size):
        field.setStyleSheet(f"background-color: rgb(244, 244, 244);\n"
                            "font: \"MS Shell Dlg 2\";;\n"
                            "\n"
                            f"border: {size}px solid rgb{color_css};\n"
                            "font-size: 15pt;\n"
                            "border-radius: 10px;")

    def tracking_note_name(self):
        new_note_name_now = self.window_7.enter_name.text()
        empty_lines = [' ' * k for k in range(1, 100)]
        if len(new_note_name_now) > 0 and new_note_name_now not in empty_lines:
            self.set_border_color_and_size(self.window_7.enter_name, '(0,200,0)', '2')
            self.general_state_note_name = True
        else:
            self.set_border_color_and_size(self.window_7.enter_name, '(244,244,244)', '1')
            self.general_state_note_name = False
        self.btn_add_state()

    def tracking_note_password(self):
        new_note_password_now = self.window_7.enter_password.text()
        empty_lines = [' ' * k for k in range(1, 100)]
        if len(new_note_password_now) > 0 and new_note_password_now not in empty_lines:
            self.set_border_color_and_size(self.window_7.enter_password, '(0,200,0)', '2')
            self.general_state_note_password = True
        else:
            self.set_border_color_and_size(self.window_7.enter_password, '(244,244,244)', '1')
            self.general_state_note_password = False
        self.btn_add_state()

    def btn_add_state(self):
        '''
        Функция отслеживает состояние полей ввода и в зависимости от него показывает
        или убирает кнопку Add. Данная кнопка появляется, если оба обязательных поля имеют
        зелёное обрамление, т.е. данные в них введены
        '''
        if self.general_state_note_password == True and self.general_state_note_name == True:
            self.window_7.btn_add_or_edit.show()
        else:
            self.window_7.btn_add_or_edit.hide()

    def hide_or_show_text(self, line_edit):
        eye_states = {
            self.window_7.enter_password: "password_eye",
            self.window_7.enter_login: "login_eye",
            self.window_7.enter_passphrase: "passphrase_eye"
        }

        state_key = eye_states.get(line_edit)
        if state_key is not None:
            state = getattr(self, state_key)
            if state == False:
                line_edit.setEchoMode(QLineEdit.EchoMode.Password)
                setattr(self, state_key, True)
            else:
                line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
                setattr(self, state_key, False)

    def generate_password_or_login(self, parameter):
        '''
        При уходе в окно генерации пароля не нужно отмечаться в road_map_list
        '''
        if parameter == 'Login':
            self.window__G.set_default_state('login_note', f'{parameter} for note')
        else:
            self.window__G.set_default_state('password_note', f'{parameter} for note')
        # self.window__G.window_G.label_special.setText(f'{parameter} for note')
        self.window__G.show()
        self.close()


class Ui_Window_7_new_note(object):
    def setupUi(self, Window_7_new_note):
        Window_7_new_note.setObjectName("Window_7_new_note")
        Window_7_new_note.setEnabled(True)
        Window_7_new_note.setWindowIcon(QtGui.QIcon("icons/key.ico"))
        Window_7_new_note.resize(1150, 600)
        Window_7_new_note.setMinimumSize(QtCore.QSize(1150, 600))
        Window_7_new_note.setMaximumSize(QtCore.QSize(1150, 600))
        Window_7_new_note.setStyleSheet("background-color: rgb(185, 185, 185);\n"
                                        "")
        Window_7_new_note.setIconSize(QtCore.QSize(40, 40))
        Window_7_new_note.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(parent=Window_7_new_note)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(450, 30, 300, 41))
        self.label.setMinimumSize(QtCore.QSize(300, 0))
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                 "font: \"MS Shell Dlg 2\";\n"
                                 "font-weight: bold;\n"
                                 "font-size: 20pt;\n"
                                 "font-color: RGB(28,28,28);\n"
                                 "color:  black;")
        self.label.setObjectName("label")
        self.btn_add_or_edit = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_add_or_edit.setGeometry(QtCore.QRect(490, 520, 171, 61))
        self.btn_add_or_edit.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_add_or_edit.setStyleSheet("QPushButton {\n"
                                           "background-color: rgba(0, 0, 0, 50);\n"
                                           "font: \"MS Shell Dlg 2\";\n"
                                           "\n"
                                           "font-size: 22pt;\n"
                                           "\n"
                                           "border-radius: 10px;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover {\n"
                                           "background-color: rgba(225,225,225,200);\n"
                                           "}")
        self.btn_add_or_edit.setObjectName("btn_add")
        self.layoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 90, 931, 421))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(32, 32))
        self.label_2.setMaximumSize(QtCore.QSize(12222, 32))
        self.label_2.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                   "font: \"MS Shell Dlg 2\";\n"
                                   "\n"
                                   "font-size: 15pt;\n"
                                   "font-color: RGB(28,28,28);\n"
                                   "color:  black;")
        self.label_2.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 32))
        self.label_3.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                   "font: \"MS Shell Dlg 2\";\n"
                                   "\n"
                                   "font-size: 15pt;\n"
                                   "font-color: RGB(28,28,28);\n"
                                   "color:  black;")
        self.label_3.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 32))
        self.label_4.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                   "font: \"MS Shell Dlg 2\";\n"
                                   "\n"
                                   "font-size: 15pt;\n"
                                   "font-color: RGB(28,28,28);\n"
                                   "color:  black;")
        self.label_4.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 32))
        self.label_5.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                   "font: \"MS Shell Dlg 2\";\n"
                                   "\n"
                                   "font-size: 15pt;\n"
                                   "font-color: RGB(28,28,28);\n"
                                   "color:  black;")
        self.label_5.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 32))
        self.label_6.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                   "font: \"MS Shell Dlg 2\";\n"
                                   "\n"
                                   "font-size: 15pt;\n"
                                   "font-color: RGB(28,28,28);\n"
                                   "color:  black;")
        self.label_6.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 32))
        self.label_7.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                   "font: \"MS Shell Dlg 2\";\n"
                                   "\n"
                                   "font-size: 15pt;\n"
                                   "font-color: RGB(28,28,28);\n"
                                   "color:  black;")
        self.label_7.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 32))
        self.label_8.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                   "font: \"MS Shell Dlg 2\";\n"
                                   "\n"
                                   "font-size: 15pt;\n"
                                   "font-color: RGB(28,28,28);\n"
                                   "color:  black;")
        self.label_8.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 32))
        self.label_9.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                   "font: \"MS Shell Dlg 2\";\n"
                                   "\n"
                                   "font-size: 15pt;\n"
                                   "font-color: RGB(28,28,28);\n"
                                   "color:  black;")
        self.label_9.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.enter_name = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.enter_name.setMaximumSize(QtCore.QSize(16777215, 32))
        self.enter_name.setToolTip("")
        self.enter_name.setStyleSheet("background-color: rgb(244, 244, 244);\n"
                                      "font: \"MS Shell Dlg 2\";;\n"
                                      "\n"
                                      "\n"
                                      "font-size: 15pt;\n"
                                      "border-radius: 10px;\n"
                                      "")
        self.enter_name.setText("")
        self.enter_name.setCursorPosition(0)
        self.enter_name.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.VisualMoveStyle)
        self.enter_name.setObjectName("enter_name")
        self.verticalLayout.addWidget(self.enter_name)
        self.enter_username = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.enter_username.setMaximumSize(QtCore.QSize(16777215, 32))
        self.enter_username.setToolTip("")
        self.enter_username.setStyleSheet("background-color: rgb(244, 244, 244);\n"
                                          "font: \"MS Shell Dlg 2\";;\n"
                                          "\n"
                                          "\n"
                                          "font-size: 15pt;\n"
                                          "border-radius: 10px;\n"
                                          "")
        self.enter_username.setText("")
        self.enter_username.setObjectName("enter_username")
        self.verticalLayout.addWidget(self.enter_username)
        self.enter_password = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.enter_password.setToolTip("")
        self.enter_password.setStyleSheet("background-color: rgb(244, 244, 244);\n"
                                          "font: \"MS Shell Dlg 2\";;\n"
                                          "\n"
                                          "\n"
                                          "font-size: 15pt;\n"
                                          "border-radius: 10px;\n"
                                          "")
        self.enter_password.setText("")
        self.enter_password.setObjectName("enter_password")
        self.verticalLayout.addWidget(self.enter_password)
        self.enter_login = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.enter_login.setToolTip("")
        self.enter_login.setStyleSheet("background-color: rgb(244, 244, 244);\n"
                                       "font: \"MS Shell Dlg 2\";;\n"
                                       "\n"
                                       "\n"
                                       "font-size: 15pt;\n"
                                       "border-radius: 10px;\n"
                                       "")
        self.enter_login.setText("")
        self.enter_login.setObjectName("enter_login")
        self.verticalLayout.addWidget(self.enter_login)
        self.enter_passphrase = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.enter_passphrase.setToolTip("")
        self.enter_passphrase.setStyleSheet("background-color: rgb(244, 244, 244);\n"
                                            "font: \"MS Shell Dlg 2\";;\n"
                                            "\n"
                                            "\n"
                                            "font-size: 15pt;\n"
                                            "border-radius: 10px;\n"
                                            "")
        self.enter_passphrase.setText("")
        self.enter_passphrase.setObjectName("enter_passphrase")
        self.verticalLayout.addWidget(self.enter_passphrase)
        self.enter_phone_number = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.enter_phone_number.setToolTip("")
        self.enter_phone_number.setStyleSheet("background-color: rgb(244, 244, 244);\n"
                                              "font: \"MS Shell Dlg 2\";;\n"
                                              "\n"
                                              "\n"
                                              "font-size: 15pt;\n"
                                              "border-radius: 10px;\n"
                                              "")
        self.enter_phone_number.setText("")
        self.enter_phone_number.setObjectName("enter_phone_number")
        self.verticalLayout.addWidget(self.enter_phone_number)
        self.enter_URL = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.enter_URL.setToolTip("")
        self.enter_URL.setStyleSheet("background-color: rgb(244, 244, 244);\n"
                                     "font: \"MS Shell Dlg 2\";;\n"
                                     "\n"
                                     "\n"
                                     "font-size: 15pt;\n"
                                     "border-radius: 10px;\n"
                                     "")
        self.enter_URL.setText("")
        self.enter_URL.setObjectName("enter_URL")
        self.verticalLayout.addWidget(self.enter_URL)
        self.enter_choose_category = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.enter_choose_category.setStyleSheet("background-color: rgb(244, 244, 244);\n"
                                                 "font: \"MS Shell Dlg 2\";;\n"
                                                 "\n"
                                                 "\n"
                                                 "font-size: 15pt;\n"
                                                 "border-radius: 10px;\n"
                                                 "")
        self.enter_choose_category.setEditable(True)
        self.enter_choose_category.setObjectName("enter_choose_category")
        self.verticalLayout.addWidget(self.enter_choose_category)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(970, 190, 41, 161))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.eye_password = QtWidgets.QToolButton(parent=self.layoutWidget1)
        self.eye_password.setMaximumSize(QtCore.QSize(16777215, 32))
        self.eye_password.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.eye_password.setStyleSheet("QToolButton {\n"
                                        "background-color: rgba(0, 0, 0, 0);\n"
                                        "font: \"MS Shell Dlg 2\";\n"
                                        "\n"
                                        "\n"
                                        "\n"
                                        "border-radius: 15px;\n"
                                        "}\n"
                                        "\n"
                                        "QToolButton:hover {\n"
                                        "background-color: rgba(225,225,225,200);\n"
                                        "}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('icons/eye.png'), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.eye_password.setIcon(icon)
        self.eye_password.setIconSize(QtCore.QSize(30, 30))
        self.eye_password.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.eye_password.setObjectName("eye_password")
        self.verticalLayout_3.addWidget(self.eye_password)
        self.eye_login = QtWidgets.QToolButton(parent=self.layoutWidget1)
        self.eye_login.setMaximumSize(QtCore.QSize(16777215, 32))
        self.eye_login.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.eye_login.setStyleSheet("QToolButton {\n"
                                     "background-color: rgba(0, 0, 0, 0);\n"
                                     "font: \"MS Shell Dlg 2\";\n"
                                     "\n"
                                     "\n"
                                     "\n"
                                     "border-radius: 15px;\n"
                                     "}\n"
                                     "\n"
                                     "QToolButton:hover {\n"
                                     "background-color: rgba(225,225,225,200);\n"
                                     "}")
        self.eye_login.setIcon(icon)
        self.eye_login.setIconSize(QtCore.QSize(30, 30))
        self.eye_login.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.eye_login.setObjectName("eye_login")
        self.verticalLayout_3.addWidget(self.eye_login)
        self.eye_passphrase = QtWidgets.QToolButton(parent=self.layoutWidget1)
        self.eye_passphrase.setMaximumSize(QtCore.QSize(16777215, 32))
        self.eye_passphrase.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.eye_passphrase.setStyleSheet("QToolButton {\n"
                                          "background-color: rgba(0, 0, 0, 0);\n"
                                          "font: \"MS Shell Dlg 2\";\n"
                                          "\n"
                                          "\n"
                                          "\n"
                                          "border-radius: 15px;\n"
                                          "}\n"
                                          "\n"
                                          "QToolButton:hover {\n"
                                          "background-color: rgba(225,225,225,200);\n"
                                          "}")
        self.eye_passphrase.setIcon(icon)
        self.eye_passphrase.setIconSize(QtCore.QSize(30, 30))
        self.eye_passphrase.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.eye_passphrase.setObjectName("eye_passphrase")
        self.verticalLayout_3.addWidget(self.eye_passphrase)
        self.btn_return_to_start = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_return_to_start.setGeometry(QtCore.QRect(950, 540, 181, 41))
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
        self.btn_again = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_again.setGeometry(QtCore.QRect(800, 540, 131, 41))
        self.btn_again.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_again.setStyleSheet("QPushButton {\n"
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
        self.btn_again.setObjectName("btn_again")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(1020, 190, 41, 111))
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btn_generate_password = QtWidgets.QToolButton(parent=self.widget)
        self.btn_generate_password.setMaximumSize(QtCore.QSize(16777215, 32))
        self.btn_generate_password.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_generate_password.setStyleSheet("QToolButton {\n"
                                                 "background-color: rgba(0, 0, 0, 0);\n"
                                                 "font: \"MS Shell Dlg 2\";\n"
                                                 "\n"
                                                 "\n"
                                                 "\n"
                                                 "border-radius: 10px;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QToolButton:hover {\n"
                                                 "background-color: rgba(225,225,225,200);\n"
                                                 "}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap('icons/G.png'), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_generate_password.setIcon(icon1)
        self.btn_generate_password.setIconSize(QtCore.QSize(25, 25))
        self.btn_generate_password.setObjectName("btn_generate_password")
        self.verticalLayout_4.addWidget(self.btn_generate_password)
        self.btn_generate_login = QtWidgets.QToolButton(parent=self.widget)
        self.btn_generate_login.setMaximumSize(QtCore.QSize(16777215, 32))
        self.btn_generate_login.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_generate_login.setStyleSheet("QToolButton {\n"
                                              "background-color: rgba(0, 0, 0, 0);\n"
                                              "font: \"MS Shell Dlg 2\";\n"
                                              "\n"
                                              "\n"
                                              "\n"
                                              "border-radius: 10px;\n"
                                              "}\n"
                                              "\n"
                                              "QToolButton:hover {\n"
                                              "background-color: rgba(225,225,225,200);\n"
                                              "}")
        self.btn_generate_login.setIcon(icon1)
        self.btn_generate_login.setIconSize(QtCore.QSize(25, 25))
        self.btn_generate_login.setObjectName("btn_generate_login")
        self.verticalLayout_4.addWidget(self.btn_generate_login)
        Window_7_new_note.setCentralWidget(self.centralwidget)

        self.retranslateUi(Window_7_new_note)
        QtCore.QMetaObject.connectSlotsByName(Window_7_new_note)

    def retranslateUi(self, Window_7_new_note):
        _translate = QtCore.QCoreApplication.translate
        Window_7_new_note.setWindowTitle(_translate("Window_7_new_note", "PasswordManager"))
        self.label.setText(_translate("Window_7_new_note", "Аdding a new note"))
        self.btn_add_or_edit.setText(_translate("Window_7_new_note", "Add"))
        self.label_2.setText(_translate("Window_7_new_note", "Name:"))
        self.label_3.setText(_translate("Window_7_new_note", "Username:"))
        self.label_4.setText(_translate("Window_7_new_note", "Password:"))
        self.label_5.setText(_translate("Window_7_new_note", "Login:"))
        self.label_6.setText(_translate("Window_7_new_note", "Passphrase:"))
        self.label_7.setText(_translate("Window_7_new_note", "Phone number:"))
        self.label_8.setText(_translate("Window_7_new_note", "URL:"))
        self.label_9.setText(_translate("Window_7_new_note", "Category:"))
        self.enter_name.setPlaceholderText(_translate("Window_7_new_note", " must not be empty"))
        self.enter_password.setPlaceholderText(_translate("Window_7_new_note", " must not be empty"))
        self.eye_password.setText(_translate("Window_7_new_note", "..."))
        self.eye_login.setText(_translate("Window_7_new_note", "..."))
        self.eye_passphrase.setText(_translate("Window_7_new_note", "..."))
        self.btn_return_to_start.setText(_translate("Window_7_new_note", "Return to start"))
        self.btn_again.setText(_translate("Window_7_new_note", "Again"))
        self.btn_generate_password.setText(_translate("Window_7_new_note", "..."))
        self.btn_generate_login.setText(_translate("Window_7_new_note", "..."))
