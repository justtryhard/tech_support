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
    # cursor.execute(query2)
    cursor.execute(query3)


