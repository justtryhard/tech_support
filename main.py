import database
import flet as ft
from flet import View, AppBar, ElevatedButton, Text
from flet import RouteChangeEvent, ViewPopEvent, CrossAxisAlignment, MainAxisAlignment
import sqlite3
from db.ticket import Ticket

user_ip = ""        # хранит айпи адрес пользователя между взятием из БД и передачей пользователю
ttr: int            # хранит информацию по срокам аварии между взятием из БД передачей пользователю


def main(page: ft.Page) -> None:   # текстовые поля для заполнения заявки пользователем
    page.title = 'Support'
    ticket1 = ft.TextField(label="Введите номер договора", width=250)
    ticket2 = ft.TextField(label="Введите контактный номер или email", width=400)
    ticket3 = ft.TextField(label="Опишите суть проблемы")

    def btn_click(e):  # здесь реализован алгоритм оставления заявки пользователем
        cnt = 0
        with sqlite3.connect('db/database.db') as db:
            problem_trigger = False
            cursor = db.cursor()
            cursor.execute(""" SELECT id FROM clients """)
            cursor1 = db.cursor()
            cursor1.execute(""" SELECT id, clients FROM problems WHERE closed = 0 """)
            rows = cursor.fetchall()
            ids = [row[0] for row in rows]
            rows1 = cursor1.fetchall()
            p_clients = [row[1] for row in rows1]
            list_clients = []
            for elem in p_clients:
                list_clients.append(list(elem.split(",")))
            problems_and_clients = dict(zip([row[0] for row in rows1], list_clients))
            for elem in problems_and_clients.values():
                if ticket1.value in elem:
                    problem = list(problems_and_clients.keys())[list(problems_and_clients.values()).index(elem)]
                    problem_trigger = True
                    cursor2 = db.cursor()
                    cursor2.execute(""" SELECT time_to_resolve FROM problems WHERE id = ?""", [problem])
                    rows = cursor2.fetchall()
                    global ttr
                    ttr = [row[0] for row in rows]
            if not ticket1.value.isdigit():
                ticket1.error_text = "Допустимы только цифры"
                page.update()
            elif not ticket1.value or int(ticket1.value) not in ids:
                ticket1.error_text = "Номер договора не найден в базе"
                page.update()
            elif problem_trigger is True:
                page.clean()
                page.go('/ticket2')
            else:
                ticket1.error_text = None
                page.update()
                cnt += 1

        if not ticket2.value:
            ticket2.error_text = "Укажите контактные данные"
            page.update()
        else:
            ticket2.error_text = None
            page.update()
            cnt += 1
        if not ticket3.value:
            ticket3.error_text = "Опишите суть проблемы"
            page.update()
        else:
            ticket3.error_text = None
            page.update()
            cnt += 1
        if cnt >= 3:
            a = Ticket()
            a.new_ticket(ticket1.value, ticket2.value, ticket3.value)
            page.clean()
            page.go('/ticket1')

    def btn_click_for_ip(e):        # здесь реализован алгоритм запроса IP пользователя
        with sqlite3.connect('db/database.db') as db:
            cursor = db.cursor()
            cursor.execute(""" SELECT id, ip FROM clients """)
            rows = cursor.fetchall()
            ips = {row[0]: row[1] for row in rows}
            if not ticket1.value.isdigit():
                ticket1.error_text = "Допустимы только цифры"
                page.update()
            elif not ticket1.value or int(ticket1.value) not in ips:
                ticket1.error_text = "Номер договора не найден в базе"
                page.update()
            else:
                global user_ip
                user_ip = str(ips.get(int(ticket1.value)))
                print(user_ip)
                page.clean()
                page.go('/ips1')

    def database_runtest(e): ## функция создания тестовой БД
        database.create()
        page.clean()
        page.go('/')

    def route_change(e: RouteChangeEvent) -> None:   #функция, отвечающая за смену страниц в приложении
        page.views.clear()

        page.views.append(
            View(
                route='/',
                controls=[
                    AppBar(title=Text('Здравствуйте!'), bgcolor='blue'),
                    Text(value='Выберите вариант из предложенных:', size=30),
                    ElevatedButton(text='Оставить заявку', on_click=lambda _: page.go('/ticket')),
                    ElevatedButton(text='Узнать настройки для роутера', on_click=lambda _: page.go('/ips')),
                    ElevatedButton(text='Иной вопрос', on_click=lambda _: page.go('/other'))
                ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=26
            )
        )
        if page.route == '/db_trouble':
            page.views.append(
                View(
                    route='/db_trouble',
                    controls=[
                        AppBar(title=Text('Некорректная БД'), bgcolor='blue'),
                        Text(value='База данных отсутствует или имеет некорректный формат', size=30),
                        Text(value='Для работы приложения следует привести БД к формату, указанному ниже:', size=15),
                        ft.Image(src='database.png'),
                        Text(value='Если Вам необходимо протестировать работу приложения, '
                                   'нажмите на кнопку ниже', size=15),
                        ElevatedButton(text='Создать тестовую БД', on_click=database_runtest),
                        ElevatedButton(text='Выйти из приложения', on_click=lambda _: page.window_close())
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26

                )

            )
        #Ticket
        if page.route == '/ticket':
            page.views.append(
                View(
                    route='/ticket',
                    controls=[
                        AppBar(title=Text('Заявка'), bgcolor='blue'),
                        Text(value='Заполните форму ниже:', size=30),
                        ticket1, ticket2, ticket3,
                        ft.ElevatedButton(text="Отправить заявку", on_click=btn_click),
                        ElevatedButton(text='Назад', on_click=lambda _: page.go('/'))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26

                )

            )

        if page.route == '/ticket1':
            page.views.append(
                View(
                    route='/ticket1',
                    controls=[
                        AppBar(title=Text('Спасибо за обращение!'), bgcolor='blue'),
                        Text(value='Ваша заявка принята! В ближайшее время с Вами свяжутся', size=30),
                        ElevatedButton(text='В начало', on_click=lambda _: page.go('/'))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26

                )

            )

        if page.route == '/ticket2':
            page.views.append(
                View(
                    route='/ticket2',
                    controls=[
                        AppBar(title=Text('Спасибо за обращение!'), bgcolor='blue'),
                        Text(value='В текущий момент по Вашему адресу наблюдаются технические неполадки', size=30),
                        Text(value='Срок устранения:', size=30),
                        Text(value=ttr, size=30),
                        ElevatedButton(text='В начало', on_click=lambda _: page.go('/'))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26

                )

            )

        # IP
        if page.route == '/ips':
            page.views.append(
                View(
                    route='/ips',
                    controls=[
                        AppBar(title=Text('Узнать настройки для роутера'), bgcolor='blue'),
                        ticket1,
                        ft.ElevatedButton(text="Отправить", on_click=btn_click_for_ip),
                        ElevatedButton(text='Назад', on_click=lambda _: page.go('/'))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )

        if page.route == '/ips1':
            page.views.append(
                View(
                    route='/ips1',
                    controls=[
                        AppBar(title=Text('Узнать настройки для роутера'), bgcolor='blue'),
                        Text(value='Ваш IP адрес:', size=30),
                        Text(value=user_ip, size=30),
                        ElevatedButton(text='В начало', on_click=lambda _: page.go('/'))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )
        # other
        if page.route == '/other':
            page.views.append(
                View(
                    route='/other',
                    controls=[
                        AppBar(title=Text('Иные вопросы'), bgcolor='blue'),
                        Text(value='С чем связан ваш вопрос?', size=30),
                        ElevatedButton(text='Добавить', on_click=lambda _: page.go('/')),
                        ElevatedButton(text='Кнопки', on_click=lambda _: page.go('/')),
                        ElevatedButton(text='И возможные', on_click=lambda _: page.go('/')),
                        ElevatedButton(text='Вопросы', on_click=lambda _: page.go('/'))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26

                )

            )

        page.update()

    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)

    try:
        conn = sqlite3.connect('db/database.db')
        cursor = conn.cursor()
        cursor.execute(""" SELECT id, address, description, clients, time_to_resolve, closed FROM problems """)
        cursor.execute(""" SELECT id, name, address, ip FROM clients """)
        cursor.execute(""" SELECT id, client_id, contact, description, closed FROM tickets """)
        print("Подключен к SQLite")
        cursor.close()
        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)

    except:
        print("Ошибка при работе с SQLite")
        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go('/db_trouble')

    finally:
        if conn:
            conn.close()
            print("Соединение с SQLite закрыто")


if __name__ == '__main__':
    ft.app(target=main)
