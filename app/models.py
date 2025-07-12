import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base

db = sa.create_engine("sqlite://memory:")
Session = sessionmaker(bind=db)
base = declarative_base()



class MailTemplate:
    def __init__(self, title: str, ):
        pass