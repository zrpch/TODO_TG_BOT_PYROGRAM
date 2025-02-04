# Architecture & Design Decisions

## Overview
The Telegram Task Manager Bot is built using the **Pyrogram** framework and utilizes **Finite State Machine (FSM)** to manage user interactions efficiently. The bot is designed to be containerized with **Docker** and supports a microservice-like architecture with separate concerns for database access, caching, and messaging.

## Technology Stack
- **Python**: Primary language for backend logic
- **Pyrogram**: Telegram API wrapper
- **PostgreSQL**: Primary database for storing users and tasks
- **Redis**: Used for caching session data
- **Docker**: Containerization for easy deployment
- **Docker Compose**: Multi-container management

## Architectural Components

### 1. **Bot Core (bot.py)**
- Initializes Pyrogram Client
- Loads environment variables from `.env`
- Registers handlers for commands, messages, and callbacks

### 2. **Handlers (handler.py)**
- Handles user interactions with FSM
- Supports registration, task creation, and task management

### 3. **Keyboards (keyboards.py)**
- Defines inline and persistent keyboard layouts for interaction

### 4. **Database (database.py & models.py)**
- PostgreSQL database for storing users and tasks
- SQLAlchemy ORM for structured interactions
- Uses raw SQL queries for performance-critical operations

### 5. **Caching Layer (cache.py)**
- Uses Redis to store temporary session data
- Reduces database load by keeping short-term data in-memory

### 6. **State Management (states.py)**
- Manages finite states of user interactions
- Stores registration, task creation, and editing steps

### 7. **Utilities (utils.py)**
- Contains helper functions like status icons for tasks

### 8. **Deployment (docker-compose.yaml)**
- Multi-container setup for PostgreSQL, Redis, and the bot
- Ensures the bot waits for database readiness before launching

## Database Schema
- **Users Table**: Stores Telegram user details
- **Tasks Table**: Stores user-created tasks

## Design Rationale
- **Separation of Concerns**: Each component has a well-defined role
- **FSM for User Flow**: Ensures a structured interaction path
- **Dockerized Deployment**: Simplifies production setup and scaling
- **Redis Caching**: Improves response time and efficiency

## Future Enhancements
- Adding role-based permissions for multi-user task collaboration
- Introducing analytics for user engagement tracking

