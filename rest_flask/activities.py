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
    Boolean,
    Date,
    ForeignKey,
    create_engine,
    select,
    func,
    inspect
)
from flask import Flask, request
from flask_restful import Resource, Api


Base = declarative_base()

# Classes for database tables
class Person(Base):
    __tablename__ = 'persons'
    id_ = Column(Integer, primary_key=True)
    name = Column(String(40))
    age = Column(Integer)

    def __repr__(self):
        return f'Person name={self.name}, age={self.age}'

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()
        


class Activity(Base):
    __tablename__ = 'activities'
    id_ = Column(Integer, primary_key=True)
    description = Column(String(30))
    completed = Column(Boolean)
    person_id = Column(Integer, ForeignKey('persons.id_'))
    responsible = relationship('Person')
    created = Column(Date, default=func.current_date)

    def __repr__(self):
        return (f'Activity: description={self.description}, completed={self.completed}, '
                'responsible={self.responsible}, created={self.created}')

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


# Classes for REST operations
class PersonDb(Resource):
    def get(self, name):
        #person = Person.query.filter_by(name=name).first()
        stmt = select(Person).where(Person.name == name)
        result = session.execute(stmt)

        if len(result) == 0:
            response = {'status': 1, 'message': 'Person not found!'}
        else:
            person = result[0]
            response = {'name': person.name, 'age': person.age}

        return response

    def post(self):
        data = request.json
        person = Person(name=data['name'], age=data['age'])
        person.save()

        return {'id': person.id_, 'name': person.name, 'age': person.age}

    def put(self, name):
        # You can only alter the age of a person
        person = Person.query.filter_by(name=name).first()
        data = request.json
        
        if len(person) == 0:
            response = {'status': 1, 'message': 'Person not found!'}
        else:
            person.age = data['age']
            person.save()
            response = {'status': 0, 'name': person.name, 'age': person.age}

        return response

    def delete(self, name):
        person = Person.query.filter_by(name=name).first()

        if len(person) == 0:
            response = {'status': 1, 'message': 'Person not found!'}
        else:
            person.delete()
            response = {'status': 0, 'message': 'Person successfully deleted!'}

        return response


class ActivityDb(Resource):
    def get(self, id_):
        #activity = Activity.query.filter_by(id_=id_).first()
        

        if len(person) == 0:
            response = {'status': 1, 'message': 'Activity not found!'}
        else:
            response = {
                'description': activity.description,
                'completed': activity.completed,
                'responsible': activity.responsible,
                'created': activity.created
            }

        return response

    def post(self):
        data = request.json
        activity = Activity(**data)
        activity.save()

        return {
            'id': activity.id_,
            'description': activity.description,
            'completed': activity.completed,
            'responsible': activity.responsible,
            'created': activity.created
        }

    def put(self, id_):
        activity = Activity.query.filter_by(id_=id_).first()

        if len(person) == 0:
            response = {'status': 1, 'message': 'Activity not found!'}
        else:
            activity.completed = not activity.completed
            activity.save()
            response = {
                'id': activity.id_,
                'description': activity.description,
                'completed': activity.completed,
                'responsible': activity.responsible,
                'created': activity.created
            }

        return response

    def delete(self, id_):
        activity = Activity.query.filter_by(id_=id_).first()

        if len(person) == 0:
            response = {'status': 1, 'message': 'Activity not found!'}
        else:
            activity.delete()
            response = {'status': 0, 'message': 'Activity successfully deleted!'}
            
        return response


class ListActivityDb(Resource):
    def get(self):
        stmt = select(Activity)
        result = session.execute(stmt)

        response = [
             {
                 'description': a.description,
                 'completed': a.completed,
                 'responsible': a.responsible,
                 'created': a.created
             } for a in result
        ]
        if len(response) == 0:
            return {'message': 'The DB is empty!'}
        else:
            return response
            
engine = create_engine('sqlite:///activities.db', echo=True)
Base.metadata.create_all(engine)
session = Session(engine)
app = Flask(__name__)
api = Api(app)
# API routes and classes
api.add_resource(PersonDb, '/person/<string:name>', '/person/')
api.add_resource(ActivityDb, '/activity/<int:id_>')
api.add_resource(ListActivityDb, '/activity', '/activity/')

if __name__ == '__main__':
    app.run(debug=True)
