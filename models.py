from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def create_table():
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE
            )
            """)
        connection.commit()
        connection.close()

    @staticmethod
    def create(username, password, is_admin=False):
        hashed_password = generate_password_hash(password, method='scrypt')
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)
                """, (username, hashed_password, is_admin))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e  # Handle error as needed
        finally:
            connection.close()

    @staticmethod
    def find_by_username(username):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
        connection.close()
        return user

    @staticmethod
    def login(username, password):
        user = User.find_by_username(username)
        if user and check_password_hash(user['password'], password):
            return user
        return None


class Kos:
    @staticmethod
    def create_table():
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS kos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                address TEXT NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                description TEXT
            )
            """)
        connection.commit()
        connection.close()

    @staticmethod
    def create(name, address, price, description):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO kos (name, address, price, description) VALUES (%s, %s, %s, %s)
            """, (name, address, price, description))
        connection.commit()
        connection.close()

    @staticmethod
    def read_all():
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM kos")
            kos_list = cursor.fetchall()
        connection.close()
        return kos_list

    @staticmethod
    def update(kos_id, name, address, price, description):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
            UPDATE kos SET name = %s, address = %s, price = %s, description = %s WHERE id = %s
            """, (name, address, price, description, kos_id))
        connection.commit()
        connection.close()

    @staticmethod
    def delete(kos_id):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM kos WHERE id = %s", (kos_id,))
        connection.commit()
        connection.close()
