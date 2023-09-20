import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse


def get_database_connection():
    url = urlparse("mysql://root:root@127.0.0.1:8889/Weather?serverVersion=5.7")
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port
    database = url.path[1:]

    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        return connection

    except Error as e:
        print("Error while connecting to MySQL", e)
        return None
