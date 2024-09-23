from sqlalchemy import Column, String, Integer, Date, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from sqlalchemy_utils import database_exists
from faker import Faker
from connections import *
import queries

Base = declarative_base()

association_table = Table(
    'association_table', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('author_id', Integer, ForeignKey('authors.id'))
)


class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    place_of_birth = Column(String)

    books = relationship('Books', secondary=association_table, back_populates='authors')


class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    category = Column(String)
    pages = Column(Integer)
    publishing_date = Column(Date)
    author_id = Column(Integer)

    authors = relationship('Authors', secondary=association_table, back_populates='books')


engine = create_engine('sqlite:///books_and_authors.db', echo=True)
Base.metadata.create_all(engine)


def create_tables():
    session = sessionmaker(bind=engine)
    session = session()
    fake = Faker()

    if not database_exists(engine.url):
        for _ in range(500):
            author = Authors(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_of_birth=fake.date_of_birth(minimum_age=25, maximum_age=100),
                place_of_birth=fake.city())
            session.add(author)
        session.commit()
        session.close()

        start_date = datetime(1925, 1, 1).date()
        end_date = datetime.today().date()

        for _ in range(1000):
            book = Books(title=fake.word(),
                         category=fake.word(),
                         pages=fake.random_int(min=50, max=1000),
                         publishing_date=fake.date_between(start_date=start_date, end_date=end_date),
                         author_id=fake.random_int(min=1, max=500))
            session.add(book)
        session.commit()
        session.close()


def save_results_to_file():
    with open('results.txt', 'w') as f:
        book_with_most_pages = queries.get_book_with_most_pages()
        f.write(
            f"1. The book with the most pages is: \n{book_with_most_pages.title}, with {book_with_most_pages.pages} pages\n\n")

        avg_pages = queries.average_pages()
        f.write(f"2. The average number of pages is: {avg_pages}\n\n")

        youngest_author = queries.youngest_author()
        f.write(
            f"3. The youngest author is: {youngest_author.first_name} {youngest_author.last_name}. She was born in {youngest_author.date_of_birth}\n\n")

        author_with_no_book = queries.author_with_no_book()
        f.write(f"4. Authors who hasn't a book at all:\n")
        for author in author_with_no_book:
            f.write(f"{author.first_name} {author.last_name}\n")

        f.write("\nAuthors with more than 3 books: \n")
        author_with_3more_books = queries.author_with_3more_books()
        for author in author_with_3more_books:
            f.write(f"{author.first_name} {author.last_name}\n")
        f.write("\n")


print("Results saved to results.txt")

if __name__ == '__main__':
    create_tables()
    save_results_to_file()
