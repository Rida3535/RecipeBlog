from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def init_app(app):
    db.init_app(app)  # Initialize SQLAlchemy with the Flask app
