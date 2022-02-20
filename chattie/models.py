from datetime import datetime

from flask_login import UserMixin

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
    ...
    Attributes
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
    ...
    
    Attributes
    ----------
    __tablename__ : sets table name
    id : id for user
    username : name for user
    email : user's email to log in
    image_file : image to upload in profile
    password : user's password
    created : user register time
    rooms : relationship, one user can 
    messages : relationship, one user can send many messages,
               message can have only one author
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
    image_file = db.Column(db.String(20), 
                           nullable=False, 
                           default='default.jpg')
    password = db.Column(db.String(60), 
                         nullable=False)
    rooms_created = db.relationship('Room', 
                                    backref='creator', 
                                    lazy=True)
    messages_sent = db.relationship('Message', 
                                    backref='author', 
                                    lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
    

class Room(db.Model, TimestampMixin):
    """
    DB model to represent chat room.
    ...
    
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
    ...
    
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
        return f"('{self.username}': '{self.message}')"
