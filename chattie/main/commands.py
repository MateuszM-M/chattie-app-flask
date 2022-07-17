from .routes import main
from chattie import db
from chattie.models import User, Profile
from chattie import bcrypt

@main.cli.command('create_db')
def create_db():
    """Creates db, mainly before first use
    Additionaly creates test user to enable
    loging without credentials.
    """
    db.create_all()

    hashed_password = bcrypt.generate_password_hash(
            "Test9090").decode('utf-8')
    db.session.add(User(
        username="test_user",
        email="testchattie@testchattie.com",
        password=hashed_password
    ))
    db.session.commit()

    user_id = User.query.filter_by(
            username="test_user").first().id
    profile = Profile(user_id=user_id)
    db.session.add(profile)
    db.session.commit()

    print("DB created")
    
    
@main.cli.command('drop_db')
def drop_db():
    """Deletes db"""
    db.drop_all()
    print("DB deleted")