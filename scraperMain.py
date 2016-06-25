from torrentScraper import checkEpisode, downloadEpisodeSeries,sendJSONtoDeluge,scrape



name = "Game of Thrones"
season = 6
episodes = 4
uploader = "ettv"
lowerLimit = 1
upperLimit = 13
freqMinutes = 2


checkEpisode(name,season,episodes,uploader,freqMinutes)
#downloadEpisodeSeries(name,season,lowerLimit,upperLimit,uploader)
#request = scrape("House of Cards","","S04E01")
#sendJSONtoDeluge(request['link'],request['name'],"192.168.0.104","8112","9324651015")