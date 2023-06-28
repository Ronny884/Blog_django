from PyQt6 import QtWidgets, QtSql
import os


class Data():
    def __init__(self):
        super(Data, self).__init__()

    def create_new_db(self, name):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(f'{os.getcwd()}/Database/{name}.db')

        if not db.open():
            pass

        query = QtSql.QSqlQuery()
        query.exec('''CREATE TABLE IF NOT EXISTS notes (
              id INTEGER PRIMARY KEY NOT NULL,
              name TEXT NOT NULL,
              username TEXT,
              password TEXT NOT NULL,
              login TEXT,
              passphrase TEXT,
              phone_number TEXT,
              url TEXT,
              category TEXT
              )''')
        query.exec()

    def add_new_note_to_target_db(self, db_name, query_values):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(f'{os.getcwd()}/Database/{db_name}.db')

        if not db.open():
            pass

        query = QtSql.QSqlQuery()
        query.prepare('''
        INSERT INTO notes (name, username, password, login, passphrase, phone_number, url, category) 
        VALUES (?,?,?,?,?,?,?,?)''')
        for query_value in query_values:
            query.addBindValue(query_value)
        query.exec()

    def select_notes_with_or_without_category(self, db_name, category):
        try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(f'{os.getcwd()}/Database/{db_name}.db')
            db.open()

            query = QtSql.QSqlQuery()
            name_list = []
            if category is None:
                query.exec('SELECT name FROM notes')
                while query.next():
                    name_list.append(query.value(0))
            else:
                query.exec('SELECT name FROM notes WHERE category = ?')
                query.bindValue(0, category)
                if query.exec():
                    while query.next():
                        name_list.append(query.value(0))
            return name_list

        except:
            return False


    def select_all_categories(self, db_name):
        try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(f'{os.getcwd()}/Database/{db_name}.db')
            db.open()

            query = QtSql.QSqlQuery()
            category_list = []
            query.exec('SELECT category FROM notes')
            while query.next():
                category_list.append(query.value(0))
            return category_list
        except:  # в случае каких угодно проблем с БД возвращаем False
            return False

    def select_parameter_for_copy(self, db_name, note_name, parameter_for_copy):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(f'{os.getcwd()}/Database/{db_name}.db')

        if not db.open():
            print("No")

        def select_password():
            global result
            query = QtSql.QSqlQuery()
            query.exec("SELECT password FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    result = query.value(0)
            return result

        def select_login():
            global result
            query = QtSql.QSqlQuery()
            query.exec("SELECT login FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    result = query.value(0)
            return result

        def select_username():
            global result
            query = QtSql.QSqlQuery()
            query.exec("SELECT username FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    result = query.value(0)
            return result

        def select_passphrase():
            global result
            query = QtSql.QSqlQuery()
            query.exec("SELECT passphrase FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    result = query.value(0)
            return result

        def select_phone_number():
            global result
            query = QtSql.QSqlQuery()
            query.exec("SELECT phone_number FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    result = query.value(0)
            return result

        def select_url():
            global result
            query = QtSql.QSqlQuery()
            query.exec("SELECT url FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    result = query.value(0)
            return result

        def select_category():
            global result
            query = QtSql.QSqlQuery()
            query.exec("SELECT category FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    result = query.value(0)
            return result

        def get_id():
            global result
            query = QtSql.QSqlQuery()
            query.exec("SELECT id FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    result = query.value(0)
            return result

        functions_for_parameters = {
            'password': select_password,
            'login': select_login,
            'username': select_username,
            'passphrase': select_passphrase,
            'phone_number': select_phone_number,
            'category': select_category,
            'url': select_url,
            'id': get_id}

        return functions_for_parameters[parameter_for_copy]()

    def delete_note(self, db_name, note_name):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(f'{os.getcwd()}/Database/{db_name}.db')

        if not db.open():
            print("No")

        query = QtSql.QSqlQuery()
        query.exec('DELETE FROM notes WHERE name = ?')
        query.bindValue(0, note_name)
        query.exec()

    def get_name_by_id(self, db_name, id):
        global result
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(f'{os.getcwd()}/Database/{db_name}.db')

        if not db.open():
            print("No")

        query = QtSql.QSqlQuery()
        query.exec('SELECT name FROM notes WHERE id = ?')
        query.bindValue(0, id)
        if query.exec():
            while query.next():
                result = query.value(0)
        return result

    def update_note(self, db_name, query_values):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(f'{os.getcwd()}/Database/{db_name}.db')

        if not db.open():
            pass

        query = QtSql.QSqlQuery()
        query.prepare('''
        UPDATE notes SET name=?, username=?, password=?, login=?, passphrase=?, phone_number=?, url=?, category=? 
        WHERE id=?''')
        for query_value in query_values:
            query.addBindValue(query_value)
        query.exec()


    def repition_chek(self, db_name, name):
        try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(f'{os.getcwd()}/Database/{db_name}.db')
            db.open()

            query = QtSql.QSqlQuery()
            name_list = []
            query.exec('SELECT name FROM notes')
            while query.next():
                name_list.append(query.value(0))
            if name not in name_list:
                return True
            else:
                return False
        except:
            return None
