#from torrentScraper import checkEpisode, downloadEpisodeSeries,sendJSONtoDeluge,scrape
import torrentScraper as mainLib


name = "Silicon Valley"
season = 3
episodes = 10
uploader = "ettv"
lowerLimit = 1
upperLimit = 10
freqMinutes = 2


#newDeluge = mainLib.Deluge()
#newDeluge.displayDetails()
#newDeluge.configure("deluge","HomePi","192.168.0.104","8112","pi","9324651015")
#newDeluge.displayDetails()
#newDeluge.testClient()

newUTorrent = mainLib.uTorrent()
newUTorrent.configure("utorrent","RajeevLaptop","localhost","8080","admin","qwerty")
newUTorrent.displayDetails()
newUTorrent.testClient()
Scraper = mainLib.MainScraper()
Scraper.configureScraper(newUTorrent)
Scraper.downloader.testClient()
Scraper.downloader.displayDetails()
#scrapedInfo = Scraper.scrape("House of Cards","","S04E02",2)
#Scraper.downloader.sendMagnetLink(scrapedInfo['link'],scrapedInfo['name'])
#ewDeluge.sendMagnetLink(scrapedInfo['link'],scrapedInfo['name'])
#heckEpisode(name,season,episodes,uploader,freqMinutes)
Scraper.downloadEpisodeSeries(name,season,lowerLimit,upperLimit,uploader)
#request = scrape("House of Cards","","S04E01")
#sendJSONtoDeluge(request['link'],request['name'],"192.168.0.104","8112","9324651015")