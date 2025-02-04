# SQL Queries and Database Structure

## Database Schema
The bot uses **PostgreSQL** as the primary database. The schema consists of two tables: `users` and `tasks`.

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL
);
```
- `id`: Unique identifier (auto-incremented).
- `telegram_id`: Unique Telegram ID of the user.
- `username`: User's chosen username (must be unique).
- `name`: User's real name.

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    telegram_id VARCHAR REFERENCES users(telegram_id) ON DELETE CASCADE
);
```
- `id`: Unique task identifier.
- `title`: Title of the task.
- `description`: Optional description of the task.
- `is_completed`: Status flag (`TRUE` if task is completed).
- `created_at`: Timestamp when the task was created.
- `telegram_id`: Foreign key linking tasks to users.

## SQL Queries

### Inserting a New User
```sql
INSERT INTO users (name, username, telegram_id) VALUES (%s, %s, %s);
```
**Python Implementation:**
```python
def create_user(self, name: str, username: str, telegram_id: str) -> None:
    with self.get_cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (name, username, telegram_id) VALUES (%s, %s, %s)",
            (name, username, telegram_id),
        )
```

### Fetching a User by Telegram ID
```sql
SELECT id, name, username FROM users WHERE telegram_id = %s;
```
**Python Implementation:**
```python
def get_user(self, telegram_id: str) -> Optional[Tuple[int, str, str]]:
    with self.get_cursor() as cursor:
        cursor.execute("SELECT id, name, username FROM users WHERE telegram_id = %s", (telegram_id,))
        return cursor.fetchone()
```

### Inserting a New Task
```sql
INSERT INTO tasks (telegram_id, title, description, created_at, is_completed) VALUES (%s, %s, %s, NOW(), FALSE);
```
**Python Implementation:**
```python
def create_task(self, telegram_id: str, title: str, description: str) -> None:
    with self.get_cursor() as cursor:
        cursor.execute(
            "INSERT INTO tasks (telegram_id, title, description, created_at, is_completed) "
            "VALUES (%s, %s, %s, NOW(), FALSE)",
            (telegram_id, title, description),
        )
```

### Retrieving All Tasks for a User
```sql
SELECT id, title, COALESCE(description, ''), is_completed FROM tasks WHERE telegram_id = %s ORDER BY created_at ASC;
```
**Python Implementation:**
```python
def get_tasks(self, telegram_id: str) -> List[Tuple[int, str, str, bool]]:
    with self.get_cursor() as cursor:
        cursor.execute(
            "SELECT id, title, COALESCE(description, ''), is_completed FROM tasks "
            "WHERE telegram_id = %s ORDER BY created_at ASC",
            (telegram_id,),
        )
        return cursor.fetchall()
```

### Updating a Task
```sql
UPDATE tasks SET title = %s WHERE id = %s;
```
**Python Implementation:**
```python
def update_task(self, task_id: int, field: str, value: str) -> None:
    with self.get_cursor() as cursor:
        cursor.execute(f"UPDATE tasks SET {field} = %s WHERE id = %s", (value, task_id))
```

### Deleting a Task
```sql
DELETE FROM tasks WHERE id = %s;
```
**Python Implementation:**
```python
def delete_task(self, task_id: int) -> None:
    with self.get_cursor() as cursor:
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
```

## Indexes and Optimization
Indexes are automatically created on primary keys (`id`). However, additional indexing may be added for performance optimization:
```sql
CREATE INDEX idx_telegram_id ON users(telegram_id);
CREATE INDEX idx_task_telegram_id ON tasks(telegram_id);
```

## Foreign Key Constraints
- The `tasks.telegram_id` column references `users.telegram_id`.
- `ON DELETE CASCADE` ensures that deleting a user will also remove their tasks.

## Summary
- The database efficiently stores user and task data.
- Queries are optimized with indexes and constraints.
- Foreign key relationships ensure data integrity.
- Python implementations match the SQL queries used.

