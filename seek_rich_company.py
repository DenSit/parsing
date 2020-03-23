'''
Seek and check companies from portal "За честный бизнес", choice from them
placed in Moscow and having income not less 40 000 000 rub a year
'''


import requests
from bs4 import BeautifulSoup

page = requests.get("https://zachestnyibiznes.ru/(your_query)&page=1")
soup = BeautifulSoup(page.content, 'html.parser')

num = soup.find("ul", class_="pagination")
count_pages = len(num.find_all('li')) - 1
dict_ref = {}
flag = 0
for j in range(1, count_pages):
    page = requests.get(f"https://zachestnyibiznes.ru/(your_query)={j}")
    soup = BeautifulSoup(page.content, 'html.parser')
    soup = soup.find_all('tr')
    for i in range(1, len(soup)):
        try:
            status = soup[i].find(style="color: #333;").get_text()[1:]
        except AttributeError:
            flag = 1
            break
        name = soup[i].find(style="font-size: 0.7em;").get_text()
        address = soup[i].find(width='220').get_text()[35:-1]
        reference = 'https://zachestnyibiznes.ru' + soup[i].find(itemprop="legalName").get('href')
        if 'Москва' in address:
            dict_ref[reference] = (name, address)
    if flag:
        break
with open('income_company1.txt', 'w', encoding='utf-8') as f:
    for url in dict_ref.keys():
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.find('div', class_="m-b-10").get_text()
        income = text.split('\n')[2]
        target = income.split(' ')[6:]
        summa = ''
        for i in target:
            if 'руб' in i:
                break
            summa += i
        if summa:
            if int(summa[:-3]) >= 40000000:
                f.write('{}; {}\n'.format(*dict_ref[url]))
                f.write(f'Доходы: {summa[:-3]}\n')
                f.write('\n')




