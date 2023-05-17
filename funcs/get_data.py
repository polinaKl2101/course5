import requests
import csv
import pandas


class EmployeeData:

    """Класс для парсинга компаний"""

    __employee_url = "https://api.hh.ru/employers?only_with_vacancies=true"

    def get_employee_data(self, search_word: str):
        """Метод для получения информации о 10 компаниях по ключевому слову
        search_word: параметр поиска
        Возвращает список словарей с полной информацией о каждой компании
        """

        params = {'text': search_word.lower(),
                  'area': '113',
                  'per_page': 10}

        return requests.get(self.__employee_url, params=params).json()['items']

    def get_employee_id(self, data: list):
        """Метод для получения id компании
        data: данные о компаниях, полученные методом get_employee_data
        Возвращает список с id компаний
        """

        companies_id = []
        for i in data:
            companies_id.append(i.get('id'))

        return companies_id

    def save_employee_data_csv(self, file_name: str, data: list):

        """Метод для сохранения данных в csv файл для их дальнейшего использования в БД
        file_name: наименование создаваемого файла
        data: данные о компаниях, полученные методом get_employee_data
        Создает csv файл
        """

        file_name = f"{file_name.title()}_emp.csv"

        fields = ['employer_id', 'employer_title', 'vacancy_count', 'url'] # заголовки для колонок

        with open(file_name, 'w', newline='') as csvfile:

            file_writer = csv.DictWriter(csvfile, fields)
            file_writer.writeheader() # запись заголовков

            for i in data: # строки
                file_writer.writerow({'employer_id': int(i['id']),
                                      'employer_title': str(i['name']),
                                      'vacancy_count': int(i['open_vacancies']),
                                      'url': str(i['alternate_url'])})


class VacancyData:

    """Класс для парсинга вакансий работодателя"""

    __vacancy_url = 'https://api.hh.ru/vacancies'

    def __init__(self):
        self.__vacancy_list = []  # для сбора вакансий
        self.__pages_for_pars = 10  # страницы для парсинга

    def pars_emp_vacancies(self, ids: list):
        """Метод для получения всех вакансий выбранных компаний
        ids: id компаний, полученных в классе EmployersData, методом get_employee_id
        Возвращает словарь со всеми вакансиями
        """
        params = {'employer_id': ids,
                  'page': self.__pages_for_pars,
                  'per_page': 100}

        return requests.get(self.__vacancy_url, params=params).json()['items']

    def get_employee_vacancy(self, ids: list):
        """Метод для получения вакансий компаний
         ids: id компаний, полученных в классе EmployersData, методом get_employee_id
         Возвращает словарь со всеми вакансиями
         """
        for emp_id in ids:
            for page in range(0, self.__pages_for_pars):
                params = {'employer_id': emp_id,
                          'page': page,
                          'per_page': 100}
                response = requests.get(self.__vacancy_url, params=params).json()['items']
                self.__vacancy_list.extend(response)

        return self.__vacancy_list

    def save_vacancy_data_csv(self, file_name: str, data: list):

        """Метод для сохранения данных в csv файл для их дальнейшего использования в БД
        file_name: наименование создаваемого файла
        data: данные о вакансиях, полученные методом get_employee_vacancy
        Создает csv файл
        """

        file_name = f"{file_name.title().strip()}_vac.csv"
        fields = ['employer_id', 'vacancy_title', 'salary_from', 'salary_to', 'url'] # заголовки для колонок

        with open(file_name, mode='w', newline='', encoding='utf-8') as csvfile:

            writer = csv.DictWriter(csvfile, fields)

            writer.writeheader() # запись заголовков
            for i in data:

                if i['salary'] is None: # если в графе зарплаты None
                    salary_from = 0
                    salary_to = 0

                else:
                    salary_from = 0 if not i['salary']['from'] else i['salary']['from']
                    salary_to = 0 if not i['salary']['to'] else i['salary']['to']

                writer.writerow(
                    {'employer_id': int(i['employer']['id']),
                     'vacancy_title': str(i['name']),
                     'salary_from': f'{salary_from}',
                     'salary_to': f'{salary_to}',
                     'url': str(i['alternate_url'])})



