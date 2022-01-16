import mysql.connector

class SnekDB(object):
    def __init__(self):
        self.cnx = mysql.connector.connect(user='', password='',
                                            host='', database='', port=3306)
        self.cursor = self.cnx.cursor(buffered=True)

    def close_db(self):
        self.cursor.close()
        self.cnx.close()