from db import DB
from models.customer import Customer
import json

async def change_customer(id_customer: int, 
                        db_postgres: DB,
                        what_replace: str,
                        recorded: str|int|float, 
                        correction: str|int|float) -> None: 
    if not recorded == correction:
        if what_replace == 'photo':
            db_customer = await db_postgres.get_customer(id_customer)
            if db_customer is not None:
                customer = Customer(**db_customer)
                photos:list = json.loads(customer.photo)
                photos.append(recorded)
                recorded = json.dumps(photos)
        await db_postgres.change_customer(what_replace, correction, id_customer)