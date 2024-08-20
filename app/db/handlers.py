import sqlalchemy as sq
from app.db.models import recreate_tables, create_tables, Users, Words, Messages, UsersWords
import psycopg2

def start_db(DSN:str):
    engine = sq.create_engine(DSN)
    return create_tables(engine)
