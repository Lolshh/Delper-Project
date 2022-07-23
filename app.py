from tempfile import mkdtemp

from flask import Flask

from views import views

app = Flask(__name__)

app.register_blueprint(views, url_prefix="/")

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
