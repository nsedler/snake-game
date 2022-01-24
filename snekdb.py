import os
import pprint
from array import array

import mysql.connector
from dotenv import load_dotenv


class SnekDB(object):
    def __init__(self):

        # The database connection information is in a .env file
        load_dotenv()

        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASS')
        db_host = os.getenv('DB_HOST')
        db_database = os.getenv('DB_DATABASE')

        self.cnx = mysql.connector.connect(user=db_user, password=db_pass,
                                           host=db_host, database=db_database, port=3306)
        self.cursor = self.cnx.cursor(buffered=True)

    def close_db(self):
        # Close the db
        self.cursor.close()
        self.cnx.close()

    def get_scoreboard(self):
        # Get all score in desc order (Highest -> Lowest)
        select_query = "select * from Scores order by Score desc"
        self.cursor.execute(select_query)

        # fetch all rows returned
        data = self.cursor.fetchall()

        # stole this bit of fancy slicing
        leaderboard_split = [data[i:i + 5] for i in range(0, len(data), 5)]
        leaderboard_book = []

        # Make a new dictionary object for each page
        for i in range(0, len(leaderboard_split)):
            new_page = {i + 1: leaderboard_split[i]}
            leaderboard_book.append(new_page)

        self.cnx.commit()
        self.close_db()

        return leaderboard_book
