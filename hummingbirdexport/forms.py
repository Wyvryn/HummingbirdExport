from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms import validators

from hummingbirdexport.models import User


class LoginForm(Form):
    username = TextField('Username', validators=[validators.required()])
    password = PasswordField('Password', validators=[validators.optional()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        # Does our the exist
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password')
            return False

        # Do the passwords match
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False

        return True
