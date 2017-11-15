import re

s = "Belong To You (feat. 6LACK) - Remix [Bonus Track]"

def is_extra_left(s):
  if s in ["(", "["]:
    return True
  else:
    return False

def is_extra_right(s):
  if s in [")", "]"]:
    return True
  else:
    return False

def process_str(s, r):
  s = s[1:len(s)-1]
  if len(s) > 5 and s[0:6] == "feat. ":
    r["artist_name"] = s[6:]
  elif s == "Bonus Track":
    r["bonus_track"] = s
  elif s == "Extended Mix":
    r["extended_mix"] = s
  else:
    r["other"] = s

def test(s):
  i = 0
  r = {}
  while i < (len(s)-1):
    print "i=", i, s[i], s
    if is_extra_left(s[i]):
      j = i+1
      while j < (len(s)):
        print "j=", j, s[j], s
        if is_extra_right(s[j]):
          process_str(s[i:j+1], r)
          s = s[:i] + s[j+1:]
          print "new s:", s
          break
        else:
          j += 1

    else:
      i += 1
  
  r["final_track_name"] = re.sub('[^A-Za-z0-9 ]+', '', s)      
  print r

def main():
  s = "Belong To You (feat. 6LACK) - Remix [Bonus Track]"
  test(s)

if __name__ == "__main__":
    main()
