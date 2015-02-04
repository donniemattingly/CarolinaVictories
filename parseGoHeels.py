__author__ = 'dmatt'

from bs4 import BeautifulSoup
import datetime
import urllib2
from databases import db,Games




class Game:
    '''
    Represents a game object with attributes
        date - a datetime object
        opponent - string of name of opponent
        location - string either "vs" or "@" indicating home or away
        result - string of either "W" or "L" indicating win or loss
        score - string of score, with winning score always coming first
            This is why we have to store the result and the score separately
    '''
    def __init__(self,date,opponent,location,result,score,sport):
        self.date = date
        self.opponent = opponent
        self.location = location
        self.result = result
        self.score = score
        self.sport = sport


    def printOut(self):
        print "The game on "+str(self.date.date())+" "+self.location+" "+self.opponent+" was a "+self.result+" with score "+self.score
def getLocation(classList):
    classes = ""
    for element in classList:
        classes = classes + str(element)
    cont = False
    if "home" in classes:
        cont = False
        loc = "vs"
    elif 'tournament' in classes:
        cont = True
        loc = ''
    else:
        loc = "@"


    return loc,cont
urlDict = {
    "mens-basketball":"http://www.goheels.com/SportSelect.dbml?SPSID=668157&SPID=12965&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON=",
    "football":"http://www.goheels.com/SportSelect.dbml?SPSID=667865&SPID=12962&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON=",
    "baseball":"http://www.goheels.com/SportSelect.dbml?SPSID=668153&SPID=12960&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON=",
    "mens-lacrosse":"http://www.goheels.com/SportSelect.dbml?SPSID=667870&SPID=12968&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON=",
    "mens-soccer":"http://www.goheels.com/SportSelect.dbml?SPSID=668163&SPID=12969&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON=",
    "wrestling":"http://www.goheels.com/SportSelect.dbml?SPSID=668167&SPID=12984&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON=",
    "womens-basketball":"http://www.goheels.com/SportSelect.dbml?SPSID=668170&SPID=12979&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON=",
    "field-hockey":"http://www.goheels.com/SportSelect.dbml?SPSID=866910&SPID=12961&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON=",
    "gymnastics":"http://www.goheels.com/SportSelect.dbml?SPSID=668059&SPID=12964&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON=",
    "womens-lacrosse":"http://www.goheels.com/SportSelect.dbml?SPSID=668067&SPID=12981&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON=",
    "womens-soccer":"http://www.goheels.com/SportSelect.dbml?SPSID=667901&SPID=12982&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON=",
    "softball":"http://www.goheels.com/SportSelect.dbml?SPSID=667889&SPID=12976&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON=",
    "volleyball":"http://www.goheels.com/SportSelect.dbml?SPSID=667898&SPID=12977&DB_OEM_ID_COUNT_=2&DB_OEM_ID_1_=3350&SITE=UNC&DB_OEM_ID=3350&DB_OEM_ID_0_=3350&Q_SEASON="
}
def get_sport(sport,years):
    baseurl = urlDict[sport]
    seasons = []
    for year in years:
        season = []
        # GoHeels uses the fall semester year for seasons whereas ESPN uses spring semester (2014-2015 is 2014 in goHeels and 2015 ESPN)
        url = baseurl+str(year)
        data = urllib2.urlopen(url).read()
        soup = BeautifulSoup(data)
        rows = soup.find(id="scheduleTable").tbody.find_all('tr')
        cont = False
        for row in rows:
            loc, cont = getLocation(row['class'])
            if cont:
                continue
            date = row.find(class_="date").text
            date = date.strip('\n\t')+str(year+1)
            if '-' in date:
                date = date[14:]
            dt = datetime.datetime.strptime(date,"%a, %b %d%Y")
            if dt.month >= 9:
                dt = datetime.datetime(year,dt.month,dt.day)
            # else:
            #     dt = datetime.datetime(year+1,dt.month,dt.day)
            opponent = row.find(class_='opponent').text.strip('\n\t')
            results = row.find(class_='results').text.strip('\n\t')
            results = results.replace("2OT","dOT")
            results = results.replace("(T)","(D)")
            score = results.rstrip('DLWdOT()Penaltysroks ')
            # score = results.strip('LW()OT ')
            if sport == "gymnastics":
                if "1st" in results:
                    result = "W"
                else:
                    result = "L"
            else:
                result = results.strip('d0123456789 -()OT')
            season.append(Game(dt,opponent,loc,result,score,sport))
        seasons.append(season)
    return seasons


# for i in get_sport("mens-basketball",[2012,2013,2014]):
#     for j in i:
#         j.printOut()

for key,value in urlDict.iteritems():
    print key
    print "*********************"
    for season in get_sport(key,[2011,2012,2013,2014]):
        for game in season:
            new_game = Games(gamedate=game.date.date(),
                             opponent=game.opponent,
                             location=game.location,
                             result=game.result,
                             score=game.score,
                             sport=game.sport)
            db.session.add(new_game)

db.session.commit()
