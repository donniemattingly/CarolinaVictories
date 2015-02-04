__author__ = 'dmatt'

 # -*- coding: latin-1 -*-
from databases import Members,Ensembles,Gig
from main import db
import re
from datetime import datetime


class Band:
    '''
    This class is a wrapper around list with some methods to help with the member instances
    which are part of an internal list, this class is also using iterators
    '''

    def __init__(self):
        self.size = 0
        self.members = []
        self.index = 0


    def __iter__(self):
        return self

    def next(self):
        self.index = self.index + 1
        if self.index >= self.size-1:
            raise StopIteration
        return self.members[self.index]

    def add(self,member):
        self.members.append(member)
        self.size = self.size + 1

    def contains(self,name):
        for i in self.members:
            if i.name in name:
                return True
        return False
    def get(self,name):
        for i in self.members:
            if i.name in name:
                return i
        return None


class Member:
    '''
    Member has properties:
        name - string name
        instrument - string name of instrument
        years - list of int years
        ensembles - list of string ensembles
    '''

    def __init__(self,name,instrument,ensemble):
        self.ensembles = []
        self.name = name[:-1]
        self.instrument = instrument
        self.victories = 0
        self.gradyear = 0
        # self.years.append(year)
        self.ensembles.append(ensemble)

    # def addYear(self,year):
    #     if year not in self.years:
    #         self.years.append(year)
    def changeInstrument(self,instrument):
        self.instrument = instrument

    def addEnsemble(self,ensemble):
        if ensemble not in self.ensembles:
            self.ensembles.append(ensemble)
    def determineYear(self):
        self.years = map(lambda x:x.name[0:4],self.ensembles)
        self.maxyear = max(self.years)
        self.maxcount= len(filter(lambda x:x==self.maxyear,self.years))
        self.minyear = min(self.years)
        self.deltayear =int(self.maxyear)-int(self.minyear)
        if self.maxcount == 2:
            self.gradyear = int(self.maxyear)
        else:
            self.gradyear = 3-self.deltayear+int(self.maxyear)
        # print self.name+ "with maxcount: "+str(self.maxcount)+" and deltayear: "+str(self.deltayear)+" and last year in: "+self.maxyear
        # print "My Guess for "+self.name+"'s graduation year is: "+str(self.gradyear)


    def printOut(self):
        head = "Student "+self.name+", a member of the "+self.instrument+" section, was in the "
        ens = ""
        for i in self.ensembles:
            ens = ens + i.name + " "
        print head + ens


instrumentNameList = ["Piccolo","Clarinet","Alto Sax","Tenor Sax","Trumpet","Mellophone","Trombone","Baritone","Tuba","Percussion"]

class Ensemble:
    '''

    '''

    def __init__(self,name,dates):
        self.name = name
        self.dates = dates

    def getVictories(self,seasons):
        # seasons is a list of each season which is a list of all the games in that season
        # this checks the dates against the dates of each game, if there is a match it records the result
        self.victories = 0
        for season in seasons:
            for game in season:
                for date in self.dates:
                    if date == game.date:
                        game.printOut()
                        if "W" in game.result:
                            self.victories = self.victories + 1

        return self.victories




def detectInstrument(str):

    for i in range(0,len(instrumentNameList)):
        if instrumentNameList[i] in str:
            return i
        elif "Flute" in str:
            return 0
    return -1




f12 = open("static/resources/BW11-12.txt")
f13 = open("static/resources/BW12-13.txt")
f14 = open("static/resources/BW13-14.txt")
f15 = open("static/resources/BW14-15.txt")

def parseLists():
    yearDict = {f12:2012,f14:2014,f15:2015,f13:2013}
    files = [f12,f13,f14,f15]
    band = Band()
    blueDict = {f12:Ensemble('2012blue',[]),f13:Ensemble('2013blue',[]),f14:Ensemble('2014blue',[]),f15:Ensemble('2015blue',[])}
    whiteDict = {f12:Ensemble('2012white',[]),f13:Ensemble('2013white',[]),f14:Ensemble('2014white',[]),f15:Ensemble('2015white',[])}
    ensembleDict = {"blue":blueDict,"white":whiteDict}
    list = ""
    name = ""
    instrument = instrumentNameList[0]

    for file in files:
        for line in file:
            year = yearDict[file]
            dval = detectInstrument(line)
            match1 = re.search(" [0-9]+\/[0-9]+ ",line,re.UNICODE)
            match2 = re.search("[A-Za-z]+ \d+, \d\d\d\d",line,re.UNICODE)
            # match = re.search()
            if ("Blue" in line) and ("Band" in line):
                list = "blue"
            elif ("White" in line) and ("Band" in line):
                list = "white"
            elif match1:
                line = str(year)+" " + line[:-2]
                dt = datetime.strptime(line,"%Y %A, %m/%d")
                if dt.month >= 10:
                    dt = datetime(year-1,dt.month,dt.day)
                ensembleDict[list][file].dates.append(dt)
            elif match2:
                line = line[:-2]
                print repr(line)
                dt = datetime.strptime(line,"%B %d, %Y")
                ensembleDict[list][file].dates.append(dt)
            elif (dval != -1):
                instrument = instrumentNameList[dval]
            elif re.match("[A-Za-z ,.'-]+ [A-Za-z ,.'-]+ $",line,re.UNICODE):
                name = line
                if not band.contains(name):
                    band.add(Member(name,instrument,ensembleDict[list][file]))
                else:
                    tempMem = band.get(name)
                    tempMem.addEnsemble(ensembleDict[list][file])
    return ensembleDict,band








years = [2011,2012,2013,2014]
ensemblesDict = {}
eDict, band = parseLists()

for key1,value1 in eDict.iteritems():
    for key2, value2 in value1.iteritems():
        new_ensemble = Ensembles(ensemblename=value2.name)
        db.session.add(new_ensemble)
        for gamedate in  value2.dates:
            new_gig = Gig(date = gamedate, sport = "mens-basketball")
            new_ensemble.gigs.append(new_gig)

db.session.commit()



for student in band:
    student.determineYear()
    db.session.add(Members(name = student.name,instrument = student.instrument,year=student.gradyear))
    db.session.commit()
    for i in student.ensembles:
        # print student.name+' was in the '+i.name
        m = db.session.query(Members).filter(Members.name == student.name).first()
        # print m
        q = db.session.query(Ensembles).filter(Ensembles.ensemblename == i.name).first()
        # print q
        # print q.ensemblename
        m.ens.append(q)


db.session.commit()

# print db.session.query(Members).all()

# for i in band:
#     # for j in i.ensembles:
#     #     i.victories = i.victories + ensemblesDict[j].victories
#     # if "Tuba" in i.instrument and len(i.ensembles) >= 5:
#     #     print i.name + " has "+ str(i.victories)+" victories"
#     i.printOut()
