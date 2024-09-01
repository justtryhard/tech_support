import sqlite3
from sqlite3 import Error

# создаём таблицы
with sqlite3.connect('db/database.db') as db:
    cursor = db.cursor()
    query1 = """ CREATE TABLE IF NOT EXISTS clients (id INTEGER, name TEXT, address TEXT,
    ip TEXT) """
    #query2 = """ CREATE TABLE IF NOT EXISTS problems (id INTEGER, address TEXT, description TEXT,
    #time_to_resolve TEXT, closed BLOB) """
    query3 = """ CREATE TABLE IF NOT EXISTS tickets (id INTEGER, client_id INTEGER, contact TEXT, description TEXT,
    closed BLOB) """
    cursor.execute(query1)
 #   cursor.execute(query2)
    cursor.execute(query3)


class Ticket:
    id: int
    cl_id: int
    contact: str
    description: str
    closed: bool

    def __init__(self):
        with sqlite3.connect('db/database.db') as db:
            cursor = db.cursor()
            query = """ SELECT id FROM tickets """
            cursor.execute(query)
            rows = cursor.fetchall()
            ids = [row[0] for row in rows]
            if len(ids) == 0:
                self.id = 0
            else:
                self.id = max(ids) + 1
            self.closed = 0

    def new_ticket(self, cl_id, contact, description):
        self.cl_id = cl_id
        self.contact = contact
        self.description = description
        try:
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()
            print("Подключение ОК")

            sql_insert = """INSERT INTO tickets
                                      (id, client_id, contact, description, closed)
                                      VALUES (?, ?, ?, ?, ?);"""
            data_tuple = (self.id, self.cl_id, self.contact, self.description, self.closed)
            cursor.execute(sql_insert, data_tuple)
            conn.commit()
            print("Заявка создана")

            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при добавлении тикета", error)
        finally:
            if conn:
                conn.close()
                print("Соединение закрыто")
