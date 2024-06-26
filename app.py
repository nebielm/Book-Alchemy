from flask import Flask
from data_models import db, Author, Book
import os

app = Flask(__name__)

# Absolute path to the current directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Ensure the 'data' directory exists
data_dir = os.path.join(basedir, 'data')
if not os.path.exists(data_dir):
    print(f"Creating directory: {data_dir}")
    os.makedirs(data_dir)
else:
    print(f"Directory already exists: {data_dir}")

# Absolute path to the database file
database_path = os.path.join(data_dir, 'library.sqlite')
print(f"Database path: {database_path}")

# Check if the database file is accessible
if os.path.exists(database_path):
    print(f"Database file already exists: {database_path}")
else:
    print(f"Database file does not exist and will be created: {database_path}")

# Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")

if __name__ == "__main__":
    app.run(debug=True)
