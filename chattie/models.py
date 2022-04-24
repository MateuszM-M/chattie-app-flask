from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import backref

from chattie import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_identifier = db.Table('user_identifier',
    db.Column('room_name', db.String(20), db.ForeignKey('room.name')),
    db.Column('user_username', db.String(20), db.ForeignKey('user.username'))
)


class TimestampMixin():
    """
    Timestamp mixin
    
    Attributes
    ---------
    created : creation object date time
    updated : update object date time
    """
    created = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.utcnow)
    updated = db.Column(db.DateTime, 
                        onupdate=datetime.utcnow)


class User(db.Model, UserMixin, TimestampMixin):
    """
    DB model to represent user.
    
    Attributes
    ----------
    __tablename__ : sets table name
    id : id for user
    username : name for user
    email : user's email to log in
    password : user's password
    created : user register time
    rooms : relationship, one user can 
    messages : relationship, one user can send many messages,
               message can have only one author
    profile : relationship, one to one with profile table
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, 
                   primary_key=True)
    username = db.Column(db.String(20), 
                         unique=True, 
                         nullable=False)
    email = db.Column(db.String(120),
                      unique=True, 
                      nullable=False)
    password = db.Column(db.String(60), 
                         nullable=False)
    rooms_created = db.relationship('Room', 
                                    backref='creator', 
                                    lazy=True)
    messages_sent = db.relationship('Message', 
                                    backref='author', 
                                    lazy=True)
    profile = db.relationship('Profile',
                              backref=backref('user',
                                              uselist=False),
                              lazy=True,)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
    
    
class Profile(db.Model):
    """
    DB model to represent profile.
    
    Attributes
    ----------
    __tablename__ : sets table name
    id : id for profile
    first_name : first_name of profile
    last_name : last_name of profile
    country : country of profile
    city : city of profile
    email : user's email to log in
    image_file : image file of profile
    about : area to write more self
    user_id : foreign key, id of linked user
    """
    __tablename__ = 'profile'
    id = db.Column(db.Integer, 
                   primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    country = db.Column(db.String(30))
    city = db.Column(db.String(30))
    image_file = db.Column(db.String(), 
                           default='default.png')
    about = db.Column(db.Text)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)
    
    def __repr__(self):
        return f"Profile('{self.id}','{self.first_name}', '{self.last_name}')"
    

class Room(db.Model, TimestampMixin):
    """
    DB model to represent chat room.
    
    Attributes
    ----------
    __tablename__ : sets table name
    id : id for room
    name : chat room name
    creator_id : foreign key, id of creator user
    participants : relationship, room can have many users as participants
                   many users can participate in many rooms
    messages : relationship, one room can have many messages,
               message can only be in one room

    """
    __tablename__ = 'room'
    id = db.Column(db.Integer, 
                   primary_key=True)
    name = db.Column(db.String(20), 
                     nullable=False, 
                     unique=True)
    creator_id = db.Column(db.Integer, 
                           db.ForeignKey('user.id'), 
                           nullable=False)
    participants = db.relationship('User', 
                                   secondary=user_identifier)
    messages = db.relationship('Message', 
                               backref='room_with_messages',
                               lazy=True, 
                               cascade="all, delete")
    
    def __repr__(self):
        return self.name


class Message(db.Model, TimestampMixin):
    """
    DB model to represent message.
    
    Attributes
    ----------
    __tablename__ : sets table name
    id : id for message
    message : message value
    username : foreign key, author name
    roomname : foreign key, room that stores message
    """
    __tablename__ = 'message'
    id = db.Column(db.Integer, 
                   primary_key=True)
    message = db.Column(db.String(1000), 
                        nullable=False)
    username = db.Column(db.String, 
                         db.ForeignKey('user.username'))
    roomname = db.Column(db.String, 
                         db.ForeignKey('room.name'), nullable=False)
    
    def __repr__(self):
        return f"('{self.username}': '{self.message[40:]}')"
