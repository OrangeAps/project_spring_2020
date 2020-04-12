from sqlalchemy import Column, String, Integer
from data.db_session import SqlAlchemyBase


class Animal(SqlAlchemyBase):
    __tablename__ = 'animals'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Питомец> id {self.id} имя {self.name} стоимость {self.cost}'