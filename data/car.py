from sqlalchemy import Column, String, Integer
from data.db_session import SqlAlchemyBase


class Car(SqlAlchemyBase):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Автомобиль🚙> id {self.id} имя {self.name} стоимость {self.cost}₽'