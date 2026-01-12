from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    saldo = Column(Float, default=0)
    banido = Column(Boolean, default=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

class Estoque(Base):
    __tablename__ = "estoque"
    id = Column(Integer, primary_key=True)
    produto = Column(String)
    conteudo = Column(String)  # login:senha
    imagem = Column(String)

class Fila(Base):
    __tablename__ = "fila"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    produto = Column(String)
    criado_em = Column(DateTime, default=datetime.utcnow)

class Pagamento(Base):
    __tablename__ = "pagamentos"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    valor = Column(Float)
    status = Column(String)
    asaas_id = Column(String)
