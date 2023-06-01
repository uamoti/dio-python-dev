#!/usr/bin/python3

import json
from sqlalchemy.orm import (
    Session,
    declarative_base,
    relationship
)
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
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
    account = relationship('Account', back_populates='client')
    
    def __repr__(self):
        return (
            f'Client(id={self.id_}, '
            f'name={self.name}, '
            f'CPF={self.cpf}, '
            f'address={self.address})'
        )


class Account(Base):
    __tablename__ = 'accounts'
    id_ = Column(Integer, primary_key=True)
    acc_type = Column(String)
    branch = Column(String)
    number = Column(Integer)
    client_id = Column(Integer, ForeignKey('clients.id_'), nullable=False)
    balance = Column(Float(precision=2))
    client = relationship('Client', back_populates='account')
    
    def __repr__(self):
        return (
            f'Account(id={self.id_}, '
            f'type={self.acc_type}, '
            f'branch={self.branch}, '
            f'number={self.number}, '
            f'balance={self.balance})'
        )

engine = create_engine('sqlite://') # Connection to DB
Base.metadata.create_all(engine) # Create tables in DB
inspector = inspect(engine)

print("\nTable names: ", inspector.get_table_names())
print("Schema name:", inspector.default_schema_name)

client_data = json.load(open('clients.json'))
clients = [Client(**data) for data in client_data]
account_data = json.load(open('accounts.json'))
accounts = [Account(**data) for data in account_data]

# Create session, add records and commit changes
session = Session(engine)
session.add_all(clients)
session.add_all(accounts)
session.commit()

print("\nCLIENTS TABLE:")
results = session.query(Client).all()

for r in results:
    print(r)

print("\nACCOUNTS TABLE:")
query = select(Account)

for acc in session.scalars(query):
    print(acc)

print("\nCLIENTS ORDERED BY NAME:")
results = session.query(Client.name).order_by()

for name in results:
    print(name[0])

print("\nCLIENTS AND BALANCE:")
results = session.query(Client, Account).join(Account).all()

for client, account in results:
    print(client.name, account.balance)

