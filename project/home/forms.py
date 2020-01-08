from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField(
        'Description', validators=[DataRequired(), Length(max=1400)])
