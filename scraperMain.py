#from torrentScraper import checkEpisode, downloadEpisodeSeries,sendJSONtoDeluge,scrape
import torrentScraper as mainLib


name = "Silicon Valley"
season = 3
episodes = 10
uploader = "ettv"
lowerLimit = 1
upperLimit = 13
freqMinutes = 2


newDeluge = mainLib.Deluge("deluge","192.168.0.100","8081","pi","9324651015")
newDeluge.displayDetails()
newDeluge.configure("HomePi","192.168.0.104","8112","pi","9324651015")
newDeluge.displayDetails()

Scraper = mainLib.MainScraper()
Scraper.configureScraper("HomePi","192.168.0.104","8112","pi","9324651015")
Scraper.downloader.displayDetails()
scrapedInfo = Scraper.scrape("House of Cards","","S02E03",2)

newDeluge.sendMagnetLink(scrapedInfo['link'],scrapedInfo['name'])
#heckEpisode(name,season,episodes,uploader,freqMinutes)
#downloadEpisodeSeries(name,season,lowerLimit,upperLimit,uploader)
#request = scrape("House of Cards","","S04E01")
#sendJSONtoDeluge(request['link'],request['name'],"192.168.0.104","8112","9324651015")