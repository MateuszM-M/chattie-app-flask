from chattie import db
from chattie.models import Message


def create_message(msg, room, username=None):
    """
    Saves message in db and passes it on to enable sending it.
    
    Parameters
    ----------
    msg : str
        message that has to be sent, cannot be empty
    room : str
        room in which message has to be sent
    username : str, optional
        sender's username
        
    Returns
    -------
    dict
        Contains username and message
    """
    if msg != "":
        message = Message(
            username=username,
            roomname=room,
            message=msg)
        db.session.add(message)
        db.session.commit()
    return {'username': username,
            'message': msg}


def listify(instrumented_list):
    """
    Take in instrumented_list which should be list of participants
    of the room chat from database and returns list.
    """
    new_list = [user.username for user in instrumented_list]
    return new_list
