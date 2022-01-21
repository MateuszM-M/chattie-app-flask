from chattie import db
from flask_login import UserMixin



class User(db.Model, UserMixin):
    pass


class Room(db.Model):
    pass


class Message(db.Model):
    pass
