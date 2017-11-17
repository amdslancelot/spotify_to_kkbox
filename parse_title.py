import re

# User Defined
import log

s = "Belong To You (feat. 6LACK) - Remix [Bonus Track]"

def is_parenthesis_left(s):
  if s in ["(", "["]:
    return True
  else:
    return False

def is_parenthesis_right(s):
  if s in [")", "]"]:
    return True
  else:
    return False

def process_str(s, r):
  s = s[1:len(s)-1]
  if len(s) > 5 and s[0:6] == "feat. ":
    r["artist"] = s[6:]
  elif s == "Bonus Track":
    r["bonus_track"] = s
  elif s == "Extended Mix":
    r["extended_mix"] = s
  else:
    r["other"] = s

# { "artist"  : "aaa",
#   "bonus_track"  : "bbb",
#   "extended_mix" : "ccc",
#   "other"        : "ddd",
#   "final_track_name_str_list" : [ "eee", "fff", "ggg" ]
def parse(s):
  i = 0
  r = {}
  while i < (len(s)-1):
    log.logger.debug( "i=%i, char=%s, str=%s" % (i, s[i], s) )
    if is_parenthesis_left(s[i]):
      j = i+1
      while j < (len(s)):
        log.logger.debug( "j=%i, char=%s, str=%s" % (j, s[j], s) )
        if is_parenthesis_right(s[j]):
          process_str(s[i:j+1], r)
          s = s[:i] + s[j+1:]
          log.logger.debug( "new s=%s" % s )
          break
        else:
          j += 1

    else:
      i += 1
  
  r["final_track_name_str_list"] = re.sub('[^A-Za-z0-9 ]+', '', s).split()
  log.logger.info("r=%s" % r)
  return r

def main():
  s = "Belong To You (feat. 6LACK) - Remix [Bonus Track]"
  parse(s)

if __name__ == "__main__":
    main()
