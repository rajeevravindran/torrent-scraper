from torrentScraper import checkEpisode, downloadEpisodeSeries

name = "Suits"
season = 5
episodes = 4
uploader = "ettv"
lowerLimit = 1
upperLimit = 15

#checkEpisode(name,season,episodes,uploader,2)
downloadEpisodeSeries(name,season,lowerLimit,upperLimit,uploader)