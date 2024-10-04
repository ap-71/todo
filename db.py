from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///tasks.db")
Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    with Session() as session:
        yield session