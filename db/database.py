import sqlite3
from sqlite3 import Error

# создаём таблицы
with sqlite3.connect('database.db') as db:
    cursor = db.cursor()
    query1 = """ CREATE TABLE IF NOT EXISTS clients (id INTEGER, name TEXT, address TEXT,
    ip TEXT) """
    query2 = """ CREATE TABLE IF NOT EXISTS problems (id INTEGER, address TEXT, description TEXT, clients TEXT,
    time_to_resolve TEXT, closed BLOB) """
    query3 = """ CREATE TABLE IF NOT EXISTS tickets (id INTEGER, client_id INTEGER, contact TEXT, description TEXT,
    closed BLOB) """
    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)



# a = Problem()
#d = Problem()
#c = Problem()
#f = Problem()
# a.new_problem("Елецкая 35к3", "Нет электричества", b, "15/01/2019, 18:00")
#c.new_problem("Авиаторов 10", "Нет электричества", e, "17/01/2019, 18:00")
#d.new_problem("Тверская 27", "Нет электричества", g, "21/01/2019, 18:00")
#f.new_problem("Ленина 54", "Нет электричества", e, "21/01/2019, 18:00")

