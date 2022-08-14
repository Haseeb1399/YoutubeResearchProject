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
            long_videos.append({'url': url, 'duration': video_duration})
            continue
        videos_not_so_long.append({'url': url, 'duration': video_duration})

    return videos_not_so_long, long_videos


def removeDuplicates(*argv):
    '''
    This function merges all lists of dictionaries, and removes duplicates from them
    '''
    temp_list = []
    for arg in argv:
        temp_list += arg

    seen = set()
    final_list = []
    for d in temp_list:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            final_list.append(d)
    return final_list


def sortList(final_list: list):
    '''
    This function takes the final list and sorts it according to the video duration
    '''
    new_list = [sorted(final_list, key=lambda d:d['duration'])]
    new_list = list(chain.from_iterable(new_list))
    return new_list


def main(driver: webdriver.Chrome):
    links_to_scrape_from = [
        "https://www.youtube.com/feed/trending",
        "https://www.youtube.com/feed/trending?bp=4gINGgt5dG1hX2NoYXJ0cw%3D%3D",
        "https://www.youtube.com/feed/trending?bp=4gIcGhpnYW1pbmdfY29ycHVzX21vc3RfcG9wdWxhcg%3D%3D",
        "https://www.youtube.com/feed/trending?bp=4gIKGgh0cmFpbGVycw%3D%3D",
    ]

    print('-- ALL TRENDING --')
    all_trending, _ = scrapeFromLink(
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
    music_trending_sorted = sortList(removeDuplicates(music_trending))
    gaming_trending_sorted = sortList(removeDuplicates(gaming_trending))
    films_trending_sorted = sortList(removeDuplicates(films_trending))

    music_urls = list(dict.fromkeys([a['url'] for a in music_trending_sorted]))
    gaming_urls = list(dict.fromkeys([a['url']
                       for a in gaming_trending_sorted]))
    films_urls = list(dict.fromkeys([a['url'] for a in films_trending_sorted]))

    # skipped videos
    # writing to all these seperate files
    print('-- WRITING TO music_only.txt --')
    with open('music_only.txt', 'w+') as f:
        for link in music_urls:
            f.write(f"'{link}',\n")

    print('-- WRITING TO gaming_only.txt')
    with open('gaming_only.txt', 'w+') as f:
        for link in gaming_urls:
            f.write(f"'{link}',\n")

    print('-- WRITING TO films_only.txt --')
    with open('films_only.txt', 'w+') as f:
        for link in films_urls:
            f.write(f"'{link}',\n")

    print('-- REMOVING DUPLICATES AND SORTING THE FINAL LIST --')
    final_list = sortList(removeDuplicates(
        all_trending, music_trending, gaming_trending, films_trending))

    final_lst = list(dict.fromkeys([a['url'] for a in final_list]))

    print('-- WRITING TO all_trending.txt --')
    # this is our main file
    with open('trending_all.txt', 'w+') as f:
        for link in final_lst:
            f.write(f"'{link}',\n")


if __name__ == '__main__':
    driver = webdriver.Chrome(options=options)
    main(driver)
    driver.quit()
    print('-- all videos have been scraped :)) --')
