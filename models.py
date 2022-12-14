from sqlalchemy import Boolean, String, Integer, Float, Column
from database import Base

class fastapi_app(Base):
    __tablename__ = "fishtestdata"
    Id = Column(Integer, primary_key=True,index=True)
    Weight = Column(Float)
    Length1 = Column(Float)
    Length2 = Column(Float)
    Length3 = Column(Float)
    Height = Column(Float)
    Width = Column(Float)
    Species = Column(String(16))
