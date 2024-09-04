import sqlite3
from sqlite3 import Error


def actual_problems():
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT id, address FROM problems WHERE closed = 0""")
        rows = cursor.fetchall()
        return [{row[0]: row[1]} for row in rows]


def pre_problem(e):
    return f' Адрес | Описание | Затронутые клиенты | Срок устранения'


def print_problem(e):
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT address, description, clients, time_to_resolve FROM problems WHERE id = ?""", [e])
        rows = cursor.fetchall()
        str2 = ''
        for row in rows:
            str2 += f'{row[0]} | {row[1]} | {row[2]} | {row[3]}'
        return str2


def set_ttr(x, y):
    try:
        sqlite_connection = sqlite3.connect('db/database.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        sql_insert = """UPDATE problems set time_to_resolve = ? where id = ?"""
        data_tuple = (y, x)
        cursor.execute(sql_insert, data_tuple)
        sqlite_connection.commit()
        print("Запись успешно вставлена в таблицу", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def problem_set_closed(num):
    try:
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        print("Подключение ОК")
        cursor.execute("UPDATE problems SET closed=1 WHERE id = ?", [num])
        conn.commit()
        print("Авария закрыта")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при закрытии аварии", error)
    finally:
        if conn:
            conn.close()
            print("Соединение закрыто")


class Problem:
    id: int
    address: str
    description: str
    clients: str
    time_to_resolve: str
    closed: bool

    def __init__(self):
        with sqlite3.connect('db/database.db') as db:
            cursor = db.cursor()
            query = """ SELECT id FROM problems """
            cursor.execute(query)
            rows = cursor.fetchall()
            ids = [row[0] for row in rows]
            if len(ids) == 0:
                self.id = 0
            else:
                self.id = max(ids) + 1
            self.closed = 0

    def new_problem(self, address, description, clients, time_to_resolve):
        self.address = address
        self.description = description
        self.clients = clients
        self.time_to_resolve = time_to_resolve

        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            print("Подключение ОК")

            sql_insert = """INSERT INTO problems
                                      (id, address, description, clients, time_to_resolve, closed)
                                      VALUES (?, ?, ?, ?, ?, ?);"""
            data_tuple = (self.id, self.address, self.description, self.clients, self.time_to_resolve, self.closed)
            cursor.execute(sql_insert, data_tuple)
            conn.commit()
            print("Авария создана")

            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при создании аварии", error)
        finally:
            if conn:
                conn.close()
                print("Соединение закрыто")
