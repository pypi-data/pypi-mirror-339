from flask import current_app


class TestBase:
    def test_default(self, app):
        with app.test_request_context():
            theme = current_app.extensions["template"]
            # print(theme)
            assert theme.bootstrap.version == 4
            css = theme.load_css()
            # print(css)
            assert "bootstrap.min.css" in css
            js = theme.load_js()
            # print(js)
            assert "jquery.min.js" in js
            assert "bootstrap.bundle.min.js" in js
