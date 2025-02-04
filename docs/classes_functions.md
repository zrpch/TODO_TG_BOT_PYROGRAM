# Description of Main Classes and Functions

## 1. `bot.py`
**Purpose**: Initializes the Telegram bot and registers message and callback handlers.
- `Client(name, api_id, api_hash, bot_token)`: Pyrogram client setup.
- `app.add_handler(MessageHandler(task_handler.handle_updates))`: Registers message updates.
- `app.add_handler(CallbackQueryHandler(callback_handler.handle_callback))`: Registers callback handling.

## 2. `handler.py`
**Purpose**: Manages incoming messages and user interactions.
### Classes:
- `TaskHandler`: Processes user messages and FSM states.
  - `handle_updates(client, message)`: Handles new messages.
  - `process_state(uid, state, message)`: Directs FSM state processing.
  - `process_command(uid, user, message)`: Executes user commands.
  - `list_all_tasks(uid, message)`: Fetches and lists tasks.
  - `register_name(uid, message)`: Handles user registration.
  - `initiate_task_creation(uid, message)`: Starts task creation flow.

- `CallbackHandler`: Manages inline button interactions.
  - `handle_callback(client, callback_query)`: Handles button clicks.
  - `toggle_task_status(callback_query, task_id)`: Marks task as complete/incomplete.
  - `delete_task(callback_query, task_id)`: Deletes a task.

## 3. `keyboards.py`
**Purpose**: Defines bot menus and inline buttons.
### Classes:
- `Buttons`: Stores button labels.
- `InlineButtons`: Stores inline button callback data.
- `Keyboards`: Defines reply keyboards.
- `InlineKeyboards`: Creates inline keyboards dynamically.

## 4. `messages.py`
**Purpose**: Stores static bot messages.
- `Messages.START_REGISTERED`: Message for returning users.
- `Messages.TASK_ADDED`: Confirms task addition.
- `Messages.task_details(task_number, title, description, status_icon)`: Formats task details.

## 5. `states.py`
**Purpose**: Defines finite state machine (FSM) states.
### Classes:
- `Keys`: Stores cache keys (e.g., `TASK_TITLE`).
- `States`: Lists FSM states (`ENTER_NAME`, `ENTER_TASK_TITLE`).

## 6. `utils.py`
**Purpose**: Provides helper functions.
- `get_task_status_icon(is_completed)`: Returns task status emoji.

## 7. `cache.py`
**Purpose**: Handles temporary user session storage via Redis.
### Class:
- `Cache`: Stores and retrieves session data.
  - `update_user_cache(uid, key, value)`: Updates user state.
  - `get_user_cache(uid, key)`: Retrieves cached data.
  - `delete_user_cache(uid)`: Clears user session.

## 8. `database.py`
**Purpose**: Manages database operations using PostgreSQL.
### Class:
- `Database`: Executes SQL queries.
  - `create_user(name, username, telegram_id)`: Registers new users.
  - `get_tasks(telegram_id)`: Fetches user tasks.
  - `update_task(task_id, field, value)`: Updates task details.

## 9. `models.py`
**Purpose**: Defines SQLAlchemy ORM models.
### Classes:
- `User`: Represents Telegram users.
  - `id`, `telegram_id`, `username`, `name`, `tasks` (relationship to `Task`).
- `Task`: Represents tasks.
  - `id`, `title`, `description`, `is_completed`, `created_at`, `telegram_id`.

