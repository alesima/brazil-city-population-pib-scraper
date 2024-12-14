from sqlalchemy import Float, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Municipio(Base):
    __tablename__ = 'municipios'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String)
    estado: Mapped[str] = mapped_column(String)
    populacao: Mapped[int] = mapped_column(Integer)
    pib_per_capita: Mapped[float] = mapped_column(Float)
    possui_cicc: Mapped[int] = mapped_column(Integer, default=0)
    possui_gcm: Mapped[int] = mapped_column(Integer, default=0)
    possui_samu: Mapped[int] = mapped_column(Integer, default=0)
