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
    def __init__(self, ddir):
        """
        This function initializes a DB (database) object, specifically
        to handle connection to PostgreSQL server.

        Inputs:
        - ddir (string): path to data files
        Outputs:
        - None

        """
        # Location of data files
        self.ddir = ddir
        # Connect to an existing database
        self.conn = psycopg2.connect(
                dbname="db_project_2021",
                user="root",
                password="root",
                host="localhost",
                port="5432"
        )

        # Open a cursor to perform database operations
        self.cur = self.conn.cursor()

    def create_tables(self):
        """
        This function creates tables in the "final_project" PostgreSQL database
        according to the specificed ER model and relational model. After
        creation, the tables are populated with data from the final "cleaned"
        csv files, using the INSERT SQL command.  Changes are committed to
        PgAdmin4, so that newly created tables can be seen also in there.

        Inputs:
        - data_files (string): path to data files
        - sql_queries ()
        Outputs:
        - None

        """

        try:
            # create table
            self.cur.execute("""
                   CREATE TABLE co2(
                       date DATE PRIMARY KEY,
                       low INTEGER NOT NULL,
                       high INTEGER NOT NULL,
                       endday INTEGER NOT NULL,
                       volume INTEGER NOT NULL
                   );
            """)

            print("Tables created!")

        except Exception as e:
            print("An error has occured in creating data tables, see: ", e)
            print("Exception TYPE:", type(e))

        co2_csv = os.path.join(self.ddir, 'final', 'co2_final.csv')

        # Copy from the csv file into the 'assignment' table
        with open(co2_csv, 'r') as f:
            next(f)  # Skip header row
            self.cur.copy_from(f, 'co2', sep=',')

        self.conn.commit()

    def convert_query_to_sql(self, q):
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
        number = 100
        text = 'foo'
        self.cur.execute(f"""
                INSERT INTO test (num, data) VALUES ({number}, {text})")
        """)

        # define queries of interest (e.g. ....)
        self.query_fig1 = f"""
                          SELECT *
                          FROM test
                          WHERE name = '{text}'
                          """

        # Query the database and obtain data as pandas dataframe (simpler for
        # our purposes)
        res = pd.read_sql_query(self.query_fig1, self.conn)

    def close_connection(self):
        """
        This function terminates connection to DB in PgAdmin4

        Inputs:
        - None
        Outputs:
        - None
        """
        # Close communication with the database
        self.cur.close()
        self.conn.close()
        print("Database connection closed!")
