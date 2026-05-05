import aiosqlite
DB_NAME = "database.db"

async def setup_database():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS levels(
        user_id INTEGER PRIMARY KEY,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1)
        """)
        await db.execute("""CREATE TABLE IF NOT EXISTS reputation(
        user_id INTEGER PRIMARY KEY,
        rep INTEGER DEFAULT 0)
        """)    
        await db.execute("""CREATE TABLE IF NOT EXISTS memories(
        user_id INTEGER,
        key TEXT,
        value TEXT
        )
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

async def add_rep(user_id, amount=1):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        INSERT OR IGNORE INTO reputation (user_id, rep)
        VALUES (?, 0)
        """, (user_id,))

        await db.execute("""
        UPDATE reputation
        SET rep = rep + ?
        WHERE user_id = ?
        """, (amount, user_id))

        await db.commit()


async def get_rep(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT rep FROM reputation
        WHERE user_id = ?
        """, (user_id,))

        data = await cursor.fetchone()

        if data is None:
            return 0

        return data[0]


async def get_top_rep(limit=10):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT user_id, rep
        FROM reputation
        ORDER BY rep DESC
        LIMIT ?
        """, (limit,))

        return await cursor.fetchall()

async def get_top_levels(limit=5):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT user_id, xp, level
        FROM levels
        ORDER BY level DESC, xp DESC
        LIMIT ?
        """, (limit,))

        return await cursor.fetchall()

async def add_memory(user_id, key, value):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        INSERT OR REPLACE INTO memories (user_id, key, value)
        VALUES (?, ?, ?)
        """, (user_id, key, value))

        await db.commit()

async def get_memory(user_id, key):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT value FROM memories
        WHERE user_id = ? AND key = ?
        """, (user_id, key))

        data = await cursor.fetchone()

        if data is None:
            return None

        return data[0]

async def delete_memory(user_id, key):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        DELETE FROM memories
        WHERE user_id = ? AND key = ?
        """, (user_id, key))

        await db.commit()



