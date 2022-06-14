import httplib2
from bs4 import BeautifulSoup as bs

"""
Author: Harris
24020257@lums.edu.pk

"""


URL_OVERALL = "https://kworb.net/youtube/trending_overall.html"  # around the globe
URL_PAKISTAN = "https://kworb.net/youtube/trending/pk.html"  # pakistan
URL_NIGERIA = "https://kworb.net/youtube/trending/ng.html"  # nigeria
URL_INDIA = "https://kworb.net/youtube/trending/in.html"  # india
URL_NEPAL = "https://kworb.net/youtube/trending/np.html"  # nepal
URL_KENYA = "https://kworb.net/youtube/trending/ke.html"  # kenya
URL_INDONESIA = "https://kworb.net/youtube/trending/id.html"  # indonesia

http = httplib2.Http()


def handleType(url: str, filename):
    _, content = http.request(url)
    links = []
    for link in bs(content, features="lxml").find_all("a", href=True):
        links.append(link["href"])

    final_links = []
    for link in links[20:]:
        link = link.split("/")
        link_temp = link[-1].replace(".html", "").replace("watch?v=", "")
        if link_temp == "javascript:overall();" or link_temp == "javascript:music();":
            continue
        result = "https://www.youtube.com/watch?v={}".format(link_temp)
        result = '"' + result + '"' + ","
        final_links.append(result)
    # to remove the duplicates
    final_links = list(dict.fromkeys(final_links))

    with open(filename, "w") as f:
        for link in final_links:
            f.write("%s\n" % link)


if __name__ == "__main__":
    type_videos = input(
        """
    Type
    \n"overall" to view top trending videos around the world
    \n"pk" to view top trending videos in Pakistan
    \n"ng" to view top trending videos in Nigeria
    \n"in" to view top trending videos in India
    \n"np" to view top trending videos in Nepal
    \n"ke" to view top trending videos in Kenya
    \n"id" to view top trending videos in Indonesia
    \nOption: """
    )
    if type_videos == "overall":
        handleType(URL_OVERALL, "output.txt")
    elif type_videos == "pk":
        handleType(URL_PAKISTAN, "pakistan.txt")
    elif type_videos == "ng":
        handleType(URL_NIGERIA, "nigeria.txt")
    elif type_videos == "in":
        handleType(URL_INDIA, "india.txt")
    elif type_videos == "np":
        handleType(URL_NEPAL, "nepal.txt")
    elif type_videos == "ke":
        handleType(URL_KENYA, "kenya.txt")
    elif type_videos == "id":
        handleType(URL_INDONESIA, "indonesia.txt")
    else:
        print("[UNKNOWN COMMAND]")
