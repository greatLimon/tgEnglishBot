import asyncio
from aiogram.utils.token import TokenValidationError
from sqlalchemy.exc import ArgumentError
from app.bot.handlers import get_bot, start_pooling
from app.db.handlers import start_db as start_database
import os
from dotenv import load_dotenv

def write_env(token:str = '', DSN:str = ''):
    if not os.path.exists('conf.env'):
        with open('conf.env', 'w') as f:
            f.write(f"token = {token}\n")
            f.write(f"DSN = {DSN}")
    else:
        load_dotenv('conf.env')
        token_old = os.getenv('token')
        dsn_old = os.getenv('DSN')
        if token == '':
            token_new = token_old
        else:
            token_new = token
        if DSN == '':
            dsn_new = dsn_old
        else:
            dsn_new = DSN
        with open('conf.env', 'w') as f:
            f.write(f"token = {token_new}\n")
            f.write(f"DSN = {dsn_new}")

def read_env(env_perem:str)->str:
    if os.path.exists('conf.env'):
        load_dotenv('conf.env')
        return os.getenv(env_perem)
    else:
        token = input_token()
        DSN = input_DSN() 
        write_env(token=token, DSN=DSN)
        load_dotenv('conf.env')
        return os.getenv(env_perem)
        

def input_token()->str:
    return input('Please, insert right token from BotFather: ')

def input_DSN()->str:
    basetype = 'postgresql'
    login = input('Insert database login: ')
    password = input('Insert database password: ')
    port = input('Insert database port: ')
    base = input('Insert database name: ')
    return f'{basetype}://{login}:{password}@{port}/{base}'
     
def get_tg_bot():
    token = read_env('token')
    try:
        return get_bot(token)
    except TokenValidationError:
        print('This token is invalid!')
        token = input_token()
        try:
            bot = get_bot(token)
            write_env(token=token)
            return bot
        except TokenValidationError:
            print('This token is invalid!')
            exit()
    
def get_db():
    DSN = read_env('DSN')
    try:
        return start_database(DSN) 
    except ArgumentError:
        print('Invalid DSN key!')
        DSN = input_DSN()
        try:
            session = start_database(DSN)
            write_env(DSN=DSN)
            return session
        except ArgumentError:
            print('This DSN key is invalid!')
            exit()
    
def main()->bool:
    db = get_db()
    bot = get_tg_bot()
    asyncio.run(start_pooling(bot, db))


if __name__ == '__main__':
    main()