import logging

from pyrogram.client import Client
from pyrogram.types import CallbackQuery, Message

from bot.keyboards import Buttons, InlineButtons, InlineKeyboards, Keyboards
from bot.messages import Messages
from bot.states import Keys, States
from bot.utils import get_task_status_icon
from cache.cache import Cache
from database.database import Database

db = Database()
cache = Cache()


class TaskHandler:
    """Handles text messages and user interactions in the chat."""

    def __init__(self, client: Client) -> None:
        self.client = client

    async def handle_updates(self, client: Client, message: Message) -> None:
        """Processes user messages and determines the correct action."""
        uid = str(message.chat.id)
        state = cache.get_user_cache(uid, Keys.STATE)
        user = db.get_user(uid)

        if state:
            await self.process_state(uid, state, message)
        else:
            await self.process_command(uid, user, message)

    async def process_state(self, uid: str, state: str, message: Message) -> None:
        """Handles different user states."""
        state_handlers = {
            States.ENTER_NAME: self.register_name,
            States.ENTER_USERNAME: self.register_username,
            States.ENTER_TASK_TITLE: self.add_task_title,
            States.ENTER_TASK_DESCRIPTION: self.add_task_description,
            States.ENTER_TASK_NUMBER: self.view_task_by_number,
            States.EDIT_TASK_TITLE: self.edit_task_title,
            States.EDIT_TASK_DESCRIPTION: self.edit_task_description,
        }
        if state in state_handlers:
            await state_handlers[state](uid, message)

    async def process_command(self, uid: str, user: object, message: Message) -> None:
        """Handles user commands outside of states."""
        command_handlers = {
            "/start": self.handle_start,
            Buttons.REGISTRATION: self.initiate_registration,
            Buttons.ALL: self.list_all_tasks,
            Buttons.ADD: self.initiate_task_creation,
            Buttons.VIEW_TASK: self.request_task_number,
            "/help": self.handle_help,
            Buttons.HELP: self.handle_help,
        }

        handler = command_handlers.get(message.text)
        if handler:
            if handler in [self.handle_start, self.handle_help]:
                await handler(uid, user, message)  # type: ignore
            else:
                await handler(uid, message)  # type: ignore
        else:
            await self.handle_unknown_command(message)

    async def handle_start(self, uid: str, user: object, message: Message) -> None:
        """Handles the /start command."""
        await message.reply(
            Messages.START_REGISTERED if user else Messages.START_NEW,
            reply_markup=Keyboards.MainMenu if user else Keyboards.RegistrationMenu,
        )

    async def handle_help(self, uid: str, user: object, message: Message) -> None:
        """Handles the /help or Help button command."""
        await message.reply(Messages.HELP_TEXT, reply_markup=Keyboards.MainMenu)

    async def handle_unknown_command(self, message: Message) -> None:
        """Handles unknown commands."""
        await message.reply(Messages.UNKNOWN_COMMAND, reply_markup=Keyboards.MainMenu)

    async def list_all_tasks(self, uid: str, message: Message) -> None:
        """Lists all tasks for the user."""
        tasks = db.get_tasks(uid)

        if not tasks:
            await message.reply(Messages.NO_TASKS_YET, reply_markup=Keyboards.MainMenu)
        else:
            task_list = "\n".join(
                [f"{get_task_status_icon(bool(task[3]))} {i + 1}. {task[1]}" for i, task in enumerate(tasks)]
            )
            await message.reply(Messages.task_list(task_list), reply_markup=Keyboards.MainMenu)

    async def initiate_registration(self, uid: str, message: Message) -> None:
        """Starts the registration process."""
        await message.reply(Messages.ENTER_YOUR_NAME)
        cache.update_user_cache(uid, Keys.STATE, States.ENTER_NAME)

    async def initiate_task_creation(self, uid: str, message: Message) -> None:
        """Starts the task creation process."""
        await message.reply(Messages.ENTER_TASK_TITLE, reply_markup=Keyboards.Hide)
        cache.update_user_cache(uid, Keys.STATE, States.ENTER_TASK_TITLE)

    async def request_task_number(self, uid: str, message: Message) -> None:
        """Asks the user to enter a task number."""
        tasks = db.get_tasks(uid)

        if not tasks:
            await message.reply(Messages.NO_TASKS_YET, reply_markup=Keyboards.MainMenu)
        else:
            await message.reply(Messages.task_number_request(len(tasks)))
            cache.update_user_cache(uid, Keys.STATE, States.ENTER_TASK_NUMBER)

    async def register_name(self, uid: str, message: Message) -> None:
        """Processes the user's name during registration."""
        cache.update_user_cache(uid, Keys.NAME, message.text)
        cache.update_user_cache(uid, Keys.STATE, States.ENTER_USERNAME)
        await message.reply(Messages.ENTER_YOUR_USERNAME)

    async def register_username(self, uid: str, message: Message) -> None:
        """Handles username registration and checks if the username is already taken."""
        name = cache.get_user_cache(uid, Keys.NAME)
        username = message.text.strip()

        if db.get_user_by_username(username):
            await message.reply(Messages.USERNAME_EXISTS)
            return

        db.create_user(name, username, uid)
        cache.delete_user_cache(uid)
        await message.reply(Messages.welcome(name), reply_markup=Keyboards.MainMenu)

    async def add_task_title(self, uid: str, message: Message) -> None:
        """Adds a task title to the cache."""
        cache.update_user_cache(uid, Keys.TASK_TITLE, message.text)
        cache.update_user_cache(uid, Keys.STATE, States.ENTER_TASK_DESCRIPTION)
        await message.reply(Messages.ENTER_TASK_DESCRIPTION, reply_markup=Keyboards.Hide)

    async def add_task_description(self, uid: str, message: Message) -> None:
        """Saves the task to the database."""
        title = cache.get_user_cache(uid, Keys.TASK_TITLE)
        db.create_task(uid, title, message.text)
        cache.delete_user_cache(uid)
        await message.reply(Messages.TASK_ADDED, reply_markup=Keyboards.MainMenu)

    async def edit_task_title(self, uid: str, message: Message) -> None:
        """Edits the title of a task."""
        await self.update_task(uid, message, Keys.TASK_TITLE)

    async def edit_task_description(self, uid: str, message: Message) -> None:
        """Edits the description of a task."""
        await self.update_task(uid, message, Keys.TASK_DESCRIPTION)

    async def update_task(self, uid: str, message: Message, field: str) -> None:
        """Updates the task title or description in the database."""
        task_id = cache.get_user_cache(uid, Keys.EDITED_TASK_ID)

        if not task_id:
            await message.reply(Messages.TASK_NOT_FOUND)
            return

        task = db.get_task(task_id)
        if not task:
            await message.reply(Messages.TASK_NOT_FOUND)
            return

        original_value = task[1] if field == Keys.TASK_TITLE else task[2]
        updated_value = message.text.strip()

        if original_value == updated_value:
            await message.reply(Messages.NO_CHANGES_MADE)
            return

        db.update_task(task_id, field, updated_value)

        tasks = db.get_tasks(uid)
        task_order = next((i + 1 for i, t in enumerate(tasks) if t[0] == task_id), -1)

        if field == Keys.TASK_TITLE:
            title_display = Messages.add_pencil(updated_value)
            description_display = task[2]
        elif field == Keys.TASK_DESCRIPTION:
            title_display = task[1]
            description_display = Messages.add_pencil(updated_value)

        if task_order == -1:
            await message.reply(Messages.TASK_NOT_FOUND)
            return

        await message.reply(
            Messages.task_details(
                task_number=task_order,
                task_title=title_display,
                task_description=description_display,
                status_icon=get_task_status_icon(task[3]),
            ),
            reply_markup=InlineKeyboards.TaskActions(task_id, bool(task[3]), ""),
        )

        await message.reply(Messages.MAIN_MENU, reply_markup=Keyboards.MainMenu)
        cache.delete_user_cache(uid)

    async def view_task_by_number(self, uid: str, message: Message) -> None:
        """Allows user to view a specific task by its number."""
        try:
            task_number = int(message.text) - 1
            tasks = db.get_tasks(uid)

            if 0 <= task_number < len(tasks):
                task_id, title, description, is_completed = tasks[task_number]

                await message.reply(
                    Messages.task_details(
                        task_number=task_number + 1,
                        task_title=title,
                        task_description=description,
                        status_icon=get_task_status_icon(is_completed),
                    ),
                    reply_markup=InlineKeyboards.TaskActions(int(task_id), bool(is_completed), ""),
                )

                await message.reply(Messages.MAIN_MENU, reply_markup=Keyboards.MainMenu)
                cache.delete_user_cache(uid)

            else:
                await message.reply(Messages.TASK_NOT_FOUND_ENT_VALID)
        except ValueError:
            await message.reply(Messages.INVALID_INPUT)
        except Exception as e:
            logging.error(f"[view_task_by_number] Error: {e}", exc_info=True)
            await message.reply(Messages.UNEXPECTED_ERROR)


class CallbackHandler:
    """Handles inline button interactions."""

    def __init__(self, client: Client) -> None:
        self.client = client

    async def handle_callback(self, client: Client, callback_query: CallbackQuery) -> None:
        """Processes inline button clicks."""
        data = callback_query.data.split(":")  # type: ignore
        if len(data) < 2:
            await callback_query.answer(Messages.INVALID_ACTION, show_alert=True)
            return

        action, task_id = data[0], int(data[1]) if isinstance(data[1], str) and data[1].isdigit() else data[1]
        task = db.get_task(int(task_id))

        if not task:
            await callback_query.answer(Messages.TASK_NOT_FOUND, show_alert=True)
            return

        action_handlers = {
            InlineButtons.TOGGLE_STATUS: lambda: self.toggle_task_status(callback_query, task[0]),
            InlineButtons.EDIT_TITLE: lambda: self.start_editing(callback_query, task[0], States.EDIT_TASK_TITLE),
            InlineButtons.EDIT_DESCRIPTION: lambda: self.start_editing(
                callback_query, task[0], States.EDIT_TASK_DESCRIPTION
            ),
            InlineButtons.CANCEL_EDIT: lambda: self.cancel_edit(callback_query, task[0]),
            InlineButtons.DELETE_TASK: lambda: self.delete_task(callback_query, task[0]),
        }

        if action in action_handlers:
            await action_handlers[action]()  # type: ignore

    async def toggle_task_status(self, callback_query: CallbackQuery, task_id: int) -> None:
        """Toggles the completion status of a task and updates the message."""
        task = db.get_task(task_id)
        if not task:
            await callback_query.answer(Messages.TASK_NOT_FOUND, show_alert=True)
            return

        task_id, title, description, is_completed = task
        new_status = not bool(is_completed)
        db.update_task(task_id, "is_completed", str(int(new_status)))

        new_icon = get_task_status_icon(new_status)
        old_icon = get_task_status_icon(is_completed)
        updated_text = callback_query.message.text.replace(old_icon, new_icon)

        try:
            if updated_text != callback_query.message.text:
                await callback_query.message.edit_text(
                    updated_text,
                    reply_markup=InlineKeyboards.TaskActions(task_id, new_status, ""),
                )
                await callback_query.answer(Messages.TASK_STATUS_UPDATED)
            else:
                await callback_query.answer(Messages.TASK_ALREADY_IN_STATUS)
        except Exception as e:
            logging.error(f"[toggle_task_status] Error: {e}", exc_info=True)
            await callback_query.answer(Messages.UNABLE_TO_UPDATE_STATUS)

    async def start_editing(self, callback_query: CallbackQuery, task_id: int, state: str) -> None:
        """Handles editing task title or description."""
        task = db.get_task(task_id)
        if not task:
            await callback_query.answer(Messages.TASK_NOT_FOUND, show_alert=True)
            return

        task_id, title, description, is_completed = task
        is_completed = bool(is_completed)

        cache.update_user_cache(callback_query.from_user.id, Keys.STATE, state)
        cache.update_user_cache(callback_query.from_user.id, Keys.EDITED_TASK_ID, task_id)

        await callback_query.message.edit_reply_markup(InlineKeyboards.TaskActions(task_id, is_completed, state))

        if state == States.EDIT_TASK_TITLE:
            await callback_query.message.reply(Messages.EDIT_TASK_TITLE)
            await callback_query.message.reply(title)
            await callback_query.message.reply(Messages.SEND_NEW_TITLE)
        elif state == States.EDIT_TASK_DESCRIPTION:
            await callback_query.message.reply(Messages.EDIT_TASK_DESCRIPTION)
            await callback_query.message.reply(description if description else Messages.NO_DESCRIPTION_YET)
            await callback_query.message.reply(Messages.SEND_NEW_DESCRIPTION)

        await callback_query.answer()

    async def cancel_edit(self, callback_query: CallbackQuery, task_id: int) -> None:
        """Cancels the editing mode."""
        task = db.get_task(task_id)
        if not task:
            await callback_query.answer(Messages.TASK_NOT_FOUND, show_alert=True)
            return

        task_id, _, _, is_completed = task
        is_completed = bool(is_completed)

        cache.delete_user_cache(callback_query.from_user.id)
        await callback_query.message.edit_reply_markup(InlineKeyboards.TaskActions(task_id, is_completed, ""))
        await callback_query.message.reply(Messages.EDITING_CANCELLED)
        await callback_query.answer()

    async def delete_task(self, callback_query: CallbackQuery, task_id: int) -> None:
        """Deletes a task from the database."""
        task = db.get_task(task_id)
        if not task:
            await callback_query.answer(Messages.TASK_NOT_FOUND, show_alert=True)
            return

        db.delete_task(task_id)
        await callback_query.message.edit_text(Messages.TASK_DELETED_SUCCESSFULLY)
        await callback_query.answer(Messages.TASK_DELETED)
