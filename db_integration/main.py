#!/usr/bin/python3

from sqlalchemy.orm import (
    Session,
    declarative_base,
    relationship
)
from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    ForeignKey,
    create_engine,
    select,
    func,
    inspect
)

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    id_ = Column(Integer, primary_key=True)
    name = Column(String(40))
    cpf = Column(String(9))
    address = Column(String(30))
    account = relationship('Account', back_populates='clients')
    
    def __repr__(self):
        return (
            f'Client(id={self.id_}, '
            'name={self.name}, '
            'CPF={self.cpf}, '
            'address={self.address})'
        )


class Account(Base):
    __tablename__ = 'accounts'
    id_ = Column(Integer, primary_key=True)
    acc_type = Column(String)
    branch = Column(String)
    number = Column(Integer)
    client_id = Column(Integer, ForeignKey('clients.id_'), nullable=False)
    balance = Column(Numeric)
    client = relationship('Client', back_populates='accounts')
    
    def __repr__(self):
        return (
            f'Account(id={self.id_}, '
            'type={self.acc_type}, '
            'branch={self.branch}, '
            'number={self.number}, '
            'balance={self.balance})'
        )

engine = create_engine('sqlite://') # Connection to DB
Base.metadata.create_all(engine) # Create tables in DB
inspector = inspect(engine)

print("Table names: ", inspector.get_table_names())
print(inspector.default_schema_name)

