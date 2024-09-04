import flet as ft
from flet import View, AppBar, ElevatedButton, Text
from flet import RouteChangeEvent, ViewPopEvent, CrossAxisAlignment, MainAxisAlignment
import sqlite3
from sqlite3 import Error
from db.ticket import Ticket, actual_tickets, pre_ticket, print_ticket, set_closed
from db.problem import problem_set_closed, actual_problems, pre_problem, print_problem, set_ttr

current_ticket: int
current_problem: int


def main(page: ft.Page) -> None:
    page.title = 'Support'
    ticket_enter = ft.TextField(label="Укажите ID заявки", width=250)
    problem_enter = ft.TextField(label="Укажите ID аварии", width=250)
    ttr_enter = ft.TextField(label="Укажите время в формате: ДД/ММ/ГГГГ, ЧЧ:ММ", width=250)
    ticket1 = ft.TextField(label="Введите номер договора", width=250)
    ticket2 = ft.TextField(label="Введите контактный номер или email", width=400)
    ticket3 = ft.TextField(label="Опишите суть проблемы")

    def btn_click(e):
        cnt = 0
        with sqlite3.connect('db/database.db') as db:
            cursor = db.cursor()
            cursor.execute(""" SELECT id FROM clients """)
            rows = cursor.fetchall()
            ids = [row[0] for row in rows]
            if not ticket1.value or int(ticket1.value) not in ids:
                ticket1.error_text = "Номер договора не найден"
                page.update()
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
            page.go('/new_ticket1')

    def ticket_watch(e):
        with sqlite3.connect('db/database.db') as db:
            cursor = db.cursor()
            cursor.execute(""" SELECT id FROM tickets""")
            rows = cursor.fetchall()
            ids = [row[0] for row in rows]
            if not ticket_enter.value or int(ticket_enter.value) not in ids:
                ticket_enter.error_text = "Заявка не найдена"
                page.update()
            else:
                page.clean()
                global current_ticket
                current_ticket = int(ticket_enter.value)
                page.go('/tickets2')

    def close_ticket(e):
        with sqlite3.connect('db/database.db') as db:
            cursor = db.cursor()
            cursor.execute(""" SELECT id FROM tickets""")
            rows = cursor.fetchall()
            ids = [row[0] for row in rows]
            if not ticket_enter.value or int(ticket_enter.value) not in ids:
                ticket_enter.error_text = "Заявка не найдена"
                page.update()
            else:
                set_closed(int(ticket_enter.value))
                page.clean()
                page.go('/tickets3')

    def problem_watch(e):
        with sqlite3.connect('db/database.db') as db:
            cursor = db.cursor()
            cursor.execute(""" SELECT id FROM problems""")
            rows = cursor.fetchall()
            ids = [row[0] for row in rows]
            if not problem_enter.value or int(problem_enter.value) not in ids:
                problem_enter.error_text = "Авария не найдена"
                page.update()
            else:
                page.clean()
                global current_problem
                current_problem = int(problem_enter.value)
                page.go('/problems2')

    def problem_set_ttr(e):
        set_ttr(current_problem, ttr_enter.value)
        page.clean()
        page.go('/problems4')

    def close_problem(e):
        with sqlite3.connect('db/database.db') as db:
            cursor = db.cursor()
            cursor.execute(""" SELECT id FROM problems""")
            rows = cursor.fetchall()
            ids = [row[0] for row in rows]
            if not problem_enter.value or int(problem_enter.value) not in ids:
                problem_enter.error_text = "Авария не найдена"
                page.update()
            else:
                set_closed(int(problem_enter.value))
                page.clean()
                page.go('/problems3')

    def route_change(e: RouteChangeEvent) -> None:
        page.views.clear()

        page.views.append(
            View(
                route='/',
                controls=[
                    AppBar(title=Text('Здравствуйте!'), bgcolor='blue'),
                    Text(value='Выберите вариант из предложенных:', size=30),
                    ElevatedButton(text='Заявки', on_click=lambda _: page.go('/tickets')),
                    ElevatedButton(text='Аварии', on_click=lambda _: page.go('/problems')),
                ],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=26
            )
        )

        if page.route == '/tickets':
            page.views.append(
                View(
                    route='/tickets',
                    controls=[
                        AppBar(title=Text('Заявки'), bgcolor='blue'),
                        Text(value='Актуальные заявки:', size=15),
                        Text(value=actual_tickets(), size=20),
                        Text(value='Посмотреть информацию по заявке', size=15),
                        ticket_enter,
                        ft.ElevatedButton(text="Открыть", on_click=ticket_watch),
                        ft.ElevatedButton(text="СОЗДАТЬ НОВУЮ ЗАЯВКУ", on_click=lambda _: page.go('/new_ticket')),
                        ElevatedButton(text='Назад', on_click=lambda _: page.go('/'))
                    ],

                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26

                )

            )

        if page.route == '/tickets2':
            page.views.append(
                View(
                    route='/tickets2',
                    controls=[
                        AppBar(title=Text('Заявки'), bgcolor='blue'),
                        Text(value=f'Заявка №{current_ticket}', size=30),
                        Text(value=pre_ticket(current_ticket), size=30),
                        Text(value=print_ticket(current_ticket), size=30),
                        ft.ElevatedButton(text="Закрыть заявку", on_click=close_ticket),
                        ElevatedButton(text='Назад', on_click=lambda _: page.go('/'))
                    ],

                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26

                )
            )
        if page.route == '/tickets3':
            page.views.append(
                View(
                    route='/tickets3',
                    controls=[
                        AppBar(title=Text('Заявки'), bgcolor='blue'),
                        Text(value=f'Заявка №{current_ticket} была закрыта!', size=30),
                        ElevatedButton(text='К заявкам', on_click=lambda _: page.go('/tickets')),
                        ElevatedButton(text='В начало', on_click=lambda _: page.go('/'))
                    ],

                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26

                )
            )
        if page.route == '/new_ticket':
            page.views.append(
                View(
                    route='/new_ticket',
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

        if page.route == '/new_ticket1':
            page.views.append(
                View(
                    route='/new_ticket1',
                    controls=[
                        AppBar(title=Text('Заявка создана'), bgcolor='blue'),
                        ElevatedButton(text='К заявкам', on_click=lambda _: page.go('/tickets')),
                        ElevatedButton(text='В начало', on_click=lambda _: page.go('/'))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26

                )

            )

        if page.route == '/problems':
            page.views.append(
                View(
                    route='/problems',
                    controls=[
                        AppBar(title=Text('Аварии'), bgcolor='blue'),
                        Text(value='Актуальные аварии (id и адрес:', size=15),
                        Text(value=actual_problems(), size=20),
                        Text(value='Посмотреть информацию об аварии:', size=15),
                        problem_enter,
                        ft.ElevatedButton(text="Открыть", on_click=problem_watch),
                        ElevatedButton(text='Назад', on_click=lambda _: page.go('/'))
                    ],

                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26

                )

            )
        if page.route == '/problems2':
            page.views.append(
                View(
                    route='/problems2',
                    controls=[
                        AppBar(title=Text('Авария'), bgcolor='blue'),
                        Text(value=f'Авария №{current_problem}', size=30),
                        Text(value=pre_problem(current_problem), size=30),
                        Text(value=print_problem(current_problem), size=30),
                        ft.ElevatedButton(text="Закрыть аварию", on_click=close_problem),
                        Text(value=f'Изменить TTR:', size=30),
                        ttr_enter,
                        ft.ElevatedButton(text="Изменить", on_click=problem_set_ttr),
                        ElevatedButton(text='Назад', on_click=lambda _: page.go('/'))
                    ],

                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26

                )

            )
        if page.route == '/problems3':
            page.views.append(
                View(
                    route='/problems3',
                    controls=[
                        AppBar(title=Text('Аварии'), bgcolor='blue'),
                        Text(value=f'Авария №{current_problem} была закрыта!', size=30),
                        ElevatedButton(text='К авариям', on_click=lambda _: page.go('/problems')),
                        ElevatedButton(text='В начало', on_click=lambda _: page.go('/'))
                    ],

                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26

                )
            )
        if page.route == '/problems4':
            page.views.append(
                View(
                    route='/problems4',
                    controls=[
                        AppBar(title=Text('Аварии'), bgcolor='blue'),
                        Text(value=f'Авария №{current_problem} была изменена!', size=30),
                        ElevatedButton(text='К авариям', on_click=lambda _: page.go('/problems')),
                        ElevatedButton(text='В начало', on_click=lambda _: page.go('/'))
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

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=main)
