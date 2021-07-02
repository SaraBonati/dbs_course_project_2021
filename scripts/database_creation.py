#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2


def db_exists(cursor, db_name):
    """Test if database :db_name: exists

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


def create_db(db_name, parameters):
    """Create new PostgreSQL database

    :db_name: name of the database
    :returns: nothing
    """
    connection = None
    try:
        # Connect to PostgreSQL server
        connection = psycopg2.connect(**parameters)
        connection.autocommit = True

        # Create cursor to perform database operations
        cursor = connection.cursor()

        print("\nPostgreSQL server information:\n")
        print(f"{connection.get_dsn_parameters()}\n")

        # Print information about connected db
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print(f"You are connected to - {record[0]}.\n")

        # Create new database if non-existing
        if not db_exists(cursor, db_name):
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database {db_name} created successfully.")
        else:
            print(f"Database {db_name} already exists.")

    except (psycopg2.DatabaseError) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Disconnected from PostgreSQL.")


if __name__ == "__main__":
    params_dict = {
        "database": "postgres",
        "host": "localhost",
        "port": "5432",
        "user": "postgres",
        "password": "postgres"
    }

    create_db("dbs_project", params_dict)
