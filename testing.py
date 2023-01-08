import requests
import shutil
from tqdm import tqdm
import time
import re
import os


SERIES_IN_SEASON = [10] * 6 + [7, 6]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}
session = requests.Session()

def get_links (url):
    global session
    session.close()
    try:
        resp = session.get(url, headers = headers)
    except:
        session.close()
        time.sleep(10)
        resp = session.get(url, headers = headers)

    url = re.sub(r'/index\S*\.m3u8','',url) + '/'

    file = str(resp.content).split (r'\n')
    links = []
    for line in file:
        if '.ts' in line:
            links.append(url + line)
    session.close()
    return links


def create_files (links, path):
    global session
    session.close()
    with open(path, 'wb') as merged:
        for url in tqdm(range(len(links))):
            try:
                resp = session.get(links[url], headers = headers)
            except:
                session.close()
                time.sleep(10)
                resp = session.get(links[url], headers = headers)
            with open('2.ts', 'wb') as new_m:
                new_m.write(resp.content)
            with open('2.ts', 'rb') as new_m:
                shutil.copyfileobj(new_m, merged)
            if (url % 45 == 0):
                time.sleep(5)
                session.close()
        try:
            os.remove('2.ts')
        except:
            pass

def main():
    fr = int(input())
    fr2 = int(input())
    path = 'Игра престолов'
    if not os.path.exists(path):
        os.makedirs(path)
    for season in range(fr, len(SERIES_IN_SEASON) + 1):
        locp = path + '/Сезон ' + str (season)
        if not os.path.exists(locp):
            os.makedirs(locp)
        links = []
        for seria in range (fr2, SERIES_IN_SEASON[season-1] + 1):
            links.append(input())
        for link in range (len(links)):
            create_files(get_links (links[link]), locp + '/Серия ' + str (link + fr2) + '.ts')
            session.close()
            time.sleep(60)
        fr2 = 1

            


if __name__ == '__main__':
    main()
