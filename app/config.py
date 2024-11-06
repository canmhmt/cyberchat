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

MAIL_SERVER = 'smtp.mailgun.org'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'postmaster@your_domain.mailgun.org'
MAIL_PASSWORD = 'your_mailgun_password'
MAIL_DEFAULT_SENDER = 'your_email@your_domain.com'
