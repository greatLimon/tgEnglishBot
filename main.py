import asyncio

# import json
from app.db.handlers import start_db
from app.bot.handlers import start_bot

def main()->bool:
    start_db()
    asyncio.run(start_bot())

# def foo():
#     data = {
#         'Words': [('I','Я'),('We','Мы'),('Your','Твое'),('You','Ты')],
#         'Messages': {
#             'start_message' : 'Привет, я бот!'
#         }
#     }
#     with open('app/db/default_values.json', 'w') as f:
#         json.dump(data, f)

if __name__ == '__main__':
    # foo()
    main()