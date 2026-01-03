from flask import Flask, jsonify
import redis
import json
import os

from dotenv import load_dotenv

load_dotenv("init.env")
redis_host = os.getenv("REDIS_HOST")
redist_port = os.getenv("REDIS_PORT")


app = Flask(__name__)

r = redis.Redis(host=redis_host, port = redist_port, decode_responses=True)


def add_to_cache_user(user_data):

    json_user_data = json.dumps(user_data)
    r.set("user:" + user_data['user_id'], json_user_data)

def add_to_cache_files(file_data):
    key = "file_data_user:" + file_data['user_id']
    json_user_data = json.dumps(file_data)
    print(key)
    r.rpush(key,json_user_data)
    r.expire(key,86400)
   




def retrieve_cache(user_id):

    retrieved_json = r.get('user:' + user_id)
    unpacked_user_data = json.loads(retrieved_json)



