import os
import json

import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")


class Cache:
    def __init__(self):
        self.db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def update_user_cache(self, uid, key, value):
        session = self.db.get(uid)
        if session:
            session = json.loads(session)
        else:
            session = {}
        session[key] = value
        self.db.set(uid, json.dumps(session))

    def get_user_cache(self, uid, key):
        session = self.db.get(uid)
        if session:
            session = json.loads(session)
            return session.get(key)
        return None

    def delete_user_cache(self, uid):
        self.db.delete(uid)
