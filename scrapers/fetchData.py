# import python libraries
import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import html5lib
# create lists to store data
summaryData = []
links = []
# csv with all the data
# function to get the links of the fanfiction posts
def getLinks():
    # get the first 1000 links
    for i in range(1, 1001):
        print(i)
        time.sleep(1)
        url = "https://www.fanfiction.net/cartoon/Transformers-Beast-Wars/?&srt=4&lan=1&r=103&p=" + str(i)
        req = requests.get(url)
        bsObj = BeautifulSoup(req.content, 'html.parser')
        posts = bsObj.findAll("div", {"class":"z-list zhover zpointer"})
        for post in posts:
            title = post.find("a", {"class":"stitle"})
            partLink = title.get('href')
            link = "https://www.fanfiction.net" + partLink
            # add the link to the list of links
            links.append(link)
            # print(link)
            summary = post.find("div", {"class":"z-indent z-padtop"}).get_text()
            infobulk = post.find("div", {"class":"z-padtop2 xgray"}).get_text()
            # try to see if data describing each post is present, including rating, language, genre
            info = infobulk.split(" - ")
            try:
                rating = info[0]
            except:
                rating = ""
            try:
                language = info[1]
            except:
                language = ""
            try:
                genre = info[2]
            except:
                genre = ""
            for bit in info:
                if "Chapters" in bit:
                    chapters = bit.split(": ")
                    chapters = chapters[1]
                else:
                    print("N/A")
                if "Words" in bit:
                    words = bit.split(": ")
                    words = words[1]
                else:
                    print("N/A")
                if "Reviews" in bit:
                    reviews = bit.split(": ")
                    reviews = reviews[1]
                else:
                    print("N/A")
                if "Favs" in bit:
                    favs = bit.split(": ")
                    favs = favs[1]
                else:
                    print("N/A")
                if "Follows" in bit:
                    follows = bit.split(": ")
                    follows = follows[1]
                else:
                    print("N/A")
            # get the date the post was created and updated where applicable
            dates = post.find("div", {"class":"z-padtop2 xgray"}).findAll("span")
            length = len(dates)
            if length == 2:
                updated = dates[0].attrs['data-xutime']
                published = dates[1].attrs['data-xutime']
            elif length == 1:
                updated = ''
                published = dates[0].attrs['data-xutime']
            # write the existing data to a dictionary and append that to a list
            data = {
                'title': title.get_text().strip(),
                'link': link.strip(),
                'summary': summary.strip(),
                'rating': rating.strip(),
                'genre': genre.strip(),
                'chapters': chapters.strip(),
                'words': words.strip(),
                'reviews': reviews.strip(),
                'favs': favs.strip(),
                'follows': follows.strip(),
                'updated': updated.strip(),
                'published': published.strip()
            }
            summaryData.append(data)

# function to write and save the summary data to a csv
def saveData(summaryData):
    filename = 'HPSummary.csv'
    #open your new csv file with a 'w' so you can write to it
    with open(filename, 'w') as output_file:
        #make headers for you columns. these must match up with the keys you set in your python dictionary, inamte
        fieldnames = [	'title',
                      'link',
                      'summary',
                      'rating',
                      'language',
                      'genre',
                      'chapters',
                      'words',
                      'reviews',
                      'favs',
                      'follows',
                      'updated',
                      'published'
                     ]
        #write these into a csv, the headers being fieldnames and the rows your list of inmates
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summaryData)
# run the two above functions
getLinks()
saveData(summaryData)
