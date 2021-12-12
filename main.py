import config
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pizza import register_handlers_pizza


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/pizza", description="Заказать пиццу"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():

    # Объявление и инициализация объектов бота и диспетчера для ТГ. Для VK и FB нужно будет создать свои конфиги. Но
    # не понятно какой API будет у них...
    bot = Bot(token=config.TG_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров для заказа пиццы
    register_handlers_pizza(dp)

    # Установка команд бота. Для старта необходимо нажать - /pizza. /cancel - отмена
    await set_commands(bot)

    #Стартуем polling
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())

