from sqlalchemy import Column, String, Integer, ForeignKey
from data.db_session import SqlAlchemyBase


class Player(SqlAlchemyBase):
    __tablename__ = 'players'
    vk_id = Column(Integer, primary_key=True, index=True, autoincrement=False, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    home_id = Column(Integer, ForeignKey('homes.id'), nullable=True)
    car_id = Column(Integer, ForeignKey('cars.id'), nullable=True)
    animal_id = Column(Integer, ForeignKey('animals.id'), nullable=True)

    def __repr__(self):
        return f'<Player> id={self.vk_id} name={self.name} last_name={self.last_name} home={self.home_id} car={self.car_id} animal={self.animal_id}'