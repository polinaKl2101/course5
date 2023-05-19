import psycopg2


class DataBaseManager:
    """Класс для обращения к БД"""

    def __init__(self, db_name, params):
        self.__db_name = db_name
        self.__params = params

    def get_companies_and_vacancies_count(self):
        """Метод для получения компаний и вакансий"""

        connection = psycopg2.connect(f'postgresql://{self.__params["user"]}:'
                f'{self.__params["password"]}@{self.__params["host"]}:'
                f'{self.__params["port"]}/{self.__db_name}')

        cursor = connection.cursor()
        sql_query = """SELECT employer_title, vacancy_count
                            FROM public.employers"""
        cursor.execute(sql_query)
        data = cursor.fetchall()
        return data

        cursor.close()
        connection.close()

    def get_all_vacancies(self):
        """"Метод для получения всех вакансий компании"""

        connection = psycopg2.connect(f'postgresql://{self.__params["user"]}:'
                                      f'{self.__params["password"]}@{self.__params["host"]}:'
                                      f'{self.__params["port"]}/{self.__db_name}')

        cursor = connection.cursor()
        sql_query = """SELECT vacancy_title, employer_title, salary_from, salary_to, vacancies.url
                            FROM employers
                            JOIN public.vacancies USING(employer_id)"""
        cursor.execute(sql_query)
        data = cursor.fetchall()
        return data

        cursor.close()
        connection.close()

    def get_avg_salary(self):
        """"Метод для получения средней ЗП"""

        connection = psycopg2.connect(f'postgresql://{self.__params["user"]}:'
                                      f'{self.__params["password"]}@{self.__params["host"]}:'
                                      f'{self.__params["port"]}/{self.__db_name}')

        cursor = connection.cursor()
        sql_query = """SELECT AVG((salary_from + salary_to) / 2) AS avg_salary
                       FROM public.vacancies
                       """

        cursor.execute(sql_query)
        data = cursor.fetchone()
        return data

        cursor.close()
        connection.close()

    def get_vacancies_with_highest_salary(self):
        """Метод для получения вакансий с наивысшей ЗП"""

        connection = psycopg2.connect(f'postgresql://{self.__params["user"]}:'
                                      f'{self.__params["password"]}@{self.__params["host"]}:'
                                      f'{self.__params["port"]}/{self.__db_name}')

        cursor = connection.cursor()
        sql_query = """SELECT vacancy_title, salary_from, url
                       FROM vacancies
                       WHERE salary_from > (SELECT AVG((salary_from + salary_to) / 2) FROM vacancies)
                       ORDER BY salary_from DESC"""

        cursor.execute(sql_query)
        data = cursor.fetchall()
        return data

        cursor.close()
        connection.close()

    def get_vacancies_with_keyword(self, search_word):
        """Метод для получения вакансий по ключевому слову"""

        with psycopg2.connect(dbname=self.__db_name, **self.__params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM vacancies
                               WHERE vacancy_title LIKE '%{search_word}%'""")

                for i in cursor.fetchall()[:15]:
                    print(i)

        connection.close()