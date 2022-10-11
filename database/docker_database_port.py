import meilisearch

client = meilisearch.Client('http://meilisearch:7700', 'masterKey')

import redis

r = redis.Redis(
	host="redis",
	port=6379, 
	db=0,
	decode_responses=True,
	)

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv('database_url', 'value does not exist')
cluster = MongoClient(database_url)
dtbs = cluster['better_news']
