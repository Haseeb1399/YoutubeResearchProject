'''
Code Author:    Harris
Email:          24020257@lums.edu.pk
'''


import httplib2
from bs4 import BeautifulSoup as bs


URL_OVERALL = 'https://kworb.net/youtube/trending_overall.html'

http = httplib2.Http()


def handleType(url: str, filename):
    _, content = http.request(url)
    links = []
    for link in bs(content, features='lxml').find_all('a', href=True):
        links.append(link['href'])

    final_links = []
    for link in links[20:]:
        link = link.split('/')
        link_temp = link[-1].replace('.html', '').replace('watch?v=', '')
        if link_temp == 'javascript:overall();' or link_temp == 'javascript:music();':
            continue
        result = 'https://www.youtube.com/watch?v={}'.format(link_temp)
        result = "" + result + ""
        final_links.append(result)
    # to remove the duplicates
    final_links = list(dict.fromkeys(final_links))

    with open(filename, 'w') as f:
        for link in final_links:
            # added speech quotes just so literal strings are written to the file
            f.write(f"'{link}'\n")


if __name__ == '__main__':
    type_videos = input('''
    Type
    "overall" to view top trending videos around the world
    "pk" to view top trending videos in Pakistan
    "ng" to view top trending videos in Nigeria
    "in" to view top trending videos in India
    "np" to view top trending videos in Nepal
    "ke" to view top trending videos in Kenya
    "id" to view top trending videos in Indonesia
    Option: ''')

    if type_videos == 'overall':
        handleType(URL_OVERALL, '{}.txt'.format(type_videos))
        print('Open {}.txt to view output'.format(type_videos))
    elif type_videos == 'pk' or type_videos == 'ng' or type_videos == 'in' or type_videos == 'np' or type_videos == 'ke' or type_videos == 'id':
        # for developing countries
        handleType('https://kworb.net/youtube/trending/{}.html'.format(type_videos),
                   '{}.txt'.format(type_videos))
        print('Open {}.txt to view output'.format(type_videos))
    else:
        print('[unknown command]')
