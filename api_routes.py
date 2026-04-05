from fastapi import APIRouter

from pydantic_models import *
from telegram_bot import *
from validation import *
from db import *

router = APIRouter(prefix="/api") # адрес формата: domain.example/api/...

@router.post("/submit") # domain.example/api/submit
async def submit(form: QuizForm):
    # ---> БД
    # ---> Отправка Боту

    # responce: status OK (если всё действительно OK)
    # если не OK: ответить стандартным HTTP-кодом
    
    if check_if_entry_is_unique(form): # проверка уникальности заявки
        
        # Отправить ЗАВЕДОМО КОРРЕКТНУЮ и уникальную форму избранным пользователям через Telegram-бота
        await send_to_telegram(form)
        
        # Сохранить ЗАВЕДОМО КОРРЕКТНУЮ и уникальную форму в базу данных
        # Немного тормозит работу, но не критично
        send_to_database(form)

    # Для удобства использования TODO: УДАЛИТЬ
    print(form)

    return {"status": "ok"}