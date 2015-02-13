__author__ = 'dmatt'
import os
from flask import Flask,session, render_template,abort,redirect,url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
import mimetypes
from databases import Games,Members,db



app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
app.config.from_envvar('CV_SETTINGS')
db.app = app
db.init_app(app)
mimetypes.add_type('image/svg+xml', '.svg')
app.debug = True






def printGameAttributes(gamelist):
    for game in gamelist:
        if game and game.sport == 'mens-basketball':
            print 'game on date '+str(game.gamedate)+'vs'+game.opponent+' was a '+game.result+' with a score of '+game.score
class NameForm(Form):
    name = StringField(validators=[Required()])
    submit = SubmitField('Find Out')

@app.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        session['search'] = form.name.data
        return redirect(url_for('results'))
    return render_template('index.html',form=form,name=name)

@app.route('/leaderboard')
def leaderboard():
    memberslist = Members.query.all()
    memberslist = sorted(memberslist,key=lambda x:x.victorycount,reverse=True)
    return render_template('leaderboard.html',memberslist=memberslist)

@app.route('/about')
def about():
    return render_template('about.html')

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
            game_instance = Games.query.filter_by(gamedate=j.date,sport=j.sport).first()
            if game_instance != None:
                member_gigs.append(game_instance)
            else:
                member_gigs.append(j.date)
    member_gigs = sorted(member_gigs,key=lambda game:game.gamedate)
    wins = filter(lambda x:x.result == 'W',member_gigs)
    victories = len(wins)
    return render_template('member.html',instrument=member.instrument,gamelist=member_gigs,member_name=member.name,num_victories=victories)

@app.route('/results',methods=['GET','POST'])
def results():
    listofmembers = sorted(map(lambda x:x.name,Members.query.all()))
    name = None
    form = NameForm()
    if form.validate_on_submit():
        session['search'] = form.name.data
        return redirect(url_for('results'))
    search = session.pop('search',None)
    if search:
        search_results=filter(lambda x:search.lower() in x.lower(),listofmembers)
        return render_template('results.html',searchresults=search_results,form=form,name=name)
    else:
        return redirect(url_for('index'))


def update_leaderboard():
    members = Members.query.all()
    for member in members:
        victoryCount = 0
        gameCount = 0
        for ensemble in member.ens:
            for gig in ensemble.gigs:
                game_instance = Games.query.filter_by(gamedate=gig.date,sport=gig.sport).first()
                gameCount = gameCount + 1;
                if game_instance and game_instance.result == "W":
                    victoryCount = victoryCount + 1
        member.victorycount = victoryCount
        member.gamecount = gameCount
    db.session.commit()




if __name__ == '__main__':
    manager.run()