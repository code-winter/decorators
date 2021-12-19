import os
from datetime import datetime as dt
import requests
import bs4
PATH = os.getcwd()  # Здесь можно подставить путь, куда будут сохраняться логи


def params_logger(path):

    def func_logger(function):

        def logger(*args, **kwargs):
            file_name = 'logs.txt'
            full_path = os.path.join(path, file_name)
            current_time = dt.now()
            name = function.__name__
            args_list = args
            kwargs_list = kwargs
            result = function(*args, **kwargs)
            if result is None:
                result = 'Void function'
            with open(full_path, 'w', encoding='utf-8') as log_file:
                log_file.write(f'Date and time: {str(current_time)}\n')
                log_file.write(f'Function name: {name}\n')
                log_file.write(f'Arguments: {str(args_list)}\n')
                log_file.write(f'Keyword arguments: {str(kwargs_list)}\n')
                log_file.write(f'Function result: {str(result)}\n')
            return result
        return logger
    return func_logger


@params_logger(PATH)
def search_preview(headers, keywords):
    print('\nSearching from main page in previews:')
    response = requests.get('https://habr.com/ru/all/', headers=headers)
    response.raise_for_status()
    webpage_text = response.text
    soup = bs4.BeautifulSoup(webpage_text, features='html.parser')
    articles = soup.find_all('article')
    for article in articles:
        title = article.find('a', class_='tm-article-snippet__title-link')
        title_text = title.find('span').text
        date = article.find('span', class_='tm-article-snippet__datetime-published')
        date_text = date.next.attrs['title']
        href = title['href']
        url = 'https://habr.com' + href
        text = article.find('div', class_='article-formatted-body article-formatted-body_version-2')
        # Это для версии 2 формата статьи
        if text is not None:
            article_text = article.find_all('p')
            for paragraph in article_text:
                for word in keywords:
                    query = paragraph.text.lower()
                    result = query.find(word.lower())
                    if result != -1:
                        print(f'\nposted on: {date_text}\ntitle: {title_text}\nlink: {url}')
                        print('__________________')
                        break
        else:
            # Это для версии 1 формата статьи
            text = article.find('div', class_='article-formatted-body article-formatted-body_version-1')
            article_text = text.text.lower()
            for word in keywords:
                result = article_text.find(word.lower())
                if result != -1:
                    print(f'\nposted on: {date_text}\ntitle: {title_text}\nlink: {url}')
                    print('__________________')
                    break


@params_logger(PATH)
def search_full(headers, keywords):
    print('\nSearching inside the articles from main page:')
    response = requests.get('https://habr.com/ru/all/', headers=headers)
    response.raise_for_status()
    webpage_text = response.text
    soup = bs4.BeautifulSoup(webpage_text, features='html.parser')
    articles = soup.find_all('article')
    for article in articles:
        title = article.find('a', class_='tm-article-snippet__title-link')
        title_text = title.find('span').text
        date = article.find('span', class_='tm-article-snippet__datetime-published')
        date_text = date.next.attrs['title']
        href = title['href']
        url = 'https://habr.com' + href
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        bs = bs4.BeautifulSoup(resp.text, features='html.parser')
        main_text = bs.find('div', class_='article-formatted-body article-formatted-body_version-2')
        # Это для версии 2 формата статьи
        if main_text is not None:
            for word in keywords:
                query = main_text.text.lower()
                result = query.find(word.lower())
                if result != -1:
                    print(f'\nposted on: {date_text}\ntitle: {title_text}\nlink: {url}')
                    print('__________________')
                    break
        else:
            # Это для версии 1 формата статьи
            main_text = bs.find('div', class_='article-formatted-body article-formatted-body_version-1')
            for word in keywords:
                query = main_text.text.lower()
                result = query.find(word.lower())
                if result != -1:
                    print(f'\nposted on: {date_text}\ntitle: {title_text}\nlink: {url}')
                    print('__________________')
                    break


def main():
    headers = {
        'Cookie': '_ga=GA1.2.527592482.1639312656; _gid=GA1.2.835289500.1639312656; habr_web_home=ARTICLES_LIST_ALL; '
                  'hl=ru; fl=ru; _ym_uid=1639312656224064126; _ym_d=1639312656; _ym_isad=1; '
                  '__gads=ID=312d76c078dca362:T=1639312658:S=ALNI_MbM5e03aFoutbBy3BQQu7Kt0voEkA',
        'Host': 'habr.com',
        'If-None-Match': 'W/"36a18-LDgiqtRFiAh1+W+kvZfReZOhw48"',
        'Referer': 'https://github.com/netology-code/py-homeworks-advanced/tree/master/6.Web-scrapping',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.93 Safari/537.36'

    }
    keywords = ['wd', 'сеть', 'алгоритм']
    while True:
        cmd = input('\nWhere do you need to search? 1 - from preview, 2 - inside the article\n')
        if cmd == '1':
            search_preview(headers, keywords)
            break
        elif cmd == '2':
            search_full(headers, keywords)
            break
        else:
            print('Wrong input')


if __name__ == '__main__':
    main()
