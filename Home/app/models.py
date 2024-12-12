from .config import connections
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, name):
        self.id = name


def login_manager_func(login_manager):
    @login_manager.user_loader
    def load_user(name):
        connection = connections()
        cursor = connection.cursor()

        cursor.execute("""
        SELECT username FROM users WHERE username = %s;
""", (name, ))
        
        data = cursor.fetchone()
        if data:
            return User(name= data[0])
        
        connection.close()
        cursor.close()

        return None
    




class querys():

    def login_user_query(name):
        connection = connections()
        cursor = connection.cursor()

        cursor.execute("""
        SELECT username, password FROM users WHERE username = %s;
""", (name,))
    
        data = cursor.fetchone()

        if data:
            return data
        
        connection.close()
        cursor.close()
        
        return None
    

    def zara_link_insert_query(url, name):
        connection = connections()
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO zara_links (zara_link, zara_username) 
        VALUES (%s, %s); 
""", (url, name))
        
        connection.commit()

        connection.close()
        cursor.close()


class show_stock_status_query():
    def show_zara_stock_status_query(name):
        connection = connections()
        cursor = connection.cursor()

        cursor.execute("""
        SELECT 
            zara_links.zara_link,
            ARRAY_AGG(
                ARRAY[zara_stocks.zara_stock, zara_stocks.zara_size]
            ) AS stock_size_list,
            zara_stocks.item_picture_url
        FROM 
            zara_stocks
        JOIN 
            zara_links ON zara_links.zara_id = zara_stocks.zara_id
        WHERE 
            zara_links.zara_username = %s
        GROUP BY 
            zara_stocks.item_picture_url, zara_links.zara_link;

        """, (name,))
        
        data = cursor.fetchall()

        connection.close()
        cursor.close()

        return data




class get_urls_query():

    def get_zara_urls_query():
        connection = connections()
        cursor = connection.cursor()

        cursor.execute("""
        SELECT zara_id, zara_link FROM zara_links;
    """)
    
        data = cursor.fetchall()

        connection.close()
        cursor.close()

        if data:
            return data
        

class zara_query():

    def checking_zara_stock_same_query(zara_id, size):
        connection = connections()
        cursor = connection.cursor()

        cursor.execute("""
        SELECT zara_stock, zara_size, zara_id FROM zara_stocks WHERE zara_id = %s AND zara_size = %s;
""", (zara_id, size))
        
        data = cursor.fetchone()

        connection.close()
        cursor.close()

        return data
        
    

    def delete_zara_stock_query(zara_id):
        connection = connections()
        cursor = connection.cursor()

        cursor.execute("""
        DELETE FROM zara_stocks WHERE zara_id = %s;
""", (zara_id,))
        
        connection.commit()

        connection.close()
        cursor.close()


    def insert_zara_stock_query(zara_stock, zara_size, zara_id, item_picture_url):
        connection = connections()
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO zara_stocks (zara_stock, zara_size, zara_id, item_picture_url) VALUES (%s, %s, %s, %s)
""", (zara_stock, zara_size, zara_id, item_picture_url))
        
        connection.commit()

        connection.close()
        cursor.close()



    def update_zara_stock_query(zara_stock, zara_id, zara_size):
        connection = connections()
        cursor = connection.cursor()
        
        cursor.execute("""
        UPDATE zara_stocks SET zara_stock = %s WHERE zara_id = %s AND zara_size = %s;
""", (zara_stock, zara_id, zara_size))
        
        connection.commit()
        
        connection.close()
        cursor.close()




