import psycopg2


class DB:
    def __init__(
        self,
        name: str,
        user="postgres",
        password="qwerty",
        host="localhost",
        port="5432",
    ):
        self.conn = psycopg2.connect(
            dbname=name, user=user, password=password, host=host, port=port
        )
        self.create_table_main()

    def create_table_main(self):
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("""CREATE TABLE IF NOT EXISTS customer (
                    id INTEGER,
                    name TEXT,
                    position INTEGER,
                    Balance FLOAT,
                    Range INTEGER,
                    When TEXT,
                    Gender TEXT,
                    Gold BOOL,
                    Valide BOOL);
                """)

                cursor.execute("""CREATE TABLE IF NOT EXISTS coincedences (
                    id INTEGER,
                    Customers TEXT);
                """)
