from abc import ABC, abstractmethod
from utils import database_utils


class BaseDBModel(ABC):
    """ Database functions for objects """
    def insert(self, attribute_list):
        """ inserts object into MYSQL db """
        table_name = str(type(locals()['self'])).split('.')[-1].split("'")[0].upper() + 'S'  # Adi's special code
        attribute_map = {}
        for attribute in attribute_list:
            attribute_map[attribute] = getattr(locals()['self'], attribute)
        amount_of_params = ", ".join((('%s, ') * len(attribute_map.values())).split(',')[:-1])
        sql_query = f"INSERT INTO {table_name} VALUES ("
        for value in attribute_map.values():
            if type(value) is not int:
                sql_query += f"'{str(value)}'" + ", "
            else:
                sql_query += str(value) + ", "
        sql_query = ", ".join(sql_query.split(', ')[:-1]) + ')'
        print(sql_query)
        database_utils.exec(sql_query)

    def retrieve(self, ctx):
        """ retrieve(s) object(s) from MYSQL db """
        pass

    def update(self, ctx):
        """ updates object onto MYSQL db object """
        pass

    def delete(self, ctx):
        """ deletes object into MYSQL db """
        pass
