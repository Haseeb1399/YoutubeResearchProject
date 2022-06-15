"""
Author: Haseeb Ahmed 23100035 @ lums.edu.pk
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from collections import Counter
from pathlib import Path

import warnings
import json

warnings.filterwarnings("ignore", category=DeprecationWarning)
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

error_list = []


def get_ad_info(driver, movie_id):
    # print("Inside Video info", movie_id)

    ad_id = driver.execute_script(
        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
    )
    time.sleep(0.3)
    skippable_add = driver.execute_script(
        'return document.getElementsByClassName("ytp-ad-skip-button-container").length'
    )
    print("Add is skippable? ",skippable_add)
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
        skip_duration = 999  # Add was not skippable.

    start_resolution = driver.execute_script(
        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
    )
    start_resolution_check = start_resolution.split("@")[0]

    attempt_count = 0
    while start_resolution_check == "0x0" or attempt_count<10:
        start_resolution = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
        )
        start_resolution_check = start_resolution
        attempt_count+=1

    time.sleep(0.5)
    while str(ad_id) == str(movie_id):
        ad_id = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
        )

    # print("Ad Id is" + str(ad_id))
    return ad_id, skippable_add, skip_duration, start_resolution


def driver_code(driver):
    list_of_urls = [
        "https://www.youtube.com/watch?v=FkheNrTgo6I",
        "https://www.youtube.com/watch?v=QUVZ6hnEPQc"
    ]

    for index, url in enumerate(list_of_urls):
        global error_list
        video_info_details = {}
        error_list = []
        unique_add_count = 0
        ad_just_played = False
        buffer_list = []
        actual_buffer_reads = []
        buffer_size_with_ad = []
        vid_res_at_each_second = []
        main_res_all = []
        previous_ad_id = url.split("=")[1]

        movie_id = url.split("=")[1]
        new_dir = "./" + str(index + 1)

        driver.get(url)

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

        time.sleep(0.2)
        ad_playing = driver.execute_script(
            "return document.getElementsByClassName('ad-showing').length"
        )
        if ad_playing:
            ad_id, skippable, skip_duration, resolution = get_ad_info(driver, movie_id)
            if ad_id not in video_info_details.keys():
                unique_add_count += 1
                video_info_details[ad_id] = {
                    "Count": 1,
                    "Skippable": skippable,
                    "SkipDuration": skip_duration,
                    "Resolution": resolution,
                }
                buffer_size_with_ad.append(
                    [ad_id,0.0] #Start of video. Main Buffer will be 0s.
                )
                previous_ad_id = ad_id
                print("Advertisement " + str(unique_add_count) + " Data collected.")

        time.sleep(0.5)

        video_duration_in_seconds = driver.execute_script(
            'return document.getElementById("movie_player").getDuration()'
        )
        if video_duration_in_seconds >= 3600:
            print(
                video_duration_in_seconds, " Seconds. Video Skipped for being too Long!"
            )
            continue

        Path(new_dir).mkdir(parents=False, exist_ok=True)

        video_playing = driver.execute_script(
            "return document.getElementById('movie_player').getPlayerState()"
        )
        time.sleep(0.5)
        if video_playing != 1:
            print("Video has now started playing")
            movie_player.send_keys(Keys.SPACE)
        else:
            print("Video is already playing")

        while True:
            # time.sleep(0.5)
            video_playing = driver.execute_script(
                "return document.getElementById('movie_player').getPlayerState()"
            )

            # time.sleep(0.5)
            ad_playing = driver.execute_script(
                "return document.getElementsByClassName('ad-showing').length"
            )
            # time.sleep(0.5)
            video_played_in_seconds = driver.execute_script(
                'return document.getElementById("movie_player").getCurrentTime()'
            )

            if video_playing != 1 and not ad_playing:
                if video_playing != 0:
                    movie_player.send_keys(Keys.SPACE)

            if ad_playing:
                # Ad is being played
                ad_just_played = True
                is_add_playing = driver.execute_script(
                    'return document.getElementsByClassName("ytp-play-button ytp-button")[0].title'
                )
                if is_add_playing != "Pause (k)":
                    movie_player.send_keys(Keys.SPACE)

                time.sleep(0.5)
                ad_id, skippable, skip_duration, resolution = get_ad_info(
                    driver, movie_id
                )

                if (str(ad_id).strip()) != (str(movie_id).strip()):
                    if ad_id != previous_ad_id:
                        print("Ad id is: ", ad_id)
                        previous_ad_id = ad_id
                        if len(actual_buffer_reads) >= 1:
                            buffer_size_with_ad.append(
                                [ad_id, actual_buffer_reads[-1]]
                            )  # Append last buffer value to keep track.
                        else:
                            buffer_size_with_ad.append(
                                [ad_id, "-1"]
                            )  # Ad was at the start.

                        if ad_id not in video_info_details.keys():
                            unique_add_count += 1
                            video_info_details[ad_id] = {
                                "Count": 1,
                                "Skippable": skippable,
                                "SkipDuration": skip_duration,
                                "Resolution": resolution,
                            }
                            print(
                                "Advertisement "
                                + str(unique_add_count)
                                + " Data collected."
                            )
                        else:
                            current_value = video_info_details[ad_id]["Count"]
                            video_info_details[ad_id]["Count"] = current_value + 1
                            print("Count of existing add increased!")

            elif video_playing == 0:
                # Video has ended
                file_dir = new_dir + "/stream_details.txt"
                file_dir_two = new_dir + "/buffer_details.txt"
                file_dir_three = new_dir + "/error_details.txt"
                file_dir_four = new_dir + "/ResolutionChanges.txt"
                file_dir_five = new_dir + "/BufferAdvert.txt"
                Main_res = max(main_res_all, key=main_res_all.count)
                video_info_details["Main_Video"] = {
                    "Url": url,
                    "Total Duration": video_duration_in_seconds,
                    "UniqueAds": unique_add_count,
                    "AvgBuffer": (sum(actual_buffer_reads) / len(actual_buffer_reads)),
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

                with open(file_dir_five, "w+") as f:
                    f.write(json.dumps(buffer_size_with_ad))
                video_info_details = {}
                unique_add_count = 0
                break
            else:
                # Video is playing normally

                # Record Resolution at each second
                res = driver.execute_script(
                    'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
                )

                new_data_point = (res, video_played_in_seconds)
                main_res_all.append(res)
                vid_res_at_each_second.append(new_data_point)

                # Get Current Buffer
                current_buffer = float(
                    driver.execute_script(
                        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[10].children[1].textContent.split(" ")[1]'
                    )
                )
                # Actual Buffer
                if ad_just_played:
                    for i in range(len(buffer_size_with_ad)):
                        if len(buffer_size_with_ad[i]) <= 2:
                            buffer_size_with_ad[i].append(current_buffer)

                    ad_just_played = False

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
                previous_ad_id = url.split("=")[1]


driver = webdriver.Chrome(options=options)
driver_code(driver)
driver.quit()
