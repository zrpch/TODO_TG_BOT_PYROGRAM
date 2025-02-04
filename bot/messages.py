class Messages:
    """UI Messages for the bot."""

    START_REGISTERED = "You are already registered!"
    START_NEW = "Welcome to the Task Management bot!"
    ENTER_YOUR_NAME = "Enter your name:"
    ENTER_YOUR_USERNAME = "Enter your username:"
    USERNAME_EXISTS = "❌ This username is already taken.\nPlease enter a different username:"

    MAIN_MENU = "🔽 Main Menu 🔽"

    ICON_DONE = "✅"
    ICON_TODO = "➡️"

    ENTER_TASK_TITLE = "Enter task title:"
    ENTER_TASK_DESCRIPTION = "Enter task description:"

    EDIT_TASK_TITLE = "✏️ Edit Task Title:\n\nOld Title to copy:"
    EDIT_TASK_DESCRIPTION = "✏️ Edit Task Description:\n\nOld Description to copy:"
    EDITING_CANCELLED = "🚫 Editing canceled!"
    SEND_NEW_TITLE = "Send a new title:"
    SEND_NEW_DESCRIPTION = "Send a new description:"
    NO_DESCRIPTION_YET = "...No description yet..."
    NO_CHANGES_MADE = "No changes have been made"

    TASK_ADDED = "Task added successfully!"
    TASK_DELETED = "✅ Task deleted!"
    TASK_DELETED_SUCCESSFULLY = "✅ Task deleted successfully!"
    TASK_NOT_FOUND = "❌ Task not found!"
    TASK_NOT_FOUND_ENT_VALID = "❌ Task not found. Enter a valid task number."
    NO_TASKS_YET = "You don't have any tasks yet."

    TASK_STATUS_UPDATED = "✅ Task status updated!"
    TASK_ALREADY_IN_STATUS = "️️⚠️ Task is already in this state."
    UNABLE_TO_UPDATE_STATUS = "⚠️ Unable to update task status!"

    HELP_TEXT = "This bot helps you manage your tasks. You can add, list, and delete tasks."
    INVALID_INPUT = "❌ Invalid input. Please enter a valid task number."
    INVALID_ACTION = "❌ Invalid action!"
    UNEXPECTED_ERROR = "⚠️ Unexpected error occurred."
    UNKNOWN_COMMAND = "Unknown command"

    MISSING_API_CREDENTIALS = "❌ Missing API credentials! Check .env file."
    INTERNAL_SERVER_ERROR = "⚠️ Internal server error. Please try again later."

    @staticmethod
    def welcome(name: str) -> str:
        """Returns the welcome message with a name."""
        return f"Welcome, {name}!"

    @staticmethod
    def task_list(task_list: str) -> str:
        """Formats the task list message."""
        return f"Your tasks:\n\n{task_list}"

    @staticmethod
    def task_number_request(max_tasks: int) -> str:
        """Returns the task number request message."""
        return f"Enter task number (from 1 to {max_tasks}):"

    @staticmethod
    def add_pencil(updated_value: str) -> str:
        """Adds a pencil emoji to the updated value."""
        return f"{updated_value} (✏️)"

    @staticmethod
    def task_details(task_number: int, task_title: str, task_description: str, status_icon: str) -> str:
        """Formats the task details message."""
        return f"{status_icon} Task № {task_number}\n\n" f"Title: {task_title}\n" f"Description: {task_description}"
