from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    field_of_study = db.Column(db.String)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    serialize_rules = ('-missions.scientist')
    missions = db.relationship('Mission', backref = 'scientist')
    planets = association_proxy('missions', 'planet')

    @validates('name')
    def validate_name(self, key, name):
        if name == '':
            raise ValueError('needs a name')
        return name 

    @validates('field_of_study')
    def validate_field_of_study(self, key, field_of_study):
        if field_of_study == '':
            raise ValueError('needs a field of study!')
        return field_of_study

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id')) 

    serialize_rules = ('-scientist.missions', 'planet.missions',)

    @validates('name')
    def validate_name(self, key, name):
        if name == '':
            raise ValueError('needs a name')
        return name 
    @validates('scientist')
    def validate_scientist(self, key, scientist):
        if scientist == '':
            raise ValueError('needs a scientist name')
        return scientist 
    @validates('planet')
    def validate_name(self, key, planet):
        if planet == '':
            raise ValueError('needs a planet')
        return planet
    @validates('missions')
     # no same missions 
    def validate_missions(self, key, mission):
        pass 

class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    serialize_rules = ('-planet.missions')
    missions = db.relationship('Mission', backref = 'planet')
    scientists = association_proxy('missions', 'scientist')
