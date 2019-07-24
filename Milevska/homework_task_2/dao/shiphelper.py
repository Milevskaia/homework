import cx_Oracle
from dao.db import OracleDb


class ShipHelper:

    def __init__(self):
        self.db = OracleDb()

    def getShip(self, ship_id):

        query = "select * from ship where ship.ship_id = {}".format(ship_id)

        result = self.db.execute(query)
        return result.fetchall()

    def updateShip(self, ship_id, ship_number, ship_date, ship_name, ship_address):
        query = "update ship set ship_number={ship_number}, ship_date={ship_date}, ship_name={ship_name}, ship_address={ship_address} where ship_id={ship_id}".format(
            ship_number=ship_number,
            ship_date=ship_date,
            ship_name=ship_name,
            ship_address=ship_address,
            ship_id=ship_id
        )
        self.db.execute(query)
