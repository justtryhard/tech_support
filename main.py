import flet as ft
from flet import View, Page, AppBar, ElevatedButton, Text
from flet import RouteChangeEvent, ViewPopEvent, CrossAxisAlignment, MainAxisAlignment


def main(page: ft.Page) -> None:
    page.title = 'Support'
    ticket1 = ft.TextField(label="Введите номер договора", width=250)
    ticket2 = ft.TextField(label="Введите контактный номер или email", width=400)
    ticket3 = ft.TextField(label="Опишите суть проблемы")
    current_ticket = []
    user_ip = ('IP: 77.86.142.143, '
               'Маска: 255.255.255.0, '
               'Шлюз:77.86.142.1,'
               'DNS: 10.30.30.2, '
               'DNS: 10.30.30.3')


    def btn_click(e):
        if not ticket1.value:
            ticket1.error_text = "Введите номер договора"
            page.update()

        #в идеале допилить проверку на существование данного номера договора

        elif not ticket2.value:
            ticket2.error_text = "Укажите контактные данные"
            page.update()
        elif not ticket3.value:
            ticket3.error_text = "Опишите суть проблемы"
            page.update()
        else:
            current_ticket.append(ticket1.value)
            current_ticket.append(ticket2.value)
            current_ticket.append(ticket3.value)
            # тут current_ticket должен отправиться в бд в виде заявки
            print(current_ticket)
            page.clean()
            page.go('/ticket1')

    def btn_click_for_ip(e):
        if not ticket1.value:
            ticket1.error_text = "Введите номер договора"
            page.update()
            # также нужна проверка на существование договора в бд
        else:
            # здесь программа должна отправить ticket1.value в бд, достать соответствующее значение
            # и упаковать его в переменную user_ip
            page.clean()
            page.go('/ips1')

    def route_change(e: RouteChangeEvent) -> None:
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
                        AppBar(title=Text('Спасибо!'), bgcolor='blue'),
                        Text(value='Ваша заявка принята! В ближайшее время с Вами свяжутся', size=30),
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

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=main)
