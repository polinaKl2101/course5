import csv
import psycopg2


class DataBaseCreator:
    """Класс для создания базы данных"""

    def __init__(self, db_name, params):

        self.__db_name = db_name
        self.__params = params

    def create_database(self):
        """Метод для создания базы данных"""

        connection = psycopg2.connect(dbname='postgres', **self.__params)
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {self.__db_name}")
        cursor.execute(f"CREATE DATABASE {self.__db_name}")

        cursor.close()
        connection.close()

    def create_tables(self):
        """Метод для создания  таблиц"""

        with psycopg2.connect(dbname=self.__db_name, **self.__params) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS public.employers (
                    employer_id int PRIMARY KEY,
                    employer_title varchar(100) NOT NULL,
                    vacancy_count int,
                    url varchar(255) NOT NULL)
                """)

            with connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS public.vacancies (
                    employer_id int,
                    vacancy_title varchar(100) NOT NULL,
                    salary_from real,
                    salary_to real,
                    url varchar(255) NOT NULL,
                    FOREIGN KEY (employer_id) REFERENCES public.employers(employer_id)) 
                """)

    def save_data_to_database(self, employers_data, vacancies_data):
        """
        Метод для заполнения таблиц
        employers_data: csv файл с данными о кампаниях
        vacancies_data: csv файл с данными о вакансиях
        """

        with psycopg2.connect(dbname=self.__db_name, **self.__params) as connection:
            with connection.cursor() as cursor:

                with open(employers_data) as file:
                    file_reader = csv.DictReader(file, delimiter=',')

                    for i in file_reader:
                        employer_id = i['employer_id']
                        employer_title = i['employer_title']
                        vacancy_count = i['vacancy_count']
                        url = i['url']

                        cursor.executemany(
                            'INSERT INTO public.employers VALUES (%s, %s, %s, %s)',
                            [(employer_id, employer_title, vacancy_count, url)])

                with open(vacancies_data, encoding='utf-8') as file:
                    file_reader = csv.DictReader(file, delimiter=',')

                    for i in file_reader:
                        employer_id = i['employer_id']
                        vacancy_title = i['vacancy_title']
                        salary_from = i['salary_from']
                        salary_to = i['salary_to']
                        url = i['url']

                        cursor.executemany(
                            'INSERT INTO public.vacancies VALUES (%s, %s, %s, %s, %s)',
                            [(employer_id, vacancy_title, salary_from, salary_to, url)])

