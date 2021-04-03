from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, Email, Optional



class LoginRegisterForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class CreatePostForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])
    topic = StringField('Topic', validators=[DataRequired()])
    start_event = DateField('Beginning', format='%Y-%m-%d', validators=[Optional()])
    end_event = DateField('Ending', format='%Y-%m-%d', validators=[Optional()])
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"rows": 20, "cols": 60})
    # tags = StringField('Tags')


class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[Optional()])
    topic = StringField('Topic', validators=[Optional()])
    start_event = DateField('Beginning', format='%Y-%m-%d', validators=[Optional()])
    end_event = DateField('Ending', format='%Y-%m-%d', validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()], render_kw={"rows": 20, "cols": 60})
