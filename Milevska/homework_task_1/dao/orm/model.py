from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class ormOwner(Base):
    __tablename__ = 'orm_owner'

    owner_phone = Column(String(11), primary_key=True)
    owner_birthday = Column(Date, nullable=False)

    orm_cars = relationship('ormCar', secondary='orm_owner_car')


class ormCar(Base):
    __tablename__ = 'orm_car'

    car_number = Column(String(10), primary_key=True)
    car_model = Column(Integer, primary_key=True)

    orm_owners = relationship('ormOwner', secondary='orm_owner_car')


class ormCarOwner(Base):
    __tablename__ = 'orm_owner_car'

    owner_phone = Column(String(11), ForeignKey('orm_owner.owner_phone'), primary_key=True)
    car_number = Column(String(10), ForeignKey('orm_car.car_number'), primary_key=True)
    car_model = Column(Integer, ForeignKey('orm_car.car_model'), primary_key=True)

