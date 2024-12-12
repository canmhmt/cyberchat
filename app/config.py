import psycopg2

def db_connection():
    connection = psycopg2.connect(
        dbname = "socketchat",
        user = "postgres",
        password = "8246",
        host = "localhost",
        port = "5432"
    )

    return connection
