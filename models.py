from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PickleType, Boolean
from db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    chat_id = Column(Integer)
    emoji = Column(String)
    subscribed = Column(Boolean)

    def __repr__(self) -> str:
        return f"User id: {self.user_id}, name: {self.first_name}"


class ImagesRating(Base):
    __tablename__ = "images_rating"

    id = Column(Integer, primary_key=True)
    image_name = Column(String)
    votes = Column(MutableDict.as_mutable(PickleType))

    def __repr__(self) -> str:
        return f"ImagesRating id: {self.id}, name: {self.image_name}"


class Anketa(Base):
    __tablename__ = "anketa"

    id = Column(Integer, primary_key=True)
    created = DateTime()
    rate = Column(Integer)
    name = Column(String)
    comment = Column(String)
    user_id = Column(Integer, ForeignKey(User.user_id), index=True, nullable=False)

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        return f"Anketa id: {self.id}, name: {self.first_name}"
