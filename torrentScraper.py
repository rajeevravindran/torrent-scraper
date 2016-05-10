import requests
from lxml import html
import re

def sendHttpRequest(url):
    print "[] Sending HTTPS request to "+str(url)
    page = requests.get(url)
    content = html.fromstring(page.content)
    print "[] Received content"
    return content

def parseByXpath(HtmlContent,xpath):
    return HtmlContent.xpath(xpath)

def searchContent(showDetails,webSiteData):
    season=format(showDetails['season'],'02d')
    episode=format(showDetails['episode'],'02d')
    search_string='S'+str(season)+'E'+str(episode)
    torrent_name = parseByXpath(webSiteData,'//*[@id="searchResult"]/tr/td/div/a/text()')
    for i in range(0,30):
        print '['+str(i)+'] Searching '+str(search_string)+' in '+str(torrent_name[i])
        match = re.search(str(search_string),torrent_name[i])
        match2= re.search(str(showDetails['uploader']),torrent_name[i])
        if ((match !=None) & (match2 != None)):
            if (match.group(0)==search_string):
                print i
                print '[] Found at node '+str(i)
                found=True
                break
    episodeNode = i + 1
    episodeNameXpath = '//*[@id="searchResult"]/tr[7]/td[2]/div/a/text()'
    episodeName = parseByXpath(webSiteData, episodeNameXpath)[0]
    episodeMagnetXpath = '//*[@id="searchResult"]/tr['+str(episodeNode)+']/td[2]/a[1]/@href'
    magnetLink = parseByXpath(webSiteData,episodeMagnetXpath)[0]
    episodeDetailsXpath =  '//*[@id="searchResult"]/tr['+str(episodeNode)+']/td[2]/font/text()'
    episodeDetails = parseByXpath(webSiteData,episodeDetailsXpath)[0]
    episodeSeedsXpath = '//*[@id="searchResult"]/tr['+str(episodeNode)+']/td[3]/text()'
    episodeSeeds = parseByXpath(webSiteData,episodeSeedsXpath)[0]
    episodeLeechXpath = '//*[@id="searchResult"]/tr['+str(episodeNode)+']/td[4]/text()'
    episodeLeech = parseByXpath(webSiteData,episodeLeechXpath)[0]
    episodeDetails = {
        'name' : episodeName,
        'link' : magnetLink,
        'details' : episodeDetails,
        'seeds' : episodeSeeds,
        'leech' : episodeLeech
    }
    return episodeDetails
  ##  //*[@id="searchResult"]/tbody/tr[6]/td[2]/font/text()
  ##  //*[@id="searchResult"]/tbody/tr[7]/td[2]/div/a

def searchEpisode(showName,uploader,season,episode):
    print "Generating Request url"
    name=showName.split()
    url = 'https://pirateproxy.pe/search/'
    for i in range(0,len(name)):
        if(i!=(len(name)-1)):
            url = url + str(name[i]) + "%20"
        else:
            url = url + str(name[i])
    url = url + "/0/99/0"
    print url
    websiteData = sendHttpRequest(url)
    showDetails = {'name':showName,'season':season,'episode':episode,'uploader':uploader}
    return searchContent(showDetails,websiteData)

episode = searchEpisode("Game of Thrones","ettv",6,2)

print " Name : "+str(episode['name'])
print " Magnet : "+str(episode['link'])
print " Details : "+episode['details']
print " Seeds : "+str(episode['seeds'])
print " Leeches : "+str(episode['leech'])
