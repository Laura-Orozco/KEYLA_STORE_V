from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:SQanlBxvgLoVyAxZaInoBOrEkzfpZPBr@ballast.proxy.rlwy.net:14976/railway"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True  
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
