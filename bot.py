import asyncio
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import admin_handlers, student_handlers, tutor_handlers

async def main():
    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    dp.include_router(admin_handlers.router)
    dp.include_router(student_handlers.router)
    dp.include_router(tutor_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
