# Telegram Task Manager Bot

This project is a Telegram bot for managing personal tasks. Users can register, create, view, and manage tasks via a simple chat interface. The bot is built using **Pyrogram** and **Finite State Machine (FSM)** for user interaction and task management.

## Features
- User registration with a unique username
- Creating, viewing, and managing tasks
- Inline menus for quick actions
- Persistent menus for navigation
- PostgreSQL database for storing user and task data
- Docker support for easy deployment

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis
- Docker & Docker Compose

### Steps
1. **Create your bot** via [@BotFather](https://t.me/BotFather)
2. Obtain your bot **TOKEN**
3. Register your app at [my.telegram.org](https://my.telegram.org/) under "API development tools"
4. Get **API_ID** and **API_HASH**
5. Create a `.env` file from `.env.template` and fill in credentials:
   ```ini
   BOT_TOKEN=your_bot_token
   API_ID=your_api_id
   API_HASH=your_api_hash
   ```
6. Create a `sessions` directory in the project root:
   ```sh
   mkdir sessions
   ```
7. **Run the bot for the first time:**
   ```sh
   python -m bot.bot
   ```
   - This will generate a `bot.session` file inside `sessions/`
   - Enter the bot **TOKEN** when prompted
   - Confirm token correctness (`y` for Yes)
8. **Run with Docker:**
   ```sh
   docker-compose up --build
   ```

## Tech Stack
- **Python** (Pyrogram, AsyncIO, PostgreSQL, Redis)
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **State Management**: FSM
- **Caching**: Redis
- **Containerization**: Docker

## License
MIT License

