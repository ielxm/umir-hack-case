# Backend (by [alexwahry](https://github.com/alexwahry))

## Используемые технологии
- [FastAPI](https://github.com/fastapi/fastapi)
- [Pydantic](https://github.com/pydantic/pydantic).
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [python-phonenumbers](https://github.com/daviddrysdale/python-phonenumbers)

## Структура проекта

```plaintext
QUIZ-HACKATHON//BACKEND 
├── api.py
├── api_routes.py
├── constants.py
├── db.py
├── main.py
├── pydantic_models.py
├── telegram_bot.py
└── validation.py
```

- ``api_routes.py`` - точки входа API
- ``api.py`` - конфигурация FastAPI, импорт из ``api_routes.py``
- ``pydantic_models.py`` - модели Pydantic
- ``constants.py`` - литерал'ы для валидации входящих данных
- ``db.py`` - реализация работы с базой данных SQLite3
- ``main.py`` - общая точка входа
- ``telegram_bot.py`` - реализация Telegram-бота
- ``validation.py`` - реализация валидации различных данных

## ``telegram_userdata.json``

Для работы с Telegram-ботом необходимо заполнить ``telegram_userdata.json`` по следующему образцу:
```json
{
  "token": "токен_Telegram-бота",
  "users": ["никнеймы(хэндлы)", "пользователей", "которые", "могут", "взаимодействовать", "с", "ботом"],
  "workers": ["оставьте", "пустым"]
}
```
Пользователям из ``users`` необходимо будет пройти регистрацию, написав боту ``/start``. После этого их ``user_id`` будет добавлен в ``workers``, и при поступление новой заявки они будут уведомлены. 