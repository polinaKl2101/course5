import requests

url = 'https://api.hh.ru/vacancies'
r = requests.get(url)
print(r.status_code)

