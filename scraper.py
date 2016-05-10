import requests
from lxml import html
import re
from time import gmtime, strftime, localtime

#print 'Enter Season number'
found=False
downloaded=False
status_file=open('status.txt','r')
data=status_file.readline()
time=status_file.readlines()
print data
if(data == 'False'):
    downloaded=False
elif(data == 'True\n'):
    downloaded=True
#season=format(input(),'02d')
season=format(6,'02d')
#print 'Enter episode number'
#episode=format(input(),'02d')
episode=format(3,'02d')
if(downloaded == False):
    print str(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    search_string='S'+str(season)+'E'+str(episode)
    print '[] Searching Game of Thrones',search_string
    print '[] Sending HTTPS request'
    page = requests.get('https://pirateproxy.pe/search/Game%20of%20Thrones/0/7/0')
    #page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
    print '[] Done. Parsing Received Search Results'
    tree = html.fromstring(page.content)
    torrent_name=tree.xpath('//*[@id="searchResult"]/tr/td/div/a/text()')
    for i in range(1,30):
        print '[] Searching '+str(search_string)+' in '+str(torrent_name[i])
        match = re.search(str(search_string),torrent_name[i])
        match2= re.search(r'ettv',torrent_name[i])
        if ((match !=None) & (match2 != None)):
            if (match.group(0)==search_string):
                print i
                print '[] Found at node '+str(i)
                found=True
                break
    ###
    if(found == True):
        n=i+1
        update_status=open('status.txt','w')
        update_status.truncate()
        update_status.write('True\n')
        update_status.write(str(strftime("%Y-%m-%d %H:%M:%S", localtime())))
        update_status.write('\n')
        update_status.write(torrent_name[n-1])
        update_status.close()
        magnet_xpath='//*[@id="searchResult"]/tr['+str(n)+']/td[2]/a[1]/@href'
        print '[] Downloading '+str(torrent_name[n-1])
        magnet_link = tree.xpath(magnet_xpath)
        print magnet_link[0]
        link="\""+str(magnet_link[0])+"\""
        payload='{"method": "auth.login", "params": ["9324651015"], "id": 1}'
        r=requests.session()
        response = r.post("http://localhost:8112/json", data=payload)
        payload2=str('{"method": "core.add_torrent_magnet", "params":[')+link+str(', {}], "id": 2}')
        response2 = r.post("http://localhost:8112/json", data=payload2)
        print response.headers
        print response.text
        print "---------"
        print response2.headers
        print response2.text
        print "---------"
    else:
        print ' <--- Not Found --> '
else:
    print "[] Looks like we already downloaded "+str(time[1])+" at "+str(time[0])+" Cheers! "
