from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy.orm import relationship

Base = declarative_base()

class Entitys(Base):
   __tablename__ = "entitys"

   id = Column(Integer, primary_key=True, autoincrement=True)
   name = Column(String, nullable=False)
   image = Column(String, nullable=True)
   user_id = Column(BigInteger, nullable=False)
   ps = relationship("Prayers")

class Prayers(Base):
    __tablename__ = "prayers"

    id = Column(Integer, primary_key=True)
    e_id = Column(ForeignKey("entitys.id"))
    text = Column(String)
