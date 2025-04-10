from .datastore.sqla import sqldb_init_app
from .babel import babel_init_app
from .template import template_init_app
from .security import security_init_app
from .utils.authorize import authorize_allow
from .admin import Admin
from .views.index_view import IndexView
from .views.user_view import UserView


class Manager:
    """This is used to manager babel,template,admin, and so on..."""

    def __init__(self, app=None):
        self.admins = []
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        if not hasattr(app, "extensions"):
            app.extensions = {}

        if "manager" in app.extensions:
            raise Exception("manager extension already exists in app.extensions.")

        app.extensions["manager"] = self

        # config extends
        if app.config.get("SQLALCHEMY_DATABASE_URI", None) is None:
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        else:
            app.config["SQLALCHEMY_USERCENTER"] = True

        # init db
        if "sqlalchemy" not in app.extensions:
            sqldb_init_app(app)

        if "babel" not in app.extensions:
            babel_init_app(app)

        if "template" not in app.extensions:
            template_init_app(app)

        if "security" not in app.extensions:
            security_init_app(app)

        # init admins
        self.init_admins(app)

    def add_admin(self, admin: Admin):
        for p in self.admins:
            if p.endpoint == admin.endpoint:
                raise Exception(
                    "Cannot have two Admin() instances with same endpoint name."
                )

            if p.url == admin.url:
                raise Exception("Cannot assign two Admin() instances with same URL.")
        self.admins.append(admin)

    def init_admins(self, app):
        admin = Admin()
        admin.init_app(app)
        if app.config.get("ADMIN_ACCESS_ENABLED", True):
            admin.set_access_callback(authorize_allow)
        self.add_admin(admin)

        index_view = IndexView()
        admin.add_view(index_view, is_menu=False)

        user_view = UserView()
        admin.add_view(user_view, is_menu=False)
