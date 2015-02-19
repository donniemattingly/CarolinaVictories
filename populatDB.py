__author__ = 'dmatt'
from main import db,Members,Games,Gig,Ensembles
db.drop_all()
db.create_all()
import parseGoHeels
import parseMembers
import parsePBS
import parsePBA
from main import update_leaderboard as  ul


def create_football_ensembles():
    fb_games = Games.query.filter_by(sport='football',location='vs')
    ensemble_names = map(lambda x:'MTH20'+str(x),[11,12,13,14])
    for i in ensemble_names:
        new_ens = Ensembles(ensemblename=i)
        print i
        new_ens_games = filter(lambda x:x.gamedate.year == int(i[3:]),fb_games)
        for j in new_ens_games:
            new_gig = Gig(sport='football',date=j.gamedate)
            new_ens.gigs.append(new_gig)
        db.session.add(new_ens)
        db.session.commit()

def assign_football_ensembles():
    fb_ensembles = filter(lambda x:'MTH' in x.ensemblename,Ensembles.query.all())
    fb_dict = {}
    for ens in fb_ensembles:
        fb_dict[ens.ensemblename[-2:]] = ens
    members = Members.query.all()
    for member in members:
        for ens in member.ens:
            if 'F' in ens.ensemblename:
                member.ens.append(fb_dict[ens.ensemblename[-2:]])
                db.session.commit()

create_football_ensembles()
assign_football_ensembles()
ul()