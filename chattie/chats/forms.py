from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from chattie.models import Room


class CreateRoomForm(FlaskForm):
    name = StringField('Room name', validators=[DataRequired()])
    submit = SubmitField('Create')
    
    def validate_name(self, name):
        name = Room.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That name is taken. Please choose a different one.')