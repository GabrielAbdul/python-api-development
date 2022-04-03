from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# create engine, responsible for establishing connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create session to communicate to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# define Base class that all table models will extend
Base = declarative_base()

# create db object
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    return False

""" def establish_db_connection(_host, _database, _user, _password):
    while True: 
        try:
            # connect to database, cursor_factory gives us table names
            conn = psycopg2.connect(host=_host, database=_database, user=_user, password=_password, cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print("Connection to database complete.")
            break
        except Exception as e:
            print("Database connection failed")
            print(e)
            time.sleep(2) """