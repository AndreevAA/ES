import datetime
import random

from inner_d.db import DB

import gen_sourse

# Генерация данных для БД
class DataGenerating:
    _db = None

    def __init__(self):
        self._db = DB()

    def generate_citizens(self):

        snp = gen_sourse.SNPs
        # cities = cities

        for passportID in range(139340, 145000000):
            t_snp = snp[random.randint(1, len(snp) - 1)].split()

            name = t_snp[1]
            surname = t_snp[0]
            patronymic = t_snp[2]

            registration = gen_sourse.cities[random.randint(1, len(gen_sourse.cities) - 1)]

            start_date = datetime.date(1960, 1, 1)
            end_date = datetime.date(2015, 2, 1)

            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            random_date = start_date + datetime.timedelta(days=random_number_of_days)

            cur_t = self._db.conn.cursor()

            # Полученные значения полей
            # usr_login, usr_psd = request.form.get('email'), request.form.get('password')

            # print(passportID, name, surname, patronymic, registration, 0, False, random_date)

            childrenNumber = 0
            if (datetime.date(2022, 2, 1) - random_date).days > 25*365:
                childrenNumber = random.randint(0, 5)

            isMarriedNow = random.choice([True, False])

            isDepth = random.choice([True, False])

            depthDate = None

            if isDepth:
                start_date = random_date
                end_date = datetime.date(2015, 2, 1)

                time_between_dates = end_date - start_date
                days_between_dates = time_between_dates.days
                random_number_of_days = random.randrange(days_between_dates)
                depthDate = start_date + datetime.timedelta(days=random_number_of_days)

            # Наличие пользователя в БД


            cur_t.execute(
                'INSERT INTO w_dir.passports ("passport_id", "name", "surname", "patronymic", "registration", '
                '"children_number", "is_married_now", "birth_date", "is_depth", "depth_date") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                (passportID, name, surname, patronymic, registration, childrenNumber, isMarriedNow, random_date, isDepth, depthDate)
            )

            # cur_t.execute("SELECT * FROM w_dir.passports;")
            # cur_t.fetchone()

            self._db.conn.commit()
            
            cur_t.close()

            # print(t_snp, registration)
