import time
import warnings
import json
import orjson
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path

mobile_emulation = {
   "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
   "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" 
}

latencyInMilliseconds = 5
downloadLimitMbps = 11
uploadLimitMbps = 5

TIME_TO_SLEEP = float(2/downloadLimitMbps)


warnings.filterwarnings("ignore", category=DeprecationWarning)
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.headless=True
error_list=[]


def to_seconds(timestr):
    seconds = 0
    for part in timestr.split(":"):
        seconds = seconds * 60 + int(part, 10)
    return seconds

def enable_stats_for_nerds(driver):

   settings = driver.find_element_by_xpath("/html/body/ytm-app/ytm-mobile-topbar-renderer/header/div/ytm-menu/button")
   settings.click()

   playback_settings = driver.find_element_by_xpath("/html/body/div[2]/div/ytm-menu-item[3]/button")
   playback_settings.click()

   stats_for_nerds=driver.execute_script("document.getElementsByClassName('menu-item-button')[1].click()")

#    stats_for_nerds = driver.find_element_by_xpath("/html/body/div[2]/dialog/div[2]/ytm-menu-item[2]/button")
#    stats_for_nerds.click()
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

    skip_retry=0
    time.sleep(0.5)
    while skip_retry<20:
        skippable_add = driver.execute_script(
            'return document.getElementsByClassName("ytp-ad-skip-button-container").length'
        )
        skip_retry+=1

    if skippable_add:
        skip_try=0
        found=False
        while skip_try<5:
            try:
                skip_duration = (
                    driver.execute_script(
                        'return document.getElementsByClassName("ytp-ad-text ytp-ad-preview-text")[0].innerText'
                    )
                )
                found=True
                break
            except:
                skip_try+=1
        if not found:
            skip_duration = -2  # Error occured, Could not get Skip Duration
    else:
        skip_duration = 999  # Add was not skippable.

    start_resolution = driver.execute_script(
        'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
    )
    start_resolution = start_resolution.split("@")[0]

    attempt_count = 0

    while start_resolution == "0x0" or attempt_count<30:
        print("Can't get add resolution!",start_resolution)
        start_resolution = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
        )
        # start_resolution_check = start_resolution
        attempt_count+=1

    time.sleep(0.5)

    ad_id = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
    )
    while str(ad_id.strip()) == str(movie_id.strip()):
        ad_id = driver.execute_script(
            'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[0].children[1].textContent.replace(" ","").split("/")[0]'
        )
        print(str(ad_id) == str(movie_id),ad_id,movie_id)

    # print("Ad Id is" + str(ad_id))
    return ad_id, skippable_add, skip_duration, start_resolution

def record_ad_buffer(driver,ad_length):
    ad_buffer_list=[]
    ad_playing = driver.execute_script(
            "return document.getElementsByClassName('ad-showing').length"
    )

    while ad_playing:
        ad_buffer = float(
            driver.execute_script(
                'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[10].children[1].textContent.split(" ")[1]'
            )
        )
        res = driver.execute_script(
                    'return document.getElementsByClassName("html5-video-info-panel-content")[0].children[2].children[1].textContent.replace(" ","").split("/")[0]'
                )
        current_time_retry=0
        while current_time_retry<10:
            try:
                ad_played = float(
                    driver.execute_script(
                        "return document.getElementsByClassName('video-stream html5-main-video')[0].currentTime"
                    )
                )
                break
            except:
                current_time_retry+=1

        ad_played_in_seconds = ad_played
        ad_buffer_list.append((ad_buffer, ad_played_in_seconds,res))

        ad_playing = driver.execute_script(
            "return document.getElementsByClassName('ad-showing').length"
        )
    
    return ad_buffer_list

def get_ad_duration(driver):
    length_retry=0
    while length_retry<50:
        try:
            ad_length = (
                driver.execute_script(
                    "return document.getElementsByClassName('video-stream html5-main-video')[0].duration"
                ))
            ad_length=float(ad_length)
            print("Ad length is!",ad_length)
            return ad_length
        except:
            length_retry+=1



def driver_code(driver):
    list_of_urls=[
        # "https://www.youtube.com/watch?v=J_qCRmQXJKs",
        # "https://www.youtube.com/watch?v=BUEAKynYvx4",
        # "https://www.youtube.com/watch?v=wcDcOnR6sl8",
        # "https://www.youtube.com/watch?v=qsOCW8YMRyw",
        # "https://www.youtube.com/watch?v=4M5jGbVfItE",
        # "https://www.youtube.com/watch?v=BddP6PYo2gs",
        # "https://www.youtube.com/watch?v=UWQi7mSy_qY",
        ]

    for index,url in enumerate(list_of_urls):
        global error_list
        video_info_details = {}
        ad_buffer_information={}
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
        retry_count=0
        while retry_count<5:
            try:
                enable_stats_for_nerds(driver)
                break
            except:
                retry_count+=1
        
        #Start Playing Video
        start_playing_video(driver)


        try:
            driver.execute_script("document.getElementsByClassName('ytm-autonav-toggle-button-container')[0].click()")
        except:
            pass


        ##Check If ad played at start
        time.sleep(TIME_TO_SLEEP)
        ad_playing = driver.execute_script(
            "return document.getElementsByClassName('ad-showing').length"
        )
        print("Playing Video: ",movie_id)
        if ad_playing:
            time.sleep(0.1)
            print("ad at start of video!")
            ad_id, skippable, skip_duration, resolution = get_ad_info(driver, movie_id)
            
            print("Ad ID: ",ad_id, "Skippable? ",skippable," Skip Duration: ",skip_duration,"Resolution: ",resolution)

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

            ad_length=get_ad_duration(driver)

            ad_buf_details = record_ad_buffer(driver,ad_length)
            to_write = {"ad_length":ad_length,"buffer":ad_buf_details}
            ad_buffer_information[ad_id]=to_write
            print("Advertisement " + str(unique_add_count) + " Data collected.")

        time.sleep(0.1)
        video_duration_in_seconds = driver.execute_script(
            'return document.getElementById("movie_player").getDuration()'
        )
        if video_duration_in_seconds >= 3600:
            video_info_details={}
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

            
            if ad_playing:
                # Ad is being played
                ad_just_played = True
                
                time.sleep(0.1)
                ad_length=get_ad_duration(driver)


                ad_id, skippable, skip_duration, resolution = get_ad_info(
                    driver, movie_id
                )
                
                print("Ad ID: ",ad_id, "Skippable? ",skippable," Skip Duration: ",skip_duration,"Resolution: ",resolution)

                if (str(ad_id).strip()) != (str(movie_id).strip()):
                    if ad_id != previous_ad_id:
                        print("Ad id is: ", ad_id)
                        previous_ad_id = ad_id

                        ## Appends the last recorded main_video_buffer when ad was played.
                        if len(actual_buffer_reads) >= 1:
                            buffer_size_with_ad.append(
                                [ad_id, actual_buffer_reads[-1]]
                            )  # Append last buffer value to keep track.
                        else:
                            buffer_size_with_ad.append(
                                [ad_id,0.0]
                            )  # Ad was at the start.


                        ## Ads video information to document.
                        if ad_id not in video_info_details.keys():
                            unique_add_count += 1
                            video_info_details[ad_id] = {
                                "Count": 1,
                                "Skippable": skippable,
                                "SkipDuration": skip_duration,
                                "Resolution": resolution,
                            }
                            ad_buf_details = record_ad_buffer(driver,ad_length)
                            to_write = {"ad_length":ad_length,"buffer":ad_buf_details}
                            ad_buffer_information[ad_id]=to_write
                            print(
                                "Advertisement "
                                + str(unique_add_count)
                                + " Data collected."
                            )
                        else:
                            current_value = video_info_details[ad_id]["Count"]
                            video_info_details[ad_id]["Count"] = current_value + 1

                            ad_buf_details = record_ad_buffer(driver,ad_length)
                            name=ad_id+"_"+ str(video_info_details[ad_id]["Count"])
                            to_write = {"ad_length":ad_length,"buffer":ad_buf_details}
                            ad_buffer_information[name]=to_write
                            print("Repeated Ad! Information Added!")

            elif video_playing == 0:
                # Video has ended
                file_dir = new_dir + "/stream_details.txt"
                file_dir_two = new_dir + "/buffer_details.txt"
                file_dir_three = new_dir + "/error_details.txt"
                file_dir_four = new_dir + "/ResolutionChanges.txt"
                file_dir_five = new_dir + "/BufferAdvert.txt"
                file_dir_six  = new_dir + "/AdvertBufferState.txt"
                Main_res = max(main_res_all, key=main_res_all.count)
                video_info_details["Main_Video"] = {
                    "Url": url,
                    "Total Duration": video_duration_in_seconds,
                    "UniqueAds": unique_add_count,
                    "AvgBuffer": (sum(actual_buffer_reads) / len(actual_buffer_reads)),
                    "Resolution": Main_res,
                }
                with open(file_dir, "wb+") as f:
                    f.write(orjson.dumps(video_info_details))

                with open(file_dir_two, "wb+") as f:
                    f.write(orjson.dumps(actual_buffer_reads))

                with open(file_dir_three, "wb+") as f:
                    f.write(orjson.dumps(error_list))

                # with open(file_dir_four, "wb+") as f:
                #     f.write(orjson.dumps(vid_res_at_each_second))

                with open(file_dir_five, "wb+") as f:
                    f.write(orjson.dumps(buffer_size_with_ad))
                
                with open(file_dir_six, "wb+") as f:
                    f.write(orjson.dumps(ad_buffer_information))
                video_info_details = {}
                unique_add_count = 0
                print("Video Finished and details written to files!")
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

driver.set_network_conditions(
    offline=False,
    latency=latencyInMilliseconds,
    download_throughput= downloadLimitMbps * 125000, #Mbps to bytes per second
    upload_throughput=uploadLimitMbps * 125000 #Mbps to bytes per second
)
driver_code(driver)
driver.quit()
