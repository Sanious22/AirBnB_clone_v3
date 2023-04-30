#!/usr/bin/python3
""" holds class User"""


import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column('password', String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship(
            "Place", back_populates='user',
            cascade='all, delete-orphan')
        reviews = relationship(
            "Review", back_populates='user',
            cascade='all, delete-orphan')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if 'id' in kwargs and 'password' in kwargs:
            super().__setattr__('password', kwargs['password'])
            del kwargs['password']
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """ensure that passwords are hashed"""
        if name == 'password':
            value = hashlib.md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
