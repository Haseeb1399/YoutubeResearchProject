'''
Code Authors:
Haseeb Ahmad
Harris Ahmad
'''


from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import warnings
import time
from pathlib import Path
import json

mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
}

warnings.filterwarnings("ignore", category=DeprecationWarning)
options = webdriver.ChromeOptions()
options.add_experimental_option("mobileEmulation", mobile_emulation)

def get_ad_info(driver: webdriver.Chrome, movie_id):
    '''
    This function helps us get ad-data from the main video
    '''
    ad_id = driver.execute_script(
        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
    )
    # sleeping for 0.5 seconds for the above function to get executed
    time.sleep(0.5)

    skippable_add: int = driver.execute_script(
        'return document.getElementsByClassName("ytp-ad-skip-button-container").length'
    )
    print(f'ad is skippable? {skippable_add}')

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
        # sets the skip_duration to 999 meaning it was 999 seconds and could not be skipped
        skip_duration = 999  # Add was not skippable.

    # this gets the resolution of the ad when it starts
    start_resolution: str = driver.execute_script(
        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
    )
    start_resolution_check = start_resolution.split("@")[0]

    # to keep track of the the number of times we ran the loop
    attempt_count = 0
    # keeps looping until we get the correct resolution of the current ad being streamed
    while start_resolution_check == "0x0" or attempt_count < 10:
        start_resolution = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
        )
        start_resolution_check = start_resolution
        attempt_count += 1
    # sleeps for 0.5 seconds for the above operation to complete
    time.sleep(0.5)

    # keep looping unless the id of the current id is the same as the argument passed to the function
    # for authentication purposes only.
    while str(ad_id) == str(movie_id):
        ad_id = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
        )

    # returns the id of the add, logical value for if the ad is skippable, the duration of the ad to skip the video (up to 6 seconds long), and the start
    # resolution of the ad
    return ad_id, skippable_add, skip_duration, start_resolution


def driver_code(driver: webdriver.Chrome):
    # forcefully open youtube in mobile mode
    driver.get('https://m.youtube.com/?persist_app=1&app=m')
    # list of urls for mobile emulation
    list_of_urls: list = [
        "https://m.youtube.com/watch?v=IpeXtG9sBEI"
    ]

    for index, url in enumerate(list_of_urls):
        # this stores the complete information of the video being played
        video_info_details: dict = {}
        # logs any errors (if found)
        error_list: list = []
        # keeps track of the count of unique ads displayed during the main video
        unique_add_count: int = 0
        # boolean set to False -- tracks whether an ad is being displayed or not
        ad_just_played: bool = False
        # stores the buffer details at every second
        buffer_list: list = []
        actual_buffer_reads: list = []
        buffer_size_with_ad: list = []
        # stores the resolution of the main video at every second -- if the video is
        # a 100 seconds long then the length of this list would be 100
        # this can stretch to as large at 3599 (>= 3600 is not allowed)
        vid_res_at_each_second: list = []
        main_res_all: list = []
        # this stores the ad id of the recent most ad played
        previous_ad_id: str = url.split("=")[1]

        movie_id: str = url.split("=")[1]
        # stores the name of the directory to store the videos in
        new_dir: str = "./" + str(index + 1)

        # spawns a chrome instance and directs to the url in the list as per the iteration of the loop
        # now direct to the url 
        driver.get(url)

        # ==================================================================================================
        # navigating using XMLpaths
        # Playing Video
        movie_player = driver.find_element_by_id("movie_player")
        hover = ActionChains(driver).move_to_element(movie_player)
        hover.perform()
        ActionChains(driver).context_click(movie_player).perform()

        # Clicking Hamburger Icon
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

        # clearing the screen by pressing ok
        ok_button = driver.find_element_by_xpath(
            "/html[1]/body[1]/div[2]/dialog[1]/div[3]/c3-material-button[1]/button[1]/div[1]")
        ok_button.click()
        # ==================================================================================================

        # sleeping for two seconds for the above operation to complete
        # successfully
        time.sleep(0.2)

        # checks if the ad is playing or not by returning a logical 0 or 1
        ad_playing = driver.execute_script(
            "return document.getElementsByClassName('ad-showing').length"
        )

        # if the ad is playing
        if ad_playing:
            # fetches all information from the get_ad_info function and stores them in appropriate
            # variables
            ad_id, skippable, skip_duration, resolution = get_ad_info(
                driver, movie_id)

            # check if the id of the current ad being played is unique
            # if unique then append into the dictionary
            if ad_id not in video_info_details.keys():
                # increment the unique ad count
                unique_add_count += 1
                # appending the information of the ad to the dictionary
                video_info_details[ad_id] = {
                    "Count": 1,
                    "Skippable": skippable,
                    "SkipDuration": skip_duration,
                    "Resolution": resolution,
                }
                # at the start of the video, the buffer size will be 0s
                buffer_size_with_ad.append(
                    [ad_id, 0.0]  # Start of video. Main Buffer will be 0s.
                )
                # current ad_id is stored in the previous_ad_id (updated) and now onto the
                # next iteration
                previous_ad_id = ad_id

                # printed to the console if all information of the current ad is collected
                print(f"Advertisement {unique_add_count}'s Data Collected")

        time.sleep(0.5)

        # collecting the duration of the main video
        video_duration_in_seconds: int = driver.execute_script(
            'return document.getElementById("movie_player").getDuration()'
        )

        # if the video is an hour or more long
        if video_duration_in_seconds >= 3600:
            # print this to the console indicating the video is skipped
            print(
                video_duration_in_seconds, " Seconds. Video Skipped for being too Long!"
            )
            # onto the next url
            continue

        # creates a new dir by the index of the url (marks what video we are playing) in the list_of_urls
        Path(new_dir).mkdir(parents=False, exist_ok=True)

        # stores the current state (integer) of the YouTube player as per YouTube's pre-set API
        # used to check if the video is playing, paused, buffering etc.
        video_playing: int = driver.execute_script(
            "return document.getElementById('movie_player').getPlayerState()"
        )
        # sleep for 0.5 seconds for the script to execute
        time.sleep(0.5)

        # checks the state of the player -- if the video has not started to play yet
        if video_playing != 1:
            # prints a confirmation message to the console
            print("Video has now started playing")
            # register an onSpace event by pressing the space button to play the video
            movie_player.send_keys(Keys.SPACE)
        else:
            # in the event it is already playing simply print this
            print("Video is already playing")

        # initiating an infinite loop
        while True:
            # time.sleep(0.5)
            # getting the state of the video
            video_playing: int = driver.execute_script(
                "return document.getElementById('movie_player').getPlayerState()"
            )

            # getting the present status of the ad (if any)
            ad_playing: int = driver.execute_script(
                "return document.getElementsByClassName('ad-showing').length"
            )
            # getting the current duration of the main video played so far
            video_played_in_seconds: int = driver.execute_script(
                'return document.getElementById("movie_player").getCurrentTime()'
            )

            # UH-OH SOMETHING IS FISHY
            # if the video is not playing and the ad is not playing
            if video_playing != 1 and not ad_playing:
                # if the video playing has not ended
                if video_playing != 0:
                    # press space to play the video
                    movie_player.send_keys(Keys.SPACE)

            # if the ad is playing
            if ad_playing:
                # bool variable to keep track of whether the ad is playing or not
                ad_just_played = True

                # checks if the ad is playing or not -- if it is paused or not
                is_add_playing = driver.execute_script(
                    'return document.getElementsByClassName("ytp-play-button ytp-button")[0].title'
                )
                # if the ad is playing
                if is_add_playing != "Pause (k)":
                    # pause the ad
                    movie_player.send_keys(Keys.SPACE)
                # sleep for 0.5 seconds for the above event to register
                time.sleep(0.5)
                # get info of the current ad being played using the get_ad_info function
                ad_id, skippable, skip_duration, resolution = get_ad_info(
                    driver, movie_id
                )

                # this means there is a new ad -- handles the case of back-to-back ads
                if (str(ad_id).strip()) != (str(movie_id).strip()):
                    # yes there are two ads
                    if ad_id != previous_ad_id:
                        # display the ad id of the current ad
                        print(f"Ad is is: {ad_id}")
                        # update the previous_ad_id to the current ad id so appropriate information
                        # is available for the next ad in the queue
                        previous_ad_id = ad_id
                        if len(actual_buffer_reads) >= 1:
                            buffer_size_with_ad.append(
                                [ad_id, actual_buffer_reads[-1]]
                            )  # Append last buffer value to keep track.
                        else:
                            buffer_size_with_ad.append(
                                [ad_id, "-1"]
                            )  # Ad was at the start

                        # if the id of the current ad is unique
                        if ad_id not in video_info_details.keys():
                            # increment the ad count
                            unique_add_count += 1
                            # store the info details of the current ad
                            video_info_details[ad_id] = {
                                "Count": 1,
                                "Skippable": skippable,
                                "SkipDuration": skip_duration,
                                "Resolution": resolution,
                            }
                            # display to the console the id of the ad and that the info has been collected
                            print(
                                f"Advertisement {unique_add_count}'s Data Collected")
                        # if the ad_id is duplicate -- info regarding the current ad has already been collected
                        # skip the ad
                        else:
                            current_value = video_info_details[ad_id]["Count"]
                            # increment the occurence count of the ad along with its ad id by 1
                            video_info_details[ad_id]["Count"] = current_value + 1
                            # print a confirmation message
                            print("Count of existing add increased!")

            # 0 is YouTube API's player state means that the video has ended
            elif video_playing == 0:
                # main video has ended playing
                # preliminaries -- make set appropriate names for the directories to store relevant pieces of information
                # this stores the details of the stream
                file_dir = new_dir + "/stream_details.txt"
                # this stores the buffer details
                file_dir_two = new_dir + "/buffer_details.txt"
                # a log file to store the errors (if any while playing the video and the ads)
                file_dir_three = new_dir + "/error_details.txt"
                # this file stores information regarding the changes in the resolution (if any)
                file_dir_four = new_dir + "/ResolutionChanges.txt"
                # this file stores information regarding the buffer of the advertisement
                file_dir_five = new_dir + "/BufferAdvert.txt"
                Main_res = max(main_res_all, key=main_res_all.count)
                # appends info of the main video in the dictionary
                video_info_details["Main_Video"] = {
                    "Url": url,
                    "Total Duration": video_duration_in_seconds,
                    "UniqueAds": unique_add_count,
                    "AvgBuffer": (sum(actual_buffer_reads) / len(actual_buffer_reads)),
                    "Resolution": Main_res,
                }
                # writing to stream_details -- storing the info of the main video
                with open(file_dir, "w+") as f:
                    f.write(json.dumps(video_info_details))

                # writing to buffer_details.txt -- storing the details of the buffer of the main video
                with open(file_dir_two, "w+") as f:
                    f.write(json.dumps(actual_buffer_reads))

                # writing to buffer_details.txt -- a log file
                with open(file_dir_three, "w+") as f:
                    f.write(json.dumps(error_list))

                # writing to ResolutionChanges.txt -- a file with a long list containing the resolution of the
                # main video captured at every second
                with open(file_dir_four, "w+") as f:
                    f.write(json.dumps(vid_res_at_each_second))

                # writing to BufferAdvert.txt -- information regarding the buffer of the main video along with the ad id
                with open(file_dir_five, "w+") as f:
                    f.write(json.dumps(buffer_size_with_ad))

                # updating the variables for the next url in the list
                # setting the dictionary to empty
                video_info_details = {}
                # unique ad count for the next video
                unique_add_count = 0
                break
            # if the video is neither paused or buffering -- playing naturally
            else:
                # Record Resolution at each second
                res = driver.execute_script(
                    'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
                )

                # append the resolution related information in the respective list
                new_data_point = (res, video_played_in_seconds)
                main_res_all.append(res)
                vid_res_at_each_second.append(new_data_point)

                # Get Current Buffer and change it to a floating point for precision -- should be a floating point before the conversion
                current_buffer = float(
                    driver.execute_script(
                        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[10].children[1].textContent.split(" ")[1]'
                    )
                )
                # Actual Buffer
                if ad_just_played:
                    # if the ad is playing, append the current buffer size to the list
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

# driver code to run the function
if __name__ == '__main__':
    # start the webdriver -- spawn a chrome instance
    driver = webdriver.Chrome(options=options)
    # pass the driver to the main function
    driver_code(driver)
    # quit when the list of urls is done
    driver.quit()
