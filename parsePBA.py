__author__ = 'dmatt'
# encoding: utf-8
from main import db
from databases import Ensembles,Members
import re

semesters = ['F11','F12','F13','F14','S12','S13','S14','S15']
pep_dict = {}
pepbands_reduced = map(lambda x:"PB"+str(x),range(1,6))
instrumentNameList = ["Piccolo","Clarinet","Alto Sax","Tenor Sax","Trumpet","Mellophone","Trombone","Baritone","Tuba","Percussion"]

def detectInstrument(str):

    for i in range(0,len(instrumentNameList)):
        if instrumentNameList[i] in str:
            return i
        elif "Flute" in str:
            return 0
    return -1


def romanNumeral(x):
    if 0 < x and x < 4:
        return 'I'*x
    elif x == 4:
        return 'IV'
    elif x == 5:
        return 'V'


pepbands = map(lambda x: 'Pep Band '+romanNumeral(x),range(1,6))


for i in range(0, 5):
    pep_dict[pepbands[i]] = pepbands_reduced[i]
count = 0
for semester in semesters:
    f = open('static/resources/PBAs/PBA'+semester+'.txt','r')
    pepband = ''
    instrument = ''
    for line in f:
        line = line.strip().replace('’','\'')
        if line != '':
            dval = detectInstrument(line)
            if line in pepbands:
                pepband = pep_dict[line]
            elif dval != -1:
                instrument = instrumentNameList[dval]
            elif re.match("[A-Za-z ,.'-]+ [A-Za-z ,.'-]+$",line,re.UNICODE):
                line = re.findall("[A-Za-z ,.'-]+ [A-Za-z ,.'-]+$",line,re.UNICODE)[0]
                print line
                member = Members.query.filter_by(name=line+' ').first()
                q = db.session.query(Ensembles).filter(Ensembles.ensemblename == pepband+semester).first()
                if member:
                    member.ens.append(q)
                    db.session.commit()
                else:
                    if 'S' in semester: year = int('20'+semester[1:])+3
                    else: year = int('20'+semester[1:0])
                    new_member = Members(name=line+' ',instrument=instrument,year=year)
                    db.session.add(new_member)
                    new_member.ens.append(q)
                    db.session.commit()
                    count += 1

print count




