import asyncpg
from config import DATABASE_URL
from models.customer import Customer  

class DB:
    async def init_pool(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL) 
        await self.init_db()
    
    async def get_customer(self, user_id:int):
        if self.pool is not None:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    'SELECT * FROM customers WHERE user_id=$1', user_id)
                return row

    async def activate_customer(self, user_id: int):
        if self.pool is not None:
            async with self.pool.acquire() as connection:
                await connection.execute('''
                    UPDATE customers
                    SET is_active = TRUE
                    WHERE user_id = $1
                ''', user_id)

    async def deactivate_customer(self, user_id: int):
        if self.pool is not None:
            async with self.pool.acquire() as connection:
                await connection.execute('''
                    UPDATE customers
                    SET is_active = FALSE
                    WHERE user_id = $1
                ''', user_id)

    async def set_gold_status(self, user_id: int):
        if self.pool is not None:
            async with self.pool.acquire() as connection:
                await connection.execute('''
                    UPDATE customers
                    SET is_gold = TRUE
                    WHERE user_id = $1
                ''', user_id)

    async def remove_gold_status(self, user_id: int):
        if self.pool is not None:
            async with self.pool.acquire() as connection:
                await connection.execute('''
                    UPDATE customers
                    SET is_gold = FALSE
                    WHERE user_id = $1
                ''', user_id)
        
    async def change_language(self, user_id: int, language: str):
        if self.pool is not None:
            async with self.pool.acquire() as connection:
                await connection.execute('''
                    UPDATE customers
                    SET language = $1
                    WHERE user_id = $2
                ''', language, user_id)

    async def add_customer(self, c: Customer):
        if self.pool is not None:
            async with self.pool.acquire() as connection:
                await connection.execute('''
                    INSERT INTO customers 
                    (user_id, username, balance, age, gender, language, info, 
                    photo, location, range, is_gold, is_active)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                ''', c.user_id, c.username, c.balance, c.age, c.gender, c.language, c.info, 
                c.photo, c.location, c.range, c.is_gold, c.is_active)

    async def change_customer(self, what_replace:str, parametr:str|int, user_id: int):
        if self.pool is not None:
            # TODO переписать на изменяемые данные
            async with self.pool.acquire() as connection:
                await connection.execute(f'''
                    UPDATE customers 
                    SET {what_replace} = $1
                    WHERE user_id = $2
                ''', parametr, user_id)

    async def init_db(self):     
        if self.pool is not None:
            async with self.pool.acquire() as connection:         
                await connection.execute('''CREATE TABLE IF NOT EXISTS customers (                 
                                id SERIAL PRIMARY KEY,                 
                                user_id INTEGER,                 
                                username TEXT,
                                balance FLOAT DEFAULT 0.0,                 
                                age INT,                 
                                gender TEXT,                 
                                language TEXT DEFAULT 'en',
                                info TEXT,                 
                                photo TEXT,                 
                                location TEXT,
                                range INTEGER DEFAULT 500,                
                                straik INTEGER DEFAULT 0,
                                role INTEGER DEFAULT 99,
                                disabled_gold TEXT DEFAULT '0',
                                is_gold BOOLEAN DEFAULT FALSE,
                                is_baned BOOLEAN DEFAULT FALSE,
                                is_active BOOLEAN);''')

            async with self.pool.acquire() as connection:         
                await connection.execute('''CREATE TABLE IF NOT EXISTS coincedences (                 
                                id INTEGER,                 
                                customers BOOLEAN);''')