import logging
from db.utils import Utils
from db.repos.abstract import AbstractRepo
import db.models as models


class passportRepoTarantool(AbstractRepo):

    connection = None
    _meta = None

    space = None

    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "space_name": "passports",
            "field_names": {"passport_id": 1, "name": 2, "surname": 3, "patronymic": 4,
                            "registration": 5, "children_number": 6, "is_married_now": 7, "birth_date": 8,
                            "is_depth": 9, "depth_date": 10}
        }

        self.space = connection.space(self._meta['space_name'])

    def save(self, model):
        if not isinstance(model, models.passport):
            logging.error("Trying to save passport object of invalid type")
            raise TypeError("Expected object is instance of passport")

        self.space.insert((model.id, model.name, model.surname, model.patronymic, model.registration, model.children_number,
                           model.is_married_now, model.birth_date, model.is_depth, model.depth_date))

    def get_by_id(self, model_id):
        obj = self.space.select(model_id)
        if len(obj) == 0:
            return None

        return models.passport(*obj[0])

    def get_by_filter(self, index, key):
        raw_objects = self.space.select(key, index=index)
        if len(obj) == 0:
            return None, None

        models_list = list()
        primary_keys = list()
        for obj in raw_objects:
            model = models.passport(*obj)
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def get_all(self):
        raw_objects = self.space.select()
        if len(raw_objects) == 0:
            return None

        models_list = list()
        for obj in raw_objects:
            models_list.append(models.passport(*obj))

        return models_list

    def remove(self, id):
        obj = self.space.delete(id)
        if len(obj) == 0:
            return None

        return obj

    def edit(self, *args, **kwargs):
        obj_id = kwargs['id']
        updated_args = Utils.get_tarantool_update_args(kwargs['fields'], self._meta['field_names'])

        return self.space.update(obj_id, updated_args)[0]


class usersRepoTarantool(AbstractRepo):

    connection = None
    _meta = None

    space = None

    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "space_name": "users",
            "field_names": {
                "id": 1,
                "login": 2,
                "password": 3,
                "acs_level": 4,
            }
        }

        self.space = connection.space(self._meta['space_name'])

    def save(self, model):
        if not isinstance(model, models.users):
            logging.error("Trying to save users object of invalid type")
            raise TypeError("Expected object is instance of users")

        self.space.insert(tuple(model.__dict__.values()))

    def get_by_filter(self, index, key):
        raw_objects = self.space.select(key, index=index)
        if len(raw_objects) == 0:
            return None, None

        models_list = list()
        primary_keys = list()
        for obj in raw_objects:
            model = models.users(*obj)
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def remove(self, id):
        obj = self.space.delete(id)
        if len(obj) == 0:
            return None

        return obj
