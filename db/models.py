from config import read_env, input_DSN

import sqlalchemy as sq
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.exc import ArgumentError

# DSN = 'postgresql+asyncpg://postgres:123321@localhost:5432/tgEnglishBot'

try:
    engine = create_async_engine(url = read_env('DSN'))
except ArgumentError:
    try:
        engine = create_async_engine(url = input_DSN())
    except ArgumentError:
        print('Invalid database data!')
        exit()

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'
    id = sq.Column(sq.Integer, primary_key = True)
    name = sq.Column(sq.String(length = 60), unique = True)

    def __str__(self):
        return f'{str(self.id)}:{self.name}'

class Words(Base):
    __tablename__ = 'words'
    id = sq.Column(sq.Integer, primary_key = True)
    word_ru = sq.Column(sq.String(length = 60), unique = False, nullable = True)
    word_en = sq.Column(sq.String(length = 60), unique = False, nullable = True)

    def __str__(self):
        return f'{str(self.id)}:{self.word_ru}:{self.word_en}'
    
class UsersWords(Base):
    __tablename__ = 'usersword'
    __table_args__ = (sq.PrimaryKeyConstraint('user_id', 'word_id'),)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'), nullable = False)
    word_id = sq.Column(sq.Integer, sq.ForeignKey('words.id'), nullable = False)
    user = relationship(Users, backref = 'users')
    word = relationship(Words, backref = 'words')

    def __str__(self):
        return f'{str(self.user_id)}:{self.word_id}'

class Messages(Base):
    __tablename__ = 'messages'
    id = sq.Column(sq.String, primary_key = True)
    text = sq.Column(sq.String(length = 1024), unique = False, nullable = False)
    
    def __str__(self):
        return f'{str(self.id)}:{self.text}'

async def create_tables()->None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)