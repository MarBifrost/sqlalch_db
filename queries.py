from sqlalchemy import desc, func
from db_objects import Books, Authors
from sqlalchemy.orm import sessionmaker
from connections import engine

Session = sessionmaker(bind=engine)
session = Session()


def get_book_with_most_pages():
    book = session.query(Books).order_by(desc(Books.pages)).first()
    return book


def average_pages():
    avg_number_of_pages = session.query(
        func.round(func.avg(Books.pages), 0)).scalar()
    return avg_number_of_pages


def youngest_author():
    youth = session.query(Authors).order_by(
        desc(Authors.date_of_birth)).first()
    return youth


def author_with_no_book():
    no_book = (session.query(Authors)
               .outerjoin(Books, Books.author_id == Authors.id)
               .filter(Books.author_id is None).limit(20)
               .all())
    return no_book


def author_with_3more_books():
    more_books = (session.query(Authors)
                  .join(Books, Books.author_id == Authors.id)
                  .group_by(Authors.id)
                  .having(func.count(Books.id) > 3)
                  .limit(20)
                  .all())
    return more_books
