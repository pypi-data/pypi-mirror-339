from flask import url_for
from flask import request
from flask import redirect
from flask import flash
from flask import abort
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from ..admin import BaseView
from ..admin import expose
from ..proxies import current_usercenter


class UserView(BaseView):
    """
    Default administrative interface index page when visiting the ``/user/`` URL.
    """

    index_template = "views/user/index.html"
    list_template = "views/user/list.html"
    login_template = "views/user/login.html"
    register_template = "views/user/register.html"

    def __init__(
        self,
        name="User",
        endpoint="user",
        url="/user",
        template_folder=None,
        static_folder=None,
        static_url_path=None,
        menu_class_name=None,
        menu_icon_type=None,
        menu_icon_value=None,
        skip_check_auth=True,
    ):
        super().__init__(
            name=name,
            endpoint=endpoint,
            url=url,
            template_folder=template_folder,
            static_folder=static_folder,
            static_url_path=static_url_path,
            menu_class_name=menu_class_name,
            menu_icon_type=menu_icon_type,
            menu_icon_value=menu_icon_value,
            skip_check_auth=skip_check_auth,
        )

    def get_login_form_class(self):
        return current_usercenter.login_form_class

    def get_register_form_class(self):
        return current_usercenter.register_form_class

    def get_users(self):
        return current_usercenter.get_users()

    def validate_login_and_get_user(self, form):
        user, error = current_usercenter.login_user_by_username_password(
            form.username.data, form.password.data
        )
        return user, error

    def validate_register_and_create_user(self, form):
        user, error = current_usercenter.create_user(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
        )
        return user, error

    @login_required
    @expose("/")
    def index(self):
        return self.render(self.index_template)

    @expose("/login/", methods=("GET", "POST"))
    def login(self):
        if current_user.is_authenticated:
            return redirect(url_for(".index"))
        form = self.get_login_form_class()()
        if form.validate_on_submit():
            user, error = self.validate_login_and_get_user(form)
            if user is None:
                flash(error, "error")
                # form.username.errors.append(error)
            else:
                if hasattr(form, "remember_me"):
                    login_user(user, remember=form.remember_me.data)
                else:
                    login_user(user)
                next_page = request.args.get("next")
                if not next_page:
                    next_page = url_for(".index")
                return redirect(next_page)
        return self.render(self.login_template, form=form)

    @expose("/register/", methods=("GET", "POST"))
    def register(self):
        if current_user.is_authenticated:
            return redirect(url_for(".index"))
        form = self.get_register_form_class()()
        if form.validate_on_submit():
            user, error = self.validate_register_and_create_user(form)
            if user is None:
                flash(error)
            else:
                login_user(user)
                return redirect(url_for(".index"))

        return self.render(self.register_template, form=form)

    @expose("/logout/")
    def logout(self):
        logout_user()
        return redirect(url_for("index.index"))
