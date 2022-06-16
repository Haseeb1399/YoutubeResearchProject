from ast import literal_eval
from pytube import YouTube
import os
import json
import time


rootdir = "C:/Users/hp/Desktop/Sproj/Active"  # Set Root folder directory.

valid_res = ["426x240", "640x360", "854x480", "1280x720", "1920x1080"]

error_logs=[]

def download_video(video_url, folder_name, type_of, video_id, resolution):
    try:
        new_res = resolution.split("x")[1].split("@")[0]
        new_res = new_res + "p"
        print("Downloading Video " + type_of, video_url, "at ", new_res)
        video_name = type_of + "@" + video_id + ".mp4"
        check_file = folder_name + video_name
        if os.path.exists(check_file):
            os.remove(video_name)

        yt = YouTube(video_url)

        yt.streams.filter(file_extension="mp4", res=new_res).first().download(
            folder_name, video_name
        )
        print("Downloaded! " + type_of, " at " + new_res)

        if type_of == "MainVideo":
            video_name_one = video_name = type_of + "@" + video_id + "@240p" + ".mp4"
            check_file_one = folder_name + video_name_one
            if os.path.exists(check_file_one):
                os.remove(video_name_one)

            print("Downloading Video " + type_of, video_url, "at 240p")

            yt.streams.filter(file_extension="mp4", res='240p').first().download(
                folder_name, video_name_one
            )
            print("Downloaded! " + type_of, " at 240p")

            video_name_two = video_name = type_of + "@" + video_id + "@1080p" + ".mp4"
            check_file_two = folder_name + video_name_two
            if os.path.exists(check_file_two):
                os.remove(video_name_two)

            print("Downloading Video " + type_of, video_url, "at 1080p")
            yt.streams.filter(file_extension="mp4", res='1080p').first().download(
                folder_name, video_name_two
            )
            print("Downloaded! " + type_of, " at 1080p")
            return True
        else:
            return True
    except Exception as e:
        print(e)
        error_logs.append((e,folder_name,video_id,video_url))
        print("Error in Downloading!")
        return False


for (
    subdir,
    dirs,
    files,
) in os.walk(rootdir):
    for file in files:
        # print(file)
        if file == "stream_details.txt":
            path = os.path.join(subdir, file)
            with open(path) as f:
                stream_file = json.loads(f.read())
                for index, item in enumerate(stream_file):
                    if item == 'Main_Video':
                        url = stream_file[item]['Url']
                        res = stream_file[item]['Resolution']
                        url_id = url.split("=")[1]
                        name = "MainVideo"
                        attempts=0
                        while True or attempts>5:
                            result = download_video(
                                url, subdir, name, url_id, res)
                            if result:
                                break
                            else:
                                attempts+=1
                                continue
                    else:
                        url = "https://www.youtube.com/watch?v="+item
                        res = stream_file[item]['Resolution']
                        url_id = item.strip()
                        name = "Advertisement"+"@"+str(index+1)
                        attempts=0
                        while True or attempts>5:
                            result = download_video(
                                url, subdir, name, url_id, res)
                            if result:
                                break
                            else:
                                attempts+=1
                                continue
    
    err_logs_dir = rootdir+"./error_logs_downloading.txt"
    with open(err_logs_dir,"w+") as f:
        f.write(json.dumps(error_logs))
    