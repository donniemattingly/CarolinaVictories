#!/usr/bin/env python

'''
Created on Nov 27, 2013

@author: dmatt
'''
import urllib2
# from Tkinter import Tk
# from tkFileDialog import askdirectory
import time
import json
import re
# from mechanize import Browser
import os
from bs4 import BeautifulSoup
global basefilename
def clearDir():
    for the_file in os.listdir(basefilename):
        file_path = os.path.join(basefilename, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e
def getName():
    global basefilename
    # basefilename = "C:\Users\mstock\Dropbox\Public\CSV"
    # basefilename = "/Users/dmatt/Desktop"
    basefilename  = "/var/www/html/parser"
def parsePT_NBAold ():
     
    soup = BeautifulSoup(urllib2.urlopen('http://www.thepredictiontracker.com/prednba.html','html5lib').read())
    if soup.get_text() == '':
        print "Sorry no games today for NBA (PT)"
        return
    else:
        pre2 = soup.find_all('pre')[1]
        split2 = unicode(pre2).splitlines()

        filename = basefilename+"/"+"PT_NBA"+time.strftime("%m_%d_%Y")+".csv"
           
        f = open(filename,"w")  
        f.write("\n")
        split2.pop(0)
        for i in split2:
            temp = i.split("        ")
            temp[:] = (value for value in temp if value != u'')
            t1 = [temp[0],temp[1]]
            t2 = temp[2].split()
            temp = t1+t2
            for j in temp:
                f.write(j.strip())
                f.write(",")
            f.write("\n")
        f.close()
def parsePT_NBA ():

    soup = BeautifulSoup(urllib2.urlopen('http://www.thepredictiontracker.com/prednba.html').read())
    if soup.get_text() == '':
        print "Sorry no games today for NBA (PT)"
        return
    else:
        pre2 = soup.find_all('pre')[1]
        split2 = unicode(pre2).splitlines()

        filename = basefilename+"/"+"PT_NBA"+time.strftime("%m_%d_%Y")+".csv"

        f = open(filename,"w")
        f.write("\n")
        split2.pop(0)
        for i in split2:
            # print i
            temp = []
            for j in re.split("(-*\d+\.*\d*)",i):
                for k in re.split("( \. )",j):
                    # for l in re.split("(([A-Za-z\'\-]+[\.]?[ ])+)",k):
                    for l in k.split("  "):
                        if l.strip() is not u'':
                            temp.append(l.strip())
            # print temp

            for j in temp:
                f.write(j.strip())
                f.write(",")
            f.write("\n")
        f.close()

def parsePT_CBB ():

    soup = BeautifulSoup(urllib2.urlopen('http://www.thepredictiontracker.com/predbb.html').read())
    if soup.get_text() == '':
        print "Sorry no games today for CBB (PT)"
        return
    else:
        pre2 = soup.find_all('pre')[1]
        split2 = unicode(pre2).splitlines()

        filename = basefilename+"/"+"PT_CBB"+time.strftime("%m_%d_%Y")+".csv"

        f = open(filename,"w")
        f.write("\n")
        split2.pop(0)
        for i in split2:
            # print i
            temp = []
            for j in re.split("(-*\d+\.*\d*)",i):
                for k in re.split("( \. )",j):
                    # for l in re.split("(([A-Za-z\'\-]+[\.]?[ ])+)",k):
                    for l in k.split("  "):
                        if l.strip() is not u'':
                            temp.append(l.strip())
            # print temp

            for j in temp:
                f.write(j.strip())
                f.write(",")
            f.write("\n")
        f.close()
    
    
def parseM_NBA ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=nba&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_NBA"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

def parseM_CBB ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=cb&sub=11590&&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_CBB"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

def parseM_MLB ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=mlb&sub=14342&&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_MLB"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

def parseM_NHL ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=nhl&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_NHL"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

def parseM_WNBA ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=wnba&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_WNBA"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

def parseM_CFL ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=cfl&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_CFL"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

def parseM_MLS ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=mls&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_MLS"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

def parseM_EPL ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=dls&sub=70206&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_EPL"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

def parseM_ITA ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=dls&sub=70211&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_ITA"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

def parseM_ESP ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=dls&sub=70232&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_ESP"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

def parseM_GER ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=dls&sub=70208&dt='+time.strftime("%Y%m%d")).read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_GER"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

def parseM_TennisM ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=atp').read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_TennisM"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')

def parseM_TennisW ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/predjson.php?s=wta').read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_TennisW"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Away,Home,AwayPred,HomePred,AwayPwin,HomePwin,AwayMargin,HomeMargin\n")       
    for i in data:
        away = i[2][0]
        home = i[3][0][2:]
        awayPred = str(i[8][0])
        homePred = str(i[9][0])
        awayPwin = str(i[10][0])
        homePwin = str(i[11][0])
        awayMar = str(i[12][0])
        homeMar = str(i[13][0])
        f.write(away+','+home+','+awayPred+','+homePred+','+awayPwin+','+homePwin+','+awayMar+','+homeMar+'\n')


def parseM_MLB_Rate ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/ratejson.php?s=205682&sub=14342').read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_MLB_Rate"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Team,Rate\n")
    for i in data:
        team = i[0][0]
        rate = str(i[6])
        f.write(team+','+rate+'\n')

def parseM_NBA_Rate ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/ratejson.php?s=203255').read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_NBA_Rate"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Team,Rate\n")
    for i in data:
        team = i[0][0]
        rate = str(i[6])
        f.write(team+','+rate+'\n')

def parseM_NHL_Rate ():
    soup = BeautifulSoup(urllib2.urlopen('http://masseyratings.com/ratejson.php?s=203254').read())
    data = json.loads(soup.get_text())
    headings = data[u'CI']
    data = data[u'DI']
    filename = basefilename+"/"+"M_NHL_Rate"+time.strftime("%m_%d_%Y")+".csv"
      
    f = open(filename,"w")
    f.write("Team,Rate\n")
    for i in data:
        team = i[0][0]
        rate = str(i[6])
        f.write(team+','+rate+'\n')

def testParse():
    soup = BeautifulSoup(urllib2.urlopen('http://www.thepredictiontracker.com/predbb.html').read())
    if soup.get_text() == '':
        print "Sorry no games today for CBB (PT)"
        return
    else:
        i = soup.find_all('pre')[1]
        for j in  unicode(i.b.next_sibling).splitlines():
            print "newline"
            print j


getName()
# testParse()
clearDir()
parseM_MLB()
parseM_NBA()
parseM_CBB()
parseM_NHL()
parseM_WNBA()
parseM_CFL()
parseM_MLS()

parsePT_NBA()
parsePT_CBB()

parseM_MLB_Rate()
parseM_NBA_Rate()
parseM_NHL_Rate()
