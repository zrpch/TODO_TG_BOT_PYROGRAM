class Messages:
    """UI Messages for the bot."""

    START_REGISTERED = "You are already registered!"
    START_NEW = "Welcome to the Task Management bot!"
    ENTER_YOUR_NAME = "Enter your name:"
    ENTER_YOUR_USERNAME = "Enter your username:"
    USERNAME_EXISTS = "❌ This username is already taken.\nPlease enter a different username:"

    EDIT_TASK_TITLE = "✏️ Edit Task Title:\n\nOld Title to copy:"
    EDIT_TASK_DESCRIPTION = "✏️ Edit Task Description:\n\nOld Description to copy:"
    SEND_NEW_TITLE = "Send a new title:"
    SEND_NEW_DESCRIPTION = "Send a new description:"
    NO_DESCRIPTION_YET = "...No description yet..."
    NO_CHANGES_MADE = "No changes have been made"

    ICON_DONE = "✅"
    ICON_TODO = "➡️"

    MAIN_MENU = "🔽 Main Menu 🔽"

    ENTER_TASK_TITLE = "Enter task title:"
    ENTER_TASK_DESCRIPTION = "Enter task description:"
    TASK_NOT_FOUND = "❌ Task not found!"

    TASK_STATUS_UPDATED = "✅ Task status updated!"
    TASK_ALREADY_IN_STATUS = "️️⚠️ Task is already in this state."
    UNABLE_TO_UPDATE_STATUS = "⚠️ Unable to update task status!"

    TASK_ADDED = "Task added successfully!"
    TASK_DELETED = "✅ Task deleted!"

    UNKNOWN_COMMAND = "Unknown command"

    HELP_TEXT = "This bot helps you manage your tasks. You can add, list, and delete tasks."
    INVALID_INPUT = "❌ Invalid input. Please enter a valid task number."
    UNEXPECTED_ERROR = "⚠️ Unexpected error occurred."
    TASK_NOT_FOUND_ENT_VALID = "❌ Task not found. Enter a valid task number."

    INVALID_ACTION = "❌ Invalid action!"

    MISSING_API_CREDENTIALS = "❌ Missing API credentials! Check .env file."

    @staticmethod
    def welcome(name: str) -> str:
        """Returns the welcome message with a name."""
        return f"Welcome, {name}!"

    @staticmethod
    def add_pencil(updated_value: str) -> str:
        """Adds a pencil emoji to the updated value."""
        return f"{updated_value} (✏️)"

    @staticmethod
    def task_details(task_number: int, task_title: str, task_description: str, status_icon: str) -> str:
        """Formats the task details message."""
        return f"{status_icon} Task № {task_number}\n\n" f"Title: {task_title}\n" f"Description: {task_description}"
