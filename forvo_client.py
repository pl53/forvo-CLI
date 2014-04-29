import json
import subprocess
import sys
try:
    import urllib.request as urllib2
except:
    import urllib2

# set your key here
# if you don't have one, apply one on api.forvo.com
#KEY=""
KEY="a42ebcb8105826cf33060bfcbe313cfc"

def forvo(word):

    word_url = "http://apifree.forvo.com/action" + \
               "/word-pronunciations/format/json/word/" + \
               word + "/language/en/key/" + KEY
    try: 
        response = urllib2.urlopen(word_url)
    except urllib2.HTTPError as e:
        checksLogger.error('HTTPError = ' + str(e.code))
    except urllib2.URLError as e:
        checksLogger.error('URLError = ' + str(e.reason))
    except httplib.HTTPException as e:
        checksLogger.error('HTTPException')
    except Exception:
        import traceback
        checksLogger.error('generic exception: ' + traceback.format_exc())

    data = response.read()
    json_data = json.loads(data)
    total_items, cc, mp3_url = json_data["attributes"]["total"], {}, []
    if total_items <= 0:
        print ("No English pronunciation found.")
        return 1
    cc["United States"] = 0 # cc is used to priortize american accent
    for i in range(total_items): 
        pathmp3 = json_data["items"][i]["pathmp3"]
        country = json_data["items"][i]["country"]
        mp3_url.append((cc.get(country, 1), pathmp3, country))
    mp3_url.sort() # prioritizing american accent

    # at most 5 prons per word, you can set another value
    output_num = min(5, len(mp3_url)) 
    for i in range(output_num): 
        print ("-- pronunciation {0}/{1}, {2} --".format(i+1, output_num, mp3_url[i][2]))
        subprocess.call(["mpg123", "-q", mp3_url[i][1]])
    return 0

if __name__ == "__main__":
    if KEY == "":
        print("no forvo api key found, please get one.")
    elif len(sys.argv) < 2:
        print("usage: forvo [word]")
    else:
        forvo(sys.argv[1])
