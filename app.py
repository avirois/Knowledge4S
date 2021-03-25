from flask import Flask
from blueprints.index import index_blueprint
from blueprints.search import search_blueprint

app = Flask(__name__)
app.register_blueprint(index_blueprint)
app.register_blueprint(search_blueprint)
app.config["DB_NAME"] = "database.db"
app.secret_key = b"\xf5\xe4\xabr\x89\xd9#^D@0\xae[R1\xcf"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
