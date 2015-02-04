__author__ = 'dmatt'
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

########Database stuff#######
class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer,primary_key=True)
    gamedate = db.Column(db.Date,nullable=False)
    opponent = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(10), nullable=False)
    result = db.Column(db.String(10))
    score = db.Column(db.String(250))
    sport = db.Column(db.String(250))

class Members(db.Model):
    __tablename__ = 'members'
    __searchable__= ['name']
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250),nullable=False)
    instrument = db.Column(db.String(250))
    year = db.Column(db.Integer)
    ensemble_id = db.Column(db.Integer,db.ForeignKey('ensembles.id'))
    ens = db.relationship("Ensembles",secondary=lambda: membersensemble_table)

class Ensembles(db.Model):
    __tablename__ = 'ensembles'
    id = db.Column(db.Integer,primary_key=True)
    ensemblename = db.Column(db.String(250),nullable=False)
    gigs = db.relationship("Gig",backref=db.backref('ensemble'))

class Gig(db.Model):
    __tablename__= 'gig'
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.Date,nullable=False)
    sport = db.Column(db.String(250))
    ensemble_id = db.Column(db.Integer,db.ForeignKey('ensembles.id'))

membersensemble_table = db.Table('membersensembles',
                              db.Column('members_id',db.Integer,db.ForeignKey("members.id"),primary_key=True),
                              db.Column('ensemble_id',db.Integer,db.ForeignKey("ensembles.id"),primary_key=True)

)