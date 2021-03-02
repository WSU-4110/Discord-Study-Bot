from abc import ABC, abstractmethod
from utils import database_utils


class BaseDBModel(ABC):
    """ Database functions for objects """

    def insert(self, attribute_list):
        """ inserts object into MYSQL db given a list of attributes"""
        table_name = self.get_table_name()
        attribute_map = {}

        #  grabs values from local object given the variable names
        for attribute in attribute_list:
            attribute_map[attribute] = getattr(locals()['self'], attribute)

        #  determine the number of parameters that need to be passed into the parameterized query
        amount_of_params = ", ".join((('%s, ') * len(attribute_map.values())).split(',')[:-1])

        #  generates parameterized INSERT query depending on the local object and variable names in attribute_list
        sql_query = f"INSERT INTO {table_name} VALUES ("
        for value in attribute_map.values():
            if type(value) is not int:
                sql_query += f"'{str(value)}'" + ", "
            else:
                sql_query += str(value) + ", "
        sql_query = ", ".join(sql_query.split(', ')[:-1]) + ')'

        return database_utils.exec(sql_query, table_name)

    def retrieve(self, message_id):
        """ retrieve(s) object(s) from MYSQL db using a message_id """
        table_name = self.get_table_name()
        sql_query = f"SELECT FROM {table_name} WHERE message_id = {message_id}"
        return database_utils.exec(sql_query)

    def update(self, attribute_list, message_id):
        """ updates object into MYSQL db object given a message_id,
        however, 'message_id', 'userid', and 'channel_id' attributes cannot be changed. """
        table_name = self.get_table_name()
        pairing = {}
        column_names = self.query_column_names()

        [column_names.remove(ele) for ele in ['message_id', 'user_id', 'channel_id']]

        #  grabs values from local object given the variable names
        for i, attribute in enumerate(attribute_list):
            pairing[column_names[i]] = getattr(locals()['self'], attribute)

        #  determine the number of parameters that need to be passed into the parameterized query
        amount_of_params = ", ".join((('%s, ') * len(pairing.values())).split(',')[:-1])

        #  generates parameterized UPDATE query depending on the local object and variable names in attribute_list
        sql_query = f"UPDATE {table_name} SET "
        for key, value in pairing.items():
            if type(value) is not int:
                sql_query += f"{key} = '{str(value)}'" + ", "
            else:
                sql_query += f"{key} = {str(value)}" + ", "
        sql_query = ", ".join(sql_query.split(', ')[:-1])
        sql_query += f" WHERE message_id = {message_id}"

        return database_utils.exec(sql_query, table_name)

    def delete(self, message_id):
        """ deletes object into MYSQL db given a message_id """
        table_name = self.get_table_name()
        sql_query = f"DELETE FROM {table_name} WHERE message_id = {message_id}"
        return database_utils.exec(sql_query, table_name)

    def query_column_names(self):
        """ describe a table and get all of the column names """
        table_name = self.get_table_name()
        pairs = database_utils.exec(f"DESCRIBE {table_name}")
        return [item[0] for item in pairs]

    def get_table_name(self):
        """ returns the table name using local objects class type """
        return str(type(locals()['self'])).split('.')[-1].split("'")[0].upper() + 'S'  # Adi's special code
