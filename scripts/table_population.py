#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT as autocommit


def populate_tables(dbname, user, password):
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
        connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host="localhost",
                port="5432")

        print(f"\nConnected with database {dbname}")
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
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    populate_tables("dbs_project", "postgres", "postgres")
