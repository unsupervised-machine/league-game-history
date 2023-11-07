from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class CreateUserForm(FlaskForm):
    puuid = StringField('PUUID: ', validators=[DataRequired()])
    summoner_name = StringField('summoner_name: ', validators=[DataRequired()])
    profile_icon_id = IntegerField('profile_icon_id: ', validators=[DataRequired()])
    summoner_level = IntegerField('summoner_level: ', validators=[DataRequired()])
    submit = SubmitField('Submit')