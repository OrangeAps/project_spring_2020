from sqlalchemy import Column, String, Integer
from data.db_session import SqlAlchemyBase


class Job(SqlAlchemyBase):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    wage = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Работа> id {self.id} название {self.id} з\п {self.wage}'