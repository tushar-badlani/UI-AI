from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum, Text, Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    


class Components(Base):
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    html = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='components')


class Likes(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    component_id = Column(Integer, ForeignKey('components.id'))
    created_at = Column(DateTime, server_default=func.now())
    # user = relationship('User', backref='likes')
    # component = relationship('Components', backref='likes')


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    comment = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    component_id = Column(Integer, ForeignKey('components.id'))
    created_at = Column(DateTime, server_default=func.now())
    # user = relationship('User', backref='comments')
    # component = relationship('Components', backref='comments')


class Layouts(Base):
    __tablename__ = 'layouts'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    html = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    # user = relationship('User', backref='layouts')
