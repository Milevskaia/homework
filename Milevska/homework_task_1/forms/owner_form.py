from flask_wtf import Form
from wtforms import StringField, SubmitField, DateField
from wtforms import validators


class OwnerForm(Form):
    owner_phone = StringField("Name: ",
                              [
                                  validators.DataRequired("Please enter your phone."),
                                  validators.Length(11, "Phone should be 11 symbols")
    ])
    owner_birthday = DateField("Birthday: ", [validators.DataRequired("Please enter your birthday.")])
    submit = SubmitField("Save")
