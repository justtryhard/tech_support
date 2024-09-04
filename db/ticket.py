import sqlite3
from sqlite3 import Error


def actual_tickets():
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT id, client_id FROM tickets WHERE closed = 0""")
        rows = cursor.fetchall()
        return [{row[0]: row[1]} for row in rows]


def pre_ticket(e):
    return f'Номер договора | Описание | Контакт'


def print_ticket(e):
    with sqlite3.connect('db/database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT client_id, description, contact FROM tickets WHERE id = ?""", [e])
        rows = cursor.fetchall()
        str2 = ''
        for row in rows:
            str2 += f'{row[0]} | {row[1]} | {row[2]}'
        return str2


def set_closed(num):
    try:
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        print("Подключение ОК")
        cursor.execute("UPDATE tickets SET closed=1 WHERE id = ?", [num])
        conn.commit()
        print("Заявка закрыта")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при закрытии тикета", error)
    finally:
        if conn:
            conn.close()
            print("Соединение закрыто")


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
