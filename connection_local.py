"""
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(database="money_tracker",
                        host="localhost",
                        user=os.getenv('DB_USERNAME'),
                        password=os.getenv('DB_PASSWORD'),
                        port="5432")
"""