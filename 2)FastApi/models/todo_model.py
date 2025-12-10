from tabnanny import check
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


from sqlalchemy import Column, Integer, String, Boolean,CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()




class Todos(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    status = Column(String, nullable=False, default="pending")
