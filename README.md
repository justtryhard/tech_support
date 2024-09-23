# Приложение, выполняющее функцию первой линии техподдержки интернет-провайдера


## database.py
Файл, при запуске которого создаётся database.db. Это тестовая база данных, она необходима для  тестирования приложения. БД имеет 3 таблицы: clients, tickets, problems.
Запускается вручную, либо с кнопки через приложение, в случае если приложение определило проблему с БД.

## main.py - запуск клиентского приложения
- приложение может принимать заявку от клиента и создавать в БД новый объект с уникальным ID;
- клиент может обратиться не по проблеме, а с вопросом о типе подключения или по необходимости узнать IP-адрес. В этом случае, приложению необходимо предоставить данные по его запросу;
- приложение может отвечать клиентам о наличии проблем на линии и сроках их устранения (в данном случаче происходит поиск по таблице problems в файле database.db, где closed != 0). Если ID клиента отсутствует среди актуальных аварий, сообщать клиенту и создавать в БД новую заявку;

## stp.py - запуск приложения для сотрудников технической поддержки
- в приложении можно просматривать список актуальных заявок, открывать заявку по ID для получения более подробной информации. На вкладке со списком заявок можно создать новую заявку, точно также как и в приложении для клиентов;
- можно производить аналогичные действия с авариями, а также менять параметр time_to_resolve;
- на страницах со списком тикетов и проблем можно закрыть необходимый тикет или проблему по ID. Допускается также закрытие уже закрытого тикета, в этом случае ничего не произойдёт.
  

## ticket.py
Файл, описывающий класс Ticket, созданный для взаимодействия main.py и таблицы tickets в database.db. 
Класс имеет атрибуты: id(int), cl_id(int) - номер договора, contact(str) - контакт, description(str) - описание, closed(bool) - сведения о решённости/нерешённости. 
id заявки генерируется автоматически при создании, поле close по умолчанию равно 0, остальные поля вводятся клиентом в соответствующем разделе при запуске main.py.

## problem.py
Аналогичный ticket'у файл, описывающий класс Problem (Аварии).
Класс имеет атрибуты: id(str), address(str), description(str) - описание, clients - информация о клиентах, затронутых данной аварией, time_to_resolve(str) - срок устранения, closed(bool) - сведения о решённости/нерешённости. 
id заявки генерируется автоматически при создании, поле close по умолчанию равно 0, остальные поля вводятся клиентом в соответствующем разделе при запуске main.py.


# в разработке:
- клиент может обратиться по иному поводу, в таком случае приложение должно задать ему несколько вопросов с вариантами ответа, собрать контактные данные клиента и, в зависимости от ответов, направить заявку в тех. поддержку, в отдел продаж, либо в финансовый отдел **(в разработке)**;
