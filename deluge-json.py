import requests

payload='{"method": "auth.login", "params": ["9324651015"], "id": 1}'
r=requests.session()
response = r.post("http://192.168.0.104:8112/json", data=payload)

print response.headers
print response.text

print "---------------"

print "---------------"

link="magnet:?xt=urn:btih:1b43cc1169821dda932868f0b317e48863717ba4&dn=Suits.S05E15.HDTV.x264-KILLERS%5Bettv%5D&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969"
payload2='{"method": "core.add_torrent_magnet", "params": ["magnet:?xt=urn:btih:16c8076181b17eee1ed8690614b0c23013378f20&dn=House+of+Cards+2013+S04E02+720p+WEBRip+X264-DEFLATE&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969", {}], "id": 2}'

response2 = r.post("http://192.168.0.104:8112/json", data=payload2)

print response2.headers
print response2.text


print "---------------"