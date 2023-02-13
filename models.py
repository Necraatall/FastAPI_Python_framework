from sqlalchemy import Boolean, Column, Integer, String

from .database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    done = Column(Boolean, index=True)
    description = Column(Integer, index=True)