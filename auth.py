# This file is used for setting up web pages, all addresses should be put here
from flask import Flask, render_template, Blueprint, redirect, url_for, request
from testing import getdata
import Function

from Function import createLinup, getplayerCareer, getTeamId, getRoster, splitRoster, getNames

auth = Blueprint('auth', __name__)

pTemp = 'test'
pList = []
change = 0


# use decorators to link the function to a url
@auth.route('/', methods=['GET', 'POST'])
def index():
    getdata()

    error = None
    # pList = []
    pName = ''
    fullname = ''
    gamesPlayed = ''
    batAvg = ''
    hr = ''
    so = ''
    RBI = ''

    if request.method == 'POST':
        if request.form['btn_identifier'] == 'search':
            pName = request.form['playerName']

            stats = getplayerCareer(pName)
            if(stats != None):
                fullname = stats['first_name'] + " " + stats['last_name']
                stats = stats['stats'][0]['stats']
                gamesPlayed = stats['gamesPlayed']
                batAvg = stats['avg']
                hr = stats['homeRuns']
                so = stats['strikeOuts']
                RBI = stats['rbi']
                global pTemp
                pTemp = fullname
            return render_template('index.html', error=error, name=fullname, gamesPlayed=gamesPlayed, batAvg=batAvg,
                                   homeruns=hr, strikeouts=so, rbi=RBI)
        else:
            return render_template('index.html', error=error)

    return render_template('index.html', error=error)  # return a string



@auth.route('/standings', methods=['GET', 'POST','EAST', 'WEST', 'CENTRAL', 'CHANGE'])
def standings():
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
            else:
                change = 0
        if request.args.to_dict()['mode'] == 'EAST':
            if(change == 0):
                num = 201
                id = '103'
                league = "American League East"
            else:
                num = 204
                id = '104'
                league = "National League East"
        if request.args.to_dict()['mode'] == 'CENTRAL':
            if(change == 0):
                num = 202
                id = '103'
                league = "American League Central"
            else:
                num = 205
                id = '104'
                league = "National League Central"
        if request.args.to_dict()['mode'] == 'WEST':
            if(change == 0):
                num = 200
                id = '103'
                league = "American League West"
            else:
                num = 203
                id = '104'
                league = "National League West"
    stat_dict = Function.getStanding(id)
    stats = stat_dict[num]
    #print(stats)
    team1 = stats['teams'][0]
    name1 = team1['name']
    w1 = team1['w']
    l1 = team1['l']
    p1 = round((team1['w'] / (team1['w'] + team1['l'])) * 100, 2)
    gb1 = team1['gb']
    team2 = stats['teams'][1]
    name2 = team2['name']
    w2 = team2['w']
    l2 = team2['l']
    p2 = round((team2['w'] / (team2['w'] + team2['l'])) * 100, 2)
    gb2 = team2['gb']
    team3 = stats['teams'][2]
    name3 = team3['name']
    w3 = team3['w']
    l3 = team3['l']
    p3 = round((team3['w'] / (team3['w'] + team3['l'])) * 100, 2)
    gb3 = team3['gb']
    team4 = stats['teams'][3]
    name4 = team4['name']
    w4 = team4['w']
    l4 = team4['l']
    p4 = round((team4['w'] / (team4['w'] + team4['l'])) * 100, 2)
    gb4 = team4['gb']
    team5 = stats['teams'][4]
    name5 = team5['name']
    w5 = team5['w']
    l5 = team5['l']
    p5 = round((team5['w'] / (team5['w'] + team5['l'])) * 100, 2)
    gb5 = team5['gb']
    return render_template('standings.html', data= "<h1>" + league + "</h1>", error = error, name1 = name1, w1 = w1, l1 = l1, p1 = p1, gb1 = gb1, name2 = name2, w2 = w2, l2 = l2, p2 = p2, gb2 = gb2, name3 = name3, w3 = w3, l3 = l3, p3 = p3, gb3 = gb3, name4 = name4, w4 = w4, l4 = l4, p4 = p4, gb4 = gb4,name5 = name5, w5 = w5, l5 = l5, p5 = p5, gb5 = gb5)



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
    global pList
    pName = ''
    fullname = ''
    gamesPlayed = ''
    batAvg = ''
    hr = ''
    so = ''
    RBI = ''
    global pTemp

    if name is not None:
        pName = name
        stats = getplayerCareer(pName)
        fullname = stats['first_name'] + " " + stats['last_name']
        stats = stats['stats'][0]['stats']
        gamesPlayed = stats['gamesPlayed']
        batAvg = stats['avg']
        hr = stats['homeRuns']
        so = stats['strikeOuts']
        RBI = stats['rbi']
        pTemp = fullname
        return render_template('lineup.html', error=error, name=fullname, gamesPlayed=gamesPlayed, batAvg=batAvg,
                               homeruns=hr, strikeouts=so, rbi=RBI)
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'search':
            pName = request.form['playerName']
            stats = getplayerCareer(pName)

            if stats is not None:
                fullname = stats['first_name'] + " " + stats['last_name']
                stats = stats['stats'][0]['stats']
                gamesPlayed = stats['gamesPlayed']
                batAvg = stats['avg']
                hr = stats['homeRuns']
                so = stats['strikeOuts']
                RBI = stats['rbi']
                pTemp = fullname
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
            # pName = request.form['playerName']
            # stats = getplayerCareer(pName)
            # fullname = stats['first_name'] + " " + stats['last_name']
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
        elif request.form['btn_identifier'] == 'submit':
            if (1):
                return redirect('/sortedLineup')
            else:
                # return error statement
                return render_template('lineup.html', error=error)
        else:
            return render_template('lineup.html', error=error)

    return render_template('lineup.html', error=error)


@auth.route('/sortedLineup')
def sortedLineup():
    # use sorting function to sort pList
    # Display sorted pList
    global pList
    sList = createLinup(pList)
    return render_template('sortedLineup.html', p1=sList[0], p2=sList[1], p3=sList[2], p4=sList[3], p5=sList[4],
                           p6=sList[5], p7=sList[6], p8=sList[7], p9=sList[8])


@auth.route('/team/<name>')
def team(name):
    id = getTeamId(name)
    roster = getRoster(id)
    roster2 = getRoster(id)
    tl = splitRoster(roster)
    names = getNames(roster2)
    return render_template('team.html', tName=name, nb1=tl[0][0], nm1=names[0], p1=tl[0][2],
                           nb2=tl[1][0], nm2=names[1], p2=tl[1][2],
                           nb3=tl[2][0], nm3=names[2], p3=tl[2][2],
                           nb4=tl[3][0], nm4=names[3], p4=tl[3][2],
                           nb5=tl[4][0], nm5=names[4], p5=tl[4][2],
                           nb6=tl[5][0], nm6=names[5], p6=tl[5][2],
                           nb7=tl[6][0], nm7=names[6], p7=tl[6][2],
                           nb8=tl[7][0], nm8=names[7], p8=tl[7][2],
                           nb9=tl[8][0], nm9=names[8], p9=tl[8][2])
