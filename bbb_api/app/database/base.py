from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "mysql://root:123456@localhost:3306/bbb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
