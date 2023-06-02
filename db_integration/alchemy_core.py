#!/usr/bin/python3

import json
from sqlalchemy import (
    Table,
    MetaData,
    ForeignKey,
    Column,
    Integer,
    Float,
    String,
    create_engine,
    text
)

engine = create_engine('sqlite:///:memory:')
metadata = MetaData()


clients = Table(
    'clients',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('cpf', String(9), nullable=False),
    Column('address', String(30)),
)


accounts = Table(
    'accounts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('acc_type', String),
    Column('branch', String, nullable=False),
    Column('number', Integer, nullable=False),
    Column('client_id', Integer, ForeignKey('clients.id'), nullable=False),
    Column('balance', Float(precision=2))
)

metadata.create_all(engine)
print("\nTABLE CLIENTS METADATA:")
print(clients.primary_key)
print(clients.constraints)
print("\nTABLE ACCOUNTS METADATA:")
print(accounts.primary_key)
print(accounts.constraints)

client_data = json.load(open('clients.json'))
account_data = json.load(open('accounts.json'))

conn = engine.connect()
conn.execute(clients.insert(), client_data)
conn.execute(accounts.insert(), account_data)

result = engine.execute(text('select * from clients'))
print("\nCLIENTS TABLE:")

for row in result:
    print(row)

query = text('select clients.name, accounts.acc_type, accounts.balance from clients join accounts on clients.id = accounts.client_id')
result = engine.execute(query)
print("\nCLIENTS, ACCOUNTS AND BALANCES:")

for row in result:
    print(row)

