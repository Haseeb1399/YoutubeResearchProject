from ast import literal_eval
from pytube import YouTube
import os
import json
import time

"""
Author: Haseeb Ahmed 23100035 @ lums.edu.pk
"""

rootdir = "C:/Users/hp/Desktop/Sproj/Active"  ##Set Root folder directory.

valid_res = ["426x240", "640x360", "854x480", "1280x720", "1920x1080"]


def download_video(video_url, folder_name, type_of, video_id, resolution):
    try:
        new_res = resolution.split("x")[1].split("@")[0]
        new_res = new_res + "p"
        print("Downloading Video " + type_of, video_url, "at ", res)
        video_name = type_of + "@" + video_id + ".mp4"
        check_file = folder_name + video_name
        if os.path.exists(check_file):
            os.remove(video_name)

        yt = YouTube(video_url)

        yt.streams.filter(file_extension="mp4", res=new_res).first().download(
            folder_name, video_name
        )
        print("Downloaded! " + type_of)
        return True
    except Exception as e:
        print(e)
        print("Error in Downloading!")
        return False


for (
    subdir,
    dirs,
    files,
) in os.walk(rootdir):
    for file in files:
        # print(file)
        if file == "error_details.txt":
            path = os.path.join(subdir, file)
            with open(path) as f:
                mainlist = [list(literal_eval(line)) for line in f]
                for item in mainlist[0]:
                    url, res, _ = item
                    url_id = url.split("=")[1]
                    path_two = os.path.join(subdir, "stream_details.txt")
                    with open(path_two) as new_f:
                        string = new_f.read()
                        info_dict = json.loads(string)
                        try:
                            advert_number = list(info_dict.keys()).index(url_id) + 1
                            advert_name = "Advertisement" + "@" + str(advert_number)
                        except:
                            advert_name = "MainVideo"

                    downloaded_check = False
                    while not downloaded_check:
                        time.sleep(5)
                        if res.split("@")[0].strip() not in valid_res:
                            res = "640x360@24"
                        downloaded_check = download_video(
                            url, subdir, advert_name, (url_id.strip()), res
                        )
