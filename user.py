from DataBaseClasses.CreateDB import DataBaseCreator
from DataBaseClasses.DBManager import DataBaseManager
from DataBaseClasses.config import config
from funcs.get_data import EmployeeData
from funcs.get_data import VacancyData


def user():
    while True:

            search_word = input('Введите слово для поиска компаний: ').lower()

            ep = EmployeeData()
            employers_data = ep.get_employee_data(search_word)

            ep.save_employee_data_csv(search_word, employers_data)
            emp_indexes = ep.get_employee_id(employers_data)

            vp = VacancyData()
            vacancies_data = vp.get_employee_vacancy(emp_indexes)
            vp.save_vacancy_data_csv(search_word, vacancies_data)

            db_name = input('Введите имя для базы данных: ').lower()

            params = config()
            dbc = DataBaseCreator(db_name, params)
            dbc.create_database()
            dbc.create_tables()
            dbc.save_data_to_database(f"{search_word.title()}_emp.csv", f"{search_word.title()}_vac.csv")
            dbm = DataBaseManager(db_name, config())

            print("Список доступных функций:"
                  "1. Получает список всех компаний и количество вакансий у каждой компании.\n"
                  "2. Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.\n"
                  "3. Получает среднюю зарплату по вакансиям.\n"
                  "4. Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
                  "5. Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.\n"
                  "6. Выход из программы")

            user_input = input('Введите номер: ').lower()

            while user_input != '6':

                if user_input == '1':
                    print(dbm.get_companies_and_vacancies_count())

                if user_input == '2':
                    print(dbm.get_all_vacancies())

                if user_input == '3':
                    print(dbm.get_avg_salary())

                if user_input == '4':
                    print(dbm.get_vacancies_with_highest_salary())

                if user_input == '5':
                    keyword = input('Введите  слово для поиска по вакансиям: ').lower()
                    dbm.get_vacancies_with_keyword(keyword)

                elif user_input not in ('1', '2', '3', '4', '5', 'помощь'):
                    print('Команда не найдена, пожалуйста, повторите ввод')

                user_input = input('Введите номер: ').lower()

            print('Программа завершена!')
            exit(0)
