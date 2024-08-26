import sqlalchemy as sq
from app.db.models import recreate_tables, create_tables, Users, Words, Messages, UsersWords
import psycopg2

def start_db(DSN:str):
    engine = sq.create_engine(DSN)
    return create_tables(engine)

async def get_message(message:str, session:sq.orm.session.Session) -> str:
    q = session.query(Messages).filter(Messages.id == message).all()
    if len(q) > 0:
        return q[0].text
    else: return message

async def get_user(user_id:str, session:sq.orm.session.Session)->bool:
    q = session.query(Users).filter(Users.name == user_id).all()
    if len(q) == 0:
        return False
    else: return True

async def create_user(user_id:str, session:sq.orm.session.Session)->bool:
    session.add(Users(name = user_id))
    for n in range(4):
        session.add(UsersWords(user_id = user_id, word_id = n+1))
    try:
        session.commit()
        return True
    except:
        return False
