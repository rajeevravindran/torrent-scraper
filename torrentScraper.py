import requests
from lxml import html
import re
from time import strftime, localtime, gmtime

class torrentClient:
    def __init__(self,type="deluge",name="deluge",ip="192.168.0.100",port="8080",username = "deluge",password = "deluge"):
        self.type = type
        self.name = name
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
    def displayDetails(self):
        #print self.name,self.ip,self.username,self.password
        print self.name+" server at "+self.ip+":"+self.port+" user ->"+self.username+" pass->"+self.password
    def configure(self,type,name,ip,port,username,password):
        self.type = type
        self.name = name
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

class Deluge(torrentClient):
    def testClient(self):
        deluge = requests.session()
        JSONString ='{"method": "auth.login", "params": ["'+str(self.password)+'"], "id": 1}'
        postRequest = "http://"+self.ip+":"+self.port+"/json"
        response = deluge.post(postRequest,data=JSONString)
        if response.ok:
            print "Test Successful"
        else:
            print "Unable to connect. Check IP,PORT or PASSWORD"

    def sendMagnetLink(self,link,name):
        link="\""+str(link)+"\""
        deluge = requests.session()
        JSONString ='{"method": "auth.login", "params": ["'+str(self.password)+'"], "id": 1}'
        postRequest = "http://"+self.ip+":"+self.port+"/json"
        response = deluge.post(postRequest,data=JSONString)
        JSONString = str('{"method": "core.add_torrent_magnet", "params":[')+link+str(', {}], "id": 2}')
        print response.headers
        response = deluge.post(postRequest,data=JSONString)
        updateLog("Downloading "+name+" "+str(response.headers))

class Transmittion(torrentClient):
    def testClient(self):
        newSession = requests.session()
        postString = "http://"+self.ip+":"+self.port+"/transmission/rpc"
        test = newSession.get(postString,auth=(self.username,self.password))
        if test.status_code == 200:
            print "Successful"
        elif test.status.code == 401:
            print "Authentication Failed. Check username and password"
        else:
            print "Connection Failed. Check server IP and port. Is Transmission running?"
    def sendMagnetLink(self,link,name):
        JSONlink = "{\"method\": \"torrent-add\", \"arguments\": {\"paused\": \"false\", \"filename\": "+str(link)+"}}"
        

class uTorrent(torrentClient):
    def testClient(self):
        utorrent = requests.session()
        postString = "http://"+self.ip+":"+self.port+"/gui/token.html"
        request = utorrent.get(postString,auth=(self.username, self.password))
        httpReturnCode = request.status_code
        if httpReturnCode == 401:
            print "uTorrent Authentication Failed. Check username and password"
        else:
            extractedHTML = html.fromstring(request.content)
            self.extractedToken = extractedHTML.xpath('//div/text()')[0]
            print "Successful. Retrieved Token -->"+self.extractedToken
    def sendMagnetLink(self,link,name):
        utorrent = requests.session()
        postString = "http://"+self.ip+":"+self.port+"/gui/token.html"
        print postString
        request = utorrent.get(postString,auth=(self.username, self.password))
        httpReturnCode = request.status_code
        if httpReturnCode == 401:
            print "uTorrent Authentication Failed. Check username and password"
        else:
            extractedHTML = html.fromstring(request.content)
            extractedToken = extractedHTML.xpath('//div/text()')[0]
            print "Successful. Retrieved Token -->"+extractedToken
        link = requests.utils.quote(link,safe='')
        postString = "http://"+self.ip+":"+self.port+"/gui/?token="+str(extractedToken)+"&action=add-url&s="+link
        print postString
        response = utorrent.get(postString,auth=(self.username, self.password))
        print response
        updateLog("Downloading "+name+" "+str(response.headers))

class MainScraper:
    def __init__(self):
        self.downloader = torrentClient()
        self.scrapeSite = "piratebay.red"
    def configureScraper(self,downloader,siteName):
        self.downloader.configure(downloader.type,downloader.name,downloader.ip,downloader.port,downloader.username,downloader.password)
        self.scrapeSite = siteName
        if downloader.type == "deluge":
            self.downloader = Deluge(downloader.type,downloader.name,downloader.ip,downloader.port,downloader.username,downloader.password)
        if downloader.type == "utorrent":
            self.downloader = uTorrent(downloader.type,downloader.name,downloader.ip,downloader.port,downloader.username,downloader.password)
    def searchContent(self,showDetails,webSiteData):
        if(showDetails['uploader']!=None):
            uploaderMatch = False
            episodeMatch = False
            i = 0
            searchLimit = 30
            search_string=showDetails['secondary']
            torrent_name = parseByXpath(webSiteData,'//*[@id="searchResult"]/tr/td/div/a/text()')
            while(episodeMatch == False):
                if(i > 29 or len(torrent_name) == 0):
                    break;
                match = re.search(str(search_string),torrent_name[i])
                match2= re.search(str(showDetails['uploader']),torrent_name[i])
                episodeUploaderXpath = '//*[@id="searchResult"]/tr['+str(i+1)+']/td[2]/font/a/text()'
                episodeUploader = parseByXpath(webSiteData,episodeUploaderXpath)
                if(len(episodeUploader)==0):
                    episodeUploader = 'Anonymous'
                else:
                    episodeUploader = episodeUploader[0]
                if (episodeUploader == showDetails['uploader'] or bool(showDetails['uploader']) == False):
                    uploaderMatch = True
                else:
                    uploaderMatch = False
                print '['+str(i).encode('utf-8')+'] Searching '+(search_string).encode('utf-8')+' by '+(showDetails['uploader']).encode('utf-8')+' in '+(torrent_name[i]).encode('utf-8')
                i = i + 1
                if ((match !=None)):
                    if (match.group(0)==search_string and uploaderMatch == True):
                        print 'Matched search'
                        print '[] Found at node '+str(i)
                        episodeMatch=True
                        break
            if(episodeMatch == True):
                print "[] Found. Parsing Details"
                episodeNode = i
                episodeNameXpath = '//*[@id="searchResult"]/tr['+str(episodeNode)+']/td[2]/div/a/text()'
                episodeName = parseByXpath(webSiteData, episodeNameXpath)[0]
                episodeMagnetXpath = '//*[@id="searchResult"]/tr['+str(episodeNode)+']/td[2]/a[1]/@href'
                magnetLink = parseByXpath(webSiteData,episodeMagnetXpath)[0]
                episodeUploaderXpath = '//*[@id="searchResult"]/tr['+str(episodeNode)+']/td[2]/font/a/text()'
                episodeUploader = parseByXpath(webSiteData,episodeUploaderXpath)[0]
                episodeDetailsXpath =  '//*[@id="searchResult"]/tr['+str(episodeNode)+']/td[2]/font/text()'
                episodeDetails = parseByXpath(webSiteData,episodeDetailsXpath)[0]+str(episodeUploader)
                episodeSeedsXpath = '//*[@id="searchResult"]/tr['+str(episodeNode)+']/td[3]/text()'
                episodeSeeds = parseByXpath(webSiteData,episodeSeedsXpath)[0]
                episodeLeechXpath = '//*[@id="searchResult"]/tr['+str(episodeNode)+']/td[4]/text()'
                episodeLeech = parseByXpath(webSiteData,episodeLeechXpath)[0]
                episodeUploaderXpath = '//*[@id="searchResult"]/tr['+str(episodeNode)+']/td[2]/font/a/text()'
                episodeUploader = parseByXpath(webSiteData,episodeUploaderXpath)[0]
                episodeDetails = {
                    'name' : episodeName,
                    'link' : magnetLink,
                    'details' : episodeDetails,
                    'seeds' : episodeSeeds,
                    'leech' : episodeLeech,
                    'uploader' : episodeUploader
                }
            if(episodeMatch == True):
                return episodeDetails
            else:
                return None
      ##  //*[@id="searchResult"]/tbody/tr[6]/td[2]/font/text()
      ##  //*[@id="searchResult"]/tbody/tr[7]/td[2]/div/a
        ## //*[@id="searchResult"]/tbody/tr[22]/td[2]/font/i

    def scrape(self,Name,uploader,secondary,pageLimit=10):
        gotEpisode = False
        page = 0
        while(gotEpisode == False):
            print "Generating Request url for page "+str(page)
            name=Name.split()
            url = 'https://'+self.scrapeSite+'/search/'
            for i in range(0,len(name)):
                if(i!=(len(name)-1)):
                    url = url + str(name[i]) + "%20"
                else:
                    url = url + str(name[i])
            url = url + "/"+str(page)+"/99/205"
            print url
            websiteData = sendHttpRequest(url)
            page = page + 1
            showDetails = {'name':Name,
                           'secondary':secondary,
                           'uploader':uploader
            }
            searchResult = self.searchContent(showDetails,websiteData)
            if(searchResult!=None):
                gotEpisode = True
                #updateLog(str(searchResult))
                updateLog("Found "+searchResult['name']+" Seeds "+str(searchResult['seeds'])+" Leech "+str(searchResult['leech'])+" Uploader "+str(searchResult['uploader']))
            if(page == pageLimit):
                updateLog(showDetails['name']+" "+showDetails['secondary']+" not found within "+str(page)+" pages")
                return {
                    'name' : 'Not Found',
                    'link' : 'Not Found',
                    'details' : 'Not Found',
                    'seeds' : 'Not Found',
                    'leech' : 'Not Found',
                    'uploader' : 'Not Found'
                }
        return searchResult

    def checkEpisode(self,name,season,episode,uploader,frequency):
        firstTime = True
        previousTime = 1
        while True:
            firstTime = True
            time = int(strftime("%M",gmtime()))
            if time%frequency == 0 and firstTime == True and time!=previousTime:
                firstTime = False
                previousTime = time
                updateLog("Checking for "+str(name)+" "+generateEpisodeNumber(season,episode))
                episodeInfo = self.scrape(name,uploader,generateEpisodeNumber(season,episode))
                if(episodeInfo['link']!='Not Found'):
                    print episodeInfo
                    self.downloader.sendMagnetLink(str(episodeInfo['link']),str(episodeInfo['name']),self.downloader.ip,self.downloader.port,self.downloader.password)
                    break;

    def downloadEpisodeSeries(self,name,season,lowerLimit,upperLimit,uploader):
        matchedEpisodes=[]
        for i in range(lowerLimit-1,upperLimit):
            episode = self.scrape(name,uploader,generateEpisodeNumber(season,i+1))
            matchedEpisodes.append(episode)
        for i in range(0,len(matchedEpisodes)):
            if(str(matchedEpisodes[i]['link']) != 'Not Found'):
                print matchedEpisodes
                self.downloader.sendMagnetLink(str(matchedEpisodes[i]['link']),str(matchedEpisodes[i]['name']))
    def cmdScrape(self,url,searchString):
        print url
def sendHttpRequest(url):
    print "[] Sending HTTPS request to "+str(url)
    try:
        page = requests.get(url)
    except requests.exceptions.RequestException, Arguement:
        updateLog(" Error "+str(Arguement))
        sendHttpRequest(url)
    content = html.fromstring(page.content)
    print "[] Received content"
    return content

def parseByXpath(HtmlContent,xpath):
    return HtmlContent.xpath(xpath)

def updateLog(logThis):
    status_file=open('events.log','a')
    status_file.write(str(strftime("%Y-%m-%d %H:%M:%S", localtime())))
    status_file.write(" --> ")
    status_file.write(logThis)
    status_file.write("\n")
    status_file.close()

def generateEpisodeNumber(season,episode):
    season=format(int(season),'02d')
    episode=format(int(episode),'02d')
    generated='S'+str(season)+'E'+str(episode)
    return generated