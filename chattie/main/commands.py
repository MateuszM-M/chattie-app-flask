from .routes import main
from chattie import db

@main.cli.command('create_db')
def create_db():
    """Creates db, mainly before first use"""
    db.create_all()
    print("DB created")
    
    
@main.cli.command('drop_db')
def drop_db():
    """Deletes db, convenient for testing"""
    db.drop_all()
    print("DB deleted")