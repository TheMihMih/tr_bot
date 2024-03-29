from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
