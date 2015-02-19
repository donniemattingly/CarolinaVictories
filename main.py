__author__ = 'dmatt'
import os.path as op
import json
from operator import attrgetter
from flask import Flask,session, render_template,abort,redirect,url_for,flash,request, jsonify
from flask.ext import admin,login
from flask.ext.admin import expose,helpers
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,form, fields, validators
from wtforms.validators import Required,Email,Length
from werkzeug.security import generate_password_hash,check_password_hash
import mimetypes
from databases import Ensembles,Gig,Games,Members,db,User




app = Flask(__name__)


manager = Manager(app)
bootstrap = Bootstrap(app)
app.config.from_envvar('CV_SETTINGS')
db.app = app
db.init_app(app)
mimetypes.add_type('image/svg+xml', '.svg')
app.debug = True


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

class MyModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated()

class MyFileAdmin(FileAdmin):
    def is_accessible(self):
        return login.current_user.is_authenticated()

class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()


    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))



def printGameAttributes(gamelist):
    for game in gamelist:
        if game and game.sport == 'mens-basketball':
            print 'game on date '+str(game.gamedate)+'vs'+game.opponent+' was a '+game.result+' with a score of '+game.score
class NameForm(Form):
    name = StringField(validators=[Required()])
    submit = SubmitField('Find Out')

class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not user.verify_password(self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        x =  db.session.query(User).filter_by(username=self.login.data).first()
        return x


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

@app.route('/runparser')
def runparser():
    import dparser
    return "Complete"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/members/<username>')
def member(username):
    username = username.replace('_',' ')
    member = Members.query.filter_by(name=username).first()
    if member == None:
        abort(404)
    member_gigs = []
    for i in member.ens:
        for j in i.gigs:
            game_instance = Games.query.filter_by(gamedate=j.date,sport=j.sport).first()
            if game_instance != None:
                member_gigs.append(game_instance)
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
@app.route('/_sortmemberslist/<column>')
def sortMembersList(column):
    memberslist = Members.query.all()
    sortedlist = sorted(memberslist,key=attrgetter(column))
    jstring =  json.dumps(map(lambda x:{'name':x.name,'instrument':x.instrument,'year':x.year,'victorycount':x.victorycount}, sortedlist))
    return jstring


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


init_login()
admin = admin.Admin(app, 'CV Admin', index_view=MyAdminIndexView(), base_template='my_master.html')
admin.add_view(MyModelView(Members,db.session))
admin.add_view(MyModelView(Ensembles,db.session))
admin.add_view(MyModelView(Gig,db.session))
admin.add_view(MyModelView(Games,db.session))

path = op.join(op.dirname(__file__), 'static')
admin.add_view(MyFileAdmin(path, '/static', name='Static'))



if __name__ == '__main__':
    manager.run()
