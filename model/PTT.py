# coding: utf-8
from sqlalchemy import Column, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


def get_table_name(table_name):
    class Information(Base):
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True}

        id = Column(BIGINT(20), primary_key=True)
        title = Column(VARCHAR(45), nullable=False)
        author = Column(VARCHAR(45), nullable=False, unique=True)
        board = Column(VARCHAR(45), nullable=False)
        hits = Column(VARCHAR(45), nullable=False)
        url = Column(VARCHAR(4096), nullable=False, unique=True)
        posted_date = Column(TIMESTAMP, nullable=False)
        description = Column(VARCHAR(4096))
        created_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
        updated_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    return Information