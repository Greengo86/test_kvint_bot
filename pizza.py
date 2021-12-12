from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

available_payment_method = ["картой", "наличкой"]
available_pizza_sizes = ["маленькую", "большую"]
available_confirm_order = ['да', 'нет']


class OrderPizza(StatesGroup):
    waiting_for_pizza_sizes = State()
    waiting_for_payment_method = State()
    waiting_for_confirm_order = State()


async def pizza_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_pizza_sizes:
        keyboard.add(name)
    await message.answer("Какую пиццу Вы хотите? Маленькую или большую?", reply_markup=keyboard)
    await OrderPizza.waiting_for_pizza_sizes.set()


async def pizza_size_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_pizza_sizes:
        # Если выбрали не тот размер пиццы, что предполагали
        await message.answer("Пожалуйста, выберите размер пиццы")
        return
    await state.update_data(size_chosen_pizza=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_payment_method:
        keyboard.add(size)
    await message.answer("Как Вы будете платить", reply_markup=keyboard)
    await state.set_state(OrderPizza.waiting_for_payment_method)


async def payment_method_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_payment_method:
        await message.answer("Пожалуйста, выберите способ оплаты")
        return
    await state.update_data(payment_method=message.text.lower())
    user_data = await state.get_data()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for size in available_confirm_order:
        keyboard.add(size)

    await state.set_state(OrderPizza.waiting_for_confirm_order)
    await message.answer(
        # Здесь в строку надо выводить предыдущие ответы по размеру и оплате
        f"Вы хотите {user_data['size_chosen_pizza']} пиццу, оплата {message.text.lower()}?",
        reply_markup=keyboard
    )


async def confirm_order(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_confirm_order:
        await message.answer("Какую пиццу Вы хотите и какой способ оплаты")
        return
    await state.update_data(order_confirm=message.text.lower())

    if message.text.lower() == 'нет':
        # Если пользователь ответит "Нет" начнём диалог Бота сначала
        await state.finish()
        await pizza_start(message)
        return

    await message.answer("Спасибо за заказ", reply_markup=types.ReplyKeyboardRemove())
    # Закончили
    await state.finish()


def register_handlers_pizza(dp: Dispatcher):
    dp.register_message_handler(pizza_start, commands="pizza", state="*")
    dp.register_message_handler(pizza_size_chosen, state=OrderPizza.waiting_for_pizza_sizes)
    dp.register_message_handler(payment_method_chosen, state=OrderPizza.waiting_for_payment_method)
    dp.register_message_handler(confirm_order, state=OrderPizza.waiting_for_confirm_order)
