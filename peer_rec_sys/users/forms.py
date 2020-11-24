from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField, widgets, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from peer_rec_sys.models import User, Tag



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
    # Custom validators are defined in functions to notify users if submitted username or email is in use
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is taken, chose another!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email is already being used, chose another!')

class LoginForm(FlaskForm):

    username = StringField('Username',
                            validators=[DataRequired(),
                                        Length(min=6, max=20)]
                            )

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class UpdateProfileForm(FlaskForm):
    # username variable is of class StringField which has been named Username
    # Passed Arguments include name and list of validators
    # The list of validators includea required validator and length validator
    username = StringField('Username',
                            validators=[DataRequired(),
                                        Length(min=6, max=20)]
                            )

    email = StringField('Email', validators=[DataRequired(), Email()])

    bio = StringField('Bio', validators=[Length(max=160)])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])

    submit = SubmitField('Update')

    # Validation occurs if username field is different from current username
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username is taken, chose another!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The email is already being used, chose another!')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()



class Taglist(FlaskForm):
    jsfunc = {'onchange': 'cbCompare(this)'}
    strength = MultiCheckboxField('label',
                                  coerce=int,
                                  # choices=[(tag.id, tag.tagname) for tag in Tag.query.all()],
                                  validators=[],
                                  render_kw=jsfunc
                                  )
    weakness = MultiCheckboxField('label',
                                  coerce=int,
                                  # choices=[(tag.id, tag.tagname) for tag in Tag.query.all()],
                                  validators=[],
                                  render_kw=jsfunc
                                  )

    submit = SubmitField('submit')


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[
        DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Submit')