"""
Author: Emaan Atique 24100028@lums.edu.pk

This program will help identify individual folders which might have data collected for the same videos. This will
avoid repetitions in the data and ensure that it is for distinct videos.

 To check for repetitions, save the Identify_Duplicates file in the same directory you are working and collecting
 your data in """

import glob

original_dict = {}
reversed_dict = {}
duplicates = False

for stream_details in glob.glob("*/stream_details.txt"):  # access the stream_details txt file in every folder
    folder_name = stream_details.split("/")[0]
    with open(stream_details, "r") as file_to_read:
        data = file_to_read.read()
        data_as_dict = eval(data)  # change the string data read from the file to a dictionary
        url = data_as_dict["Main_Video"]["Url"]
        original_dict[folder_name] = url  # Add data to a dictionary with the folder name as key and video URL as value

for folder, video_link in original_dict.items():
    if video_link in reversed_dict:
        reversed_dict[video_link] = reversed_dict[video_link] + [folder]  # If a given video URL is present in more
        # than one folder, append the folder numbers
    else:
        reversed_dict[video_link] = [folder]

for folders in reversed_dict.values():
    if len(folders) > 1:  # Checks if a video is repeated across multiple folders
        duplicates = True
        folder_str = folders[0]
        for val in folders:
            if val == folders[0]:
                continue
            folder_str = folder_str + ", " + val
        print("The following folders have the same video: ", folder_str)

if len(original_dict) == 0:  # If the current directory does not have any folder with the stream_details.txt file
    print("No directory with video data")
else:
    if duplicates is False:  # If all videos in the folders are distinct
        print("There are no repetitions in the data collected")
