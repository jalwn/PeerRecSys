from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets




class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class LikeForm(FlaskForm):
    like = SubmitField()
    ignore = SubmitField()

class Taglist2(FlaskForm):
    jsfunc = {'onchange': 'cbCompare(this)'}
    tags = MultiCheckboxField('label',
                                  coerce=int,
                                  # choices=[(tag.id, tag.tagname) for tag in Tag.query.all()],
                                  validators=[],
                                  )
    enterTag = StringField('tag')
    submit = SubmitField('submit')