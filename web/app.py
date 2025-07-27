from flask import Flask
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.student_list import student_list_bp

app = Flask(__name__)
app.secret_key = "super-secret-key"

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(student_list_bp)


if __name__ == "__main__":
    app.run(port=10301)