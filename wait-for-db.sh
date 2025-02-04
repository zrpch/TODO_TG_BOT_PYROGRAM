#!/bin/bash
set -e

host="$POSTGRES_HOST"
port="$POSTGRES_PORT"
redis_host="$REDIS_HOST"
redis_port="$REDIS_PORT"

echo "⏳ Ожидание PostgreSQL ($host:$port)..."
until pg_isready -h "$host" -p "$port"; do
  sleep 1
done
echo "✅ PostgreSQL доступен."

echo "⏳ Ожидание Redis ($redis_host:$redis_port)..."
until redis-cli -h "$redis_host" -p "$redis_port" ping | grep -q "PONG"; do
  sleep 1
done
echo "✅ Redis доступен, запускаем миграции..."

exec "$@"