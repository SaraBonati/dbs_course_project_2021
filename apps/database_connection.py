# This script defines all functions/classes concernign connection to the
# PostgreSQL client PgAdmin4.

# Group: Sara Bonati - Elica Tokmakchieva - Tobias Sandmann
# ----------------------------------------------------------------------

# general utility import
import numpy as np
import pandas as pd
import os
import json
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

# define database class to handle connections and queries
class DB():
    def __init__(self,dname):
        """
        This function initializes a DB (database) object, specifically
        to handle connection to PostgreSQL server.

        Inputs:
        - None
        Outputs:
        - None

        """
        try:
            # Connect to an existing database
            self.conn = psycopg2.connect(
                    dbname=dname,
                    user="postgres",
                    password="assign9",
                    host="localhost",
                    port="5432"
            )

            # Open a cursor to perform database operations
            self.cur = self.conn.cursor()
            print("Connected to database "+dname)

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def convert_query_to_sql(self, q):
        """
        This function converts a Python string/object data type in
        appropriate

        Inputs:
        - q: query in string format
        Outputs:
        - None
        """

        # Query the database and obtain data as pandas dataframe (simpler for
        # our purposes)
        res = pd.read_sql_query(q, self.conn)
        return res

    def close_connection(self):
        """
        This function terminates connection to DB in PgAdmin4

        Inputs:
        - None
        Outputs:
        - None
        """
        if self.conn:
            # Close communication with the database
            self.cur.close()
            self.conn.close()
            print("Database connection closed!")
