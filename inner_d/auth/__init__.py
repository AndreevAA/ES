from inner_d import cookies
from flask import Blueprint, render_template, redirect, url_for, request
from flask_classful import FlaskView, route

# Объект авторизации
from inner_d.db import DB


class Auth(FlaskView):

    # Направление адреса
    # _auth = Blueprint('auth', __name__)

    # Текущие куки
    _cookies = None

    # Поле статуса авторизации
    _is_user_authenticated = None

    # Объект связки БД
    _db = None

    # Создание объекта авторизации
    def __init__(self):

        # Обновление куки
        self._cookies = cookies.Cookies()

        # Получение объекта БД
        self._db = DB()

    # Вход в аккаунт
    def login(self):
        # Проверка на наличие текущей авторизации
        if self._cookies.is_auth_opened():
            return redirect(url_for('Cabinet:dashboard'))

        # Текущей авторизации нет, генерируем страницу
        return render_template('main-dark/auth_login.html')

    # Действие от входа в аккаунт
    @route('/login', methods=['POST'])
    def login_post(self):

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
            self._cookies.set_auth_opened(usr_id, usr_login)
            return redirect(url_for('Cabinet:dashboard'))

        return redirect(url_for('Auth:login'))

    @route('/signup')
    def signup(self):
        return render_template('signup.html')

    @route('/signup', methods=['POST'])
    def signup_post(self):

        return redirect(url_for('Auth:login'))

    @route('/log_out')
    def log_out(self):
        self._cookies.set_auth_closed()
        return redirect(url_for('Auth:login'))

    @route('/log_out', methods=["POST", "GET"])
    def log_out(self):
        self._cookies.set_auth_closed()
        return redirect(url_for('Auth:login'))
