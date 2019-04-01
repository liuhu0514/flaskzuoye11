from sqlalchemy import create_engine
engin = create_engine('mysql+mysqlconnector://root:123456@localhost/flaskdb',
                                    encoding='utf8', echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(bind=engin)
from sqlalchemy import Column, Integer, String, ForeignKey


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    pname = Column(String(50), nullable=False)
    pdetails = Column(String(10000))
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engin)


