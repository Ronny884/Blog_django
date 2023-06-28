from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyEventHandler_3(FileSystemEventHandler):
    """
    Класс необходим для обработки случая, когда пользователь находится на окне 3, но при этом удаляются файлы БД.
    Окно автоматически перезагружается, если происходит удаление файла. Вместе с этим восстанавливается текст строки
    поиска, если таковой был введён
    """
    def __init__(self):
        self.window__3 = None
        if not os.path.exists(f'{os.getcwd()}/Database'):
            os.mkdir(f'{os.getcwd()}/Database')
        if not os.path.exists(f'{os.getcwd()}/Alpha'):
            os.mkdir(f'{os.getcwd()}/Alpha')

        self.observer_db = Observer()
        self.observer_db.schedule(self, f'{os.getcwd()}/Database', recursive=True)
        self.observer_db.start()

        self.observer_salt = Observer()
        self.observer_salt.schedule(self, f'{os.getcwd()}/Alpha', recursive=True)
        self.observer_salt.start()

    def window_update(self):
        text = self.window__3.window_3.search_line.text()
        self.window__3.set_default_state()
        self.window__3.window_3.search_line.setText(text)

    def on_deleted(self, event):
        self.window_update()

    def on_moved(self, event):
        self.window_update()

    def on_created(self, event):
        self.window_update()


class Window_3_database_selection_functional(QMainWindow):
    def __init__(self):
        super(Window_3_database_selection_functional, self).__init__()
        self.window_3 = Ui_Window_3_database_selection()
        self.window_3.setupUi(self)
        self.window__1 = None
        self.window__4 = None
        self.db_without_salt = []

        self.set_default_state()
        self.window_3.btn_return_to_start.clicked.connect(self.return_to_start)
        self.window_3.search_line.textChanged.connect(self.tracking_search_query)
        self.window_3.listWidget.itemClicked.connect(self.handle_item_click)

    def set_default_state(self):
        self.window_3.search_line.setText('')
        if os.path.exists(f'{os.getcwd()}/Database'):
            self.window_3.listWidget.setFont(QFont("MS Shell Dlg 2", 20))
            self.window_3.listWidget.clear()
            for file_name in os.listdir(f'{os.getcwd()}/Database'):
                if file_name.endswith('.db'):
                    item = QListWidgetItem('  ' + file_name.replace('.db', ''))

                    if os.path.isfile(f'{os.getcwd()}/Alpha/{file_name.replace(".db", ".bin")}'):
                        item.setForeground(QColor("black"))
                        if item.text().strip() in self.db_without_salt:
                            self.db_without_salt.remove(item.text().strip())
                        self.window_3.listWidget.addItem(item)
                    else:
                        item.setForeground(QtGui.QColor(110, 110, 110))
                        if item.text().strip() not in self.db_without_salt:
                            self.db_without_salt.append(item.text().strip())
                        self.window_3.listWidget.addItem(item)

    def handle_item_click(self, item):
        if item.text().strip() in self.db_without_salt:
            self.error_window = QMessageBox()
            self.error_window.setWindowTitle('SaltNotFound')
            self.error_window.setText('There is no decryption file for this database')
            self.error_window.setIcon(QMessageBox.Icon.Warning)
            self.error_window.setStandardButtons(QMessageBox.StandardButton.Ok)
            self.error_window.setDetailedText('The "Alpha" folder should contain a file for decrypting the selected '
                                              'database. Its name must match the name of the database, for example, '
                                              f'for the "{item.text().strip()}" database, the name would be '
                                              f'"{item.text().strip()}.bin". In this case, '
                                              'this file could have been deleted, moved, or renamed, which could cause '
                                              'the program to work incorrectly. Check its presence and the correctness '
                                              'of the name.')
            self.error_window.exec()
        else:
            self.chosen_name = item.text().strip()
            self.window__1.road_map_list.append(3)
            self.window__4.add_chosen_db_name(self.chosen_name)
            self.window__4.show()
            self.close()

    def return_to_start(self):
        self.window__1.road_map_list.append(3)
        self.set_default_state()
        self.window__1.show()
        self.close()

    def tracking_search_query(self):
        query = self.window_3.search_line.text().strip().lower()
        self.window_3.listWidget.clear()
        for file_name in os.listdir(f'{os.getcwd()}/Database'):
            if file_name.endswith('.db') and query in file_name.lower():
                self.window_3.listWidget.addItem('  ' + file_name.replace('.db', ''))


class Ui_Window_3_database_selection(object):
    def setupUi(self, Window_3_database_selection):
        Window_3_database_selection.setObjectName("Window_3_database_selection")
        Window_3_database_selection.setEnabled(True)
        Window_3_database_selection.resize(1150, 600)
        Window_3_database_selection.setWindowIcon(QtGui.QIcon("icons/key.ico"))
        Window_3_database_selection.setMinimumSize(QtCore.QSize(1150, 600))
        Window_3_database_selection.setMaximumSize(QtCore.QSize(1150, 600))
        Window_3_database_selection.setStyleSheet("background-color: rgb(185, 185, 185);\n"
"")
        Window_3_database_selection.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(parent=Window_3_database_selection)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(440, 30, 300, 41))
        self.label.setMinimumSize(QtCore.QSize(300, 0))
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"\n"
"font: \"MS Shell Dlg 2\";\n"
"font-weight: bold;\n"
"font-size: 20pt;\n"
"font-color: RGB(28,28,28);\n"
"color:  black;")
        self.label.setObjectName("label")
        self.btn_return_to_start = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_return_to_start.setGeometry(QtCore.QRect(790, 520, 151, 41))
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
        self.search_line.setGeometry(QtCore.QRect(211, 101, 731, 51))
        self.search_line.setToolTip("")
        self.search_line.setStyleSheet("background-color: rgb(244, 244, 244);\n"
"font: \"MS Shell Dlg 2\";;\n"
"\n"
"\n"
"font-size: 20pt;\n"
"border-radius: 10px;")
        self.search_line.setText("")
        self.search_line.setCursorPosition(0)
        self.search_line.setCursorMoveStyle(QtCore.Qt.CursorMoveStyle.VisualMoveStyle)
        self.search_line.setObjectName("search_line")
        self.btn_search = QtWidgets.QToolButton(parent=self.centralwidget)
        self.btn_search.setGeometry(QtCore.QRect(950, 110, 41, 41))
        self.btn_search.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('icons/search.png'), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_search.setIcon(icon)
        self.btn_search.setIconSize(QtCore.QSize(40, 40))
        self.btn_search.setObjectName("btn_search")
        self.listWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(211, 172, 731, 331))
        self.listWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.listWidget.setStyleSheet("background-color: rgba(0, 0, 0, 40);\n"
"border-radius: 10px;")
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.listWidget.setObjectName("listWidget")
        Window_3_database_selection.setCentralWidget(self.centralwidget)

        self.retranslateUi(Window_3_database_selection)
        QtCore.QMetaObject.connectSlotsByName(Window_3_database_selection)

    def retranslateUi(self, Window_3_database_selection):
        _translate = QtCore.QCoreApplication.translate
        Window_3_database_selection.setWindowTitle(_translate("Window_3_database_selection", "PasswordManager"))
        self.label.setText(_translate("Window_3_database_selection", "Choose the database"))
        self.btn_return_to_start.setText(_translate("Window_3_database_selection", "Return to start"))
        self.search_line.setPlaceholderText(_translate("Window_3_database_selection", " enter database name for search"))
        self.btn_search.setText(_translate("Window_3_database_selection", "..."))


