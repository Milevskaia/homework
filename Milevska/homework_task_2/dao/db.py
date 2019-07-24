import cx_Oracle
from dao.credentials import *

class OracleDb(object):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            try:
                connection = cx_Oracle.connect(username, password, databaseName)
                cursor = connection.cursor()

                cursor.execute('SELECT * FROM v$version')
                db_version = cursor.fetchone()

                print("New connection to {} created".format(db_version[0]))

                OracleDb._instance.connection = connection
                OracleDb._instance.cursor = cursor

            except Exception as error:
                print('Error: connection not established {}'.format(error))

        else:
            print('Connection already established')

        return cls._instance

    def __init__(self):
        self.connection = self._instance.connection
        self.cursor = self._instance.cursor

    def execute(self, query):
        try:
            result = self.cursor.execute(query)
        except Exception as error:
            print('error execting query "{}", error: {}'.format(query, error))
            return None
        else:
            return result

    def __del__(self):
        self.cursor.close()
        self.connection.close()


if __name__=="__main__":
    db = OracleDb()