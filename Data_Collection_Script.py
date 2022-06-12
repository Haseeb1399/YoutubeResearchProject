"""
Author: Haseeb Ahmed 23100035 @ lums.edu.pk
"""


import time
from unittest import skip
from black import err
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from pytube import YouTube
from pathlib import Path

import warnings
import json


warnings.filterwarnings("ignore", category=DeprecationWarning)
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

error_list = []


def download_video(video_url, folder_name, type_of, video_id, resolution):
    try:
        res = resolution.split("x")[1].split("@")[0]
        res = res + "p"
        print("Downloading Video " + type_of, video_url, "at ", res)
        video_name = type_of + "@" + video_id + ".mp4"
        yt = YouTube(video_url)
        yt.streams.filter(res=res, file_extension="mp4").first().download(
            folder_name, video_name
        )
        print("Downloaded! " + type_of)
        return video_name
    except:
        data = (video_url, resolution, folder_name)
        error_list.append(data)
        print("Error in Downloading!")


def get_ad_info(driver, movie_id):
    # print("Inside Video info", movie_id)

    ad_id = driver.execute_script(
        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
    )
    skippable_add = driver.execute_script(
        'return document.getElementsByClassName("ytp-ad-skip-button-container").length'
    )
    if skippable_add:
        try:
            skip_duration = int(
                driver.execute_script(
                    'return document.getElementsByClassName("ytp-ad-text ytp-ad-preview-text")[0].innerText'
                )
            )
        except:
            skip_duration = -2  # Error occured, Could not get Skip Duration
    else:
        skip_duration = -1  # Add was not skippable.

    start_resolution = driver.execute_script(
        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
    )
    time.sleep(1)
    while str(ad_id) == str(movie_id):
        ad_id = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
        )

    # print("Ad Id is" + str(ad_id))
    return ad_id, skippable_add, skip_duration, start_resolution


def driver_code(driver):

    list_of_urls = [
        "https://www.youtube.com/watch?v=z2WcI2Hr_Co",
        "https://www.youtube.com/watch?v=fL-XnEuXajY",
        "https://www.youtube.com/watch?v=Kygad1DiJ04",
        "https://www.youtube.com/watch?v=fQjertX8xjM",
        "https://www.youtube.com/watch?v=WcOJ2mRlg4Y",
        "https://www.youtube.com/watch?v=wvz97-lNPH8",
        "https://www.youtube.com/watch?v=Lq1xEf9wWEY",
        "https://www.youtube.com/watch?v=_WWsKXmttEw",
        "https://www.youtube.com/watch?v=m1r6WysI1cQ",
        "https://www.youtube.com/watch?v=OXHCt8Ym9gw",
        "https://www.youtube.com/watch?v=a_BEn1G2d5o",
        "https://www.youtube.com/watch?v=0x_5vG7SUKE",
        "https://www.youtube.com/watch?v=vdWLp2wKEa4",
        "https://www.youtube.com/watch?v=NgsWGfUlwJI",
        "https://www.youtube.com/watch?v=7uTk-oCNfTI",
        "https://www.youtube.com/watch?v=VwlFSBpJRsM",
        "https://www.youtube.com/watch?v=Tr6VA3A8PcU",
        "https://www.youtube.com/watch?v=MWNpBHATT-w",
        "https://www.youtube.com/watch?v=Hwybp38GnZw",
        "https://www.youtube.com/watch?v=VNVV41VIBV8",
        "https://www.youtube.com/watch?v=9eE0GTSsNrk",
        "https://www.youtube.com/watch?v=R77hSoAyXeY",
        "https://www.youtube.com/watch?v=6W0VySsuc94",
        "https://www.youtube.com/watch?v=LdJeg54DWWY",
        "https://www.youtube.com/watch?v=0Ix1vRaqva4",
        "https://www.youtube.com/watch?v=o0xuJK1VMAM",
        "https://www.youtube.com/watch?v=j2gAVtEe-QU",
        "https://www.youtube.com/watch?v=N6tv11_KMiM",
        "https://www.youtube.com/watch?v=HgrC_h8-2FM",
        "https://www.youtube.com/watch?v=DVXdc5Wxv5k",
        "https://www.youtube.com/watch?v=40q1eiOlzi4",
        "https://www.youtube.com/watch?v=aJiRhUPTAUM",
        "https://www.youtube.com/watch?v=U2BoSsIyyks",
        "https://www.youtube.com/watch?v=-_b72e4mV-g",
        "https://www.youtube.com/watch?v=2lpPFLxhTkw",
        "https://www.youtube.com/watch?v=VFCwRBonQiM",
        "https://www.youtube.com/watch?v=a4MugKAb_dM",
        "https://www.youtube.com/watch?v=EgoRy9YcwUg",
        "https://www.youtube.com/watch?v=aXYQcYRsZiQ",
        "https://www.youtube.com/watch?v=OkcAGO6gHIk",
        "https://www.youtube.com/watch?v=Mva_NeLchRg",
        "https://www.youtube.com/watch?v=kgDjUv9bBu4",
        "https://www.youtube.com/watch?v=YdZkLJi9fuk",
        "https://www.youtube.com/watch?v=Lvea6VTC_M0",
    ]

    for index, url in enumerate(list_of_urls):
        global error_list
        error_list = []
        new_dir = "./" + str(index + 1)

        # Opening Browser
        driver.get(url)
        Path(new_dir).mkdir(parents=False, exist_ok=True)  # Making Directory

        time.sleep(5)  # Wait

        # Hover over the video element
        movie_player = driver.find_element_by_id("movie_player")
        hover = ActionChains(driver).move_to_element(movie_player)
        hover.perform()

        # Right Click and select stats for nerds

        ActionChains(driver).context_click(movie_player).perform()
        options = driver.find_elements_by_class_name("ytp-menuitem")
        for option in options:
            option_child = option.find_element_by_class_name("ytp-menuitem-label")
            if option_child.text == "Stats for nerds":
                option_child.click()
                print("Enabled stats collection.")

        time.sleep(2)
        video_playing = driver.execute_script(
            "return document.getElementById('movie_player').getPlayerState()"
        )

        if video_playing != 1:
            print("Video has now started playing")
            movie_player.send_keys(Keys.SPACE)
        else:
            print("Video is already playing")

        time.sleep(0.5)

        video_duration_in_seconds = driver.execute_script(
            'return document.getElementById("movie_player").getDuration()'
        )

        video_info_details = {}
        unique_add_count = 0
        original_downloaded = False
        previous_ad_id = url.split("=")[1]
        buffer_list = []
        actual_buffer_reads = []
        vid_res_at_each_second = []
        Main_res = None

        while True:
            time.sleep(0.5)
            video_playing = driver.execute_script(
                "return document.getElementById('movie_player').getPlayerState()"
            )
            if video_playing != 1:
                if video_playing != 0:
                    movie_player.send_keys(Keys.SPACE)

            time.sleep(0.5)
            ad_playing = driver.execute_script(
                "return document.getElementsByClassName('ad-showing').length"
            )
            time.sleep(0.5)
            video_played_in_seconds = driver.execute_script(
                'return document.getElementById("movie_player").getCurrentTime()'
            )

            if ad_playing:
                # Ad is being played
                time.sleep(1)
                movie_id = url.split("=")[1]
                time.sleep(1)
                ad_id, skippable, skip_duration, resolution = get_ad_info(
                    driver, movie_id
                )

                if (str(ad_id).strip()) != (str(movie_id).strip()):
                    if ad_id != previous_ad_id:
                        print("Ad id is: ", ad_id)
                        previous_ad_id = ad_id

                        if ad_id not in video_info_details.keys():
                            unique_add_count += 1
                            video_info_details[ad_id] = {
                                "Count": 1,
                                "Skippable": skippable,
                                "SkipDuration": skip_duration,
                                "Resolution": resolution,
                            }
                            video_url = "https://www.youtube.com/watch?v=" + ad_id
                            video_name = "Advertisement" + "@" + str(unique_add_count)
                            download_video(
                                video_url, new_dir, video_name, ad_id, resolution
                            )

                        else:
                            current_value = video_info_details[ad_id]["Count"]
                            video_info_details[ad_id]["Count"] = current_value + 1

            elif video_playing == 0:
                # Video has ended
                file_dir = new_dir + "/stream_details.txt"
                file_dir_two = new_dir + "/buffer_details.txt"
                file_dir_three = new_dir + "/error_details.txt"
                video_info_details["Main_Video"] = {
                    "Url": url,
                    "Total Duration": video_duration_in_seconds,
                    "UniqueAds": unique_add_count,
                    "AvgBuffer": (sum(buffer_list) / len(buffer_list)),
                    "Resolution": Main_res,
                }
                with open(file_dir, "w+") as f:
                    f.write(json.dumps(video_info_details))

                with open(file_dir_two, "w+") as f:
                    f.write(json.dumps(actual_buffer_reads))

                with open(file_dir_three, "w+") as f:
                    f.write(json.dumps(error_list))

                video_info_details = {}
                unique_add_count = 0
                original_downloaded = False
                break
            else:
                # Video is playing normally

                # Record Resolution at each second
                res = driver.execute_script(
                    'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
                )

                new_data_point = (res, video_played_in_seconds)

                vid_res_at_each_second.append(new_data_point)

                ##Get Current Buffer
                current_buffer = float(
                    driver.execute_script(
                        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[10].children[1].textContent.split(" ")[1]'
                    )
                )
                # Actual Buffer
                actual_buffer_reads.append(current_buffer)
                # Current Buffer/(Video Left)
                try:
                    buffer_ratio = float(
                        current_buffer
                        / (video_duration_in_seconds - video_played_in_seconds)
                    )
                except:
                    buffer_ratio = 0

                buffer_list.append(buffer_ratio)

                ##To download the Main Video Only once.
                if original_downloaded == False and (
                    (video_played_in_seconds / video_duration_in_seconds)
                    > 0.3  # Downloads if 30% of Movie has been played.
                ):
                    video_name = "MainVideo"
                    Main_res = res
                    download_video(url, new_dir, video_name, (url.split("=")[1]), res)
                    original_downloaded = True

                previous_ad_id = url.split("=")[1]


driver = webdriver.Chrome(options=options)
driver_code(driver)
driver.quit()
"""

Step 1: Load Video
Step 2: Right Click and Enable Stats for Nerds
Step 3: Identify if the video playing is an Ad or not.
Step 3: Get Video ID
Step 4: While video plays, Keep checking if ad being played or not

"""
