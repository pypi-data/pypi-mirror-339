# simple.py

from flask import Flask
from flask_exts import Manager

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"
# Manager init
manager = Manager()
manager.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
