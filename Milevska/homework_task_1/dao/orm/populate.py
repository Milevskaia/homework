
from dao.orm.model import *
from dao.db import OracleDb

db = OracleDb()

Base.metadata.create_all(db.sqlalchemy_engine)


session = db.sqlalchemy_session

session.query(ormCarOwner).delete()
session.query(ormCar).delete()
session.query(ormOwner).delete()

John = ormOwner(
    owner_phone='80991122211',
    owner_birthday='10-OCT-2001'
)

Johny = ormOwner(
    owner_phone='80960011211',
    owner_birthday='11-OCT-2001'
)

Jonathan = ormOwner(
    owner_phone='80960011211',
    owner_birthday='11-OCT-2000'
)

Toyota = ormCar(
    car_number='123ABC',
    car_model=11,
)

Audi = ormCar(
    car_number='ABC123',
    car_model=22,
)

Deo = ormCar(
    car_number='QWERTY123',
    car_model=14
)

John.orm_cars.append(Toyota)
John.orm_cars.append(Audi)

Johny.orm_cars.append(Deo)

Jonathan.orm_cars.append(Deo)

Jonathan.orm_cars.append(Toyota)


session.add_all([Toyota, Audi, Deo, John, Johny, Jonathan, ])

session.commit()

