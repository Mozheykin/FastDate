import asyncpg
from config import DATABASE_URL
from models.customer import Customer  

class DB:
    async def get_pool(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL) 
        await self.init_db()
        return self.pool
    
    async def get_customer(self, user_id:int):
        async with self.pool.acquire() as connection:
             await connection.execute('SELECT * FROM customers WHERE user_id=?', (user_id,))
             return await connection.fetch()
    
    async def add_customer(self, c: Customer):
        async with self.pool.acquire() as connection:
            await connection.execute('INSERT INTO customers VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                     (c.user_id, c.username, c.balance, c.age, c.gender, 
                                      c.language, c.info, c.photo, c.location, c._range, 
                                      c.is_gold, c.is_active))
    
    async def init_db(self):     
        async with self.pool.acquire() as connection:         
            await connection.execute('''CREATE TABLE IF NOT EXISTS customers (                 
                            id SERIAL PRIMAR, %s, %sY KEY,                 
                            user_id BIGINT UNIQUE,                 
                            username TEXT,
                            balance FLOAT,                 
                            age INT,                 
                            gender TEXT,                 
                            language TEXT,
                            info TEXT,                 
                            photo TEXT,                 
                            location TEXT,
                            range INTEGER,                 
                            is_gold BOOLEAN DEFAULT FALSE,
                            is_active BOOLEAN);''')

        async with self.pool.acquire() as connection:         
            await connection.execute('''CREATE TABLE IF NOT EXISTS coincedences (                 
                            id INTEGER,                 
                            customers BOOLEAN);''')