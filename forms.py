from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistationForm(FlaskForm):
    # username variable is of class StringField which has been named Username
    # Passed Arguments include name and list of validators
    # The list of validators includea required validator and length validator
    username = StringField('Username', 
                            validators=[DataRequired(), 
                                        Length(min=6, max=20)]
                            )

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

    # EqualTo validator to check the siilarity between the confirm field and password field
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), 
                                                Length(min=6),
                                                EqualTo('password')]
                                    )

    submit = SubmitField('Sign Up') 

class LoginForm(FlaskForm):

    username = StringField('Username', 
                            validators=[DataRequired(), 
                                        Length(min=6, max=20)]
                            )

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login') 