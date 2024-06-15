from db import DB

async def change_customer(id_customer: int, 
                        db_postgres: DB,
                        what_replace: str,
                        recorded: str|int|float, 
                        correction: str|int|float) -> None: 
    if not recorded == correction:
        await db_postgres.change_customer(what_replace, correction, id_customer)