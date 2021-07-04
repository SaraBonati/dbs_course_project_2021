# DBS_project_2021

Gitlab repository for the Project assignment of the Database Systems course SS2021

## Requirements
We use __PostgreSQL__ (and PgAdmin4) as DBMS.

For Python modules see the file `requirements.txt`

## How to get started
A *backup.tar* file is available in `data\dump`: with this file the database used for the project can be restored in PgAdmin4.
Note that in the file `apps\database_connection.py` the user credentials to connect to the database (username and password) need 
to be changed to the local user's username and password in order for the application to connect successfully to the database.

After cloning the repository and navigating to the repository directory the app can be launched in terminal by typing

```
streamlit run main_app.py
```