# This file is used for setting up web pages, all addresses should be put here
from flask import Flask, render_template, Blueprint, redirect, url_for, request
from flask import *
from testing import getdata
import Function

from Function import createLineup, getplayerCareer, getTeamId, getRoster, splitRoster, getNames

auth = Blueprint('auth', __name__)

pTemp = 'test'
pList = []
change = 0
teamDic = []
teamList = []
context = {}
# pList = []
pName = fullname = gamesPlayed = batAvg = hr = so = RBI = ""
global yearOrCareer


def getPlayerListForHome(stats):
    global fullname, gamesPlayed, batAvg, hr, so, RBI
    fullname = stats['first_name'] + " " + stats['last_name']
    stats = stats['stats'][0]['stats']
    gamesPlayed = stats['gamesPlayed']
    batAvg = stats['avg']
    hr = stats['homeRuns']
    so = stats['strikeOuts']
    RBI = stats['rbi']
    print(fullname, gamesPlayed)
    global pTemp
    pTemp = fullname

# use decorators to link the function to a url
@auth.route('/', methods=['GET', 'POST'])
def index():
    getdata()
    global fullname
    error = None
    if "name" in str(request.url):
        name = str(request.url).split("name=",1)[1]
        name = name.replace("+", " ")
        stats = getplayerCareer(name)
        if (stats != None):
           getPlayerListForHome(stats)
        return render_template('index.html', error=error, name=fullname, gamesPlayed=gamesPlayed, batAvg=batAvg,
                               homeruns=hr, strikeouts=so, rbi=RBI)
    if request.method == 'POST':
        if request.form.get('csStats') == 'season':
            yearOrCareer = "season"
        else:
            yearOrCareer = "career"
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'search':
            pName = request.form['playerName']
            stats = Function.getplayer(pName, yearOrCareer, "hitting")
            if(stats != None):
               getPlayerListForHome(stats)
               print(fullname)
               return render_template('index.html', error=error, name=fullname, gamesPlayed=gamesPlayed, batAvg=batAvg,
                                      homeruns=hr, strikeouts=so, rbi=RBI)
            else:
                fullname = "SEASON HAS NOT STARTED YET NO DATA"
            return render_template('index.html', error=error, name=fullname, gamesPlayed=gamesPlayed, batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI)
        else:
            return render_template('index.html', error=error)

    return render_template('index.html', error=error)  # return a string



@auth.route('/standings', methods=['GET', 'POST','EAST', 'WEST', 'CENTRAL', 'CHANGE'])
def standings():
    teamDic = []
    context = {}
    leagueList = ["East", "Central", "West"]
    nlID = [204,205,203]
    alID = [201,202,200]
    teamIDs = []
    global change
    error = None
    league = "American League East"
    num = 200
    id = '103'
    print(request.args.to_dict())

    if request.method == 'GET' and ('mode' in request.args.to_dict()):
        if request.args.to_dict()['mode'] == 'CHANGE':
            if(change == 0 ):
                change = 1
                id = '104'
            else:
                change = 0
                id = '103'


    for y in range(3):
        teamDic = []
        if(id == '103'):
            stat_dict = Function.getStanding(id)
            stats = stat_dict[alID[y]]
            league = "American League "
        else:
            stat_dict = Function.getStanding(id)
            stats = stat_dict[nlID[y]]
            league = "National League "
        for x in range(5):
            team = stats['teams'][x]
            name = str(team['name'])
            wins = team['w']
            loses = team['l']
            try:
                percent = round((team['w'] / (team['w'] + team['l'])) * 100, 2)
            except:
                percent = 0
            gamesToBeat = team['gb']
            teamList = [name,wins,loses,percent,gamesToBeat]
            teamDic.append(teamList)
        context[leagueList[y]] = teamDic
        context["league"] = "<h1>" + league + "</h1>"
    print(context)

    return render_template('standings.html', data= context)



@auth.route('/welcome')
def welcome():
    # pList = []
    return render_template('welcome.html')  # render a template


@auth.route('/login', methods=['GET', 'POST'])
def login():
    pList = []
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect('/welcome')
    return render_template('login.html', error=error)


@auth.route('/register')
def register():
    pList = []
    from app import db
    return render_template('register.html')


@auth.route('/logout')
def logout():
    pList = []
    return 'Logout'


@auth.route('/profile')
def profile():
    pList = []
    return render_template('profile.html')


@auth.route('/lineup/', defaults={'name': None}, methods=['GET', 'POST'])
@auth.route('/lineup/<name>', methods=['GET', 'POST'])
def lineup(name):
    # players = createLinup(["Aaron Judge", "Anthony Rizzo", "Kyle Higashioka","Andrew Benintendi", "Aaron Hicks","Jose Trevino","Tim Locastro","Josh Donaldson", "Harrison Bader"])
    # return render_template('lineup.html', player1 = players[0], player2 = players[1], player3 = players[2], player4 = players[3], player5 = players[4], player6 = players[5], player7 = players[6], player8 = players[7], player9 = players[8])
    error = None
    global fullname, gamesPlayed, batAvg, hr, so, RBI
    if name is not None:
        pName = name
        stats = getplayerCareer(pName)
        getPlayerListForHome(stats)
        return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed, batAvg=batAvg,
                               homeruns=hr, strikeouts=so, rbi=RBI)
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'search':
            pName = request.form['playerName']
            stats = getplayerCareer(pName)
            if stats is not None:
                getPlayerListForHome(stats)
            if len(pList) == 1:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0],
                                       )
            elif len(pList) == 2:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1])
            elif len(pList) == 3:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2])
            elif len(pList) == 4:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2],
                                       p4=pList[3])
            elif len(pList) == 5:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2],
                                       p4=pList[3], p5=pList[4])
            elif len(pList) == 6:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2],
                                       p4=pList[3], p5=pList[4], p6=pList[5])
            elif len(pList) == 7:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2],
                                       p4=pList[3], p5=pList[4],
                                       p6=pList[5], p7=pList[6])
            elif len(pList) == 8:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2],
                                       p4=pList[3], p5=pList[4],
                                       p6=pList[5], p7=pList[6], p8=pList[7])
            elif len(pList) == 9:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2],
                                       p4=pList[3], p5=pList[4],
                                       p6=pList[5], p7=pList[6], p8=pList[7], p9=pList[8])
            return render_template('lineup.html', error = error, name = fullname, gamesPlayed = gamesPlayed, batAvg = batAvg, homeruns = hr, strikeouts = so, rbi = RBI)

        elif request.form['btn_identifier'] == 'add':
            if len(pList) < 9:
                pList.append(pTemp)
            # error, too many players in lineup, max is 9
            if len(pList) == 1:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0])
            elif len(pList) == 2:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1])
            elif len(pList) == 3:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2])
            elif len(pList) == 4:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2],
                                       p4=pList[3])
            elif len(pList) == 5:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2],
                                       p4=pList[3], p5=pList[4])
            elif len(pList) == 6:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2],
                                       p4=pList[3], p5=pList[4], p6=pList[5])
            elif len(pList) == 7:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2],
                                       p4=pList[3], p5=pList[4],
                                       p6=pList[5], p7=pList[6])
            elif len(pList) == 8:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2],
                                       p4=pList[3], p5=pList[4],
                                       p6=pList[5], p7=pList[6], p8=pList[7])
            elif len(pList) == 9:
                return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed,
                                       batAvg=batAvg,
                                       homeruns=hr, strikeouts=so, rbi=RBI, p1=pList[0], p2=pList[1], p3=pList[2],
                                       p4=pList[3], p5=pList[4],
                                       p6=pList[5], p7=pList[6], p8=pList[7], p9=pList[8])
        elif request.form['btn_identifier'] == 'clear':
            pList.clear()
        elif request.form['btn_identifier'] == 'submit':
            if (1):
                return redirect('/sortedLineup')
            else:
                return render_template('lineup.html', error=error)
        else:
            return render_template('lineup.html', error=error)

    return render_template('lineup.html', error=error)


@auth.route('/sortedLineup')
def sortedLineup():
    # use sorting function to sort pList
    # Display sorted pList
    global pList
    sList = createLineup(pList)
    pList.clear()
    try:
        return render_template('sortedLineup.html', p1=sList[0], p2=sList[1], p3=sList[2], p4=sList[3], p5=sList[4],
                        p6=sList[5], p7=sList[6], p8=sList[7], p9=sList[8])
    except TypeError:
       return render_template('lineup.html',p1='Invalid lineup please input 9 players')



@auth.route('/team/<name>', methods=['GET', 'POST'])
def team(name):
    error = None
    id = getTeamId(name)
    roster = getRoster(id)
    context["playerName"] = getNames(roster)
    context["playerList"] = splitRoster(roster)
    context["teamName"] = name
    print(splitRoster(roster))
    return render_template('team.html', data=context)
