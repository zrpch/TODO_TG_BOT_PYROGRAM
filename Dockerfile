FROM python:3.13

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y postgresql-client redis-tools && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/wait-for-db.sh