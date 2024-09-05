import sqlite3
from sqlite3 import Error
from db.ticket import Ticket, set_closed
from db.problem import Problem, problem_set_closed


# создаём таблицы
with sqlite3.connect('db/database.db') as db:
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

# создаём клиентов
    query4 = """INSERT INTO clients (id, name, address, ip)
                          VALUES (233, "Рога и Копыта", "Косыгина 23", "10.20.2.23");"""
    query5 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (234, "ООО 'Поставщик поставок'", "Поставочная 12", "10.20.2.25");"""
    query6 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (247, "ООО 'ТКЛ'", "Ленинградский пр-кт 79", "10.20.2.26");"""
    query7 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (278, "ООО 'Острый Глаз'", "Тверская 17", "10.20.2.27");"""
    query8 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (289, "ООО 'Лилия'", "Кронштадтский б-р 23", "10.20.2.28");"""
    query9 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (305, "ООО 'Нежность'", "Большая Никитская 36", "10.20.2.29");"""
    query10 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (376, "ООО 'Хозяйка'", "Люблинская 58", "10.20.2.30");"""
    query11 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (387, "ООО 'Дело'", "Жуков пр-д 17", "10.20.2.31");"""
    query12 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (456, "ООО 'Помощник'", "Большая Пионерская 23", "10.20.2.32");"""
    query13 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (567, "ООО 'Жилищник'", "Волоколамское ш. 78", "10.20.2.33");"""
    query14 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (754, "ООО 'ХимПромТорг'", "Походный пр-д 17", "10.20.2.34");"""
    query15 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (755, "ИП Петров А.А.", "Волгоградский пр-кт 48", "10.20.2.35");"""
    query16 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (788, "ООО 'Приморье'", "Бауманская 24", "10.20.2.36");"""
    query17 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (845, "ООО 'Выпечка'", "Чонгарский б-р 8", "10.20.2.37");"""
    query18 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (867, "ООО 'Восток'", "Щербаковская 56", "10.20.2.38");"""
    query19 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (876, "ИП Иванов И.И.", "Ярославское ш. 97", "10.20.2.39");"""
    query20 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (954, "ООО 'Урожай'", "Ставропольская 58", "10.20.2.40");"""
    query21 = """INSERT INTO clients(id, name, address, ip)
                          VALUES (991, "ООО 'Предприятие'", "Кузнецкий мост 16", "10.20.2.41");"""

    cursor.execute(query4)
    cursor.execute(query5)
    cursor.execute(query6)
    cursor.execute(query7)
    cursor.execute(query8)
    cursor.execute(query9)
    cursor.execute(query10)
    cursor.execute(query11)
    cursor.execute(query12)
    cursor.execute(query13)
    cursor.execute(query14)
    cursor.execute(query15)
    cursor.execute(query16)
    cursor.execute(query17)
    cursor.execute(query18)
    cursor.execute(query19)
    cursor.execute(query20)
    cursor.execute(query21)

#создаём аварии

a = Problem()
a.new_problem('Елецкая 36', "Нет электричества", "233,247,387",
              "15/09/2024, 18:00")
b = Problem()
b.new_problem('Тверская 28', "Обрыв оптической линии", "278",
              "18/09/2024, 14:00")
c = Problem()
c.new_problem('Авиаторов 10', "Авария на трансформаторной подстанции", "289,376",
              "12/09/2024, 10:00")
problem_set_closed(2) # закроем аварию с id=2
d = Problem()
d.new_problem('Ленина 54', "Нет электричества", "954,755",
              "20/09/2024, 17:00")

#создаём заявки
e = Ticket()
(e.new_ticket('954', "89999999999", "Нет интернета"))
f = Ticket()
(f.new_ticket('845', "88888888888", "Нестабильная работа услуги"))
g = Ticket()
(g.new_ticket('788', "87777777777", "Отсутствует услуга"))
h = Ticket()
(h.new_ticket('867', "86666666666", "Отсутствует услуга"))
i = Ticket()
(i.new_ticket('567', "85555555555", "Отсутствует услуга"))
set_closed(2)
