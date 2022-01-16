import mysql.connector
import os

from dotenv import load_dotenv


class SnekDB(object):
    def __init__(self):

        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASS')
        db_host = os.getenv('DB_HOST')
        db_database = os.getenv('DB_DATABASE')

        load_dotenv()
        self.cnx = mysql.connector.connect(user=db_user, password=db_pass,
                                           host=db_host, database=db_database, port=3306)
        self.cursor = self.cnx.cursor(buffered=True)

    def close_db(self):
        self.cursor.close()
        self.cnx.close()
