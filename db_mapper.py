import sqlite3


class Db:

    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

    def getAllMoviesOrderedByRating(self):
        return self.cursor.execute("""SELECT * FROM movies ORDER BY rating DESC""")

    def getAllProjectionForMovie(self, movie_id, date=None):

        query = """SELECT
                        m.name AS movie_name,
                        p.id AS projection_id,
                        p.movie_id,
                        p.type,
                        p.date,
                        p.time,
                        (100 - COUNT(p.id)) AS spots_available
                   FROM movies m
                   LEFT JOIN projections p
                   ON m.id = p.movie_id
                    LEFT JOIN reservations r
                    ON p.id = r.projection_id
                    WHERE
                        p.movie_id = ?
                        :dateCondition
                    GROUP BY p.id
                    ORDER BY date"""

        if date is None:
            query = query.replace(':dateCondition', '')
            return self.cursor.execute(query, (movie_id, ))
        else:
            query = query.replace(':dateCondition', 'AND p.date = ?')
            return self.cursor.execute(query, (movie_id, date))

    def seatsInRoom(self, projection_id):
        query = """SELECT
                        row,
                        col
                    FROM reservations
                    WHERE projection_id = ?"""
        return self.cursor.execute(query, (projection_id, ))

    def chekIfSeatIsFree(self, projection_id, row, col):
        query = """SELECT
                        count(*) as count
                    FROM reservations
                    WHERE
                        row = ? and col = ?
                        and projection_id = ?"""
        self.cursor.execute(query, (row, col, projection_id))
        q = self.cursor.fetchone()
        print(q[0])
        return q[0] < 1

    # List of tuples -> [(username, projection_id, row, col), (username, projection_id, row, col), ...]
    def make_reservation(self, reservations):
        self.cursor.executemany("""INSERT INTO reservations(username, projection_id, row, col)
            VALUES(?, ?, ?, ?)""", reservations)
        self.db.commit()

    def cancel_reservation(self, name):
        self.cursor.execute("""DELETE FROM reservations WHERE username = ?""", (name,))
        self.db.commit()
