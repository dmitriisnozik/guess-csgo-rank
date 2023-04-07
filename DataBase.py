class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def amount(self) -> int:
        res = self.__cur.execute("SELECT rowid FROM video ORDER BY rowid DESC")
        return int(res.fetchone()[0])

    def get_video(self, rowid: int) -> list:
        res = self.__cur.execute(f"SELECT * FROM video WHERE rowid = {rowid}")
        return res.fetchone()

    def add(self, url: str, rank: str) -> None:
        self.__cur.execute(f"INSERT INTO video (url, rank) VALUES ('{url}', '{rank}')")
        self.__db.commit()
