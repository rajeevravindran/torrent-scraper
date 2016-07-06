#from torrentScraper import checkEpisode, downloadEpisodeSeries,sendJSONtoDeluge,scrape
import torrentScraper as mainLib


name = "New Girl"
season = 3
episodes = 16
uploader = ""
lowerLimit = 7
upperLimit = 23
freqMinutes = 2


#newDeluge = mainLib.Deluge()
#newDeluge.displayDetails()
#newDeluge.configure("deluge","HomePi","192.168.0.104","8112","pi","9324651015")
#newDeluge.displayDetails()
#newDeluge.testClient()

newUTorrent = mainLib.Deluge()
newUTorrent.configure("deluge","HomePi","192.168.0.104","8112","pi","9324651015")
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