from torrentScraper import checkEpisode, downloadEpisodeSeries

name = "Suits"
season = 4
episodes = 4
uploader = ""
lowerLimit = 1
upperLimit = 16

#checkEpisode(name,season,episodes,uploader,2)
downloadEpisodeSeries(name,season,lowerLimit,upperLimit,uploader)