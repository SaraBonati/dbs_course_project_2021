# This script defines all functions/classes concernign connection to the 
# PostgreSQL client PgAdmin4.

# Group: Sara Bonati - Elica Tokmakchieva - Tobias Sandmann
#---------------------------------------------------------------------------

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
    def __init__(self,ddir):
        """
        This function initializes a DB (database) object, specifically
        to handle connection to PostgreSQL server.
        
        Inputs:
        - ddir (string): path to data files
        Outputs:
        - None

        """
        #location of data files
        self.ddir= ddir
        #Connect to an existing database
        self.conn = psycopg2.connect("dbname=test user=postgres password=assign9 port=5432")
        # Open a cursor to perform database operations
        self.cur = self.conn.cursor()

    def create_tables(self):
        """
        This function creates tables in the "final_project" PostgreSQL database according to
        the specificed ER model and relational model. After creation, the tables are populated
        with data from the final "cleaned" csv files, using the INSERT SQL command.
        Changes are committed to PgAdmin4, so that newly created tables can be seen also in there.
        
        Inputs:
        - data_files (string): path to data files
        - sql_queries ()
        Outputs:
        - None

        """
        self.co2_table = pd.read_csv(os.path.join(self.ddir,'final','co2_final.csv'))
        self.gdp_table = pd.read_csv(os.path.join(self.ddir,'final','gdp_final.csv'))

        try:
            # create table 
            self.cur.execute("""
                            CREATE TABLE assignment (
                            date INTEGER PRIMARY KEY,
                            low INTEGER NOT NULL,
                            high INTEGER NOT NULL,
                            endday INTEGER NOT NULL,
                            volume INTEGER NOT NULL
                            )
                            """)

            print("Tables created!")
        
        except Exception as error:
            print("An error has occured in creating data tables, see: ",error)
            print ("Exception TYPE:", type(error))
        
        
        try:
            # fill table with data from csv file
            for i in range(len(self.co2_table)):
                self.cur.execute("INSERT INTO assignment (date,low,high,endday,volume) VALUES (%s, %s, %s, %s, %s)",(self.co2_table.loc[i,'Datum'],
                                                                                                                     self.co2_table.loc[i,' Tief'],
                                                                                                                     self.co2_table.loc[i,' Hoch'],
                                                                                                                     self.co2_table.loc[i,' Tagesendwert'],
                                                                                                                     self.co2_table.loc[i,' Handelsvolumen']))

            
            print("Tables filled with data!")
        
        except Exception as error:
            print("An error has occured in filling data tables, see: ",error)
            print ("Exception TYPE:", type(error))
        
        # commit changes to pgadmin4 (so that you can see newly created table there)
        self.conn.commit()



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
        
        # define queries of interest (e.g. ....)
        self.query_fig1 = "SELECT * FROM test"

        # Query the database and obtain data as pandas dataframe (simpler for our purposes)
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


