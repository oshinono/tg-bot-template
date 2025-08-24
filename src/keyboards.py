from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import Base

async def get_index_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            
        ]
    )

async def get_simple_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад ⬅️", callback_data="back")]
        ]
    )

async def get_default_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад ⬅️", callback_data="back")],
            [InlineKeyboardButton(text="Главная 🔙", callback_data="index")]
        ]
    )

async def get_objects_keyboards(objects: list[Base], name: str, current_sort: str = None) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()

    if objects:
        for i, object in enumerate(objects):
            data = f"{name}_{getattr(object, 'id', i)}"
            b.add(InlineKeyboardButton(text=str(object), callback_data=data))

        b.adjust(2, repeat=True)

    b.row(InlineKeyboardButton(text="+", callback_data=f"add_new_{name}"))
    b.row(InlineKeyboardButton(text="Назад ⬅️", callback_data="index"))

    return b.as_markup()


async def get_delete_message():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Скрыть", callback_data="delete_notification")]
    ])