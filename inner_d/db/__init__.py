import psycopg2


# Объект связки БД
class DB:

    # Поле соединение с БД
    conn = None

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="ES",
            user='postgres',
            password='qwerty')

    # def is_moderate_access_level(self):
    #