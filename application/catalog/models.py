from sqlalchemy import Column, Integer, String, Text, ForeignKey
from db import Base

class Users(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String(250), nullable=False)
  password = Column(String(250), nullable=False)
  api_key = Column(String(250), nullable=False)

  def __init__(self, username=None, password=None, api_key=None):
    self.username = username
    self.password = password
    self.api_key = api_key

  def __repr__(self):
    return '<User %r>' % (self.username)
  


class Categories(Base):
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  name = Column(String(250), nullable=False)
 
  def __init__(self, name=None):
    self.name = name
  
  
  def __repr__(self):
    return '<Category %r>' % (self.name)


class Items(Base):
  __tablename__ = 'items'

  id = Column(Integer, primary_key=True)
  category_id = Column(Integer, ForeignKey('categories.id'))
  user_id = Column(Integer, ForeignKey('users.id'))
  title = Column(String(250), nullable=False)
  description = Column(Text, nullable=False)

  @property
  def serialize(self):
    return {
        'id'         : self.id,
        'many2many'  : self.serialize_many2many
    }