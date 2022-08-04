import time
import warnings
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from pathlib import Path

mobile_emulation = {
   "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
   "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" 
}

warnings.filterwarnings("ignore", category=DeprecationWarning)
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
error_list=[]


def enable_stats_for_nerds(driver):

   settings = driver.find_element_by_xpath("/html/body/ytm-app/ytm-mobile-topbar-renderer/header/div/ytm-menu/button")
   settings.click()

   playback_settings = driver.find_element_by_xpath("/html/body/div[2]/div/ytm-menu-item[3]/button")
   playback_settings.click()

#    stats_for_nerds = driver.find_element_by_xpath("/html/body/div[2]/dialog/div[2]/ytm-menu-item[2]/button")
   stats_for_nerds=driver.execute_script("document.getElementsByClassName('menu-item-button')[1].click()")

   exit_dialog = driver.find_element_by_xpath("/html/body/div[2]/dialog/div[3]/c3-material-button/button")
   exit_dialog.click()

def start_playing_video(driver):
    player_state = driver.execute_script(
      "return document.getElementById('movie_player').getPlayerState()"
    )
    if player_state==5:
        driver.execute_script("document.getElementsByClassName('ytp-large-play-button ytp-button')[0].click()")
    else:
        raise Exception("Invalid state!")


def play_video_if_not_playing(driver):
   player_state = driver.execute_script(
      "return document.getElementById('movie_player').getPlayerState()"
   )    
   if player_state != 1:
      driver.execute_script(
         "document.getElementsByClassName('icon-button player-control-play-pause-icon')[0].click()"
      )

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
            skip_duration = (
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

    print(str(ad_id) == str(movie_id),ad_id,movie_id)
    while str(ad_id) == str(movie_id):
        ad_id = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
        )
        print(str(ad_id) == str(movie_id),ad_id,movie_id)

    # print("Ad Id is" + str(ad_id))
    return ad_id, skippable_add, skip_duration, start_resolution


def driver_code(driver):
    list_of_urls=[
        'https://www.youtube.com/watch?v=QEXycDe5abg', 
        'https://www.youtube.com/watch?v=0hktCJ64uH4', 
        'https://www.youtube.com/watch?v=gMhqxShOxpY', 
        'https://www.youtube.com/watch?v=Zhpk3ML7bIQ', 
        'https://www.youtube.com/watch?v=Cp-rJ6hGqlw', 
        'https://www.youtube.com/watch?v=wHiqO9LkeIM', 
        'https://www.youtube.com/watch?v=SUyzF0MidbQ', 
        'https://www.youtube.com/watch?v=1dbAMXOKt-A', 
        'https://www.youtube.com/watch?v=g4ppjLWHpFc', 
        "https://www.youtube.com/watch?v=8umKYwwKxjQ", 
        "https://www.youtube.com/watch?v=T-_zSI4OuJI", 
        "https://www.youtube.com/watch?v=-YDlvZAsHmc",
        "https://www.youtube.com/watch?v=J_qCRmQXJKs",
        "https://www.youtube.com/watch?v=BUEAKynYvx4",
        "https://www.youtube.com/watch?v=eXbjEl3xfMk"
    ]

    for index,url in enumerate(list_of_urls):
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
        time.sleep(2)
        
        #Enable Stats
        enable_stats_for_nerds(driver)
        #Start Playing Video
        start_playing_video(driver)

        ##Check If ad played at start
        time.sleep(0.5)
        ad_playing = driver.execute_script(
            "return document.getElementsByClassName('ad-showing').length"
        )
        print(movie_id)
        if ad_playing:
            print("ad at start of video!")
            ad_id, skippable, skip_duration, resolution = get_ad_info(driver, movie_id)
            while True:
                if ad_id == movie_id:
                    ad_id,_,_,_ = get_ad_info(driver,movie_id)
                else:
                    break
    
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
        
        ad_playing = driver.execute_script(
            "return document.getElementsByClassName('ad-showing').length"
        )
        if video_playing != 1 and not ad_playing:
            play_video_if_not_playing(driver)
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

            # if video_playing != 1 and not ad_playing:
            #     if video_playing != 0:
            #         play_video_if_not_playing(driver)

            if ad_playing:
                # Ad is being played
                ad_just_played = True
                # is_add_playing = driver.execute_script(
                #     'return document.getElementsByClassName("ytp-play-button ytp-button")[0].title'
                # )
                # if is_add_playing != "Pause (k)":
                #     driver.execute_script("document.getElementsByClassName('html5-video-container')[0].click()")

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
                # file_dir_two = new_dir + "/buffer_details.txt"
                file_dir_three = new_dir + "/error_details.txt"
                # file_dir_four = new_dir + "/ResolutionChanges.txt"
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

                # with open(file_dir_two, "w+") as f:
                #     f.write(json.dumps(actual_buffer_reads))

                with open(file_dir_three, "w+") as f:
                    f.write(json.dumps(error_list))

                # with open(file_dir_four, "w+") as f:
                #     f.write(json.dumps(vid_res_at_each_second))

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


driver = webdriver.Chrome(options=chrome_options)
driver_code(driver)
driver.quit()
