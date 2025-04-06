from neo4j import GraphDatabase

"""
    Класс содержащий логику работы с бд neo4j
"""


class Neo4jConnection:

    # TODO move settings to some file or class
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", pwd="123456789"):

        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None

        try:
            self.__driver = GraphDatabase.driver(uri, auth=(user, pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):

        if self.__driver is not None:
            self.__driver.close()

    # TODO: need to add decorator for run and execute_write
    def run(self, query, parameters=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None

        try:
            session = self.__driver.session()
            result = session.run(query, parameters)
            print(list(result))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()

    def execute_query(self, query, needLog=False):
        assert self.__driver is not None, "Driver not initialized!"
        session = None

        try:
            result = self.__driver.execute_query(query)
            if needLog: print(list(result))
            return result
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()

    def read_all(self, query):
        assert self.__driver is not None, "Driver not initialized!"
        session = None

        try:
            session = self.__driver.session()
            result = session.execute_read(get_node, query)
            return result
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()

    def execute_write(self, transaction_function, *args):
        assert self.__driver is not None, "Driver not initialized!"
        session = None

        try:
            session = self.__driver.session()
            session.execute_write(transaction_function, *args)
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()


def get_node(tx, query, bounds=None):
    results = tx.run(query, parameters=bounds).to_df()
    return results
