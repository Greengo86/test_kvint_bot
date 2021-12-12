import pytest
from unittest.mock import AsyncMock
import pizza
from aiogram.contrib.fsm_storage.memory import MemoryStorage


@pytest.mark.asyncio
async def test_pizza_size_handler():
    text_mock = "маленькую"
    message_mock = AsyncMock(text=text_mock)
    state_mock = AsyncMock(storage=MemoryStorage())
    await pizza.pizza_size_chosen(message=message_mock, state=state_mock)
    message_mock.answer.assert_called_with(text_mock)


@pytest.mark.asyncio
async def test_payment_method_handler():
    text_mock = "картой"
    message_mock = AsyncMock(text=text_mock)
    state_mock = AsyncMock(storage=MemoryStorage())
    await pizza.payment_method_chosen(message=message_mock, state=state_mock)
    message_mock.answer.assert_called_with(text_mock)
