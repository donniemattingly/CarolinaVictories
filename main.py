__author__ = 'dmatt'
import os
from flask import Flask,request, render_template,abort,redirect,url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import StringField,SubmitField
from wtforms.validators import Required
import flask.ext.whooshalchemy as whooshalchemy
import mimetypes



app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'thisneedstobechanged'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carolinavictories.db'
db = SQLAlchemy(app)
mimetypes.add_type('image/svg+xml', '.svg')
app.debug = True

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

listofmembers = Members.query.all()
listofmembers = map(lambda x:x.name,listofmembers)
listofgames = Games.query.all()

whooshalchemy.whoosh_index(app, Members)


def printGameAttributes(gamelist):
    for game in gamelist:
        if game and game.sport == 'mens-basketball':
            print 'game on date '+str(game.gamedate)+'vs'+game.opponent+' was a '+game.result+' with a score of '+game.score
class NameForm(Form):
    name = StringField(validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        return redirect(url_for('member',username=name.replace(' ','_')))
    return render_template('index.html',form=form,name=name)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html',memberslist=listofmembers)

@app.route('/testmember')
def about():
    abort(404)

@app.route('/gamelist')
def gamelist():
    return render_template('gamelist.html',gamelist=listofgames)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/members/<username>')
def member(username):
    username = username.replace('_',' ')+' '
    member = Members.query.filter_by(name=username).first()
    if member == None:
        abort(404)
    member_gigs = []
    for i in member.ens:
        for j in i.gigs:
            game_instance = Games.query.filter_by(gamedate=j.date,sport='mens-basketball').first()
            if game_instance != None:
                member_gigs.append(game_instance)
            else:
                member_gigs.append(j.date)
    member_gigs = sorted(member_gigs,key=lambda game:game.gamedate)
    wins = filter(lambda x:x.result == 'W',member_gigs)
    victories = len(wins)
    return render_template('testmember.html',instrument=member.instrument,gamelist=member_gigs,member_name=member.name,num_victories=victories)




if __name__ == '__main__':
    manager.run()