import psycopg2


def connections():
    connection = psycopg2.connect(
        database = "home",
        user = "postgres",
        password = "8246",
        host = "localhost",
        port = "5432"
    )

    return connection