import asyncio
from app.db.handlers import start_db
from app.bot.handlers import start_bot

def main()->bool:
    start_db()
    asyncio.run(start_bot())

if __name__ == '__main__':
    main()