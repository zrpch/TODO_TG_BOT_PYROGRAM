import os
import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager
from typing import Optional, List, Tuple

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_NAME")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")


class Database:
    """Handles all database operations using raw SQL queries."""

    def __init__(self):
        """Initializes a connection to the PostgreSQL database."""
        self.connection = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        self.connection.autocommit = True

    @contextmanager
    def get_cursor(self):
        """Provides a database cursor for executing queries."""
        cursor = self.connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def create_user(self, name: str, username: str, telegram_id: str) -> None:
        """Registers a new user in the database."""
        with self.get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (name, username, telegram_id) VALUES (%s, %s, %s)", (name, username, telegram_id)
            )

    def get_user(self, telegram_id: str) -> Optional[Tuple[int, str, str]]:
        """Retrieves user information by Telegram ID."""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT id, name, username FROM users WHERE telegram_id = %s", (telegram_id,))
            return cursor.fetchone()

    def get_user_by_username(self, username: str) -> Optional[int]:
        """Checks if a username already exists in the database."""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            return result[0] if result else None

    def create_task(self, telegram_id: str, title: str, description: str) -> None:
        """Adds a new task to the database."""
        with self.get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO tasks (telegram_id, title, description, created_at, is_completed) "
                "VALUES (%s, %s, %s, NOW(), FALSE)",
                (telegram_id, title, description),
            )

    def get_tasks(self, telegram_id: str) -> List[Tuple[int, str, str, bool]]:
        """Fetches all tasks for a specific user and ensures description is never None."""
        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT id, title, COALESCE(description, ''), is_completed FROM tasks "
                "WHERE telegram_id = %s ORDER BY created_at ASC",
                (telegram_id,),
            )
            return cursor.fetchall()

    def get_task(self, task_id: int) -> Optional[Tuple[int, str, str, bool]]:
        """Retrieves a specific task by its ID."""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT id, title, description, is_completed FROM tasks WHERE id = %s", (task_id,))
            return cursor.fetchone()

    def update_task(self, task_id: int, field: str, value: str) -> None:
        """Updates the title or description of a task."""
        with self.get_cursor() as cursor:
            cursor.execute(f"UPDATE tasks SET {field} = %s WHERE id = %s", (value, task_id))

    def delete_task(self, task_id: int) -> None:
        """Deletes a task by ID."""
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))

    def get_task_order(self, task_id: int, telegram_id: str) -> Optional[int]:
        """Returns the task order (index) for a given task in the user's task list."""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT id FROM tasks WHERE telegram_id = %s ORDER BY created_at ASC", (telegram_id,))
            tasks = cursor.fetchall()
            task_ids = [task[0] for task in tasks]

            return task_ids.index(task_id) + 1 if task_id in task_ids else None
