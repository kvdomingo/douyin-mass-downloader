import json
import requests
from tqdm import tqdm
from selenium import webdriver


def main() -> None:
    with open('list.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    short_data = []
    for video in data['aweme_list']:
        short_data.append({'id': video['aweme_id'], 'url': video['share_url']})
    with open('src.json', 'w', encoding='utf-8') as f:
        json.dump(short_data, f, indent=2)
    data = short_data

    driver = webdriver.Firefox()
    driver.implicitly_wait(5)
    for dat in tqdm(data):
        driver.get(dat['url'])
        element = driver.find_element('css selector', 'video')
        src = element.get_attribute('src')
        res = requests.get(src, stream=True)
        with open(f'download/{dat["id"]}.mp4', 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    driver.close()


if __name__ == '__main__':
    main()
