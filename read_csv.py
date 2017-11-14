import csv, requests, json, pprint

pp = pprint.PrettyPrinter(indent=4)
cred = 'MmU4ZmMwMGI5ZGZiYjU0NzA5YWQ0ZjA2NGQyOWM0ODg6YmVkMzliNmVjYmFjYmMzOGQxNjM1NTFmYzE0YjVmMDk='
token = '0dJGENv47oSWOho7rlZZ0Q=='
url = 'https://api.kkbox.com/v1.1/search?'
q = ''
t = 'track'
territory = 'TW'
offset = '0'
limit = '5'
result = []

headers = { 'accept': 'application/json',
            'authorization': 'Bearer ' + token
          }

with open('lans_radio_ep1.csv', 'rb') as f:
  reader = csv.reader(f)
  count = 0
  for row in reader:
    # Spotify URI,Track Name,Artist Name,Album Name,Disc Number,Track Number,Track Duration (ms),Added By,Added At
    #print '/'.join(row), len(row)

    count += 1
    if count == 1:
      continue

    if len(row) == 0:
      break
    
    q_trackname = row[1]
    q_artistname = row[2]
    q_albumname = row[3]
    q = q_artistname + " " + q_trackname
    print q
    
    r = requests.get(url + 'q=\"' + q + 
                          '\"&t=' + t +
                          '&territory=' + territory + 
                          '&offset=' + offset +
                          '&limit=' + limit,
                     headers=headers)
    r_json = r.json()
    data = r_json['tracks']['data']
    for d in data:
      r_album = d['album']['name']
      r_album_artist = d['album']['artist']['name']
      r_track_name = d['name']
      r_track_url = d['url']

      if r_album == q_albumname and r_album_artist == q_artistname and r_track_name == q_trackname:
        tmp = { "album" : r_album,
                "album_artist" : r_album_artist,
                "track_name" : r_track_name,
                "track_url" : r_track_url}
        result.append(tmp)
        break
    
    #if count == 2:
    #  break

  pp.pprint(result)
  print count, "VS", len(result)
