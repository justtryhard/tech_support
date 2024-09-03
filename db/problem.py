import sqlite3
from sqlite3 import Error


def problem_set_closed(num):
    try:
        conn = sqlite3.connect('database.db')
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
        with sqlite3.connect('database.db') as db:
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
            conn = sqlite3.connect('database.db')
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


