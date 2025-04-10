import pytest
from flask import url_for
from flask import abort
from flask_exts.admin import expose
from flask_exts.admin import BaseView
from flask_exts.admin import Admin
from flask_exts.admin.menu import MenuLink

from ..funcs import print_app_endpoint_rule
from ..funcs import get_app_endpoint_rule


class MockView(BaseView):
    allow_access = True

    @expose("/")
    def index(self):
        return "Success!"

    @expose("/test/")
    def test(self):
        return self.render("mock.html")

    def is_accessible(self):
        if self.allow_access:
            return super().is_accessible()
        return False

    def _handle_view(self, fn, **kwargs):
        if not self.allow_access:
            return self.inaccessible_callback(fn, **kwargs)


class MockNoindexView(BaseView):
    allow_access = True

    @expose("/test/")
    def test(self):
        return self.render("mock.html")

    def is_accessible(self):
        if self.allow_access:
            return super().is_accessible()
        return False


class MockExtendView(MockView):
    @expose("/test2/")
    def test2(self):
        return self.render("mock.html")


def test_baseview_defaults():
    view = MockView()
    assert view.name == "Mock View"
    assert view.endpoint == "mockview"
    assert view.url is None
    assert view.static_folder is None
    assert view.admin is None
    assert view.blueprint is None


def test_admin_default():
    admin = Admin()
    # print(admin.name)
    # print(admin.url)
    # print(admin.endpoint)
    # print(admin._views)
    # print(admin.menu)
    assert admin.name == "Admin"
    assert admin.url == "/admin"
    assert admin.endpoint == "admin"
    assert admin.app is None


def test_admin_menu():
    admin = Admin()
    menu = admin.menu
    assert menu.admin == admin
    menu.add_category("Category1", "class-name", "icon-type", "icon-value")
    view_1 = MockView(name="Test 1", endpoint="test1")
    view_2 = MockView(name="Test 2", endpoint="test2")
    view_3 = MockView(name="Test 3", endpoint="test3")

    admin.add_view(view_1, category="Category1")
    admin.add_view(view_2, category="Category2")
    admin.add_view(view_3, category="Category2")

    # print(menu._menu)
    # print(menu._menu_categories)
    # print(menu._menu_links)

    assert "Category1" in menu._menu_categories
    assert "Category2" in menu._menu_categories

    for m in menu.menus():
        if m.name == "Category1":
            menu_category1 = m
        if m.name == "Category2":
            menu_category2 = m

    assert menu_category1.get_class_name() == "class-name"
    assert menu_category1.get_icon_type() == "icon-type"
    assert menu_category1.get_icon_value() == "icon-value"
    assert len(menu_category1.get_children()) == 1
    assert menu_category1.get_children()[0].name == "Test 1"

    assert menu_category2.get_class_name() is None
    assert menu_category2.get_icon_type() is None
    assert menu_category2.get_icon_value() is None
    assert len(menu_category2.get_children()) == 2
    assert menu_category2.get_children()[0].name == "Test 2"
    assert menu_category2.get_children()[1].name == "Test 3"

    # Categories don't have URLs
    assert menu_category1.get_url() is None
    assert menu_category2.get_url() is None

    view_3.allow_access = False
    # Categories are only accessible if there is at least one accessible child
    assert menu_category2.is_accessible()
    children = menu_category2.get_children()
    assert len(children) == 1
    assert children[0].is_accessible()


def test_app_admin_default(app, client, admin):
    # print(app.blueprints)
    # print_app_endpoint_rule(app)

    assert len(app.blueprints) == 3
    assert "template" in app.blueprints
    assert "index" in app.blueprints
    assert "user" in app.blueprints

    assert admin is not None
    assert admin.name == "Admin"
    assert admin.url == "/admin"
    assert admin.endpoint == "admin"
    assert admin.app is not None

    # Check if default view was added
    assert len(admin._views) == 2
    index_view = admin._views[0]
    user_view = admin._views[1]

    # check index_view
    assert index_view is not None
    assert index_view.endpoint == "index"
    assert index_view.url == "/"
    assert index_view.index_template == "index.html"

    # check user_view
    assert user_view is not None
    assert user_view.endpoint == "user"
    assert user_view.url == "/user"
    assert user_view.index_template == "views/user/index.html"

    assert get_app_endpoint_rule(app, "index.index") == "/"
    assert get_app_endpoint_rule(app, "index.admin_index") == "/admin/"
    assert get_app_endpoint_rule(app, "user.index") == "/user/"
    assert get_app_endpoint_rule(app, "user.login") == "/user/login/"
    assert get_app_endpoint_rule(app, "user.logout") == "/user/logout/"
    assert get_app_endpoint_rule(app, "user.register") == "/user/register/"

    with app.test_request_context():
        index_index_url = url_for("index.index")
        admin_index_url = url_for("index.admin_index")
        user_index_url = url_for("user.index")
        user_login_url = url_for("user.login")
        user_logout_url = url_for("user.logout")
        user_register_url = url_for("user.register")

    assert index_index_url == "/"
    assert admin_index_url == "/admin/"
    assert user_index_url == "/user/"
    assert user_login_url == "/user/login/"
    assert user_logout_url == "/user/logout/"
    assert user_register_url == "/user/register/"

    rv = client.get(index_index_url)
    assert rv.status_code == 200
    rv = client.get(admin_index_url)
    assert rv.status_code == 200
    rv = client.get(user_index_url)
    assert rv.status_code == 302
    rv = client.get(user_login_url)
    assert rv.status_code == 200
    rv = client.get(user_register_url)
    assert rv.status_code == 200
    rv = client.get(user_logout_url)
    assert rv.status_code == 302


def test_app_admin_add_view(app, client, admin: Admin):
    mock_view = MockView()
    admin.add_view(mock_view)
    
    # print(app.blueprints)
    # print_app_endpoint_rule(app)
    assert len(app.blueprints) == 4
    assert "mockview" in app.blueprints
    assert len(admin._views) == 3

    with app.test_request_context():
        mock_index_url = url_for("mockview.index")
        mock_test_url = url_for("mockview.test")

    assert mock_index_url == "/admin/mockview/"
    assert mock_test_url == "/admin/mockview/test/"

    rv = client.get(mock_index_url)
    assert rv.status_code == 200
    rv = client.get(mock_test_url)
    assert rv.status_code == 200


def test_admin_raise_same_admin(manager):
    admin = Admin()
    with pytest.raises(Exception):
        manager.add_admin(admin)


def test_multiple_admins(app, client, manager):
    class FirstView(BaseView):
        @expose("/")
        def index(self):
            return "first"

    class SecondView(BaseView):
        @expose("/")
        def index(self):
            return "second"

    admin1 = Admin(app, name="Admin1", url="/admin1", endpoint="admin1")
    admin1.add_view(FirstView())
    manager.add_admin(admin1)

    # Create second administrative interface under /admin2
    admin2 = Admin(app, name="Admin2", url="/admin2", endpoint="admin2")
    admin2.add_view(SecondView())
    manager.add_admin(admin2)

    assert len(manager.admins) == 3

    assert admin1.name == "Admin1"
    assert admin1.url == "/admin1"
    assert admin1.endpoint == "admin1"
    assert len(admin1._views) == 1

    assert admin2.name == "Admin2"
    assert admin2.url == "/admin2"
    assert admin2.endpoint == "admin2"
    assert len(admin2._views) == 1

    # print(app.blueprints)
    # print_app_endpoint_rule(app)
    assert len(app.blueprints) == 5
    assert "firstview" in app.blueprints
    assert "secondview" in app.blueprints
    assert len(admin1._views) == 1
    assert len(admin2._views) == 1

    with app.test_request_context():
        first_index_url = url_for("firstview.index")
        second_index_url = url_for("secondview.index")

    assert first_index_url == "/admin1/firstview/"
    assert second_index_url == "/admin2/secondview/"

    rv = client.get(first_index_url)
    assert rv.status_code == 200
    assert rv.text == "first"
    rv = client.get(second_index_url)
    assert rv.status_code == 200
    assert rv.text == "second"


def test_permissions(client, admin):
    view = MockView()
    admin.add_view(view)

    rv = client.get("/admin/")
    assert rv.status_code == 200

    rv = client.get("/admin/mockview/")
    assert rv.data == b"Success!"

    rv = client.get("/admin/mockview/test/")
    assert rv.data == b"Success!"

    # Check authentication failure
    view.allow_access = False
    rv = client.get("/admin/mockview/")
    assert rv.status_code == 403


def test_inaccessible_callback(client, admin):
    view = MockView()
    admin.add_view(view)
    view.allow_access = False
    view.inaccessible_callback = lambda *args, **kwargs: abort(418)
    rv = client.get("/admin/mockview/")
    assert rv.status_code == 418


def test_menu_links(client, admin):
    menu = admin.menu
    menu.add_link(MenuLink("TestMenuLink1", endpoint=".index"))
    menu.add_link(MenuLink("TestMenuLink2", url="http://python.org/"))
    rv = client.get("/admin/")
    data = rv.get_data(as_text=True)
    # print(data)
    assert "TestMenuLink1" in data
    assert "TestMenuLink2" in data
