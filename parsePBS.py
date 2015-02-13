# encoding: utf-8
__author__ = 'dmatt'
from main import Games,db
from databases import Ensembles,Gig
from datetime import datetime
from fuzzywuzzy import fuzz,process
import re

class PreGig:
    def __init__(self,sport,date):
        self.sport = sport
        self.date = date

class Pepband:
    def __init__(self,number,semester,year):
        self.number = number
        self.semester = semester
        self.year = year
        self.gigs = []

sports_list = ['womens-lacrosse', 'football', 'wrestling', 'mens-lacrosse',
               'baseball', 'softball', 'field-hockey',
               'womens-basketball', 'volleyball', 'womens-soccer', 'mens-soccer',
               'gymnastics']

def isSport(text):
    if "vs" in text:
        return True
    else:
        return False

def isDate(text):
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    result = filter(lambda x: x in text,months)+filter(lambda x: x in text,days)
    if len(result) > 0:
        return True
    else:
        return False

def convertInitialisms(text):
    initials = {'WBall':'womens-basketball','VB':'volleyball','MS':'mens-soccer','Bball':'basketball',
                'FH':'field-hockey','WS':'womens-soccer','SB':'softball','GYM':'gymnastics',
                'WBB':'womens-basketball','WL':'womens-lacrosse','ML':'mens-lacrosse'}
    klist = initials.keys()
    if 'MBB' in text:
        return None
    for key in klist:
        if key in text:
            text = text.replace(key,initials[key])
    return text

def matchLists(results,key):
    from main import Games
    for i in results[0]:
        print i
    sports = results[0]
    dates = results[1]

    print sports
    print dates
    for i in sports:
        print "******************************"
        print i
        sport = i[0]
        opponent = i[1]
        potentialMatches = Games.query.filter_by(sport=sport)
        potentialMatches = filter(lambda x:x.gamedate.year == int('20'+key[-2:]),potentialMatches)
        hiratio = 0
        correct = potentialMatches[0]
        for j in potentialMatches:
            for k in dates:
                if j.gamedate == k.date():
                    if fuzz.ratio(j.opponent,opponent) > hiratio:
                        correct = j
        print sport + str(correct.gamedate) + str(correct.opponent) + str(hiratio)











semesters = ['F11','F12','F13','F14','S12','S13','S14','S15']
pepbands = map(lambda x:"PB"+str(x),range(1,6))
print pepbands
results = {}
master = open("static/resources/PBSs/PBSmaster.txt")
for line in master:
    current = []
    token = line.replace('’','\'').strip()
    if token:
        if token in semesters:
            key = token
            # print key
        elif token in pepbands:
            band = token
            new_ensemble = Ensembles(ensemblename=band+key)
            curEnsemble = new_ensemble
            db.session.add(curEnsemble)
            print band+key
            db.session.commit()
        else:
            giglist = token.split()
            strdate = "20"+key[-2:]+' '+reduce(lambda x,y:x+' '+y,giglist[:3])
            date =  datetime.strptime(strdate,"%Y %A, %B %d")
            sport = convertInitialisms(reduce(lambda x,y:x+' '+y,giglist[3:]).split('vs')[0])
            possibleDates = Games.query.filter_by(gamedate = date.date()).all()
            choice = process.extractOne(sport,map(lambda x:x.sport,possibleDates))
            if choice:
                if choice[1] > 90:
                    gig = filter(lambda x:x.sport == choice[0],possibleDates)[0]
                    new_gig = Gig(date=gig.gamedate,sport=gig.sport)
                    # Ensembles.query.filter_by(ensemblename=curEnsemble).first().gigs.append(new_gig)
                    curEnsemble.gigs.append(new_gig)
                    # print gig.gamedate.strftime('%A, %B %d') +' '+ gig.sport +' vs '+ gig.opponent
                    # print token
                    # print '*******************************************************'
    db.session.commit()







