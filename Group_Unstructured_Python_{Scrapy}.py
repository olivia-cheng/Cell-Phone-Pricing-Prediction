import requests
from bs4 import BeautifulSoup
from pprint import pprint
import random
headers_list = [
    # Firefox 77 Mac
    {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 92.0 Win10
    {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 91.0 Win10
    {
    "Connection": "keep-alive",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    # Firefox 90.0 Win10
    {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
    }
]
import csv
from time import sleep

rows = []
for i in range(0, 25):
    # sleep(randint(20, 25))
    url = 'https://losangeles.craigslist.org/d/los-angeles-ca/search/moa?s=' + str(
        i * 120) + '&lat=34.037&lon=-118.305&search_distance=200'
    print(url)

    # url = 'https://tippecanoe.craigslist.org/d/cell-phones/search/moa'
    # data = requests.get(url)

    my_data = []

    headers = random.choice(headers_list)
    r = requests.Session()
    r.headers = headers
    data = r.get(url)

    html = BeautifulSoup(data.text, 'html.parser')

    # rows=[]
    for a in html.find_all('a', class_="result-title hdrlnk"):

        # print("Found the URL:", a['href'])

        url = a['href']
        data = requests.get(url)

        post_data = []

        html = BeautifulSoup(data.text, 'html.parser')

        # title
        title = html.find("span", id="titletextonly")
        # title=title.text
        if title is None:
            title = ''
        else:
            title = title.text

        # location
        location = html.find("small")
        if location is None:
            location = ''
        else:
            location = location.text

        # price
        price = html.find("span", class_="price")
        if price is None:
            price = ''
        else:
            price = price.text

        description = html.find("section", id="postingbody")
        # desc=description.text.split('\n')[5]
        desc = ' '.join(description.text.strip().split('\n'))

        attr = html.find("p", class_="attrgroup")
        attrs = [i for i in attr.text.split('\n') if i != '']

        postinfo = html.find("div", class_="postinginfos")
        postid = postinfo.text.split('\n')[1]
        postDate = postinfo.text.split('\n')[2]
        updateDate = postinfo.text.split('\n')[3]

        notice = html.find("ul", class_="notices")
        notice = notice.text.replace('\n', '')

        post_data.append(title)
        post_data.append(location)
        post_data.append(price)
        post_data.append(desc)
        post_data.append(attrs)
        post_data.append(postid)
        post_data.append(postDate)
        post_data.append(updateDate)
        post_data.append(notice)
        post_data.append(url)
        rows.append(post_data)

# field names
fields = ['Title', 'Location', 'Price', 'Description', 'Attributes', 'Post ID', 'Post Date', 'Update Date', 'Notice',
          'Url', ]

with open('cellphone_data_srhdist200.csv', 'w', newline='', encoding='utf-8') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)

    write.writerow(fields)
    write.writerows(rows)