from abc import ABC

import statsapi
import logging
import Function
## from flask_table import Table, Col

def getdata():
 list = ["Oswaldo Cabrera", "Paul Goldschmidt", "Aaron Judge", "Giancarlo Stanton", "Cody Bellinger","Josh Donaldson", "Anthony Rizzo", "Juan Soto", "Gleyber Torres"]
 print(Function.createLineup(list))
 """
   ## logger = logging.getLogger('statsapi')
   ## logger.setLevel(logging.DEBUG)
   ## rootLogger = logging.getLogger()
   ## rootLogger.setLevel(logging.DEBUG)
   ## ch = logging.StreamHandler()
   ## formatter = logging.Formatter("%(asctime)s - %(levelname)8s - %(name)s(%(thread)s) - %(message)s")
   ## ch.setFormatter(formatter)
   ## rootLogger.addHandler(ch)
    standings = Function.getStanding("103")
    print(standings)
    ##print(statsapi.standings(leagueId=103, date='10/1/2022'))
    print ("type name of player1")
    name = 'Aaron Judge'
    ##print ("type name of player2")
    ##name2 = input()
    ##print("type career or season")
    careerOrSeason = 'season'
    ##print("type hitting or pitching")
    pos = 'hitting'

    stats = Function.getplayer(name, careerOrSeason, pos)
    final = Function.getSepcificStatNum(stats, "homeRuns")
    testing = ["Aaron Judge", "Anthony Rizzo", "Kyle Higashioka","Andrew Benintendi", "Aaron Hicks","Jose Trevino","Tim Locastro","Josh Donaldson", "Harrison Bader"]
    ##Function.createLinup(testing)


    team = Function.getTeam("nyy")
    teamId = Function.getTeamId("nyy")
    roster = Function.getRoster("142")
    roster = Function.splitRoster(roster)
    print(Function.getStanding("104"))
    print(stats)
    print(roster)
    print(team)
    print(teamId)
    print(final)

    return stats
    """
    ##for team in statsapi.lookup_team('ny'):
    ##    print(team)
    ##print("What stat")
    ##statName = input()
    #Function.compareToAverage(name)
    ##final = Function.getSepcificStat(stats, statName)
    ##print(final)
    ##print(stats)
