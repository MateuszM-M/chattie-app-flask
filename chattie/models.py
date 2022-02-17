from datetime import datetime
from chattie import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Table,  Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_identifier = db.Table('user_identifier',
    db.Column('room_name', db.String(20), db.ForeignKey('room.name')),
    db.Column('user_username', db.String(20), db.ForeignKey('user.username'))
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # participates_in = db.Column(db.Integer, db.ForeignKey('room.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    
    # participates_in = db.relationship('Room', secondary=AssociationTable)
    rooms = db.relationship('Room', foreign_keys=[room_id])
    messages = db.relationship('Message', foreign_keys=[message_id])
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    
    # participant_names = db.Column(db.Integer, db.ForeignKey('user.username'))
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    
    participants = db.relationship('User', secondary=user_identifier)
    messages = db.relationship('Message', foreign_keys=[message_id], cascade="all,delete")
    
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return self.name


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), db.ForeignKey('user.username'))
    roomname = db.Column(db.String(20), db.ForeignKey('room.name'), nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[username])
    room = db.relationship('Room', foreign_keys=[roomname])

    def __repr__(self):
        return f"('{self.username}': '{self.message}')"