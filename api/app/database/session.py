from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

from app.database.base import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session_factory = scoped_session(SessionLocal, scopefunc=lambda: "app")

Base = declarative_base()

Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    """
    Retorna uma sessão do banco de dados para uma requisição HTTP.

    Returns:
        Session: sessão do banco de dados
    """
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
