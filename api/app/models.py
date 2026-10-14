"""Modelos do banco de dados."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Consulta(Base):
    """Histórico de CNPJs consultados."""

    __tablename__ = "consultas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cnpj: Mapped[str] = mapped_column(String(14), unique=True, index=True)
    razao_social: Mapped[str | None] = mapped_column(String(255))
    nome_fantasia: Mapped[str | None] = mapped_column(String(255))
    situacao: Mapped[str | None] = mapped_column(String(60))
    municipio: Mapped[str | None] = mapped_column(String(120))
    uf: Mapped[str | None] = mapped_column(String(2))
    total_consultas: Mapped[int] = mapped_column(Integer, default=1)
    ultima_consulta: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    primeira_consulta: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
