class Messages:
    """UI Messages for the bot."""

    START_REGISTERED = "You are already registered!"
    START_NEW = "Welcome to the Task Management bot!"
    ENTER_YOUR_NAME = "Enter your name:"
    ENTER_YOUR_USERNAME = "Enter your username:"
    USERNAME_EXISTS = "❌ This username is already taken.\nPlease enter a different username:"

    UNKNOWN_COMMAND = "Unknown command"

    MISSING_API_CREDENTIALS = "❌ Missing API credentials! Check .env file."

    HELP_TEXT = "This bot helps you manage your tasks. You can add, list, and delete tasks."

    @staticmethod
    def welcome(name: str) -> str:
        """Returns the welcome message with a name."""
        return f"Welcome, {name}!"