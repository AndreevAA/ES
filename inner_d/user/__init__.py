# Объект пользователя системы
class User:

    # Доступные данные
    usr_id, usr_login = None, None

    # Создание объекта пользователя системы
    def __init__(self, usr_id, usr_login):
        self.usr_id = usr_id
        self.usr_login = usr_login
    