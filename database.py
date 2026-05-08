import aiosqlite
import os
DB_NAME = os.getenv("DB_NAME", "database.db")

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
        await db.execute("""CREATE TABLE IF NOT EXISTS daily_rewards(
        user_id INTEGER PRIMARY KEY,
        last_claim TEXT
        )
       """)
        await db.execute("""CREATE TABLE IF NOT EXISTS rep_cooldowns(
        user_id INTEGER PRIMARY KEY,
        last_rep TEXT
        )
       """)
        await db.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        coins INTEGER DEFAULT 0,
        gems INTEGER DEFAULT 0,
        crates INTEGER DEFAULT 0
        )
       """)
        try:
            await db.execute(
        "ALTER TABLE users ADD COLUMN crates INTEGER DEFAULT 0"
    )
        except:
            pass
        try:
            await db.execute(
        "ALTER TABLE users ADD COLUMN gems INTEGER DEFAULT 0"
    )
        except:
            pass

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
            xp += amount
            required_xp = 150 * level
            while xp >= required_xp:
                xp -= required_xp
                level += 1
                required_xp = level * 150
            await db.execute(
                "UPDATE levels SET xp = ?, level = ? WHERE user_id = ?",
                (xp, level, user_id)
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
async def get_last_rep(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """SELECT last_rep FROM rep_cooldowns WHERE user_id = ?""",
            (user_id,)
        )
        data = await cursor.fetchone()
        return data

async def update_rep_cooldown(user_id, timestamp):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            INSERT OR REPLACE INTO rep_cooldowns(user_id, last_rep)
            VALUES (?, ?)
            """,
            (user_id, timestamp)
        )
        await db.commit()

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

async def get_all_memories(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT key, value FROM memories
        WHERE user_id = ?
        """, (user_id,))

        return await cursor.fetchall()

# DAILY REWARDS

async def get_last_daily(user_id):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT last_claim FROM daily_rewards WHERE user_id = ?",
            (user_id,)
        )

        data = await cursor.fetchone()

        return data


async def update_daily(user_id, timestamp):

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            INSERT INTO daily_rewards (user_id, last_claim)
            VALUES (?, ?)
            ON CONFLICT(user_id)
            DO UPDATE SET last_claim = excluded.last_claim
            """,
            (user_id, timestamp)
        )

        await db.commit()

async def add_coins(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        INSERT OR IGNORE INTO users(user_id, coins)
        VALUES(?, 0)
        """, (user_id,))

        await db.execute("""
        UPDATE users
        SET coins = coins + ?
        WHERE user_id = ?
        """, (amount, user_id))

        await db.commit()

async def get_coins(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        INSERT OR IGNORE INTO users(user_id, coins)
        VALUES(?, 0)
        """, (user_id,))

        cursor = await db.execute("""
        SELECT coins FROM users
        WHERE user_id = ?
        """, (user_id,))

        data = await cursor.fetchone()

        return data[0]

async def get_gems(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT gems FROM users WHERE user_id = ?",
            (str(user_id),)
        )
        data = await cursor.fetchone()

        if data is None:
            await db.execute(
                "INSERT INTO users(user_id, coins, gems, crates) VALUES (?, 0, 0, 0)",
                (str(user_id),)
            )
            await db.commit()
            return 0

        return data[0]


async def add_gems(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""INSERT OR IGNORE INTO users(user_id, coins, gems, crates) VALUES(?, 0, 0, 0)""", 
        (user_id,)
        )
        await db.execute(
            "UPDATE users SET gems = gems + ? WHERE user_id = ?",
            (amount, str(user_id))
        )
        await db.commit()


async def get_crates(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT crates FROM users WHERE user_id = ?",
            (str(user_id),)
        )

        data = await cursor.fetchone()

        if data is None:
            await db.execute(
                "INSERT INTO users(user_id, coins, gems, crates) VALUES (?, 0, 0, 0)",
                (str(user_id),)
            )

            await db.commit()
            return 0

        return data[0]


async def add_crates(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            "INSERT OR IGNORE INTO users(user_id, coins, gems, crates) VALUES (?, 0, 0, 0)",
            (str(user_id),)
        )

        await db.execute(
            "UPDATE users SET crates = crates + ? WHERE user_id = ?",
            (amount, str(user_id))
        )

        await db.commit()