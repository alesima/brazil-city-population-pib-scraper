from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Municipio(Base):
    __tablename__ = 'municipios'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    estado = Column(String)
    populacao = Column(Integer)
    pib_per_capita = Column(Float)
    possui_cicc = Column(Integer, default=0)
    possui_gcm = Column(Integer, default=0)
    possui_samu = Column(Integer, default=0)
