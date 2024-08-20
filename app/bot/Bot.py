from aiogram import Bot
from aiogram.utils.token import TokenValidationError

import os
from dotenv import load_dotenv
    
class Tg_bot():
    def __init__(self):
        self._token = self._load_token()
        if self._token == '':
            self._token = self._input_token()
        self.bot = self._create_bot_class(self._token)
        if self.bot == None:
            exit()     

    def _input_token(self)->str:
        token = input('Insert token from BotFather: ')
        with open('conf.env', 'w') as f:
            f.write(f"token = '{token}'")
        return token

    def _load_token(self)->str:
        load_dotenv('conf.env')
        return os.getenv('token')

    def _create_bot_class(self, token:str, error:bool = False)->Bot:
        try:
            bot = Bot(token=token)
            return bot
        except TokenValidationError:
            print('Token is incorrect!')
            if not error:
                tkn = self._input_token()
                bot =  self._create_bot_class(self, tkn, True)
                return bot
            return None

