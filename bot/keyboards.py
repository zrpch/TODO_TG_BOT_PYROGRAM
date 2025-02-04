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

    TOGGLE_STATUS = "toggle_status"
    EDIT_TITLE = "edit_task_title"
    EDIT_DESCRIPTION = "edit_task_description"
    DELETE_TASK = "delete_task"
    CANCEL_EDIT = "cancel_edit"


class Labels:
    """UI Labels for Buttons and Messages."""

    CANCEL_EDIT = "🚫 Cancel Editing"
    DELETE_TASK = "❌ Delete"

    TOGGLE_TODO = "➡️ TODO"
    TOGGLE_DONE = "✅ Done"
    EDIT_TITLE = "✏️ Title"
    EDIT_DESCRIPTION = "✏️ Descr"


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

    @staticmethod
    def TaskActions(task_id: int, is_completed: bool, user_state: str) -> InlineKeyboardMarkup:
        """
        Returns an inline keyboard for managing tasks.

        :param task_id: The unique ID of the task.
        :param is_completed: Whether the task is marked as completed.
        :param user_state: The current state of the user (e.g., editing).
        :return: Inline keyboard markup for task actions.
        """
        toggle_text = Labels.TOGGLE_TODO if is_completed else Labels.TOGGLE_DONE

        if user_state in {States.EDIT_TASK_TITLE, States.EDIT_TASK_DESCRIPTION}:
            buttons = [
                [InlineKeyboardButton(toggle_text, callback_data=f"{InlineButtons.TOGGLE_STATUS}:{task_id}")],
                [InlineKeyboardButton(Labels.CANCEL_EDIT, callback_data=f"{InlineButtons.CANCEL_EDIT}:{task_id}")],
                [InlineKeyboardButton(Labels.DELETE_TASK, callback_data=f"{InlineButtons.DELETE_TASK}:{task_id}")],
            ]
        else:
            buttons = [
                [InlineKeyboardButton(toggle_text, callback_data=f"{InlineButtons.TOGGLE_STATUS}:{task_id}")],
                [
                    InlineKeyboardButton(Labels.EDIT_TITLE, callback_data=f"{InlineButtons.EDIT_TITLE}:{task_id}"),
                    InlineKeyboardButton(
                        Labels.EDIT_DESCRIPTION, callback_data=f"{InlineButtons.EDIT_DESCRIPTION}:{task_id}"
                    ),
                ],
                [InlineKeyboardButton(Labels.DELETE_TASK, callback_data=f"{InlineButtons.DELETE_TASK}:{task_id}")],
            ]

        return InlineKeyboardMarkup(buttons)
