import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs


class Insta:

    def __init__(self, tag, min_followers):
        self.url = f'https://www.instagram.com/explore/tags/{tag}/'
        self.min_followers = int(min_followers)

    def parse(self):
        blogers = []
        browser = webdriver.Chrome(r'C:\Users\user\AppData\Local\Google\Chrome\chromedriver.exe')
        browser.get(self.url)
        count = 0
        lenOfPage = browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = True
        with open("target_blogers.txt", "w", encoding='utf-8') as f:
            while match:
                lastCount = lenOfPage
                time.sleep(3)
                lenOfPage = browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount == lenOfPage or count >= 10:
                    match = False

                source_data = browser.page_source
                bs_data = bs(source_data, 'html.parser')
                body = bs_data.find('body')
                lst_a = body.findAll('a')
                for ref in lst_a:
                    if ref['href']:
                        if '/p/' in ref['href']:
                            link = 'https://www.instagram.com' + ref['href']
                            browser.get(link)
                            source = browser.page_source
                            data = bs(source, 'html.parser')
                            body = data.find('body')
                            account = f"https://www.instagram.com{body.a['href']}"
                            browser.get(account)
                            source = browser.page_source
                            data = bs(source, 'html.parser')
                            name = data.title.text
                            if 'Страница не найдена' in name:
                                break
                            text = data.get_text
                            try:
                                followers = int(
                                    str(text).split('followers')[1].split('title="')[1].split('"')[0].replace(' ', ''))
                            except IndexError:
                                break
                            try:
                                name = name.split('(')[1].split(')')[0]
                            except IndexError:
                                name = name.split(' •')[0]

                            if followers < self.min_followers:
                                print(f'{name}  Подписчики: {followers} Так себе блогер')
                            else:
                                print(f'{name}  Подписчики: {followers} !!! То что нужно!!!')
                                f.write(f'{name}  followers: {followers}\n')
                            print('__' * 33)
            count += 1
        return blogers


if __name__ == '__main__':
    tag = input("Input hash-tag for searching blogers, for example: fitness,  food, спорт...: ")
    min_followers = input(" Input minimum count of followers: ")
    obj = Insta(tag, min_followers)
    obj.parse()
    print()
    print("The file 'target_blogers.txt' was created in current directory. Good luck!")



