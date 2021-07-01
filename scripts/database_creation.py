#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT as autocommit


def db_exists(cursor, db_name):
    """
    Test if a database named :db_name: already exists

    :cursor:  cursor of connected DBMS
    :db_name: name of the database
    :returns: 1 or None
    """

    cursor.execute(f"""
            SELECT 1
            FROM pg_catalog.pg_database
            WHERE datname = '{db_name}'
    """)
    return cursor.fetchone()


def create_db(db_name, user, password):
    """
    Create new PostgreSQL database

    :db_name: name of the database
    :returns: nothing
    """
    connection = None
    try:
        # Connect to PostgreSQL server
        connection = psycopg2.connect(
                dbname="postgres",
                user=user,
                password=password,
                host="localhost",
                port="5432")

        connection.set_isolation_level(autocommit)

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        print("\nPostgreSQL server information:\n")
        print(f"{connection.get_dsn_parameters()}\n")

        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print(f"You are connected to - {record[0]}\n")

        if not db_exists(cursor, db_name):
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database {db_name} created successfully.")
        else:
            print(f"Database {db_name} already exists.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    create_db("dbs_project", "postgres", "postgres")
