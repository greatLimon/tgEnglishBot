import os
from dotenv import load_dotenv

def write_env(token:str = '', DSN:str = '')->dict:
    if not os.path.exists('conf.env'):
        with open('conf.env', 'w') as f:
            f.write(f"token = {token}\n")
            f.write(f"DSN = {DSN}")
        return {
            'token' : f'{token}',
            'DSN' : f'{DSN}'
        }
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
        return {
            'token' : f'{token_new}',
            'DSN' : f'{dsn_new}'
        }

def read_env(env_perem:str)->str:
    if os.path.exists('conf.env'):
        load_dotenv('conf.env')
        return os.getenv(env_perem)
    else:
        token = input_token()
        DSN = input_DSN() 
        return write_env(token=token, DSN=DSN)[env_perem]
        
        
def input_token()->str:
    token = input('Please, insert right token from BotFather: ')
    write_env(token=token)
    return token

def input_DSN()->str:
    basetype = 'postgresql+asyncpg'
    login = input('Insert database login: ')
    password = input('Insert database password: ')
    port = input('Insert database port: ')
    base = input('Insert database name: ')
    dsn =  f'{basetype}://{login}:{password}@{port}/{base}'
    write_env(DSN=dsn)
    return dsn
