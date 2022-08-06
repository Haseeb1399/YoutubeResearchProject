import warnings
import orjson
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from pathlib import Path

mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
}

warnings.filterwarnings("ignore", category=DeprecationWarning)
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
error_list = []


def enable_stats_for_nerds(driver: webdriver.Chrome):
    '''
    This function locates and enables stats for nerds
    '''
    settings = driver.find_element_by_xpath(
        "/html/body/ytm-app/ytm-mobile-topbar-renderer/header/div/ytm-menu/button")
    settings.click()

    playback_settings = driver.find_element_by_xpath(
        "/html/body/div[2]/div/ytm-menu-item[3]/button")
    playback_settings.click()

# on the settings page, navigate to the stats for nerds option
    stats_for_nerds = driver.find_element_by_xpath(
        "/html/body/div[2]/dialog/div[2]/ytm-menu-item[2]/button")
    # click on stats
    stats_for_nerds.click()
    exit_dialog = driver.find_element_by_xpath(
        "/html/body/div[2]/dialog/div[3]/c3-material-button/button")
    exit_dialog.click()


def start_playing_video(driver: webdriver.Chrome):
    '''
    This function gets the state of the player and starts playing the video
    '''
    player_state = driver.execute_script(
        "return document.getElementById('movie_player').getPlayerState()"
    )
    if player_state == 5:
        play = driver.find_element_by_xpath("/html/body/div[@id='player-container-id']/div[@id='player']/div[@id='movie_player']/div[@class='ytp-cued-thumbnail-overlay']/button[@class='ytp-large-play-button ytp-button']")
        play.click()
    else:
        raise Exception("Invalid state!")


def play_video_if_not_playing(driver: webdriver.Chrome):
    '''
    This function hovers over the youtube player, and plays the video
    '''
    player_state = driver.execute_script(
        "return document.getElementById('movie_player').getPlayerState()"
    )
    if player_state != 1:
        movie_player = driver.find_element_by_id("movie_player")
        hover = ActionChains(driver).move_to_element(movie_player)
        hover.perform()
        ActionChains(driver).context_click(movie_player).perform()

        # now click on the large play button
        large_play_button = driver.find_element_by_xpath("/html/body/div[@id='player-container-id']/div[@id='player-control-container']/ytm-custom-control/div[@id='player-control-overlay']/div[@class='player-controls-content']/div[4]/div[@class='player-controls-middle center']/button[@class='icon-button player-control-play-pause-icon']/c3-icon/svg[@class='[object SVGAnimatedString]']/g[@class='[object SVGAnimatedString]']/path[@class='[object SVGAnimatedString]']")
        large_play_button.click()


def get_ad_info(driver: webdriver.Chrome, movie_id):
    # print("Inside Video info", movie_id)

    ad_id = driver.execute_script(
        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
    )
    # time.sleep(0.3)
    skippable_add = driver.execute_script(
        'return document.getElementsByClassName("ytp-ad-skip-button-container").length'
    )
    print("Add is skippable? ", skippable_add)
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
    while start_resolution_check == "0x0" or attempt_count < 10:
        start_resolution = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
        )
        start_resolution_check = start_resolution
        attempt_count += 1


    print(str(ad_id) == str(movie_id), ad_id, movie_id)
    while str(ad_id) == str(movie_id):
        ad_id = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
        )
    print(str(ad_id) == str(movie_id), ad_id, movie_id)

    if ad_id != 'empty_video':
        return ad_id, skippable_add, skip_duration, start_resolution


def driver_code(driver):
    list_of_urls = [
        "https://youtube.com/watch?v=I1QgIOEUYIo"
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
        # time.sleep(2)

        # for mobile phones, we first need to play the video to enable stats for nerd
        start_playing_video(driver)

        # video is being played now play the video
        enable_stats_for_nerds(driver)
        # Start Playing Video

        # bug-fix: check if the duration of the video in 3600 seconds -- if so skip before collecting the data
        video_duration_in_seconds = driver.execute_script(
            'return document.getElementById("movie_player").getDuration()'
        )
        if video_duration_in_seconds >= 3600:
            print(
                video_duration_in_seconds, " Seconds. Video Skipped for being too Long!"
            )
            continue

        ad_playing = driver.execute_script(
            "return document.getElementsByClassName('ad-showing').length"
        )

        print(movie_id)
        if ad_playing:
            print("ad at start of video!")
            ad_id, skippable, skip_duration, resolution = get_ad_info(
                driver, movie_id)
            while True:
                if ad_id == movie_id:
                    ad_id, _, _, _ = get_ad_info(driver, movie_id)
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
                    [ad_id, 0.0]  # Start of video. Main Buffer will be 0s.
                )
                previous_ad_id = ad_id
                print("Advertisement " + str(unique_add_count) + " Data collected.")


        Path(new_dir).mkdir(parents=False, exist_ok=True)

        video_playing = driver.execute_script(
            "return document.getElementById('movie_player').getPlayerState()"
        )

        ad_playing = driver.execute_script(
            "return document.getElementsByClassName('ad-showing').length"
        )

        if video_playing != 1 and not ad_playing:
            play_video_if_not_playing(driver)
        else:
            print("Video is already playing")

        while True:
            # # time.sleep(0.5)
            video_playing = driver.execute_script(
                "return document.getElementById('movie_player').getPlayerState()"
            )

            # # time.sleep(0.5)
            ad_playing = driver.execute_script(
                "return document.getElementsByClassName('ad-showing').length"
            )
            # # time.sleep(0.5)
            video_played_in_seconds = driver.execute_script(
                'return document.getElementById("movie_player").getCurrentTime()'
            )

            if ad_playing:
                # Ad is being played
                ad_just_played = True
                
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
                file_dir_three = new_dir + "/error_details.txt"
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
                    f.write(orjson.dumps(video_info_details).decode())

                with open(file_dir_three, "w+") as f:
                    f.write(orjson.dumps(error_list).decode())

                with open(file_dir_five, "w+") as f:
                    f.write(orjson.dumps(buffer_size_with_ad).decode())

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
