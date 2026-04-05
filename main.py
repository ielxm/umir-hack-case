import uvicorn
import asyncio

from api import app
from db import initialize_database
from telegram_bot import run_telegram_bot

API_ADDRESS = "127.0.0.1"
API_PORT = 8000

async def main():
    # Инициализация базы данных
    initialize_database()
    
    uvicorn_config = uvicorn.Config(app, host=API_ADDRESS, port=API_PORT, loop="asyncio")
    uvicorn_server = uvicorn.Server(uvicorn_config)

    await asyncio.gather(
        uvicorn_server.serve(),
        run_telegram_bot()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Уведомление: Процесс успешно остановлен")