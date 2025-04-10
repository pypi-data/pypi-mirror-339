from ...forms import FlaskForm
from .mixins import LoginForm as MixLoginForm


class LoginForm(FlaskForm, MixLoginForm):
    pass
