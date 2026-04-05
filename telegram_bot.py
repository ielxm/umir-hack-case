from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from typing import Tuple

import json
import asyncio

from pydantic_models import *

USERDATA_PATH="telegram_userdata.json"

def load_users_data() -> Tuple[str, list[str], list[int]]:
    with open(USERDATA_PATH, "r") as file:
        data = json.load(file)

    token: str = data.get("token")
    users: List[str] = data.get("users")
    workers: List[int] = data.get("workers")

    if not token:
        raise ValueError(f"Ошибка: TOKEN не может быть пуст. Возможно, USERDATA_PATH поверждён или не существует")

    return (token, users, workers)

def append_worker(worker: int) -> None:
    indent_size = 2
    
    with open(USERDATA_PATH, "r") as file:
        data = json.load(file)
        data["workers"].append(worker)

    with open(USERDATA_PATH, "w") as file:
        json.dump(data, file, indent=indent_size, ensure_ascii=False)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user is None: 
        return
    
    if update.message is None:
        return
    
    user = update.effective_user
    message = update.message # pyright: ignore[reportUnusedVariable]

    _, users, workers = load_users_data()

    if user.username is not None and user.username in users:
        if user.id not in workers:
            append_worker(user.id)
            await update.message.reply_text("Вы были подписаны на получение уведомлений о новых заявках.")
        else:
            await update.message.reply_text("Вы уже подписаны на получение уведомлений о новых заявках. \nПри поступление новой заявки вы будете уведомлены.")

    else:
        await update.message.reply_text("Вам не позволено взаимодействовать с данным Telegram-ботом.")

async def send_to_telegram(form: QuizForm) -> None:
    token, _, workers = load_users_data()
    contacts = form.contacts
    rooms_to_include = ", ".join(form.rooms_to_include).lower()

    bot = Bot(token=token)
    
    text = (
        f"<b>Новая заявка на дизайн проект!</b>\n\n"
        
        f"<b>▫️ Тип помещения:</b> {form.apartment_type}\n"
        f"<b>▫️ Зоны:</b> {rooms_to_include}\n"
        f"<b>▫️ Площадь:</b> {form.size:g} м²\n"
        f"<b>▫️ Бюджет:</b> {form.budget:g} млн. ₽\n\n"

        f"{f'<b>▫️ Комментарий:</b> {form.comment}\n\n' if form.comment else ''}"

        f"<b>Контакты заказчика:</b>\n"
        f"<b>👤 Имя:</b> {contacts.name}\n"
        f"<b>📞 Номер телефона:</b> <code>{contacts.phone_number}</code>\n"
        f"<b>📧 E-mail:</b> {contacts.email}"
    )

    for id in workers:
        try:
            await bot.send_message(
                chat_id=id,
                text=text,
                parse_mode="HTML"
            )
        
        except Exception as error:
            raise RuntimeError(f"Ошибка: [worker: {id}] - {error}")

async def run_telegram_bot():
    token, _, _ = load_users_data()
    
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    await app.initialize()
    await app.start()
    
    if app.updater:
        await app.updater.start_polling()
        await asyncio.Event().wait()
    else:
        raise RuntimeError("Ошибка: app.updater не может быть None")