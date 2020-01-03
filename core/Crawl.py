#!/usr/bin/python3
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
import sys
import requests
import argparse


# save content to file url method
def saveFile(data):
    path = Path()/args['directory']/f'data{data[0]}.txt'
    with open(path, 'w') as file:
        soup = BeautifulSoup(requests.get(data[1]).text, 'html.parser')
        content = soup.select_one('.read__content')
        for i in content('script'):
            i.decompose()
        title = soup.select_one('.read__title').get_text().strip(
        )
        content = content.get_text().strip()
        file.write(title+'\n')
        file.write(content)


# argument documentary
arg = argparse.ArgumentParser()
arg.add_argument("directory", help="Directory output all crawl file")
option = arg.add_mutually_exclusive_group()
option.add_argument("-p", "--page-limit",
                    help="limit file by number of files", type=int)
option.add_argument("-d", "--day-limit",
                    help="limit file by days backward", type=int)
args = vars(arg.parse_args())

# dinamic link
indexlink = "http://indeks.kompas.com/terpopuler/?site=all&date="

# get time of today
date = datetime.today()

# number of day and limit
day, day_limit = 1, args['day_limit'] if args['day_limit'] != None else None

# number of page and limit
page, page_limit = 0, args['page_limit'] if args['page_limit'] != None else None

# looping to get dynamic link by time
with open('../data/link/link.txt', 'w') as file:
    while True:
        link = f'{indexlink}{date.strftime("%Y-%m-%d")}'
        # looping to get all detail link
        while True:
            print(f'Getting url from : {link}')
            soup = BeautifulSoup(requests.get(
                link).text.encode('utf-8'), 'html.parser')
            print("Url found      : ", len(soup.select('.article__title')))
            for url in soup.select('.article__title'):
                urls = url.find('a')['href']
                file.write(urls+'\n')
                try:
                    # clean url and put on directory
                    saveFile([page+1, urls])
                except AttributeError:
                    print('error atribute..')
                page += 1
                if page == page_limit:
                    sys.exit(f'Program reach maximum {page_limit} page')
            else:
                break
        if day == day_limit:
            sys.exit(f'Program reach maximum {day_limit} day')
        date += timedelta(days=-1)
        day += 1
