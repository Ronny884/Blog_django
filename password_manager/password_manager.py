from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import os

from Window_1_start import Window_1_start_functional
from Window_5_new_db import Window_5_new_db_functional
from Window_7_new_note import Window_7_new_note_functional
from Window_3_database_selection import Window_3_database_selection_functional, MyEventHandler_3
from Window_4_authorization import Window_4_authorization_functional
from Window_9_db_interior import Window_9_db_interior_functional
from Window_10_look_note import Window_10_look_note_functional
from Window_Generation import Window_Generating_functional
from encryption import Encryption

LOCK_FILE_PATH = f'{os.getcwd()}/file.lock'

def check_lock_file():
    if os.path.exists(LOCK_FILE_PATH):
        QMessageBox.critical(None, "Error", "Another instance of the application is already running.")
        return False
    else:
        try:
            with open(LOCK_FILE_PATH, "w"):
                pass
            return True
        except IOError:
            QMessageBox.critical(None, "Error", "Failed to create lock file.")
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if not check_lock_file():
        sys.exit(1)

    watch_dog_3 = MyEventHandler_3()

    window__1 = Window_1_start_functional()
    window__5 = Window_5_new_db_functional()
    window__7 = Window_7_new_note_functional()
    window__3 = Window_3_database_selection_functional()
    window__4 = Window_4_authorization_functional()
    window__9 = Window_9_db_interior_functional()
    window__10 = Window_10_look_note_functional()
    window__G = Window_Generating_functional()
    enc = Encryption()
    window__1.show()
    app.aboutToQuit.connect(window__1.encryption_before_closing_the_program)


    window__1.window__5 = window__5
    window__1.window__3 = window__3
    window__1.window__7 = window__7
    window__1.window__9 = window__9
    window__1.window__10 = window__10
    window__1.window__G = window__G

    window__3.window__1 = window__1
    window__3.window__4 = window__4

    watch_dog_3.window__3 = window__3
    enc.watch_dog = watch_dog_3

    window__4.window__1 = window__1
    window__4.window__3 = window__3
    window__4.window__9 = window__9
    window__4.window__G = window__G

    window__5.window__1 = window__1
    window__5.window__7 = window__7
    window__5.window__9 = window__9
    window__5.window__G = window__G

    window__7.window__5 = window__5
    window__7.window__1 = window__1
    window__7.window__9 = window__9
    window__7.window__10 = window__10
    window__7.window__G = window__G

    window__9.window__1 = window__1
    window__9.window__3 = window__3
    window__9.window__7 = window__7
    window__9.window__10 = window__10

    window__10.window__9 = window__9
    window__10.window__7 = window__7
    window__10.window__1 = window__1

    window__G.window__1 = window__1
    window__G.window__5 = window__5
    window__G.window__7 = window__7

    sys.exit(app.exec())
