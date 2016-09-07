import torrentScraper as mainLib
from sys import argv

site = argv[1]
name = argv[2]
season = int(argv[3])
episodes = int(argv[4])
uploader = argv[5]
lowerLimit = int(argv[6])
upperLimit = int(argv[7])
freqMinutes = 2

newUTorrent = mainLib.Deluge()
newUTorrent.configure("deluge","HomePi","192.168.0.104","8112","pi","9324651015")
newUTorrent.displayDetails()
newUTorrent.testClient()
Scraper = mainLib.MainScraper()
Scraper.configureScraper(newUTorrent,site)
Scraper.downloader.testClient()
Scraper.downloader.displayDetails()
Scraper.downloadEpisodeSeries(name,season,lowerLimit,upperLimit,uploader)