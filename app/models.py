from flask_login import UserMixin
from .config import db_connection

connection = db_connection()

cursor = connection.cursor()

class User(UserMixin):
    def __init__(self, name):
        self.id = name


def login_manager_func(login_manager):
    @login_manager.user_loader
    def load_user(username):
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        data = cursor.fetchone()

        if data:
            return User(name=data[0])
        
        return None


class query():

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email


    def create_user_query(name, hashed_password, email):
        cursor.execute("""
        INSERT INTO users (username, password, email) VALUES(%s, %s, %s);
    """,(name, hashed_password, email))
        
        connection.commit()


    def read_user_query(name):
        cursor.execute("""
        SELECT user_id, username, password FROM users WHERE username = %s;
    """, (name,))
        
        data = cursor.fetchone()

        if data:
            return data
        
        return None
        

    def delete_user_query(name):
        cursor.execute("""
        DELETE FROM users WHERE username = %s;
    """, (name,))
        
        connection.commit()


class profile_picture_queries():

    def save_profile_picture_path_query(file_path, id):
        cursor.execute("""
        INSERT INTO user_profile_photo (pp_path, user_pp_id) VALUES (%s, %s)
    """, (file_path, id))

        connection.commit()

    
    def read_profile_picture_path_query(user_id):
        cursor.execute("""
        SELECT pp_path FROM user_profile_photo WHERE user_pp_id = %s;
    """, (user_id,))
        
        data = cursor.fetchone()

        if data:
            return data
        
        return None
    
    
    def delete_profile_picture_path_query(user_id):
        cursor.execute("""
        DELETE FROM user_profile_photo WHERE user_pp_id = %s;
    """, (user_id,))
        
        connection.commit()