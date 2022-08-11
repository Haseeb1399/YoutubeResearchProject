from ast import literal_eval
from pytube import YouTube
import os
import json
import time
import isodate

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

"""
Author: Haseeb Ahmed 23100035 @ lums.edu.pk
"""

rootdir = ".\\"  # Set Root folder directory.

valid_res = ["426x240", "640x360", "854x480", "1280x720", "1920x1080"]
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

API_KEY = "AIzaSyCkZ3xsdhG0pYDa2b_-LTIoyu4TDrU4FXY"


def get_duration(vid_id):
    # See instructions for running these code samples locally:
    # https://developers.google.com/explorer-help/code-samples#python

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY
    )

    request = youtube.videos().list(part="contentDetails,statistics", id=vid_id)
    response = request.execute()
    dur = response["items"][0]["contentDetails"]["duration"]

    in_seconds = isodate.parse_duration(dur)
    return in_seconds.total_seconds()


for (
    subdir,
    dirs,
    files,
) in os.walk(rootdir):
    for file in files:
        # print(file)
        if file == "stream_details.txt":
            path = os.path.join(subdir, file)
            new_dict = {}
            with open(path) as f:
                new_dict = json.load(f)
                id_list = list(new_dict.keys())
                for id in id_list:
                    if id == "Main_Video":
                        continue

                    new_id = id.strip()
                    time_in_seconds = get_duration(new_id)
                    new_dict[id]["Duration"] = time_in_seconds

            with open(path, "w") as f:
                f.write(json.dumps(new_dict))

print("Added time!")
"""
240p 1080p --> Main Video
we also have the video at the resolution it was played it. --> Keep? Remove?

360p 

240p 1080p --> Each Ad.

"""

"""

Ubunutu 18. --> System--> 2.7
Virt-manager > 3.4

"""
