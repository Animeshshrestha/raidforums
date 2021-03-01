from enum import Enum
from sqlalchemy import create_engine, Column, Table, ForeignKey, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary, JSON)

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()

class CategoryType(Enum):

    General='General'
    Staff = 'Staff'
    Other = 'Other'
    Tech = 'Tech'
    Tutorials = 'Tutorials'
    Marketplace = 'Marketplace'
    Leaks = 'Leaks'
    Cracking = 'Cracking'
    RaidingRelated = 'RaidingRelated'

class StringEnum(TypeDecorator):

    impl = String

    def __init__(self, enumtype, *args, **kwargs):
        super(StringEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class ForumSection(DeclarativeBase):
    __tablename__ = "forum_section_table"

    id = Column(Integer, primary_key=True)
    category = Column(StringEnum(CategoryType), nullable=False)
    sub_category = Column(String, nullable=True)
    forum_name = Column(String(length=200), nullable=False)
    forum_description = Column(String(length=200), nullable=False)
    forum_link = Column(String(length=200), nullable=False)
    threads_count = Column(String, nullable=False)
    posts_count = Column(String, nullable=False)
    forum_last_post = Column(JSON, nullable=False, default={})