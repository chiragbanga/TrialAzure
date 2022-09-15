from sqlalchemy import Boolean, String, Integer, Float, Column
from databaseconnection import Base

class database1(Base):
    __tablename__ = "fishtestdata"
    Id = Column(Integer, primary_key=True,index=True)
    Weight = Column(Float)
    Length1 = Column(Float)
    Length2 = Column(Float)
    Length3 = Column(Float)
    Height = Column(Float)
    Width = Column(Float)
    Species = Column(String(16))
