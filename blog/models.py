from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# class Blog(Base):
#     __tablename__ = 'blogs'
#     id = Column(Integer,primary_key = True,index = True)
#     title  = Column(String)
#     blog = Column(String)


# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer,primary_key = True,index = True)
#     name = Column(String)
#     email = Column(String)
#     password = Column(String)

#Relationship with ForeignKey
class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer,primary_key = True,index = True)
    title  = Column(String)
    blog = Column(String)
    creator_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User",back_populates='blogs')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key = True,index = True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blog", back_populates='creator')