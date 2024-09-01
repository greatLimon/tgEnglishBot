from sqlalchemy import select, update, delete
from db.models import Users, Words, Messages, UsersWords, async_session

async def fill_default_values(data:dict)->None:
    for id_word, words in enumerate(data['Words']):
        await add_word(id_word+1, words[1], words[0])
    for message_id, message in data['Messages'].items():
        await add_message(message_id, message)
        # print('You need to restart program!')

async def add_word(id, word_ru:str, word_en:str):
    async with async_session() as session:
        obj = Words(id = id,word_ru = word_ru, word_en = word_en)
        session.add(obj)
        try:
            await session.commit()
        except:
            print(f'Error! Cant add to DB value {obj}')

async def add_message(message_id:str, text:str):
    async with async_session() as session:
        obj = Messages(id = message_id, text = text)
        session.add(obj)
        try:
            await session.commit()
        except:
            print(f'Error! Cant add to DB value {obj}')

async def get_message(message_id:str):
    async with async_session() as session:
        message = await session.scalar(select(Messages).where(Messages.id == message_id))
        if not message:
            return message_id
        else:
            return message.text
        
async def get_user_by_id(user_id:int)->bool:
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.id == user_id))
        if user: return True
        else: return False

async def add_user(user_id:int, name:str)->bool:
    async with async_session() as session:
        session.add(Users(id = user_id,name = name))
        try:
            await session.commit()
        except:
            session.add(Users(id = user_id,name = 'Unknown'))
            try:
                await session.commit()
            except:
                return False
        for n in range(4):
            session.add(UsersWords(user_id = user_id, word_id = n+1))
            try:
                await session.commit()
            except:
                return False
        return True
    
async def add_users_word(word_ru:str, word_en:str, user_id:int)->bool:
    async with async_session() as session:
        new_word = await session.scalar(select(Words).where(Words.word_ru == word_ru, Words.word_en == word_en))
        if not new_word:
            session.add(Words(word_ru = word_ru, word_en = word_en))
            try:
                await session.commit()
            except:
                return False
        new_word = await session.scalar(select(Words).where(Words.word_ru == word_ru, Words.word_en == word_en))
        new_word_id = new_word.id
        userword = await session.scalar(select(UsersWords).where(UsersWords.word_id == new_word_id))
        if not userword:
            session.add(UsersWords(user_id = user_id, word_id = new_word_id))
            try:
                await session.commit()
            except: 
                return False
        return True
        
        

async def delete_word_from_db(word_ru:str, word_en:str, user_id:int)->bool:
    async with async_session() as session:
        found_word = await session.scalar(select(Words).where(Words.word_ru == word_ru, Words.word_en == word_en))
        if found_word:
            found_word_id = found_word.id
            if not found_word_id in (1,2,3,4):
                users_words = await session.scalars(select(UsersWords).where(UsersWords.word_id == found_word_id))
                if users_words:
                    only_user = True
                    users_words_data = users_words.all()
                    if len(users_words_data) > 1:
                        for word in users_words_data:
                            if word.user_id != user_id:
                                only_user = False
                    if only_user:
                        obj =  delete(UsersWords).where(UsersWords.user_id == user_id, UsersWords.word_id == found_word_id)
                        await session.execute(obj)                      
                        try:
                            await session.commit()
                        except:
                            return False
                        obj = delete(Words).where(Words.id == found_word_id)
                        await session.execute(obj)
                        try:
                            await session.commit()
                        except:
                            return False
                    else:
                        obj = delete(UsersWords).where(UsersWords.user_id == user_id, UsersWords.word_id == found_word_id)
                        await session.execute(obj)
                        try:
                            await session.commit()
                        except:
                            return False
    return True

async def get_userwords(user_id:str)->list | None:
    async with async_session() as session:
            result_list = []
            userwords = await session.scalars(select(Words).join(UsersWords).where(Words.id == UsersWords.word_id, UsersWords.user_id == user_id))
            result = userwords.all()
            for word in result:
                result_list.append((word.word_ru, word.word_en))
            return result_list


