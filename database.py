import aiosqlite
DB_NAME = "database.db"

async def setup_database():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS levels(
        user_id INTEGER PRIMARY KEY,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1)
        """)
        await db.commit()

async def add_xp(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
         cursor = await db.execute(
            "SELECT xp, level FROM levels WHERE user_id = ?",
            (user_id,)
         )
         data = await cursor.fetchone()

         if data is None:
            await db.execute(
                "INSERT INTO levels (user_id, xp, level) VALUES (?, ?, ?)",
                (user_id, amount, 1)
            )
         else:
            xp, level = data
            new_xp = xp + amount
            await db.execute(
                "UPDATE levels SET xp = ? WHERE user_id = ?",
                (new_xp, user_id)
            )
         await db.commit()

async def get_user_data(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT xp, level FROM  levels WHERE user_id = ?",
            (user_id,)
        )
        return await cursor.fetchone()



