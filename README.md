# Приложение, выполняющее функцию первой линии техподдержки интернет-провайдера

- приложение может принимать заявку от клиента и создавать в БД новый объект с уникальным ID. Объект имеет 4 поля: ID заявки, ID клиента, контакт для связи, суть проблемы. Первое поле генерируется автоматически, остальные вводятся клиентом;
- приложение может отвечать клиентам о наличии проблем на линии и сроках их устранения. Если информация о проблеме отсутствует в БД, сообщать клиенту о передаче обращения в службу тех. поддержки (в разработке);
- сотрудники поддержки должны иметь право вносить в БД информацию о неполадках и о том, какие ID клиентов затронуты данной проблемой. Предполагаю, что информация о неполадках будет храниться в отдельной таблице (в разработке);
- клиент может обратиться не по проблеме, а с вопросом о типе подключения или по необходимости узнать IP-адрес. В этом случае, приложению необходимо предоставить данные по его запросу - готово;
- клиент может обратиться по иному поводу, в таком случае приложение должно задать ему несколько вопросов с вариантами ответа, собрать контактные данные клиента и, в зависимости от ответов, направить заявку в тех. поддержку, в отдел продаж, либо в финансовый отдел (в разработке);
