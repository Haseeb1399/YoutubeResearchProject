'''
Connect to your designated developing country using NordVPN and run the script
Run the script

Code Author: Harris
'''


from selenium import webdriver
import pandas as pd
import time
import warnings
from bs4 import BeautifulSoup as BS
from pprint import pprint

warnings.filterwarnings("ignore", category=DeprecationWarning)
options = webdriver.ChromeOptions()

# this speeds up the optimization by stopping the images from loading
options.add_argument('--blank-settings=imagesEnabled=false')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
data = []


driver = webdriver.Chrome(options=options)
driver.get("https://www.youtube.com/feed/trending")

soup = BS(driver.page_source, features="lxml")
trending_videos: list = soup.find_all("a", id="video-title")

for vid in trending_videos:
    data.append({"title": vid['title'], "url": vid['href']})


time.sleep(2)
driver.quit()

final_data = []
# removing shorts from the dictionary
for vid in data:
    if vid['url'][0:7] == '/shorts':
        continue
    temp_url = vid['url']
    temp = f'https://www.youtube.com{temp_url}'
    final_data.append({"title": vid['title'], "url": temp})


df = pd.DataFrame(final_data)
pprint(df)

# writing to the trending.txt file
with open('trending.txt', 'w') as f:
    for vid in final_data:
        url = vid['url']
        f.write(f"'{url}',\n")
