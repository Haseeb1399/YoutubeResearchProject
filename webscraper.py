'''
Connect to your designated developing country using NordVPN and run the script
Note: this webscraper runs for an approximate of 5-6 minutes (depending on your connection speed
and CPU's job scheduling). Do NOT remove time.sleep() calls from this source.

Edit: This final list is sorted according to the video durations

Code Author: Harris (24100315)
'''

from selenium import webdriver
import time
import warnings
from bs4 import BeautifulSoup as BS
import time
from itertools import chain
import random

warnings.filterwarnings("ignore", category=DeprecationWarning)
options = webdriver.ChromeOptions()
options.headless = False

# this speeds up the optimization by stopping the images from loading
options.add_argument('--blank-settings=imagesEnabled=false')
options.add_experimental_option("excludeSwitches", ["enable-logging"])

links_to_scrape_from = [
    "https://www.youtube.com/feed/trending",
    "https://www.youtube.com/feed/trending?bp=4gINGgt5dG1hX2NoYXJ0cw%3D%3D",
    "https://www.youtube.com/feed/trending?bp=4gIcGhpnYW1pbmdfY29ycHVzX21vc3RfcG9wdWxhcg%3D%3D",
    "https://www.youtube.com/feed/trending?bp=4gIKGgh0cmFpbGVycw%3D%3D",
]


def scrapeFromLink(driver: webdriver.Chrome, url: str):
    '''
    @returns: tuple(dict,dict)
    '''
    driver.get(url)
    sleep_time = 10
    print(f'-- sleeping for {sleep_time} seconds --')
    time.sleep(sleep_time)
    data = []
    soup = BS(driver.page_source, features="lxml")
    trending_videos: list = soup.find_all('a', id='video-title')
    for vid in trending_videos:
        data.append({'title': vid['title'], 'url': vid['href']})

    time.sleep(2)

    final_data = []
    for vid in data:
        if vid['url'][0:7] == '/shorts':
            continue
        temp_url = vid['url']
        temp = f'https://www.youtube.com{temp_url}'
        final_data.append({"title": vid['title'], "url": temp})

    videos_not_so_long = []
    long_videos = []

    for vid in final_data:
        url = vid['url']
        driver.get(url)
        video_duration = driver.execute_script(
            'return document.getElementById("movie_player").getDuration()'
        )
        if video_duration >= 3600:
            print(f'Video {url} skipped for being too long!')
            long_videos.append(url)
            continue
        videos_not_so_long.append(url)

    return videos_not_so_long, long_videos


def removeDuplicates(lst: list):
    to_return = list(dict.fromkeys(lst))
    return to_return


def writeToFile(filename: str, urls: list):
    print(f'-- WRITING TO {filename} --')
    with open(filename, 'w+') as f:
        for url in urls:
            f.write(f"'{url}',\n")


def main(driver: webdriver.Chrome):
    links_to_scrape_from = [
        "https://www.youtube.com/feed/trending",
        "https://www.youtube.com/feed/trending?bp=4gINGgt5dG1hX2NoYXJ0cw%3D%3D",
        "https://www.youtube.com/feed/trending?bp=4gIcGhpnYW1pbmdfY29ycHVzX21vc3RfcG9wdWxhcg%3D%3D",
        "https://www.youtube.com/feed/trending?bp=4gIKGgh0cmFpbGVycw%3D%3D",
    ]

    print('-- ALL TRENDING --')
    # this also includes videos that are not related to any of them three categories
    general_trending, _ = scrapeFromLink(
        driver, links_to_scrape_from[0])

    print('-- MUSIC ONLY --')
    music_trending, _ = scrapeFromLink(
        driver, links_to_scrape_from[1])

    print('-- GAMING ONLY --')
    gaming_trending, _ = scrapeFromLink(
        driver, links_to_scrape_from[2])

    print('-- FILMS ONLY--')
    films_trending, _ = scrapeFromLink(
        driver, links_to_scrape_from[3])

    # maintaing separate text files for all three categories
    # usable list
    music_trending = removeDuplicates(music_trending)
    gaming_trending = removeDuplicates(gaming_trending)
    films_trending = removeDuplicates(films_trending)
    general_trending = removeDuplicates(general_trending)

    # skipped videos
    # writing to all these seperate files
    writeToFile('music_only.txt', music_trending)
    writeToFile('gaming_only.txt', gaming_trending)
    writeToFile('films_only.txt', films_trending)
    writeToFile('general_urls.txt', general_trending)

    # picking randomly from the four lists
    temp_list = random.sample(music_trending, 15) + random.sample(gaming_trending, 15) + \
        random.sample(films_trending, 15) + random.sample(general_trending, 15)

    # removing suplicates and sorting the lists
    temp_list = removeDuplicates(temp_list)
    random.shuffle(temp_list)
    final_list = temp_list
    writeToFile('usable.txt', final_list)


if __name__ == '__main__':
    driver = webdriver.Chrome(options=options)
    main(driver)
    driver.quit()
    print('-- all videos have been scraped :)) --')
