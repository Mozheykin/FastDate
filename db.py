import asyncpg
from config import DATABASE_URL  


class DB:
    async def __init__(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL) 
        await self.init_db()
        return self.pool
    
    async def init_db(self):     
        async with self.pool.acquire() as connection:         
            await connection.execute('''CREATE TABLE IF NOT EXISTS customers (                 
                            id SERIAL PRIMARY KEY,                 
                            user_id BIGINT UNIQUE,                 
                            username TEXT,
                            balance FLOAT,                 
                            age INT,                 
                            gender TEXT,                 
                            info TEXT,                 
                            photo TEXT,                 
                            location GEOMETRY(Point, 4326),
                            range INTEGER,                 
                            is_gold BOOLEAN DEFAULT FALSE,
                            is_active BOOLEAN);''')

        async with self.pool.acquire() as connection:         
            await connection.execute('''CREATE TABLE IF NOT EXISTS coincedences (                 
                            id INTEGER,                 
                            customers BOOLEAN);''')