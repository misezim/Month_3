import sqlite3

from aiohttp.web_routedef import delete


class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS reviews(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone_number TEXT,
            food_rating INTEGER,
            cleanliness_rating INTEGER,
            extra_comments TEXT
            )
            """)
            conn.execute("""CREATE TABLE IF NOT EXISTS dishes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price FLOAT,
            description TEXT,
            cover TEXT,
            category TEXT
            )
            """)
            conn.commit()

    def save_reviews(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT INTO reviews (name, phone_number, food_rating, cleanliness_rating, extra_comments)
                VALUES (?, ?, ?, ?, ?)

                """,
                (data["name"], data["phone_number"], data["food_rating"], data["cleanliness_rating"], data["extra_comments"] )

            )
    def save_dish(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT INTO dishes (name, price, description, cover, category)
                VALUES (?, ?, ?, ?, ?)

                """,
                (data["name"], data["price"], data["description"], data["cover"], data["category"])

            )


    def get_dishes_by_category(self):
        with sqlite3.connect(self.path) as conn:
            result = conn.execute("""SELECT * FROM dishes 
                                     ORDER BY price DESC""")
            result.row_factory = sqlite3.Row
            data = result.fetchall()
            return [dict(row) for row in data]