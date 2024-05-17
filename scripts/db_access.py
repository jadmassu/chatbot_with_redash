import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
import csv
import re


def connect_to_database(connection_params: dict):
    """
    Connects to the PostgreSQL database.
    paramters:
        connection_params is a dictionary that define the following:
        {
            'dbname': 'your_database_name',
            'user': 'your_username',
            'password': 'your_password',
            'host': 'your_host',
            'port': 'your_port'
            }
    """
    try:
        connection = psycopg2.connect(**connection_params)
        print("CONNECTED")

        return connection
    except psycopg2.Error as e:
        print(f"Error: Unable to connect to the database. {e}")
        return None


def create_database(connection_params: dict, database_name: str):
    """
        connection_params = {
        'dbname': 'your_database_name',
        'user': 'your_username',
        'password': 'your_password',
        'host': 'your_host',
        'port': 'your_port'
    }
    """
    try:
        # Connect to the default 'postgres' database
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Create a new database
        cursor.execute(f"CREATE DATABASE {database_name}")

        # Commit the changes and close the connection
        connection.commit()
        connection.close()

        print(f"Database '{database_name}' created successfully.")
    except psycopg2.Error as e:
        print(f"Error: Unable to create the database. {e}")


# def create_table(connection_params: dict, database_name: str, table_name: str, table_schema: str):
#     """
#     database_name = 'your_database'
#     table_name = 'new_table'
#     table_schema = '''
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255),
#     age INT,
#     email VARCHAR(255)
#     """
#     try:
#         # Connect to the specified database
#         connection_params['dbname'] = database_name
#         connection = psycopg2.connect(**connection_params)
#         cursor = connection.cursor()

#         # Create the table using the provided schema
#         cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({table_schema})")

#         # Commit the changes and close the connection
#         connection.commit()
#         connection.close()

#         print(f"Table '{table_name}' created successfully.")
#     except psycopg2.Error as e:
#         print(f"Error: Unable to create the table. {e}")


def traverse_directory(connection, directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            folder_name = (
                re.sub(r"\([^)]*\)", "", os.path.basename(root))
                .replace(" ", "")
                .replace("_", "")
                .replace("-", "_")
                .lower()
            )
            table_name = (
                folder_name
                + "_"
                + re.sub(r"\([^)]*\)", "", file.split(".")[0])
                .replace(" ", "")
                .replace("_", "")
                .replace("-", "_")
                .lower()
            )
            headers = [
                re.sub(r"\([^)]*\)", "", header)
                .replace(" ", "")
                .replace("_", "")
                .replace("-", "_")
                .lower()
                for header in get_csv_headers(file_path)
            ]
            try:
                # print (headers)
                # print (table_name)
                # print (folder_name)
                create_table(connection, table_name, headers)
                insert_data(connection, table_name, file_path)
            except Exception as e:
                print(f"An error occurred while processing {file_path}: {e}")


def get_csv_headers(csv_file_path):
    with open(csv_file_path, "r") as file:
        reader = csv.reader(file)
        headers = next(reader)
    return headers


def create_table(connection_params, table_name, headers):
    connection = psycopg2.connect(**connection_params)

    cursor = connection.cursor()
    columns = ", ".join([f"{header} TEXT" for header in headers])
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"

    try:
        cursor.execute(create_table_sql)
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"An error occurred while creating table {table_name}: {e}")


def insert_data(connection_params, table_name, csv_file_path):
    connection = psycopg2.connect(**connection_params)

    cursor = connection.cursor()
    with open(csv_file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if needed
        for row in reader:
            insert_sql = (
                f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(row))})"
            )
            try:
                cursor.execute(insert_sql, tuple(row))
            except Exception as e:
                print(f"An error occurred while inserting data into {table_name}: {e}")
    connection.commit()


# Connect to the database


def read_table_to_dataframe(table_name, connection_params):
    """
    Reads a PostgreSQL table into a pandas dataframe.
    """
    connection = connect_to_database(connection_params)
    if connection:
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, connection)
        connection.close()
        return df
    else:
        print("Error, no connection detected!")
        return None


def write_dataframe_to_table(df, table_name, connection_params):
    """
    Writes a pandas dataframe to a new table in the PostgreSQL database.
    """
    engine = create_engine(
        f"postgresql://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['dbname']}"
    )
    df.to_sql(table_name, engine, index=False, if_exists="replace")
    print(f"Dataframe successfully written to the '{table_name}' table.")


def update_table_by_appending(df, table_name, connection_params):
    """
    Appends a pandas dataframe to an existing PostgreSQL table.
    """
    engine = create_engine(
        f"postgresql://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['dbname']}"
    )
    df.to_sql(table_name, engine, index=False, if_exists="append")
    print(f"Dataframe successfully appended to the '{table_name}' table.")


def delete_table(table_name, connection_params):
    """
    Deletes a table from the PostgreSQL database.
    """
    connection = connect_to_database(connection_params)
    if connection:
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        connection.commit()
        connection.close()
        print(f"Table '{table_name}' successfully deleted.")
    else:
        print("Error: Unable to connect to the database.")
