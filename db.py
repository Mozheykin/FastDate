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
             row = await connection.fetchrow('SELECT * FROM customers WHERE user_id=$1', user_id)
             return row

    async def activate_customer(self, user_id: int):
        async with self.pool.acquire() as connection:
            await connection.execute('''
                UPDATE customers
                SET is_active = TRUE
                WHERE user_id = $1
            ''', user_id)

    async def deactivate_customer(self, user_id: int):
        async with self.pool.acquire() as connection:
            await connection.execute('''
                UPDATE customers
                SET is_active = FALSE
                WHERE user_id = $1
            ''', user_id)

    async def set_gold_status(self, user_id: int):
        async with self.pool.acquire() as connection:
            await connection.execute('''
                UPDATE customers
                SET is_gold = TRUE
                WHERE user_id = $1
            ''', user_id)

    async def remove_gold_status(self, user_id: int):
        async with self.pool.acquire() as connection:
            await connection.execute('''
                UPDATE customers
                SET is_gold = FALSE
                WHERE user_id = $1
            ''', user_id)
        
    async def add_customer(self, c: Customer):
        async with self.pool.acquire() as connection:
            await connection.execute('''
                INSERT INTO customers (user_id, username, balance, age, gender, language, info, 
                                    photo, location, range, is_gold, is_active)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            ''', c.user_id, c.username, c.balance, c.age, c.gender, c.language, c.info, 
            c.photo, c.location, c.range, c.is_gold, c.is_active)


    # async def add_customer(self, c: Customer):
    #     async with self.pool.acquire() as connection:
    #         await connection.execute('INSERT INTO customers VALUES(user_id=$1, username=$2,'\
    #             'balance=$3, age=$4, gender=$5, language=$6, info=$7, photo=$8, location=$9,'\
    #             'range=$10, is_gold=$11, is_active=$12)', c.user_id, c.username, c.balance, 
    #             c.age, c.gender, c.language, c.info, c.photo, c.location, c.range, 
    #             c.is_gold, c.is_active)
    
    async def init_db(self):     
        async with self.pool.acquire() as connection:         
            await connection.execute('''CREATE TABLE IF NOT EXISTS customers (                 
                            id SERIAL PRIMARY KEY,                 
                            user_id INTEGER,                 
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