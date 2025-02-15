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


list = ["Oswaldo Cabrera", "Paul Goldschmidt", "Aaron Judge", "Giancarlo Stanton","Cody Bellinger", "Josh Donaldson", "Anthony Rizzo", "Juan Soto", "Gleyber Torres"]


print(Function.createPlayerList(list))



#print( statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2022,'gameType':'W'})['people'] if x['fullName']=='Chad Green'), 'pitching', 'career') )

#print( statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2022,'gameType':'W'})['people'] if x['fullName']=='Nestor Cortes'), 'pitching', 'season') )

#print( statsapi.league_leaders('earnedRunAverage',statGroup='pitching',limit=5,season=2022) )
