#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT as autocommit


def populate_tables(parameters):
    """
    Populate PostgreSQL tables with data from CSV files
    """
    filenames = [
            "COUNTRY",
            "POPULATION",
            "GDP",
            "HEALTH",
            "EDUCATION",
            "POLLUTION",
            "SECURITY"]

    try:
        # Connect to PostgreSQL server
        connection = psycopg2.connect(**parameters)

        print(f'\nConnected with database {parameters["database"]}')
        connection.set_isolation_level(autocommit)
        cursor = connection.cursor()

        # Populate all tables one after the other
        for filename in filenames:
            with open(f'../data/final/{filename}.csv', 'r') as f:
                cursor.copy_expert(
                        f"COPY {filename.lower()} FROM STDIN WITH HEADER CSV",
                        f)
            print(f"Table {filename.lower()} populated.")

        print("All done!")
    except (psycopg2.Error, psycopg2.DatabaseError) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Disconnected from PostgreSQL.")


if __name__ == "__main__":
    params_dict = {
        "host": "localhost",
        "port": "5432",
        "database": "dbs_project",
        "user": "postgres",
        "password": "postgres",
    }

    populate_tables(params_dict)
