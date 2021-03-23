from flask import Flask, render_template, request
from blueprints.index import index_blueprint
from blueprints.uploads import upload_blueprint
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.register_blueprint(index_blueprint)
app.register_blueprint(upload_blueprint)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
