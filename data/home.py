from sqlalchemy import Column, String, Integer, ForeignKey
from data.db_session import SqlAlchemyBase


class Home(SqlAlchemyBase):
    __tablename__ = 'homes'
    id = Column(Integer, primary_key=True, index=True, autoincrement=False, nullable=False)
    name = Column(String, nullable=False)
    

    def __repr__(self):
        return f'<Player> id={self.vk_id} name={self.name} last_name={self.last_name} home={self.home_id} car={self.car_id} animal={self.animal_id}'