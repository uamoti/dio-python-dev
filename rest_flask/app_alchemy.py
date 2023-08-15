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
    Float,
    ForeignKey,
    create_engine,
    select,
    func,
    inspect
)

Base = declarative_base()

class Developer(Base):
    __tablename__ = 'developers'
    id_ = Column(Integer, primary_key=True)
    name = Column(String(40))
    age = Column(Integer)
    email = Column(String(30))

    def __repr__(self):
        return f'Developer name={self.name}, age={self.age}, email={self.email}'


class Skill(Base):
    __tablename__ = 'skills'
    id_ = Column(Integer, primary_key=True)
    name = Column(String(20))

    def __repr__(self):
        return f'Skill name={self.name}'



class DevSkill(Base):
    __tablename__ = 'devskills'
    id_ = Column(Integer, primary_key=True)
    developer = Column(Integer, ForeignKey('developers.id_'), nullable=False)
    skill = Column(Integer, ForeignKey('skills.id_'), nullable=False)


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
session = Session(engine)

devs = [
    Developer(name='Linus Torvalds', age=46, email='ltorvalds@linux.org'),
    Developer(name='Guido van Rossum', age=51, email='guido@python.org'),
    Developer(name='Bjarne Stroustrup', age=64, email='bjarne@ibm.com'),
    Developer(name='Rick Hickey', age=48, email='rick@clojure.org')
]

skills = [
    Skill(name='linux'),
    Skill(name='java'),
    Skill(name='clojure'),
    Skill(name='c'),
    Skill(name='git'),
    Skill(name='python'),
    Skill(name='sql'),
    Skill(name='bash'),
    Skill(name='rust')
]

devskill = [
    DevSkill(developer=1, skill=1),
    DevSkill(developer=1, skill=4),
    DevSkill(developer=1, skill=5),
    DevSkill(developer=2, skill=4),
    DevSkill(developer=2, skill=6),
    DevSkill(developer=3, skill=4),
    DevSkill(developer=3, skill=9),
    DevSkill(developer=3, skill=8),
    DevSkill(developer=4, skill=2),
    DevSkill(developer=4, skill=3),
    DevSkill(developer=4, skill=7)
]

session.add_all(devs)
session.add_all(skills)
session.add_all(devskill)
session.commit()

results = session.query(Developer).all()
print('-' * 20)
print('DEVELOPERS TABLE')
print('-' * 20)

for result in results:
    print(result)

stmt = select(Developer.name, Skill.name).join_from(Developer, DevSkill).join(Skill)
result = session.execute(stmt)
print('-' * 30)
print('DEVELOPERS AND THEIR SKILLS')
print('-' * 30)

for name, skill in result:
    print(f'{name} - {skill}')
