# This script defines all functions/classes concernign connection to the 
# PostgreSQL client PgAdmin4.

# Group: Sara Bonati - Elica Tokmakchieva - Tobias Sandmann
#---------------------------------------------------------------------------

# general utility import
import numpy as np
import pandas as pd
import os
import psycopg2


# preliminary code (from https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries)

class DB():
    def __init__(self,auth):
        """
        This function initializes a DB (databse) object, specifically
        to handle connection to PostgreSQL server.
        
        Inputs:
        - auth: 
        Outputs:
        - None

        """

        #Connect to an existing database
        self.conn = psycopg2.connect("dbname=test user=postgres")
        # Open a cursor to perform database operations
        self.cur = self.conn.cursor()

    def convert_query_to_sql(self,q):
        """
        This function converts a Python string/object data type in 
        appropriate
        
        Inputs:
        - q: 
        Outputs:
        - None
        """
        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no more SQL injections!)
        self.cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))

        # Query the database and obtain data as Python objects
        self.cur.execute("SELECT * FROM test;")
        self.cur.fetchone()
    
    def close_connection(self):
        """
        This function terminates connection to DB

        Inputs:

        Outputs:
        """
        # Close communication with the database
        self.cur.close()
        self.conn.close()
        print("Database connection closed!")

# Execute a command: this creates a new table
#cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
# Make the changes to the database persistent
#conn.commit()

