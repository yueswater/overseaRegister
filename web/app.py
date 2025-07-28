from flask import Flask

from routes.api_routes import api_bp
from routes.auth_routes import auth_bp
from routes.registered_list import registered_list_bp
from routes.student_list import student_list_bp
from routes.student_routes import student_bp

app = Flask(__name__)
app.secret_key = "super-secret-key"

app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)
app.register_blueprint(student_bp)
app.register_blueprint(student_list_bp)
app.register_blueprint(registered_list_bp)


@app.route("/ping")
def ping():
    return "pong", 200

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
