import json, datetime, re

allmytweets = []
with open('./data/tweet.js', 'r') as f:
    lines = f.readlines()
    lines[0] = '['
    allmytweets = json.loads('\n'.join(lines))

def gettext(tweet):
    return tweet['tweet']['full_text']
# convert 'created_at' in twitter to date object
def gettweettime(tweet):
    rawdata = tweet['tweet']['created_at'].split(' ')
    year = int(rawdata[5])
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month = months.index(rawdata[1]) + 1
    day = int(rawdata[2])
    instant = rawdata[3].split(':')
    hour = int(instant[0])
    minute = int(instant[1])
    second = int(instant[2])
    date = datetime.datetime(year, month, day, hour, minute, second, tzinfo=datetime.timezone.utc)
    return date.astimezone(datetime.timezone(datetime.timedelta(hours=9)))

# get all my tweets last year
fromdate = datetime.datetime(2021, 1, 1, 0, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
todate = datetime.datetime(2022,1, 9, 0, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
targettweets = []
for tweet in allmytweets:
    tweetdate = gettweettime(tweet)
    if tweetdate >= fromdate and tweetdate <= todate:
        targettweets.append(gettext(tweet))

# get all lines including the word 'ピアノ'
screentime = 0
def calcscreentime(line):
    ret = [0, 0]
    substr = line[3:]
    i = 0
    tmp = ''
    while i < len(substr):
        if substr[i] == '時':
            try:
                ret[0] = int(tmp)
            except ValueError:
                ret = (0, 0)
                break
            tmp = ''
            i += 2
        elif substr[i] == '分':
            try:
                ret[1] = int(tmp)
            except ValueError:
                ret = (0, 0)
                break
            tmp = ''
            i += 1
        else:
            tmp += substr[i]
            i += 1
    # print(ret)
    return ret[0]*60 + ret[1]

prefix = '^ピアノ.*'
suffix = '.*((分$)|(時間$))'
for text in targettweets:
    lines = text.split('\n')
    for line in lines:
        line.strip()
        if re.match(prefix, line) and re.match(suffix, line):
            screentime += calcscreentime(line)

print(f'Your piano screentime ... {screentime//60}時間{screentime%60}分')
