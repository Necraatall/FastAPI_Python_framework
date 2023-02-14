from sqlalchemy import Boolean, Column, Integer, String
from typing import Union, List
from database import Base
from sqlalchemy.orm import Relationship

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    done = Column(Boolean, index=True)
    # TODO: how to make interval 1-5
    priority = Column(Integer, index=True)

