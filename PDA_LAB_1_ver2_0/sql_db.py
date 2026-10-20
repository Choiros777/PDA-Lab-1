from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///vacancies.db")
Base = declarative_base()

class Vacancy(Base):
    __tablename__ = "vacancies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    employer = Column(String)
    address = Column(String)
    salary = Column(String)
    experience = Column(String)
    workinghours = Column(String)
    workingdays = Column(String)
    employmenttype = Column(String)
    workformat = Column(String)
    payfrequency = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)