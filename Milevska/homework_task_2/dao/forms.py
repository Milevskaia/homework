from datetime import datetime

from flask_wtf import Form
from wtforms import StringField,   SubmitField,  IntegerField, DateField
from wtforms import validators, ValidationError


class ShipForm(Form):
    ship_id = IntegerField('ship_id: ', [validators.DataRequired('Please enter ship_id.')])
    ship_number = StringField('ship_number: ', [validators.Length(12, 12, "6 symbols allowed")])
    ship_date = DateField('ship_date: ', [validators.DataRequired('Please enter ship_id.')])
    ship_name = StringField('ship_number: ', [validators.Length(0, 40, "40 symbols allowed")])
    ship_address = StringField('ship_address: ', [validators.Length(0, 40, "100 symbols allowed")])

    def validate_ship_date(self, field):
        if field < datetime.strptime('2000-01-01', 'YYYY-MM-DD'):
            raise ValidationError('Date is wrong. Must be more than 2000-01-01')
