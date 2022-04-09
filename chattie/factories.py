import factory
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from chattie import bcrypt, db
import datetime

from .models import (Message, Profile, Room, TimestampMixin, User,
                     user_identifier)

fake = Faker()

engine = create_engine('postgresql:///:memory:')
session = scoped_session(sessionmaker(bind=engine))


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """User factory for typical user"""
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n)
    username = fake.user_name()
    email = factory.LazyAttribute(
        lambda x: f"{x.username}@example.com".lower())
    password = bcrypt.generate_password_hash(
            'User1Pass!').decode('utf-8')
    

class SecondUserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """User without relations"""
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n+1)
    username = fake.user_name()
    email = factory.LazyAttribute(
        lambda x: f"{x.username}@example.com".lower())
    password = bcrypt.generate_password_hash(
            'User2Pass!').decode('utf-8')
    
    
class ProfileFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Profile factory for typical user"""
    class Meta:
        model = Profile
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n)
    first_name = fake.first_name()
    last_name = fake.last_name()
    country = fake.country()
    city = fake.city()
    about = fake.sentence(nb_words=10)
    user_id = factory.SubFactory(UserFactory)
    
    
class RoomFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Room factory"""
    class Meta:
        model = Room
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n)
    creator_id = factory.SubFactory(UserFactory)
    name = fake.word()
    
    
class MessageFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Message factory"""
    class Meta:
        model = Message
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n)
    message = fake.user_name()
    username = factory.SubFactory(UserFactory)
    roomname = factory.SubFactory(RoomFactory)
