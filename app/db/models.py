import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from app.config import read_env, input_DSN
from sqlalchemy.exc import ArgumentError

try:
    engine = sq.create_engine(read_env('DSN'))
    print('DB is active')
except ArgumentError:
    try:
        engine = sq.create_engine(input_DSN())
        print('DB is active')
    except ArgumentError:
        print('This DSN key is invalid!')
        exit()
Session = sessionmaker(bind=engine)()


Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = sq.Column(sq.Integer, primary_key = True)
    name = sq.Column(sq.String(length = 60), unique = True)

class Words(Base):
    __tablename__ = 'words'
    id = sq.Column(sq.Integer, primary_key = True)
    word_ru = sq.Column(sq.String(length = 60), unique = False, nullable = True)
    word_en = sq.Column(sq.String(length = 60), unique = False, nullable = True)
    
class UsersWords(Base):
    __tablename__ = 'usersword'
    __table_args__ = (sq.PrimaryKeyConstraint('user_id', 'word_id'),)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'), nullable = False)
    word_id = sq.Column(sq.Integer, sq.ForeignKey('words.id'), nullable = False)
    user = relationship(Users, backref = 'users')
    word = relationship(Words, backref = 'words')

class Messages(Base):
    __tablename__ = 'messages'
    id = sq.Column(sq.String, primary_key = True)
    text = sq.Column(sq.String(length = 1024), unique = False, nullable = False)

def recreate_tables()->None:
    Base.metadata.drop_all(engine)
    create_tables(engine)

def create_tables()->None:
    Base.metadata.create_all(engine)
