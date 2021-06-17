import pymysql

class SQL:
    def __init__(self) -> None:
        self.db = pymysql.connect(
            host="124.71.140.75",
            user="jol",
            port=3306,
            password="12345678",
            database="jol"
        )
        
    def read(self):
        with self.db.cursor() as cursor:
            sql = "SELECT * FROM "