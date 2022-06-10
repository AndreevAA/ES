import json
from io import StringIO

import graphics
from inner_d import cookies, db, config
from flask import Blueprint, render_template, redirect, url_for, request
from flask_classful import FlaskView, route

# Объект авторизации
from inner_d.db import DB


# Объект ЛК
class Cabinet(FlaskView):

    # Текущие куки
    _cookies = None

    # Объект связки БД
    _db = None

    # Создание объекта кабинета
    def __init__(self):
        self._cookies = cookies.Cookies()

        # Получение объекта БД
        self._db = DB()

    # Обработка массива
    def _get_lab_val(self, arr):
        labels, values = [], []

        for elem in arr:
            labels.append(elem[0])
            values.append(elem[1])

        return labels, values

    # Действие от входа в аккаунт
    @route('/cabinet', methods=['POST'])
    def cabinet(self):
        # Проверка на наличие текущей авторизации
        if self._cookies.is_auth_opened():
            return redirect(url_for('Cabinet:dashboard'))

        # Курсор на БД
        cur_t = self._db.conn.cursor()

        # Полученные значения полей
        usr_login, usr_psd = request.form.get('email'), request.form.get('password')

        # Наличие пользователя в БД
        cur_t.execute(
            'select id, login, password from inner_s.users where login = %s and password = %s',
            (usr_login, usr_psd)
        )

        # Количество найденных пользователей в БД
        f_usr = cur_t.fetchall()

        # id пользователя
        usr_id = f_usr[0][0]

        cur_t.close()

        # Пользователь с введенными полями существует в БД
        if len(f_usr) == 1:
            # Установка Куки
            self._cookies.set_auth_opened(usr_id, usr_login)

            print("SUCCESS_WRITE")

            return redirect(url_for('Cabinet:dashboard'))

        return redirect(url_for('Auth:login'))

        # return render_template('login.html')

        # Действие от входа в аккаунт

    # Действие от входа в аккаунт
    @route('/moderate', methods=['POST'])
    def moderate_post(self):
        try:

            # Полученные значения полей
            user_update = request.form.get('user_update')

            # Получение значений
            user_id, user_login, user_password, user_ac_level = request.form.get('id'), \
                                                                request.form.get('login'), \
                                                                request.form.get('password'), \
                                                                request.form.get('acs_level')

            t_db_cur = self._db.conn.cursor()

            # Проверка возможности обновления пользователя
            t_db_cur.execute(
                "select * from is_update_user_available('{usr_id}', '{usr_login}', '{user_password}');".format(
                    usr_id=user_id, usr_login=user_login, user_password=user_password))

            if len(t_db_cur.fetchall()) <= 1:
                t_db_cur.execute(
                    "select * from update_user('{usr_id}', '{usr_login}', '{user_password}', '{user_ac_level}');".format(
                        usr_id=user_id, usr_login=user_login, user_password=user_password, user_ac_level=user_ac_level))

                return self.moderate_comp("Success_update!")

        except EOFError:
            print()

        return self.moderate_comp("Error update (Field Error)")

    @route('/moderate')
    def moderate(self):
        return self.moderate_comp("Data fetched!")

    def moderate_comp(self, message):
        # Проверка на наличие текущей авторизации
        if not self._cookies.is_auth_opened():
            return redirect(url_for('Auth:login'))

        usr_id, usr_login = self._cookies.get_auth_cookie()

        # Проверка уровня доступа
        t_db_cur = self._db.conn.cursor()

        # Запрос уровней доступа
        t_db_cur.execute("select * from get_user_access_level('{usr_id}', '{usr_login}');".format(usr_id=usr_id, usr_login=usr_login))

        lev = t_db_cur.fetchall()[0][0]

        if lev == config.USR_ACS_L:
            return redirect(url_for('Cabinet:dashboard'))
        if lev == config.ADMIN_ACS_L:
            return redirect(url_for('Cabinet:admin'))

        t_db_cur.execute("select * from inner_s.users;")

        users = [["id", "login", "password", "acs_level", "Действие"]]

        for t_l in t_db_cur.fetchall():
            t_l_l = []
            for p in t_l:
                t_l_l.append(p)
            users.append(t_l_l)

        t_db_cur.execute(
            "select passport_id, name, surname, patronymic, children_number from w_dir.passports where passport_id < 1000;")

        # print(t_db_cur.fetchall())

        passports = [
            ["passport_id", "name", "surname",
             "patronymic", "children_number", "Действие"]]

        for t_l in t_db_cur.fetchall():
            t_l_l = []
            for p in t_l:
                t_l_l.append(p)
            passports.append(t_l_l)

        print(users)
        print(passports)

        users_io = StringIO()
        json.dump(users, users_io)

        passports_io = StringIO()
        json.dump(passports, passports_io)

        return render_template('main-dark/moderate.html', users=users_io, message=message, passports=passports_io)

    # Действие от входа в аккаунт
    @route('/admin', methods=['POST'])
    def admin_post(self):

        try:

            # Полученные значения полей
            user_update = request.form.get('user_update')

            # Получение значений
            user_id, user_login, user_password, user_ac_level = request.form.get('id'), \
                                                                request.form.get('login'), \
                                                                request.form.get('password'), \
                                                                request.form.get('acs_level')

            if str(user_update) != 'None' and str(user_id) != None:

                t_db_cur = self._db.conn.cursor()

                # Проверка возможности обновления пользователя
                t_db_cur.execute("select * from is_update_user_available('{usr_id}', '{usr_login}', '{user_password}');".format(usr_id=user_id, usr_login=user_login, user_password=user_password))

                if len(t_db_cur.fetchall()) <= 1:
                    t_db_cur.execute(
                        "select * from update_user('{usr_id}', '{usr_login}', '{user_password}', '{user_ac_level}');".format(
                            usr_id=user_id, usr_login=user_login, user_password=user_password, user_ac_level=user_ac_level))

                    return self.admin_comp("Success_update!")

        except EOFError:
            print()

        try:
            # Полученные значения полей
            create_user = request.form.get('create_user')

            # Получение значений
            user_login, user_password, user_ac_level = request.form.get('login'), \
                                                                request.form.get('password'), \
                                                                request.form.get('acs_level')

            if (str(create_user) != 'None' and str(user_login) != 'None'):
                t_db_cur = self._db.conn.cursor()

                t_db_cur.execute(
                    "select max(id) from inner_s.users")

                user_id = t_db_cur.fetchall()[0][0] + 1

                # Проверка возможности обновления пользователя
                t_db_cur.execute(
                    "select * from is_update_user_available('{usr_id}', '{usr_login}', '{user_password}');".format(
                        usr_id=user_id, usr_login=user_login, user_password=user_password))

                if len(t_db_cur.fetchall()) < 1:
                    t_db_cur.execute(
                        "select * from create_user('{usr_id}', '{usr_login}', '{user_password}', '{user_ac_level}');".format(
                            usr_id=user_id, usr_login=user_login, user_password=user_password, user_ac_level=user_ac_level))

                return self.admin_comp("Success_create!")
        except EOFError:
            print()

        try:
            # Полученные значения полей
            delete_data = request.form.get('delete_data')

            # Получение значений
            table_name_i, id_i = request.form.get('table_name'), request.form.get('id')

            if str(delete_data) != 'None' and str(table_name_i) != 'None' and str(id_i) != 'None':
                t_db_cur = self._db.conn.cursor()

                # Проверка возможности удаления пользователя
                t_db_cur.execute(
                    "select * from inner_s.{table_name} where id='{id}';".format(
                        table_name=table_name_i, id=id_i))

                if len(t_db_cur.fetchall()) == 1:
                    t_db_cur.execute(
                        "delete from inner_s.{table_name} where id='{id}';".format(
                        table_name=table_name_i, id=id_i))
                    return self.admin_comp("Success_delete!")
                else:
                    return self.admin_comp("Row_doesnt_exist!")

                return self.admin_comp("Error_delete!")
        except EOFError:
            print()

        return self.admin_comp("Error update (Field Error)")

    @route('/admin')
    def admin(self):
        return self.admin_comp("Data fetched!")

    def admin_comp(self, message):
        # Проверка на наличие текущей авторизации
        if not self._cookies.is_auth_opened():
            return redirect(url_for('Auth:login'))

        usr_id, usr_login = self._cookies.get_auth_cookie()

        # Проверка уровня доступа
        t_db_cur = self._db.conn.cursor()

        # Запрос уровней доступа
        t_db_cur.execute("select * from get_user_access_level('{usr_id}', '{usr_login}');".format(usr_id=usr_id, usr_login=usr_login))

        lev = t_db_cur.fetchall()[0][0]
        if lev == config.USR_ACS_L:
            return redirect(url_for('Cabinet:dashboard'))
        if lev == config.MODERATOR_ACS_L:
            return redirect(url_for('Cabinet:moderate'))

        t_db_cur.execute("select * from inner_s.users;")

        users = [["id", "login", "password", "acs_level", "Действие"]]

        for t_l in t_db_cur.fetchall():
            t_l_l = []
            for p in t_l:
                t_l_l.append(p)
            users.append(t_l_l)

        t_db_cur.execute("select passport_id, name, surname, patronymic, children_number from w_dir.passports where passport_id < 1000;")

        # print(t_db_cur.fetchall())

        passports = [
            ["passport_id", "name", "surname",
             "patronymic", "children_number", "Действие"]]

        for t_l in t_db_cur.fetchall():
            t_l_l = []
            for p in t_l:
                t_l_l.append(p)
            passports.append(t_l_l)

        print(users)
        print(passports)

        users_io = StringIO()
        json.dump(users, users_io)

        passports_io = StringIO()
        json.dump(passports, passports_io)

        return render_template('main-dark/admin.html', users=users_io, message=message, passports=passports_io)

    # Главная страница
    def dashboard(self):

        # Проверка на наличие текущей авторизации
        if not self._cookies.is_auth_opened():
            return redirect(url_for('Auth:login'))

        t_db = DB()
        t_db_cur = t_db.conn.cursor()

        city = request.values.get('city')

        t_db_cur.execute("select * from city_exist_cnt('{}')".format(city))

        if request.values.get("city") is None or t_db_cur.fetchall()[0][0] == 0:
            city = 'Не указано'

        t_db_cur.execute("select * from cit_alive_rate_by_year_city('{}');".format(city))
        cit_alive_lab, cit_alive_val = self._get_lab_val(t_db_cur.fetchall())
        cit_alive = graphics.Graphics('Население', cit_alive_lab, cit_alive_val)

        t_db_cur.execute("select * from birth_rate_by_year_city('{}');".format(city))
        b_lab, b_val = self._get_lab_val(t_db_cur.fetchall())
        birth = graphics.Graphics('Рождаемость в год', b_lab, b_val)

        t_db_cur.execute("select * from depth_rate_by_year_city('{}');".format(city))
        b_lab, b_val = self._get_lab_val(t_db_cur.fetchall())
        depth = graphics.Graphics('Смертность в год', b_lab, b_val)

        t_db_cur.execute("select * from life_length_rate_by_year_city('{}');".format(city))
        life_length_lab, life_length_val = self._get_lab_val(t_db_cur.fetchall())
        life_length = graphics.Graphics('Продолжительность жизни по годам', life_length_lab, life_length_val)

        return render_template('main-dark/simple_charts.html', birth=birth, depth=depth, life_length=life_length, cit_alive=cit_alive)


