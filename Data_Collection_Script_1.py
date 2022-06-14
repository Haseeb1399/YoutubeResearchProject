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
        # "https://www.youtube.com/watch?v=7XpyUV6BfMA",
        # "https://www.youtube.com/watch?v=a-66x7RjlGE",
        # "https://www.youtube.com/watch?v=eL7QpeT2ITE",
        # "https://www.youtube.com/watch?v=scWWtJ5yic0",
        # "https://www.youtube.com/watch?v=IRpxHYEt-xk",
        # "https://www.youtube.com/watch?v=PxVZf_lbVCM",
        # "https://www.youtube.com/watch?v=OFywZLXUceM",
        # "https://www.youtube.com/watch?v=K0DxVEQiQx4",
        # "https://www.youtube.com/watch?v=LPntr-moiBM",
        # "https://www.youtube.com/watch?v=7SKfpXpW2Bc",
        # "https://www.youtube.com/watch?v=kXpOEzNZ8hQ",
        # "https://www.youtube.com/watch?v=dsOfWhdSmXQ",
        # "https://www.youtube.com/watch?v=wMICplh-bhw",
        # "https://www.youtube.com/watch?v=7G_aNAd9IiQ",
        # "https://www.youtube.com/watch?v=NjUNo2U55D0",
        # "https://www.youtube.com/watch?v=PYYWWivHORQ",
        # "https://www.youtube.com/watch?v=VajZGDxMgfk",
        # "https://www.youtube.com/watch?v=GdoBJbjIWRQ",
        # "https://www.youtube.com/watch?v=0nOrTI3WT1s",
        # "https://www.youtube.com/watch?v=t8YQvdQa_mA",
        # "https://www.youtube.com/watch?v=EcSBD5dLbOA",
        # "https://www.youtube.com/watch?v=PnW6kcl4Yp8",
        # "https://www.youtube.com/watch?v=ig6NiVr7TpE",
        # "https://www.youtube.com/watch?v=_WlgWvWSgos",
        # "https://www.youtube.com/watch?v=QUVZ6hnEPQc",
        # "https://www.youtube.com/watch?v=Eu65eY3Fvgo",
        # "https://www.youtube.com/watch?v=Aa-Frqm4eQU",
        # "https://www.youtube.com/watch?v=RdvIsNUtNzk",
        # "https://www.youtube.com/watch?v=7IV9CeorNqU",
        # "https://www.youtube.com/watch?v=AC1gxPDRmv4",
        # "https://www.youtube.com/watch?v=NK9Cz_mdms8",
        # "https://www.youtube.com/watch?v=z2EOZOxC6VE",
        # "https://www.youtube.com/watch?v=29mOKSd0f-E",
        # "https://www.youtube.com/watch?v=izb0NbfuUr8",
        # "https://www.youtube.com/watch?v=8sdV6sTq_Jc",
        # "https://www.youtube.com/watch?v=rfOmB9tx3Bc",
        # "https://www.youtube.com/watch?v=kwlGsNyr5e8",
        # "https://www.youtube.com/watch?v=ZIzP-IHLbAU",
        # "https://www.youtube.com/watch?v=gmgbU-zj-FI",
        # "https://www.youtube.com/watch?v=tpStfn9MLDM",
        # "https://www.youtube.com/watch?v=k9p9yL9RbIM",
        # "https://www.youtube.com/watch?v=qVUgtDqCwKM",
        # "https://www.youtube.com/watch?v=psLxq1-y-Uw",
        # "https://www.youtube.com/watch?v=0h9GDCoyyJs",
        # "https://www.youtube.com/watch?v=wjhBeaCkscg",
        # "https://www.youtube.com/watch?v=TuBQoU26-LQ",
        # "https://www.youtube.com/watch?v=jMl3hphx8GI",
        # "https://www.youtube.com/watch?v=hmIlskBr1Hw",
        # "https://www.youtube.com/watch?v=Hwybp38GnZw",
        # "https://www.youtube.com/watch?v=nZX8mY251nw",
        # "https://www.youtube.com/watch?v=tpFljbJxZiw",
        # "https://www.youtube.com/watch?v=6xoB4ZiKKn0",
        "https://www.youtube.com/watch?v=c6ri-MFdNLY",
        "https://www.youtube.com/watch?v=7FVaxc-4-FQ",
        "https://www.youtube.com/watch?v=OXHCt8Ym9gw",
        "https://www.youtube.com/watch?v=IYQ42VKfR0U",
        "https://www.youtube.com/watch?v=uY9gP3ZG20w",
        "https://www.youtube.com/watch?v=guN4GPzFmoI",
        "https://www.youtube.com/watch?v=qUmt7OSHM50",
        "https://www.youtube.com/watch?v=-Hb0tcPNki8",
        "https://www.youtube.com/watch?v=q3nIItk0-wU",
        "https://www.youtube.com/watch?v=jU11bwiJl_8",
        "https://www.youtube.com/watch?v=OAti-mH_QZY",
        "https://www.youtube.com/watch?v=Z71k9rfJQ1c",
        "https://www.youtube.com/watch?v=hyrNWGY8YFc",
        "https://www.youtube.com/watch?v=2ymz6PiCWIw",
        "https://www.youtube.com/watch?v=qMBGouonBnA",
        "https://www.youtube.com/watch?v=Tb6xGDiSscc",
        "https://www.youtube.com/watch?v=bSAlE_WgHxY",
        "https://www.youtube.com/watch?v=BwEbIu5b4Ds",
        "https://www.youtube.com/watch?v=YOyJKLMCXKA",
        "https://www.youtube.com/watch?v=VCgeokWbRfc",
        "https://www.youtube.com/watch?v=3Ml0DrBH9h8",
        "https://www.youtube.com/watch?v=082UkRjqojw",
        "https://www.youtube.com/watch?v=CjGcIAnuH1M",
        "https://www.youtube.com/watch?v=45kSKBfA3Jo",
        "https://www.youtube.com/watch?v=OYe9vYhsGws",
        "https://www.youtube.com/watch?v=Y2548TkfH8k",
        "https://www.youtube.com/watch?v=xZQ_Qw2IJOQ",
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
        time.sleep(0.5)
        if video_playing != 1:
            print("Video has now started playing")
            movie_player.send_keys(Keys.SPACE)
        else:
            print("Video is already playing")

        time.sleep(0.5)

        video_duration_in_seconds = driver.execute_script(
            'return document.getElementById("movie_player").getDuration()'
        )
        if video_duration_in_seconds > 3600:
            continue

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

            time.sleep(0.5)
            ad_playing = driver.execute_script(
                "return document.getElementsByClassName('ad-showing').length"
            )
            time.sleep(0.5)
            video_played_in_seconds = driver.execute_script(
                'return document.getElementById("movie_player").getCurrentTime()'
            )
            # print(video_playing)
            if video_playing != 1 and not ad_playing:
                if video_playing != 0:
                    movie_player.send_keys(Keys.SPACE)

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
                                video_url,
                                new_dir,
                                video_name,
                                (ad_id.strip()),
                                resolution,
                            )

                        else:
                            current_value = video_info_details[ad_id]["Count"]
                            video_info_details[ad_id]["Count"] = current_value + 1

            elif video_playing == 0:
                # Video has ended
                file_dir = new_dir + "/stream_details.txt"
                file_dir_two = new_dir + "/buffer_details.txt"
                file_dir_three = new_dir + "/error_details.txt"
                file_dir_four = new_dir + "/ResolutionChanges.txt"
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

                with open(file_dir_four, "w+") as f:
                    f.write(json.dumps(vid_res_at_each_second))

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
