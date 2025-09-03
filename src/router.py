from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import get_index_keyboard
from aiogram.fsm.context import FSMContext
from utils import clear_state

router = Router()


async def handle_index(update: Message | CallbackQuery, state: FSMContext):
    await clear_state(state)
    text = "Telegram Template by oshinoko"
    keyboard = await get_index_keyboard()

    if isinstance(update, Message):
        await update.answer(text, reply_markup=keyboard)
    else:
        await update.message.edit_text(text, reply_markup=keyboard)


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await handle_index(message, state)


@router.callback_query(F.data == "index")
async def index_callback(callback: CallbackQuery, state: FSMContext):
    await handle_index(callback, state)


@router.callback_query(F.data == "delete_notification")
async def remove_noti(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == "empty")
async def empty(callback: CallbackQuery):
    await callback.answer()
