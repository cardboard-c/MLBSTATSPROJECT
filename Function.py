import statsapi
from datetime import datetime
from operator import itemgetter
import logging
##League year by year averages for 30 plate apperances(also the average)

##first spot should ingore power hitters if they average more than .09 hr per game (more than 15 a season)
AVG = .243
SB = 0.51
HR = 6.601
RBI = 4.09
BB = 3.09


def getplayer(name, yearlyOrCareer, pos):
    #stat = statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players', {'season': 2022, 'gameType': 'W'})['people'] if x['fullName'] == name), pos, yearlyOrCareer)
    stat = statsapi.player_stat_data(next(x['id'] for x in statsapi.get('sports_players', {'season': 2022, 'gameType': 'W'})['people'] if x['fullName'] == name), pos, yearlyOrCareer, sportId=1)
    #stat = stat.split()[7:]
    return stat

def getTeamId(teamName):

    team = statsapi.lookup_team(teamName)
    teamID = team[0]['id']
    return teamID

def getRoster(teamId):
    roster = statsapi.roster(teamId, rosterType=None, season=datetime.now().year, date=None)
    return roster

def splitRoster(roster):
    #grab the string of every player on the team split by line
    playerTotal = list(roster.split("\n"))
    playerNotParsed = []
    #for that string stated above split by spaces
    for item in playerTotal:
        s = list(item.split(" "))
        playerNotParsed.append(s)
    final = []
    #since not every posistion has 2 letters there are some empty elements of the list created for palyers this for loop cleans up any empty elements
    for player in playerNotParsed:
        tmp = []
        for elementOfPlayer in player:
            if(elementOfPlayer!= ''):
                tmp.append(elementOfPlayer)
        if(tmp):
            final.append(tmp)
    return final


def getNames(roster):
    l = splitRoster(roster)
    x = []
    for item in l:
        del item[0:4]
        str = " "
        temp = str.join(item)
        x.append(temp)

    return x


def getTeam(teamName):
    team = statsapi.lookup_team(teamName)
    return team

def getplayerCareer(name):
    #stat = statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players', {'season': 2022, 'gameType': 'W'})['people'] if x['fullName'] == name), pos, yearlyOrCareer)
    try:
        stat = statsapi.player_stat_data(next(x['id'] for x in statsapi.get('sports_players', {'season': 2022, 'gameType': 'W'})['people'] if x['fullName'] == name), "hitting", "career", sportId=1)
        return stat
    except:
        return None;


def getSepcificStat(stats, statName):
    index = 0
    stats_dict = {}

    while index < len(stats):
        stats_dict[stats[index]] = stats[index + 1]
        index += 2
    print(stats_dict.keys())
    final = statName + " :" + stats_dict[statName + ':']
    return final

def getSepcificStatNum(stats, statName):
    stats
    fullname = stats['first_name'] + " " + stats['last_name']
    stats = stats['stats'][0]['stats']
    final = stats[statName]
    return final

def getStanding(leagueId):
    standings = statsapi.standings_data(leagueId, division="all", include_wildcard=True, season=None, standingsTypes=None, date=None)
   ## standings = statsapi.standings(leagueId=103, date='10/1/2022')
    return standings

def compare(name1, name2, statName):
    p1 = getplayer(name1,"career", "hitting")
    p2 = getplayer(name2,"career", "hitting")
    p1_stat = getSepcificStatNum(p1,statName)
    p2_stat = getSepcificStatNum(p2,statName)
    differnce = abs(int(p1_stat) - int(p2_stat))
    if(p1_stat > p2_stat):
        print(name1 + " has " + str(differnce) + " more " + statName +" than " + name2)
    elif(p1_stat < p2_stat):
        print(name2 + " has " + str(differnce) + " more " + statName + " than " + name1)


#takes list of players including all stats called player stats and a list of player names
#then it sorts by batting average of the players from highest to lowest
def sortByAVG(playerList, names):
    AVGList = {}
    sortedDic = {}
    for i in range(9):
        AVGList[names[i]]= getSepcificStatNum(playerList[i],"avg")
    sortedList = sorted(AVGList, key=AVGList.get, reverse=True)

    for i in sortedList:
        sortedDic[i] = AVGList[i]
    print(sortedDic)
    return sortedList

#createPlayerList creates a list of 9 players including all their career hitting stats
def createPlayerList(names):
    playerList = []
    for i in range(9):
        playerList.append(getplayer(names[i], "career", "hitting"))
    return playerList

#TODO Make this better more ideal lineup and not just sort by avg
def createLineup(names):
    playerList = createPlayerList(names)
    lineUp = sortByAVG(playerList, names)
    return lineUp













""" THIS IS REALLY DOG DO NOT USE USE FUNCTIONS ABOVE THANK YOU 

def compareToAverage(testing):
    BasePlyer = [AVG, SB, HR, RBI, BB]
    p1Count = p2Count = p3Count = p4Count = p5Count = p6Count = p7Count = p8Count = p9Count = 0
    differnce1 = differnce2 = differnce3 = differnce4 = differnce5 = differnce6 = differnce7 = differnce8 = differnce9 = 0
    statIndex =["avg","baseOnBalls","stolenBases","caughtStealing"]
    diffList = [differnce1,differnce2,differnce3,differnce4,differnce5,differnce6,differnce7,differnce8,differnce9]
    countList =[p1Count, p2Count,p3Count,p4Count,p5Count,p6Count,p7Count,p8Count,p9Count]
    editedList = [None] * 8
    output = [editedList,"string"]
    p1 = getplayer(testing[0], "season", "hitting")
    p2 = getplayer(testing[1], "season", "hitting")
    p3 = getplayer(testing[2], "season", "hitting")
    p4 = getplayer(testing[3], "season", "hitting")
    p5 = getplayer(testing[4], "season", "hitting")
    p6 = getplayer(testing[5], "season", "hitting")
    p7 = getplayer(testing[6], "season", "hitting")
    p8 = getplayer(testing[7], "season", "hitting")
    p9 = getplayer(testing[8], "season", "hitting")
    p1_stat = p2_stat = p3_stat = p4_stat = p5_stat = p6_stat = p7_stat = p8_stat = p9_stat = 0.0
    playerList = [p1,p2,p3,p4,p5,p6,p7,p8,p9]
    playerStatList = [p1_stat, p2_stat, p3_stat, p4_stat, p5_stat, p6_stat, p7_stat, p8_stat, p9_stat]
    holder = 0;
    for x in statIndex:
        index = 0
        for y in playerList:
            playerStatList[index] = float(getSepcificStatNum(playerList[index], statIndex[holder]))
            if(statIndex[holder] != "caughtStealing"):
                diffList[index] = diffList[index] + (playerStatList[index] - BasePlyer[holder])
            else:
                diffList[index] = diffList[index] - playerStatList[index]
            print(diffList)
            print("index" + str(index))
            index = index + 1
        countList += diffList
        holder = holder + 1
    countList = diffList
    biggest = max(countList)
    first = countList.index(biggest)
    firstPerson = testing[first]
    print(countList)
    i = 0
    j = 0
    for x in range(9):
        if(testing[i] == firstPerson):
            i = i + 1
        else:
            editedList[j] = testing[i]
            i = i + 1
            j = j + 1
        print(i)
    output[0] = editedList
    print(editedList)
    output[1] = firstPerson
    return output
    """
