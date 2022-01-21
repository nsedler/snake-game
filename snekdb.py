import os
import pprint
from array import array

import mysql.connector
from dotenv import load_dotenv


class SnekDB(object):
    def __init__(self):

        load_dotenv()

        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASS')
        db_host = os.getenv('DB_HOST')
        db_database = os.getenv('DB_DATABASE')

        self.cnx = mysql.connector.connect(user=db_user, password=db_pass,
                                           host=db_host, database=db_database, port=3306)
        self.cursor = self.cnx.cursor(buffered=True)

    def close_db(self):
        self.cursor.close()
        self.cnx.close()

    def get_scoreboard(self):
        select_query = "select * from Scores order by Score desc"
        self.cursor.execute(select_query)
        data = self.cursor.fetchall()

        leaderboard_split = [data[i:i + 5] for i in range(0, len(data), 5)]
        leaderboard_book = []

        for i in range(0, len(leaderboard_split)):
            new_page = {i + 1: leaderboard_split[i]}
            leaderboard_book.append(new_page)
        # pp = pprint.PrettyPrinter(depth=4)
        # pp.pprint(leaderboard_book[1])

        # cur_book_page = leaderboard_book[1][2]
        # for scoreid, score, name in cur_book_page:
        #     print(f'{score}___{name}')
        #     print("______________")

        self.cnx.commit()
        self.close_db()

        return leaderboard_book
