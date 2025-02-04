from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from bot.states import States


class Buttons:
    """Defines text labels for main menu buttons."""

    ADD = "➕ Add new task"
    ALL = "📇 All tasks"
    VIEW_TASK = "🎯 Task by №"
    REGISTRATION = "😎 Registration"
    HELP = "Help"


class InlineButtons:
    """Defines callback data for inline buttons."""

    pass


class Labels:
    """UI Labels for Buttons and Messages."""

    pass


class Keyboards:
    """Defines main menu keyboards with reply buttons."""

    RegistrationMenu = ReplyKeyboardMarkup(
        [[KeyboardButton(Buttons.REGISTRATION), KeyboardButton(Buttons.HELP)]], resize_keyboard=True
    )

    MainMenu = ReplyKeyboardMarkup(
        [
            [KeyboardButton(Buttons.ADD), KeyboardButton(Buttons.ALL), KeyboardButton(Buttons.VIEW_TASK)],
            [KeyboardButton(Buttons.HELP)],
        ],
        resize_keyboard=True,
    )

    Hide = ReplyKeyboardRemove()


class InlineKeyboards:
    """Defines inline keyboards for task actions."""

    pass
