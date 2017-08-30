import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """The user table"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    picture = Column(String(450), nullable=False)
    email = Column(String(450))

    @property
    def serialize(self):
        """creates JSON object for api endpoint"""
        return {
            'name': self.name,
            'picture': self.picture,
            'id': self.id,
            'email': self.email
        }

class ToyStore(Base):
    """The toystore table"""
    __tablename__ = 'toystore'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    address = Column(String(250))
    phone_number = Column(String(15))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
        """creates JSON object for api endpoint"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'address': self.address,
            'phone_number': self.phone_number
        }


class Toy(Base):
    """The toy table"""
    __tablename__ = 'toy'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    color = Column(String(250))
    toystore_id = Column(Integer, ForeignKey('toystore.id'))
    toystore = relationship(ToyStore)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)




# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):
        """creates JSON object for api endpoint"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'color': self.color
        }


engine = create_engine('sqlite:///toystoredb.db')


Base.metadata.create_all(engine)