from ast import literal_eval
from logging import root
from re import sub
from turtle import towards

from numpy import size
import pytube
from pytube import YouTube
import os
import pafy
import json
import time


rootdir = ".\\"

error_file = rootdir + "\\errors_log.txt"

error_logs = []
valid_res = ["240", "360", "480", "720", "1080"]


def get_bytes(url, res):
    try:
        yt = YouTube(url)
        new_res = res.split("x")[1].split("@")[0]
        if new_res in valid_res:
            new_res = new_res + "p"
        else:
            new_res = "360p"  # Default res is 360p.

        native_size = (
            yt.streams.filter(file_extension="mp4",
                              res=new_res).first().filesize
        )
        size_240p = yt.streams.filter(
            file_extension="mp4", res="240p").first().filesize
        try:
            size_720p = (
                yt.streams.filter(file_extension="mp4",
                                  res="720p").first().filesize
            )
        except:
            size_720p = (
                yt.streams.filter(file_extension="mp4")
                .get_highest_resolution()
                .filesize
            )

        print("url", native_size, size_240p, size_720p)
        return native_size, size_240p, size_720p
    except Exception as e:
        print(e)
        error_logs.append([e, url, res])


# get_bytes("https://www.youtube.com/watch?v=7BxpvzkaXjQ", "0x0@25 ")

for (
    subdir,
    dirs,
    files,
) in os.walk(rootdir):
    for file in files:
        if file == "stream_details.txt":
            print("In folder", subdir)
            path = os.path.join(subdir, file)
            new_dict = None
            with open(path) as f:
                stream_file = json.loads(f.read())
                for index, item in enumerate(stream_file):
                    if item == "Main_Video":
                        url = stream_file[item]["Url"]
                        res = stream_file[item]["Resolution"]
                        native, small, large = get_bytes(url, res)
                        stream_file["Main_Video"]["Size"] = native
                        stream_file["Main_Video"]["Size240p"] = small
                        stream_file["Main_Video"]["Size720p"] = large
                    else:
                        url = "https://www.youtube.com/watch?v=" + item
                        res = stream_file[item]["Resolution"]
                        native, small, large = get_bytes(url, res)
                        stream_file[item]["Size"] = native
                        stream_file[item]["Size240p"] = small
                        stream_file[item]["Size720p"] = large

                new_dict = stream_file

            print()
            if new_dict:
                with open(path, "w+") as f:
                    f.write(json.dumps(new_dict))
            else:
                print("Error!", subdir)
