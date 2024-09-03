from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from defaultapp.config import Config


@contextmanager
def session_scope():
    # SQLAlchemy usage with a different Session as Flask app, to use outside flask context calls

    some_engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    SessionEng = sessionmaker(bind=some_engine)
    session = SessionEng()
    session.expire_on_commit = False
    try:
        # this is where the "work" happens!
        yield session
        # always commit changes!
        session.commit()
    except:
        # if any kind of exception occurs, rollback transaction
        session.rollback()
        raise
    finally:
        session.close()
