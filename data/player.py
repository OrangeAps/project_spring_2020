from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from data.db_session import SqlAlchemyBase, dt


class Player(SqlAlchemyBase):
    __tablename__ = 'players'
    vk_id = Column(Integer, primary_key=True, index=True, autoincrement=False, nullable=False)
    name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    money = Column(Integer, default=0, nullable=False)
    job = Column(Integer, ForeignKey('jobs.id'), default=1, nullable=True)
    home_id = Column(Integer, ForeignKey('homes.id'), default=1, nullable=True)
    car_id = Column(Integer, ForeignKey('cars.id'), default=1, nullable=True)
    animal_id = Column(Integer, ForeignKey('animals.id'), default=1, nullable=True)
    created_date = Column(DateTime, default=dt.now, nullable=False)

    def __repr__(self):
        return f'<Player> id={self.vk_id} name={self.name} last_name={self.last_name} cash={self.money} job={self.job} home={self.home_id} car={self.car_id} animal={self.animal_id}'