import statsapi
import logging
import Function
logger = logging.getLogger('statsapi')
logger.setLevel(logging.DEBUG)
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)8s - %(name)s(%(thread)s) - %(message)s")
ch.setFormatter(formatter)
rootLogger.addHandler(ch)

print ("type name of player")
name = input()
print("type career or season")
careerOrSeason =input()
print("type hitting or pitching")
pos = input()

stats = Functions.getplayer(name, careerOrSeason, pos)
for team in statsapi.lookup_team('ny'):
    print(team)
print(statsapi.standings(date='07/04/2021'))
print("What statA")
statName = input()
final = Functions.getSepcificStat(stats, statName)
print(final)



#print( statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2022,'gameType':'W'})['people'] if x['fullName']=='Chad Green'), 'pitching', 'career') )

#print( statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2022,'gameType':'W'})['people'] if x['fullName']=='Nestor Cortes'), 'pitching', 'season') )

#print( statsapi.league_leaders('earnedRunAverage',statGroup='pitching',limit=5,season=2022) )
