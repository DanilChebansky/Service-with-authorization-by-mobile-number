# Service-with-authorization-by-mobile-number
Сервис, который позволяет пользователям регистрироваться и авторизовываться по номеру телефона, а также использовать и распространять инвайт-коды.

## Использование c помощью **Docker**
* В виртуальном окружении загрузите зависимости:
  
```sh
$ pip install -r requirements.txt
```

* Добавьте файл **.env** (по примеру **.env.sample**)
* Запустите терминал и выполните команду:

```sh
$ docker-compose up -d --build
```

## Разработка

Реализовано 2 приложения:
`interface` - интерфейс на Django Templates для базового тестирования функционала. /
`users` - API представление

### users:

Модель **User**:

* *phone*
* *email*
* *city*
* *invite_code* - код приглашения
* *invite_input* - вводимый код приглашения от другого пользователя

#### Контроллеры:

* для создания пользователя
* для получения данных пользователя
* для редактирования данных
* для выведения списка пользователя (доступно только для администратора)
* для удаления пользователя (доступно только для администратора)

#### Сервисные функции:

* create_invite_code - функция, создающая код для приглашения и проверяющая его на уникальность

#### Валидация:

* Реализована валидация номера телефона на количество цифр и корректность

### interface:

* Реализован простейший интерфейс с помощью **Django Templates** для тестирования функционала

### Отправка СМС:

* Имитирована функцией print() через 3 секунды после "отправки кода"

## Тестирование:

* Запуск тестирования:

```sh
$ coverage run --source='.' manage.py test
```

* Отображения статистики:

```sh
$ coverage report
```
или, если статистика необходима в виде файла .html:

```sh
$ coverage html
```
