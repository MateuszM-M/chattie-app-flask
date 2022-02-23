from chattie.models import Room
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class CreateRoomForm(FlaskForm):
    """
    Form to create a room.
    
    Form contains name field and submit button.
    Name cannot be empty and have to be unique.
    """
    name = StringField('Room name', validators=[DataRequired()])
    submit = SubmitField('Create')
    
    def validate_name(self, name):
        """Checks if name is uniqe."""
        name = Room.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError(
                'That name is taken. Please choose a different one.')
