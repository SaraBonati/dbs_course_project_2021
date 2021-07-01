#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT as autocommit


def populate_tables(dbname, user, password):
    """
    Populate PostgreSQL tables with data from CSV files
    """
    try:

# from here
        connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host="localhost",
                port="5432")

        print(f"\nConnected with database {dbname}")
        cursor = connection.cursor()

        with open('../data/final/COUNTRY.csv', 'r') as csv:
            cursor.copy_expert(
                    "COPY country \
                     FROM STDIN WITH HEADER CSV",
                    csv)
            print("Table country populated.")
# to here

        print("All done!")
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    populate_tables("dbs_project", "postgres", "postgres")
