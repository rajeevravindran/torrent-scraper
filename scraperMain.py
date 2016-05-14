from torrentScraper import checkEpisode, downloadEpisodeSeries,sendJSONtoDeluge,scrape



name = "Person of Interest"
season = 5
episodes = 14
uploader = ""
lowerLimit = 1
upperLimit = 13

#checkEpisode(name,season,episodes,uploader,2)
#downloadEpisodeSeries(name,season,lowerLimit,upperLimit,uploader)
request = scrape("Person of Interest","","Season 1")
sendJSONtoDeluge(request['link'],request['name'],"192.168.0.104","8112","9324651015")