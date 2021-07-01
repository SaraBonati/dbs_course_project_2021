#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT as autocommit


def create_tables(dbname, user, password):
    """
    Creates tables in the project's PostgreSQL database

    :dbname: name of the database
    """
    commands = (
            """
            CREATE TABLE country (
                name varchar(50) PRIMARY KEY,
                code varchar(3) UNIQUE NOT NULL,
                partofworld varchar(50) NOT NULL
            )
            """,
            """
            CREATE TABLE population (
                cname varchar(50) NOT NULL,
                year integer NOT NULL,
                count bigint,
                growth numeric(11,9),
                share_urban numeric(6,3),
                share_sanitation numeric(8,5),
                PRIMARY KEY (cname, year),
                FOREIGN KEY (cname)
                    REFERENCES country (name)
            )
            """,
            """
            CREATE TABLE gdp (
                cname varchar(50) NOT NULL,
                year integer NOT NULL,
                value numeric(17,2),
                PRIMARY KEY (cname, year),
                FOREIGN KEY (cname)
                    REFERENCES country (name)
            )
            """,
            """
            CREATE TABLE health (
                cname varchar(50) NOT NULL,
                year integer NOT NULL,
                life_exp numeric(6,3),
                share_gdp_health numeric(12,9),
                mental_health_daly numeric(12,9),
                mental_health_share numeric(12,9),
                PRIMARY KEY (cname, year),
                FOREIGN KEY (cname)
                    REFERENCES country (name)
            )
            """,
            """
            CREATE TABLE pollution (
                cname varchar(50) NOT NULL,
                year integer NOT NULL,
                co2 numeric(14,3),
                indoor_death_rate numeric(14,9),
                outdoor_death_rate numeric(5,2),
                PRIMARY KEY (cname, year),
                FOREIGN KEY (cname)
                    REFERENCES country (name)
            )
            """,
            """
            CREATE TABLE education (
                cname varchar(50) NOT NULL,
                year integer NOT NULL,
                share_gdp_primary numeric(14,12),
                share_gdp_secondary numeric(14,12),
                share_gdp_tertiary numeric(14,12),
                share_pop_tertiary numeric(4,2),
                primary_rate numeric(14,11),
                secondary_rate numeric(14,11),
                PRIMARY KEY (cname, year),
                FOREIGN KEY (cname)
                    REFERENCES country (name)
            )
            """,
            """
            CREATE TABLE security (
                cname varchar(50) NOT NULL,
                year integer NOT NULL,
                unemployment_rate numeric(10,8),
                avg_annual_working_hours numeric(8,4),
                homicide_rate numeric(10,7),
                hr_score numeric(9,8),
                hr_violations numeric(3,1),
                happiness numeric(10,9),
                trust numeric(8,6),
                PRIMARY KEY (cname, year),
                FOREIGN KEY (cname)
                    REFERENCES country (name)
            )
            """)

    connection = None
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

        # Create the tables one after the other
        for command in commands:
            cursor.execute(command)

        print("Tables created successfully.")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    create_tables("dbs_project", "postgres", "postgres")
