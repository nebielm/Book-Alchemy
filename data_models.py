from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(String)
    date_of_death = Column(String)
    books = db.relationship('Book', backref ='author')

    def __repr__(self):
        return f"Author(id = {self.id}, name = {self.name})"

    def __str__(self):
        return f" ID = {self.id}, Name = {self.name}, Birth date = {self.birth_date}, Death date = {self.date_of_death}"


class Book(db.Model):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String)
    title = Column(String)
    publication_year = Column(String)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __repr__(self):
        return f"Book(id = {self.id}, title = {self.title}, author_id = {self.author_id})"

    def __str__(self):
        return f" ID = {self.id}, ISBN = {self.isbn}, title = {self.title}, Publication Year = {self.publication_year}"
