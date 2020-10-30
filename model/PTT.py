# coding: utf-8
from sqlalchemy import Column, ForeignKey, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, ENUM, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Info(Base):
    __tablename__ = 'ptt'

    id = Column(BIGINT(20), primary_key=True)
    title = Column(VARCHAR(45), nullable=False)
    author = Column(VARCHAR(45), nullable=False, unique=True)
    board = Column(VARCHAR(45), nullable=False)
    hits = Column(VARCHAR(45), nullable=False)
    url = Column(VARCHAR(4096), nullable=False, unique=True)
    posted_date = Column(TIMESTAMP, nullable=False)
    description = Column(VARCHAR(4096))
    update_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))