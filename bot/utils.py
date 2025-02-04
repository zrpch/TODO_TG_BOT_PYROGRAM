from bot.messages import Messages


def get_task_status_icon(is_completed: bool) -> str:
    """Return a string emoji icon based on the task completion status."""
    return Messages.ICON_DONE if is_completed else Messages.ICON_TODO
