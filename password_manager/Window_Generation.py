from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QLineEdit
import pyperclip
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from enum import Enum, IntEnum
import secrets
from math import log2
from Window_9_db_interior import Window_9_db_interior_functional as win_9


class Characters(Enum):
    """
    Библиотека enum предназначена для работы с перечислениями. Класс Enum данной библиотеки мы используем как
    родительский для создания своего класса, атрибуты которого в последствии будет использовать предпочтительнее из
    сооброжений лучшей читаемости кода, безопасности и тд
    """
    btn_lower = ascii_lowercase
    btn_upper = ascii_uppercase
    btn_digits = digits
    btn_special = punctuation


class StrengthToEntropy(IntEnum):
    """
    Класс IntEnum используется для создания перечислений, где все значения - целые числа
    """
    Pathetic = 0
    Weak = 30
    Good = 50
    Strong = 70
    Excellent = 120


class Window_Generating_functional(QMainWindow):
        def __init__(self):
            super(Window_Generating_functional, self).__init__()
            self.window_G = Ui_Window_Generating()
            self.window_G.setupUi(self)

            self.window__1 = None
            self.window__5 = None
            self.window__7 = None
            self.GENERATE_PASSWORD = ('btn_lower', 'btn_upper', 'btn_digits', 'btn_special', 'btn_regenerate')

            # при нажатии кнопок с названиями из этого кортежа, вызывется функция установки пароля в поле.
            # также пароль генерируется при установке дефолтного состояния

            for btn in self.GENERATE_PASSWORD:
                getattr(self.window_G, btn).clicked.connect(self.set_password)

            self.window_G.btn_eye.clicked.connect(self.hide_or_show)
            self.window_G.btn_copy.clicked.connect(self.copy)
            self.window_G.btn_apply.clicked.connect(self.apply)
            self.window_G.btn_close.clicked.connect(self.close_and_again)
            self.connect_slider_to_spinbox()

        def set_default_state(self, target, text):
            self.window_G.btn_special.show()
            self.window_G.btn_apply.show()
            self.target = target
            self.window_G.line_password.setEchoMode(QLineEdit.EchoMode.Normal)
            if target == 'from_start':
                self.window_G.slider_length.setValue(0)
                self.window_G.btn_apply.hide()
                self.window_G.btn_close.setText('Again')
            elif target == 'password_db':
                self.window_G.btn_special.hide()
                self.window_G.btn_close.setText('Close')
                self.window_G.slider_length.setValue(9)
            else:
                self.window_G.slider_length.setValue(0)
                self.window_G.btn_close.setText('Close')

            self.set_password()
            self.window_G.label_special.setText(text)

            self.window_G.btn_digits.setCheckable(True)
            self.window_G.btn_digits.setChecked(True)

            self.window_G.btn_lower.setCheckable(True)
            self.window_G.btn_lower.setChecked(True)

            self.window_G.btn_upper.setCheckable(True)
            self.window_G.btn_upper.setChecked(True)

            self.window_G.btn_special.setChecked(False)

        def create_new(self, lenght: int, characters: str) -> str:
            """
            Используется библиотека secrets, позволяющая генерировать криптографически безопасные значения и
            последовательности. Источник случайности берётся из параметров ОС, что уже делает её напорядок надежнее
            того же random, у которого источник случайности задаётся в seed
            :param lenght: длина пароля
            :param characters: строка со всеми символами, разрешенными к использованию
            :return: строка, представляющаю собой конечный вариант пароля
            """
            return ''.join(secrets.choice(characters) for _ in range(lenght))

        def get_entropy(self, lenght: int, character_number: int) -> float:
            """
            Энтропия пароля - это мера случайности или неопределенности пароля. Она позволяет оценить сложность и
            стойкость пароля от взлома. Чем выше энтропия, тем сложнее угадать или подобрать пароль.
            Энтропия пароля зависит от разнообразия символов, используемых в пароле, а также от его длины.
            Чем больше символов и чем длиннее пароль, тем выше энтропия
            """
            try:
                entropy = lenght * log2(character_number)
                return round(entropy, 2)
            except:
                return False

        def connect_slider_to_spinbox(self):
            """
            Связываем значение счётчика с длиной слайдера и наоборот
            """
            self.window_G.slider_length.valueChanged.connect(self.window_G.spinBox_lenght.setValue)
            self.window_G.spinBox_lenght.valueChanged.connect(self.window_G.slider_length.setValue)
            self.window_G.spinBox_lenght.valueChanged.connect(self.set_password)

        def get_characters(self) -> str:
            """
            Метод для получения символов отмеченных кнопок. Они будут добавляться в переменную chars. Проходимся по
            атрибутам класса Characters и, если нажата соответствующая кнопка (получено разрешение на использование
            указанной группы символов), добавляем эту строку к chars
            """
            chars = ''

            for btn in Characters:
                if getattr(self.window_G, btn.name).isChecked():
                    chars += btn.value
            return chars

        def set_password(self):
            """
            выводим в строку пароль, сгенерированный методом create_new. Строку допустимых символов берём из метода
            get_characters
            """
            try:
                self.window_G.line_password.setText(self.create_new(lenght=self.window_G.spinBox_lenght.value(),
                                                                    characters=self.get_characters()))
            except IndexError:
                self.window_G.line_password.clear()

            self.set_strength()

        def get_character_number(self):
            """
            Метод получения количества символов
            """
            num = 0
            character_number = {
                'btn_lower': len(Characters.btn_lower.value),
                'btn_upper': len(Characters.btn_upper.value),
                'btn_digits': len(Characters.btn_digits.value),
                'btn_special': len(Characters.btn_special.value)
            }

            for btn in character_number.items():
                if getattr(self.window_G, btn[0]).isChecked():
                    num += btn[1]
            return num

        def set_strength(self):
            length = len(self.window_G.line_password.text())
            char_num = self.get_character_number()

            for strength in StrengthToEntropy:
                if self.get_entropy(length, char_num) >= strength.value:
                    self.window_G.label_info.setText(f'Strength: {strength.name}')
                if self.target == 'password_db':
                    if self.window_G.spinBox_lenght.value() < 9:
                        self.window_G.label_info.setText('Not enough characters')
                        self.window_G.btn_apply.hide()
                    else:
                        self.window_G.btn_apply.show()

        def hide_or_show(self):
            if self.window_G.line_password.echoMode() is QLineEdit.EchoMode.Normal:
                self.window_G.line_password.setEchoMode(QLineEdit.EchoMode.Password)
            else:
                self.window_G.line_password.setEchoMode(QLineEdit.EchoMode.Normal)

        def copy(self):
            pyperclip.copy(self.window_G.line_password.text())
            win_9().copy_information('Copied', self.window_G.btn_copy)

        def apply(self):
            if self.target == 'password_db':
                self.window__5.window_5.enter_master_password.setText(self.window_G.line_password.text())
            elif self.target == 'login_note':
                self.window__7.window_7.enter_login.setText(self.window_G.line_password.text())
            else:
                self.window__7.window_7.enter_password.setText(self.window_G.line_password.text())
            self.close_and_again()

        def close_and_again(self):
            if self.target == 'from_start':
                self.window__1.show()
            elif self.target == 'password_db':
                self.window__5.show()
            else:
                self.window__7.show()
            self.close()


class Ui_Window_Generating(object):
    def setupUi(self, Window_Generating):
        Window_Generating.setObjectName("Window_Generating")
        Window_Generating.setEnabled(True)
        Window_Generating.setWindowIcon(QtGui.QIcon("icons/key.ico"))
        Window_Generating.resize(1150, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Window_Generating.sizePolicy().hasHeightForWidth())
        Window_Generating.setSizePolicy(sizePolicy)
        Window_Generating.setMinimumSize(QtCore.QSize(1150, 600))
        Window_Generating.setMaximumSize(QtCore.QSize(1150, 600))
        Window_Generating.setStyleSheet("background-color: rgb(185, 185, 185);\n"
"")
        Window_Generating.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(parent=Window_Generating)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(480, 60, 300, 41))
        self.label.setMinimumSize(QtCore.QSize(300, 50))
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"\n"
"font: \"MS Shell Dlg 2\";\n"
"font-weight: bold;\n"
"font-size: 27pt;\n"
"font-color: RGB(28,28,28);\n"
"color:  black;")
        self.label.setObjectName("label")
        self.label_special = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_special.setGeometry(QtCore.QRect(140, 160, 591, 31))
        self.label_special.setMinimumSize(QtCore.QSize(100, 0))
        self.label_special.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(72, 72, 72);\n"
"\n"
"font: \"MS Shell Dlg 2\";\n"
"font-size: 16pt;\n"
"\n"
"\n"
"")
        self.label_special.setObjectName("label_special")

        self.label_info = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_info.setGeometry(QtCore.QRect(490, 265, 591, 31))
        self.label_info.setMinimumSize(QtCore.QSize(100, 0))
        self.label_info.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                         "color: rgb(72,72,72);\n"
                                         "\n"
                                         "font: \"MS Shell Dlg 2\";\n"
                                         "font-size: 16pt;\n"
                                         "\n"
                                         "\n"
                                         "")
        self.label_info.setObjectName("label_info")

        self.slider_length = QtWidgets.QSlider(parent=self.centralwidget)
        self.slider_length.setGeometry(QtCore.QRect(130, 310, 830, 22))
        self.slider_length.setStyleSheet("QSlider::groove:horizontal {\n"
"    border: 1px solid #bbb;\n"
"    background: #ddd;\n"
"    height: 8px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #fff;\n"
"    border: 1px solid #777;\n"
"    width: 17px;\n"
"    height: 17px;\n"
"    margin: -5px 0;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background: rgba(0,0,0,100);\n"
"    border: 1px solid #777;\n"
"    height: 8px;\n"
"    border-radius: 4px;\n"
"}")
        self.slider_length.setMaximum(99)
        self.slider_length.setProperty("value", 0)
        self.slider_length.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider_length.setInvertedAppearance(False)
        self.slider_length.setInvertedControls(False)
        self.slider_length.setObjectName("slider_length")
        self.spinBox_lenght = QtWidgets.QSpinBox(parent=self.centralwidget)
        self.spinBox_lenght.setGeometry(QtCore.QRect(970, 300, 51, 41))
        self.spinBox_lenght.setStyleSheet("background-color: rgba(0, 0, 0, 50);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 14pt;\n"
"\n"
"border-radius: 10px;")
        self.spinBox_lenght.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.spinBox_lenght.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_lenght.setProperty("value", 0)
        self.spinBox_lenght.setObjectName("spinBox_lenght")
        self.btn_copy = QtWidgets.QToolButton(parent=self.centralwidget)
        self.btn_copy.setGeometry(QtCore.QRect(70, 200, 51, 51))
        self.btn_copy.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_copy.setStyleSheet("QToolButton {\n"
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
        icon.addPixmap(QtGui.QPixmap("icons/copy_2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_copy.setIcon(icon)
        self.btn_copy.setIconSize(QtCore.QSize(40, 40))
        self.btn_copy.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.btn_copy.setObjectName("btn_copy")
        self.btn_regenerate = QtWidgets.QToolButton(parent=self.centralwidget)
        self.btn_regenerate.setGeometry(QtCore.QRect(1040, 200, 51, 51))
        self.btn_regenerate.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_regenerate.setStyleSheet("QToolButton {\n"
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
        icon1.addPixmap(QtGui.QPixmap("icons/regenerate.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_regenerate.setIcon(icon1)
        self.btn_regenerate.setIconSize(QtCore.QSize(40, 40))
        self.btn_regenerate.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.btn_regenerate.setObjectName("btn_regenerate")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(130, 200, 891, 51))
        self.groupBox.setStyleSheet("background-color: rgb(244, 244, 244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 13pt;\n"
"border-radius: 10px;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.btn_eye = QtWidgets.QToolButton(parent=self.groupBox)
        self.btn_eye.setGeometry(QtCore.QRect(840, 0, 51, 51))
        self.btn_eye.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_eye.setStyleSheet("QToolButton {\n"
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/eye.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_eye.setIcon(icon2)
        self.btn_eye.setIconSize(QtCore.QSize(40, 40))
        self.btn_eye.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.btn_eye.setObjectName("btn_eye")
        self.line_password = QtWidgets.QLineEdit(parent=self.groupBox)
        self.line_password.setGeometry(QtCore.QRect(10, 0, 821, 51))
        self.line_password.setToolTip("")
        self.line_password.setStyleSheet("background-color: rgb(244, 244, 244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 20pt;\n"
"border-radius: 10px;")
        self.line_password.setText("")
        self.line_password.setPlaceholderText("")
        self.line_password.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.VisualMoveStyle)
        self.line_password.setObjectName("line_password")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(130, 380, 891, 51))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_lower = QtWidgets.QPushButton(parent=self.widget)
        self.btn_lower.setMaximumSize(QtCore.QSize(333, 33))
        self.btn_lower.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_lower.setStyleSheet("QPushButton {\n"
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
"}\n"
"\n"
"QPushButton:checked {\n"
"background-color: rgba(225,225,225,160);\n"
"}")
        self.btn_lower.setCheckable(True)
        self.btn_lower.setChecked(True)
        self.btn_lower.setObjectName("btn_lower")
        self.horizontalLayout.addWidget(self.btn_lower)
        self.btn_upper = QtWidgets.QPushButton(parent=self.widget)
        self.btn_upper.setMaximumSize(QtCore.QSize(16777215, 33))
        self.btn_upper.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_upper.setStyleSheet("QPushButton {\n"
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
"}\n"
"QPushButton:checked {\n"
"background-color: rgba(225,225,225,160);\n"
"}")
        self.btn_upper.setCheckable(True)
        self.btn_upper.setChecked(True)
        self.btn_upper.setObjectName("btn_upper")
        self.horizontalLayout.addWidget(self.btn_upper)
        self.btn_digits = QtWidgets.QPushButton(parent=self.widget)
        self.btn_digits.setMaximumSize(QtCore.QSize(16777215, 33))
        self.btn_digits.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_digits.setStyleSheet("QPushButton {\n"
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
"}\n"
"QPushButton:checked {\n"
"background-color: rgba(225,225,225,160);\n"
"}")
        self.btn_digits.setCheckable(True)
        self.btn_digits.setChecked(True)
        self.btn_digits.setObjectName("btn_digits")
        self.horizontalLayout.addWidget(self.btn_digits)
        self.btn_special = QtWidgets.QPushButton(parent=self.widget)
        self.btn_special.setMaximumSize(QtCore.QSize(16777215, 33))
        self.btn_special.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_special.setStyleSheet("QPushButton {\n"
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
"}\n"
"QPushButton:checked {\n"
"background-color: rgba(225,225,225,160);\n"
"}")
        self.btn_special.setCheckable(True)
        self.btn_special.setObjectName("btn_special")
        self.horizontalLayout.addWidget(self.btn_special)
        self.widget1 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(410, 480, 331, 61))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_apply = QtWidgets.QPushButton(parent=self.widget1)
        self.btn_apply.setMaximumSize(QtCore.QSize(16777215, 46))
        self.btn_apply.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_apply.setStyleSheet("QPushButton {\n"
"background-color: rgba(0, 0, 0, 50);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 17pt;\n"
"\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_apply.setObjectName("btn_apply")
        self.horizontalLayout_2.addWidget(self.btn_apply)
        self.btn_close = QtWidgets.QPushButton(parent=self.widget1)
        self.btn_close.setMaximumSize(QtCore.QSize(16777215, 46))
        self.btn_close.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_close.setStyleSheet("QPushButton {\n"
"background-color: rgba(0, 0, 0, 50);\n"
"font: \"MS Shell Dlg 2\";\n"
"\n"
"font-size: 17pt;\n"
"\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: rgba(225,225,225,200);\n"
"}")
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_2.addWidget(self.btn_close)
        Window_Generating.setCentralWidget(self.centralwidget)

        self.retranslateUi(Window_Generating)
        QtCore.QMetaObject.connectSlotsByName(Window_Generating)

    def retranslateUi(self, Window_Generating):
        _translate = QtCore.QCoreApplication.translate
        Window_Generating.setWindowTitle(_translate("Window_Generating", "PasswordManager"))
        self.label.setText(_translate("Window_Generating", "Generation"))
        self.btn_copy.setText(_translate("Window_Generating", "..."))
        self.btn_regenerate.setText(_translate("Window_Generating", "..."))
        self.btn_eye.setText(_translate("Window_Generating", "..."))
        self.btn_lower.setText(_translate("Window_Generating", "a-z"))
        self.btn_upper.setText(_translate("Window_Generating", "A-Z"))
        self.btn_digits.setText(_translate("Window_Generating", "0-9"))
        self.btn_special.setText(_translate("Window_Generating", "*$%"))
        self.btn_apply.setText(_translate("Window_Generating", "Apply"))
        self.btn_close.setText(_translate("Window_Generating", "Close"))
