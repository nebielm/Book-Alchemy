from flask import Flask, render_template, request
from data_models import db, Author, Book
import requests
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

BASE_URL = 'https://www.googleapis.com/books/v1/volumes?q=isbn:'

# Create a database connection
engine = create_engine('sqlite:///data/library.sqlite')

# Create a database session
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

# # Absolute path to the current directory
# basedir = os.path.abspath(os.path.dirname(__file__))
#
# # Ensure the 'data' directory exists
# data_dir = os.path.join(basedir, 'data')
# if not os.path.exists(data_dir):
#     print(f"Creating directory: {data_dir}")
#     os.makedirs(data_dir)
# else:
#     print(f"Directory already exists: {data_dir}")
#
# # Absolute path to the database file
# database_path = os.path.join(data_dir, 'library.sqlite')
# print(f"Database path: {database_path}")
#
# # Check if the database file is accessible
# if os.path.exists(database_path):
#     print(f"Database file already exists: {database_path}")
# else:
#     print(f"Database file does not exist and will be created: {database_path}")
#
# # Configuration for SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db.init_app(app)
#
# with app.app_context():
#     try:
#         db.create_all()
#         print("Database tables created successfully")
#     except Exception as e:
#         print(f"Error creating database tables: {e}")
#


@app.route('/add_author', methods=['POST', 'GET'])
def add_author():
    if request.method == 'GET':
        return render_template('add_author.html', message='Please enter and submit.')
    message = "Something went wrong, Try again"
    if request.method == 'POST':
        author_name = request.form.get("name")
        author_birthdate = request.form.get("birthdate")
        author_date_of_death = request.form.get("date_of_death")
        author = Author(name=author_name, birth_date=author_birthdate, date_of_death=author_date_of_death)
        session.add(author)
        session.commit()
        message = f'{author_name} successfully added to database'
    return render_template('add_author.html', message=message)


@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    if request.method == 'GET':
        authors = session.query(Author.name).all()
        return render_template('add_book.html', message='Please enter and submit.', authors=authors)
    message = "Something went wrong, Try again"
    if request.method == 'POST':
        book_title = request.form.get("title")
        book_isbn = request.form.get("isbn")
        book_publication_year = request.form.get("publication_year")
        book_author = request.form.get("author")
        author = session.query(Author).filter(Author.name == book_author).one()
        book = Book(isbn=book_isbn, title=book_title, publication_year=book_publication_year, author_id=author.id)
        session.add(book)
        session.commit()
        authors = session.query(Author.name).all()
        message = f'{book_title} successfully added to database'
    return render_template('add_book.html', message=message, authors=authors)


@app.route('/', methods=['GET'])
def home():
    x = request.args.get('sort')
    if x == "title":
        books = session.query(Book).order_by(Book.title.asc()).all()
        print(books)
    elif x == "author":
        books = session.query(Book).join(Author).order_by(Author.name.asc()).all()
    else:
        books = session.query(Book).order_by(Book.publication_year.asc()).all()
    info = {}
    for book in books:
        res = requests.get(BASE_URL + book.isbn)
        book_dict = res.json()
        cover_url = book_dict['items'][0]['volumeInfo']['imageLinks']['thumbnail']
        author = session.query(Author.name).filter(Author.id == book.author_id).one()
        info[book.title] = [author, cover_url]
    return render_template('home.html', books=books, info=info)


if __name__ == "__main__":
    app.run(debug=True)
