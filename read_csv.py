import csv, requests, json, pprint, re

pp = pprint.PrettyPrinter(indent=4)
cred = 'MmU4ZmMwMGI5ZGZiYjU0NzA5YWQ0ZjA2NGQyOWM0ODg6YmVkMzliNmVjYmFjYmMzOGQxNjM1NTFmYzE0YjVmMDk='
token = 'yFbSHPHs+vXX2q0lvTBC+w=='
url = 'https://api.kkbox.com/v1.1/search?'
q = ''
t = 'track'
territory = 'TW'
offset = '0'
limit = '12'
result = []

headers = { 'accept': 'application/json',
            'authorization': 'Bearer ' + token
          }

def str_decode(s):
  decode_seq = ['utf-8', 'utf-16', 'utf-32']
  for e in decode_seq:
    try:
      s = s.decode(e)
    except:
      print "Decoding", s, "to", e, "ERROR!"
    return s
    
def compare_strs(s1, s2):
  print "str type:", s1, "(", type(s1), ") VS ", s2, "(", type(s2), ")"
  if s1.lower() == s2.lower():
    return True
  return False
  

def is_same_track(trackname1, trackname2, artistname1, artistname2):
  # Compare track names
  track_compare2 = re.sub("[\(\[].*?[\)\]]", "", str_decode(trackname1).strip())
  track_compare1 = re.sub("[\(\[].*?[\)\]]", "", str_decode(trackname2).strip())
  min_track_length = min(len(track_compare1), len(track_compare2))
  print "track compare: <", track_compare1, "> VS <", track_compare2, ">"
  #print "track compare: <", (hex(ord(c)) for c in track_compare1), "> VS <", (hex(ord(c)) for c in track_compare2), ">"
  if not compare_strs(track_compare1[:min_track_length], track_compare2[:min_track_length]):
    print "track name not the same!"
    return False
  print "track name is the same."
 
  # Compare artist names 
  for single_artist_name1 in str_decode(artistname1).split(","):
    for single_artist_name2 in str_decode(artistname2).split(","):
      #artist_compare1 = ''.join(e for e in single_artist_name1 if e.isalnum())
      #artist_compare2 = ''.join(e for e in single_artist_name2 if e.isalnum())
      artist_compare1 = re.sub( "[\(\[].*?[\)\]]", "", single_artist_name1.replace(".", "").replace(" ", "") )
      artist_compare2 = re.sub( "[\(\[].*?[\)\]]", "", single_artist_name2.replace(".", "").replace(" ", "") )
      #min_artistname_length = min(len(artist_compare1), len(artist_compare2))
      print "artist compare:", artist_compare1, "VS", artist_compare2
      if compare_strs(artist_compare1, artist_compare2):
        print "[SUCCESS] track name & artist name are the same."
        return True


with open('lans_radio_ep1.csv', 'rb') as f:
  reader = csv.reader(f)
  count = 0
  for row in reader:
    print "----------------------------------------------"
    is_found_match = False
    # Spotify URI,Track Name,Artist Name,Album Name,Disc Number,Track Number,Track Duration (ms),Added By,Added At
    #print '/'.join(row), len(row)

    print "row:", row
    count += 1
    if count == 1:
      continue #skip title row

    if len(row) == 0:
      break #skip ending empty row
    
    q_trackname = row[1]
    q_artistname = row[2]
    q_albumname = row[3]
    q = q_artistname + " " + q_trackname
    print "q=", q
    
    r = requests.get(url + 'q=\"' + q + 
                          '\"&t=' + t +
                          '&territory=' + territory + 
                          '&offset=' + offset +
                          '&limit=' + limit,
                     headers=headers)
    r_json = r.json()
    try:
      data = r_json['tracks']['data']
    except:
      print r_json
      exit()
      
    for d in data:
      r_album = d['album']['name']
      r_album_artist = d['album']['artist']['name']
      r_track_name = d['name']
      r_track_url = d['url']

      #if r_album == q_albumname and r_album_artist == q_artistname and r_track_name == q_trackname:
      if is_same_track(q_trackname, r_track_name, q_artistname, r_album_artist):
        tmp = { "album" : r_album,
                "album_artist" : r_album_artist,
                "track_name" : r_track_name,
                "track_url" : r_track_url}
        result.append(tmp)
        is_found_match = True
        break
      else:
        print "( track name:", q_trackname, "VS", r_track_name, ")"
        print "( artist name:", q_artistname, "VS", r_album_artist, ")"
        print "( album name:", q_albumname, "VS", r_album, ")"
    
    if not is_found_match:
      print "[ERROR] not the same song!"
      print

    #if count == 2:
    #  break

  pp.pprint(result)
  print count, "VS", len(result)
