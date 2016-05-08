import requests
from lxml import html
import re
print 'Enter Season number'
found=False
#season=format(input(),'02d')
season=format(6,'02d')
#print 'Enter episode number'
#episode=format(input(),'02d')
episode=format(2,'02d')
search_string='S'+str(season)+'E'+str(episode)
print '[INFO] Searching ',search_string
print '[INFO] SENDING REQUEST'
page = requests.get('https://pirateproxy.pe/search/Game%20of%20Thrones/0/7/0')
#page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
print '[INFO] DONE'
tree = html.fromstring(page.content)
torrent_name=tree.xpath('//*[@id="searchResult"]/tr/td/div/a/text()')
for i in range(1,30):
    print 'Searching '+str(search_string)+' in '+str(torrent_name[i])
    match = re.search(str(search_string),torrent_name[i])
    if(match !=None):
        if (match.group(0)==search_string):
            print i
            print 'Found at node '+str(i)
            found=True
            break
###
if(found == True):
    n=i+1
    magnet_xpath='//*[@id="searchResult"]/tr['+str(n)+']/td[2]/a[1]/@href'
    print ' Downloading '+str(torrent_name[n-1])
    magnet_link = tree.xpath(magnet_xpath)
    print magnet_link[0]
    link="\""+str(magnet_link[0])+"\""
    payload='{"method": "auth.login", "params": ["9324651015"], "id": 1}'
    r=requests.session()
    response = r.post("http://192.168.0.104:8112/json", data=payload)
    payload2=str('{"method": "core.add_torrent_magnet", "params":[')+link+str(', {}], "id": 2}')
    response2 = r.post("http://192.168.0.104:8112/json", data=payload2)
    print response.headers
    print response.text
    print "---------"
    print response2.headers
    print response2.text
    print "---------"
else:
    print 'Not Found'

