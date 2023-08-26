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

    def __str__(self):
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
    completed = Column(Boolean, default=False)
    person_id = Column(Integer, ForeignKey('persons.id_'))
    responsible = relationship('Person')
    created = Column(Date, default=func.current_date())

    def __str__(self):
        return (f'Activity: description={self.description}, completed={self.completed}, '
                'responsible={self.responsible.name}, created={self.created}')

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()


# Classes for REST operations
class PersonDb(Resource):
    def get(self, name):
        """Retrieve a person by its name"""
        stmt = select(Person).where(Person.name == name)
        result = session.execute(stmt).first()
        
        if result is None:
            response = {'status': 1, 'message': 'Person not found!'}
        else:
            person = result[0]
            response = {'name': person.name, 'age': person.age}

        return response

    def put(self, name):
        """Update a person's age. The person is retrieved by name."""
        data = request.json
        stmt = select(Person).where(Person.name == name)
        result = session.execute(stmt).first()
        
        if result is None:
            response = {'status': 1, 'message': 'Person not found!'}
        else:
            person = result[0]
            person.age = data['age']
            response = {'status': 0, 'name': person.name, 'age': person.age}

        return response

    def delete(self, name):
        """Remove a person from the DB (by its name)."""
        stmt = select(Person).where(Person.name == name)
        result = session.execute(stmt).first()

        if result is None:
            response = {'status': 1, 'message': 'Person not found!'}
        else:
            person = result[0]
            person.delete()
            response = {'status': 0, 'message': 'Person successfully deleted!'}

        return response


class ActivityDb(Resource):
    def get(self, id_):
        """Retrieve and activity by its ID."""
        stmt = select(Activity).where(Activity.id_ == id_)
        result = session.execute(stmt).first()
        
        if result is None:
            response = {'status': 1, 'message': 'Activity not found!'}
        else:
            activity = result[0]
            response = {
                'description': activity.description,
                'completed': activity.completed,
                'responsible': activity.responsible,
                'created': activity.created
            }

        return response

    def put(self, id_):
        """Update an activity's 'completed' status. The activity is retrieved by ID-"""
        activity = session.execute(select(Activity).where(Activity.id_ == id_)).first()
        
        if activity is None:
            response = {'status': 1, 'message': 'Activity not found!'}
        else:
            activity = activity[0]
            activity.completed = not activity.completed
            activity.save()
            response = {
                'id': activity.id_,
                'description': activity.description,
                'completed': activity.completed,
                'responsible': activity.responsible.name,
                'created': str(activity.created)
            }

        return response

    def delete(self, id_):
        """Remove an activity from the DB (by its ID)."""
        activity = session.execute(select(Activity).where(Activity.id_ == id_)).first()

        if activity is None:
            response = {'status': 1, 'message': 'Activity not found!'}
        else:
            activity = activity[0]
            activity.delete()
            response = {'status': 0, 'message': 'Activity successfully deleted!'}
            
        return response


class ListPersonDb(Resource):
    def get(self):
        """List all registered persons."""
        result = session.execute(select(Person))
        response = [{'name': p[0].name, 'age': p[0].age} for p in result]
        
        if len(response) == 0:
            return {'message': 'No one registered yet.'}
        else:
            return response

    def post(self):
        """Add a person to the DB"""
        data = request.json
        person = Person(name=data['name'], age=data['age'])
        person.save()

        return {'id': person.id_, 'name': person.name, 'age': person.age}

    def put(self, name):
        """Update a person's age. The person is retrieved by name."""
        data = request.json
        stmt = select(Person).where(Person.name == name)
        result = session.execute(stmt).first()
        
        if result is None:
            response = {'status': 1, 'message': 'Person not found!'}
        else:
            person = result[0]
            person.age = data['age']
            response = {'status': 0, 'name': person.name, 'age': person.age}

        return response


class ListActivityDb(Resource):
    def get(self):
        """List all the activities in the DB."""
        stmt = select(Activity)
        result = session.execute(stmt)
        response = [
             {
                 'description': a[0].description,
                 'completed': a[0].completed,
                 'responsible': a[0].responsible.name,
                 'created': str(a[0].created)
             } for a in result
        ]

        if len(response) == 0:
            return {'message': 'No registered activity yet.'}
        else:
            return response
            
    def post(self):
        """Add an activity to the DB."""
        data = request.json
        name = data['responsible']
        person = session.execute(select(Person).where(Person.name == name)).first()

        if person is None:
            response = {'status': 1, 'message': 'Responsible person not registered.'}
        else:
            desc = data['description']
            resp = person[0]
            activity = Activity(
                description=desc,
                responsible=resp
            )
            activity.save()
            response = {
                'id': activity.id_,
                'description': activity.description,
                'completed': activity.completed,
                'responsible': activity.responsible.name,
                'created': str(activity.created)
            }

        return response


class ListActivityPerPerson(Resource):
    def get(self, name):
        result = session.execute(select(Person).where(Person.name == name)).first()

        if result is None:
            return {'status': 1, 'message': 'Person not found.'}
        else:
            person = result[0]
            result = session.execute(select(Activity).where(Activity.responsible == person))

            if result is None:
                return {'message': 'No activity registered for this person'}
            else:
                response = [{
                    'description': a[0].description,
                    'completed': a[0].completed,
                    'created': str(a[0].created)
                } for a in result]

                return response
            
engine = create_engine('sqlite:///activities.db', echo=True)
Base.metadata.create_all(engine)
session = Session(engine)
app = Flask(__name__)
api = Api(app)
# API routes and classes
api.add_resource(PersonDb, '/person/<string:name>')
api.add_resource(ListPersonDb, '/person', '/person/')
api.add_resource(ActivityDb, '/activity/<int:id_>')
api.add_resource(ListActivityDb, '/activity', '/activity/')
api.add_resource(ListActivityPerPerson, '/activity/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
