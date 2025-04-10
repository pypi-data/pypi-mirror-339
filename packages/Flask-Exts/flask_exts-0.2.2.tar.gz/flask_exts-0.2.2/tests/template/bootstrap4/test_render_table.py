from flask import render_template_string, request
from ...models import db, reset_models
from ...models.message import Message


def test_render_simple_table(app, client):
    @app.route("/table")
    def test():
        reset_models()
        for i in range(3):
            msg = Message(text=f"Test message {i+1}")
            db.session.add(msg)
        db.session.commit()
        page = request.args.get("page", 1, type=int)
        pagination = Message.query.paginate(page=page, per_page=10)
        messages = pagination.items
        titles = [("id", "#"), ("text", "Message")]
        return render_template_string(
            """
            {% from 'macro/table.html' import render_table %}
            {{ render_table(messages, titles) }}
            """,
            titles=titles,
            messages=messages,
        )

    response = client.get("/table")
    data = response.get_data(as_text=True)
    # print(data)
    assert '<table class="table">' in data
    assert '<th scope="col">#</th>' in data
    assert '<th scope="col">Message</th>' in data
    assert '<th scope="row">1</th>' in data
    assert "<td>Test message 1</td>" in data


def test_render_safe_table(app, client):
    @app.route("/table")
    def test():
        db.drop_all()
        db.create_all()
        for i in range(10):
            msg = Message(text=f"Test <em>message</em> {i+1}")
            db.session.add(msg)
        db.session.commit()
        page = request.args.get("page", 1, type=int)
        pagination = Message.query.paginate(page=page, per_page=10)
        messages = pagination.items
        titles = [("id", "#"), ("text", "Message")]
        return render_template_string(
            """
            {% from 'macro/table.html' import render_table %}
            {{ render_table(messages, titles, safe_columns=('text'), urlize_columns=('text')) }}
            """,
            titles=titles,
            messages=messages,
        )

    response = client.get("/table")
    data = response.get_data(as_text=True)
    assert '<table class="table">' in data
    assert '<th scope="col">#</th>' in data
    assert '<th scope="col">Message</th>' in data
    assert '<th scope="row">1</th>' in data
    assert "<td>Test <em>message</em> 1</td>" in data


def test_render_urlize_table(app, client):
    @app.route("/table")
    def test():
        db.drop_all()
        db.create_all()
        for i in range(10):
            msg = Message(text=f"Test https://t.me {i+1}")
            db.session.add(msg)
        db.session.commit()
        page = request.args.get("page", 1, type=int)
        pagination = Message.query.paginate(page=page, per_page=10)
        messages = pagination.items
        titles = [("id", "#"), ("text", "Message")]
        return render_template_string(
            """
            {% from 'macro/table.html' import render_table %}
            {{ render_table(messages, titles, urlize_columns=('text')) }}
            """,
            titles=titles,
            messages=messages,
        )

    response = client.get("/table")
    data = response.get_data(as_text=True)
    assert '<table class="table">' in data
    assert '<th scope="col">#</th>' in data
    assert '<th scope="col">Message</th>' in data
    assert '<th scope="row">1</th>' in data
    assert (
        '<td>Test <a href="https://t.me" rel="noopener">https://t.me</a> 1</td>' in data
    )


def test_render_customized_table(app, client):
    @app.route("/table")
    def test():
        db.drop_all()
        db.create_all()
        for i in range(10):
            msg = Message(text=f"Test message {i+1}")
            db.session.add(msg)
        db.session.commit()
        page = request.args.get("page", 1, type=int)
        pagination = Message.query.paginate(page=page, per_page=10)
        messages = pagination.items
        titles = [("id", "#"), ("text", "Message")]
        return render_template_string(
            """
            {% from 'macro/table.html' import render_table %}
            {{ render_table(messages, titles, table_classes='table-striped',
            header_classes='thead-dark', body_classes='table-group-divider',
            caption='Messages') }}
            """,
            titles=titles,
            messages=messages,
        )

    response = client.get("/table")
    data = response.get_data(as_text=True)
    assert '<table class="table table-striped">' in data
    assert '<thead class="thead-dark">' in data
    assert '<tbody class="table-group-divider">' in data
    assert "<caption>Messages</caption>" in data


def test_render_responsive_table(app, client):
    @app.route("/table")
    def test():
        db.drop_all()
        db.create_all()
        for i in range(10):
            msg = Message(text=f"Test message {i+1}")
            db.session.add(msg)
        db.session.commit()
        page = request.args.get("page", 1, type=int)
        pagination = Message.query.paginate(page=page, per_page=10)
        messages = pagination.items
        titles = [("id", "#"), ("text", "Message")]
        return render_template_string(
            """
            {% from 'macro/table.html' import render_table %}
            {{ render_table(messages, titles, responsive=True,
            responsive_class='table-responsive-sm') }}
            """,
            titles=titles,
            messages=messages,
        )

    response = client.get("/table")
    data = response.get_data(as_text=True)
    assert '<div class="table-responsive-sm">' in data


def test_build_table_titles(app, client):
    @app.route("/table")
    def test():
        db.drop_all()
        db.create_all()
        for i in range(10):
            msg = Message(text=f"Test message {i+1}")
            db.session.add(msg)
        db.session.commit()
        page = request.args.get("page", 1, type=int)
        pagination = Message.query.paginate(page=page, per_page=10)
        messages = pagination.items
        return render_template_string(
            """
            {% from 'macro/table.html' import render_table %}
            {{ render_table(messages) }}
            """,
            messages=messages,
        )

    response = client.get("/table")
    data = response.get_data(as_text=True)
    assert '<table class="table">' in data
    assert '<th scope="col">#</th>' in data
    assert '<th scope="col">Text</th>' in data
    assert '<th scope="row">1</th>' in data
    assert "<td>Test message 1</td>" in data


def test_build_table_titles_with_empty_data(app, client):
    @app.route("/table")
    def test():
        messages = []
        return render_template_string(
            """
            {% from 'macro/table.html' import render_table %}
            {{ render_table(messages) }}
            """,
            messages=messages,
        )

    response = client.get("/table")
    assert response.status_code == 200


def todo_test_render_table_with_actions(app, client):
    @app.route("/table/<string:recipient>/<int:message_id>/resend")
    def test_resend_message(recipient, message_id):
        return f"Re-sending {message_id} to {recipient}"

    @app.route("/table/<string:sender>/<int:message_id>/view")
    def test_view_message(sender, message_id):
        return f"Viewing {message_id} from {sender}"

    @app.route("/table/<string:sender>/<int:message_id>/edit")
    def test_edit_message(sender, message_id):
        return f"Editing {message_id} from {sender}"

    @app.route("/table/<string:sender>/<int:message_id>/delete")
    def test_delete_message(sender, message_id):
        return f"Deleting {message_id} from {sender}"

    @app.route("/table/new-message")
    def test_create_message():
        return "New message"

    @app.route("/table")
    def table():
        db.drop_all()
        db.create_all()
        for i in range(10):
            msg = Message(text=f"Test message {i+1}", sender="me", recipient="john_doe")
            db.session.add(msg)
        db.session.commit()
        page = request.args.get("page", 1, type=int)
        pagination = Message.query.paginate(page=page, per_page=10)
        messages = pagination.items
        titles = [("id", "#"), ("text", "Message")]
        return render_template_string(
            """
            {% from 'macro/table.html' import render_table %}
            # URL arguments with URL tuple
            {{ render_table(messages, titles, model=model, show_actions=True,
            custom_actions=[
                (
                    'Resend',
                    'bootstrap-reboot',
                    ('test_resend_message', [('recipient', ':recipient'), ('message_id', ':id')])
                )
            ],
            view_url=('test_view_message', [('sender', ':sender'), ('message_id', ':id')]),
            edit_url=('test_edit_message', [('sender', ':sender'), ('message_id', ':id')]),
            delete_url=('test_delete_message', [('sender', ':sender'), ('message_id', ':id')]),
            new_url=('test_create_message')
            ) }}
            """,
            titles=titles,
            model=Message,
            messages=messages,
        )

    @app.route("/table-with-dict-data")
    def dict_data_table():
        row_dicts = [
            {
                "id": i + 1,
                "text": f"Test message {i + 1}",
                "sender": "me",
                "recipient": "john_doe",
            }
            for i in range(10)
        ]

        messages = row_dicts
        titles = [("id", "#"), ("text", "Message")]
        return render_template_string(
            """
            {% from 'macro/table.html' import render_table %}
            # URL arguments with URL tuple
            {{ render_table(messages, titles, show_actions=True,
            custom_actions=[
                (
                    'Resend',
                    'bootstrap-reboot',
                    ('test_resend_message', [('recipient', ':recipient'), ('message_id', ':id')])
                )
            ],
            view_url=('test_view_message', [('sender', ':sender'), ('message_id', ':id')]),
            edit_url=('test_edit_message', [('sender', ':sender'), ('message_id', ':id')]),
            delete_url=('test_delete_message', [('sender', ':sender'), ('message_id', ':id')]),
            new_url=('test_create_message')
            ) }}
        """,
            titles=titles,
            messages=messages,
        )

    for url in ["/table", "/table-with-dict-data"]:
        response = client.get(url)
        data = response.get_data(as_text=True)
        assert "bootstrap-icons.svg#bootstrap-reboot" in data
        assert 'href="/table/john_doe/1/resend"' in data
        assert 'title="Resend">' in data
        assert 'href="/table/me/1/view"' in data
        assert 'action="/table/me/1/delete"' in data
        assert 'href="/table/me/1/edit"' in data
        assert 'href="/table/new-message"' in data


def test_customize_icon_title_of_table_actions(app, client):
    @app.route("/table")
    def test():
        db.drop_all()
        db.create_all()
        for i in range(10):
            msg = Message(text=f"Test message {i+1}")
            db.session.add(msg)
        db.session.commit()
        page = request.args.get("page", 1, type=int)
        pagination = Message.query.paginate(page=page, per_page=10)
        messages = pagination.items
        return render_template_string(
            """
            {% from 'macro/table.html' import render_table %}
            {{ render_table(messages, model=model, show_actions=True,
            view_url='/view',
            edit_url='/edit',
            delete_url='/delete',
            new_url='/new') }}
            """,
            model=Message,
            messages=messages,
        )

    response = client.get("/table")
    data = response.get_data(as_text=True)
    assert 'title="View">' in data
    assert 'title="Edit">' in data
    assert 'title="Remove">' in data
    assert 'title="Create">' in data
    assert "Category A" in data
