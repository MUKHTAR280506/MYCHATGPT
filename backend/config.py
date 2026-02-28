
from database import Base , engine
from db_tables import Chat

def init_db():
    print("Creating Database tables")
    Base.metadata.create_all(engine)
    print("Tables created successfully")


