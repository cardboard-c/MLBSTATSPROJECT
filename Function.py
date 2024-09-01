import statsapi
from datetime import datetime
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

def second(input):
    p1Count = 0
    p2Count = 0
    p3Count = 0
    p4Count = 0
    p5Count = 0
    p6Count = 0
    p7Count = 0
    p8Count = 0
    editedList = [None] * 7
    output = [editedList, "string"]
    p1 = getplayer(input[0], "season", "hitting")
    p1_stat = float(getSepcificStatNum(p1, "avg"))
    p2 = getplayer(input[1], "season", "hitting")
    p2_stat = float(getSepcificStatNum(p2, "avg"))
    p3 = getplayer(input[2], "season", "hitting")
    p3_stat = float(getSepcificStatNum(p3, "avg"))
    p4 = getplayer(input[3], "season", "hitting")
    p4_stat = float(getSepcificStatNum(p4, "avg"))
    p5 = getplayer(input[4], "season", "hitting")
    p5_stat = float(getSepcificStatNum(p5, "avg"))
    p6 = getplayer(input[5], "season", "hitting")
    p6_stat = float(getSepcificStatNum(p6, "avg"))
    p7 = getplayer(input[6], "season", "hitting")
    p7_stat = float(getSepcificStatNum(p7, "avg"))
    p8 = getplayer(input[7], "season", "hitting")
    p8_stat = float(getSepcificStatNum(p8, "avg"))
    differnce1 = (p1_stat - AVG) * 100
    differnce2 = (p2_stat - AVG) * 100
    differnce3 = (p3_stat - AVG) * 100
    differnce4 = (p4_stat - AVG) * 100
    differnce5 = (p5_stat - AVG) * 100
    differnce6 = (p6_stat - AVG) * 100
    differnce7 = (p7_stat - AVG) * 100
    differnce8 = (p8_stat - AVG) * 100
    p1_stat = float(getSepcificStatNum(p1, "baseOnBalls"))
    p2_stat = float(getSepcificStatNum(p2, "baseOnBalls"))
    p3_stat = float(getSepcificStatNum(p3, "baseOnBalls"))
    p4_stat = float(getSepcificStatNum(p4, "baseOnBalls"))
    p5_stat = float(getSepcificStatNum(p5, "baseOnBalls"))
    p6_stat = float(getSepcificStatNum(p6, "baseOnBalls"))
    p7_stat = float(getSepcificStatNum(p7, "baseOnBalls"))
    p8_stat = float(getSepcificStatNum(p8, "baseOnBalls"))
    differnce1 = differnce1 + (p1_stat - BB)
    differnce2 = differnce2 + (p2_stat - BB)
    differnce3 = differnce3 + (p3_stat - BB)
    differnce4 = differnce4 + (p4_stat - BB)
    differnce5 = differnce5 + (p5_stat - BB)
    differnce6 = differnce6 + (p6_stat - BB)
    differnce7 = differnce7 + (p7_stat - BB)
    differnce8 = differnce8 + (p8_stat - BB)
    p1Count += (differnce1)
    p2Count += (differnce2)
    p3Count += (differnce3)
    p4Count += (differnce4)
    p5Count += (differnce5)
    p6Count += (differnce6)
    p7Count += (differnce7)
    p8Count += (differnce8)
    playerDiffList = [p1Count,p2Count,p3Count,p4Count,p5Count,p6Count,p7Count,p8Count]
    biggest = max(playerDiffList)
    first = playerDiffList.index(biggest)
    firstPerson = input[first]
    print(str(p1Count) + " " + str(p2Count) + " " + str(p3Count))
    i = 0
    j = 0
    for x in range(8):
        if (input[i] == firstPerson):
            i = i + 1
        else:
            editedList[j] = input[i]
            i = i + 1
            j = j + 1
        print(i)
    output[0] = editedList
    output[1] = firstPerson

    return output


def third(input):
    p1Count = 0
    p2Count = 0
    p3Count = 0
    p4Count = 0
    p5Count = 0
    p6Count = 0
    p7Count = 0
    editedList = [None] * 6
    output = [editedList, "string"]
    p1 = getplayer(input[0], "season", "hitting")
    p1_stat = float(getSepcificStatNum(p1, "avg"))
    p2 = getplayer(input[1], "season", "hitting")
    p2_stat = float(getSepcificStatNum(p2, "avg"))
    p3 = getplayer(input[2], "season", "hitting")
    p3_stat = float(getSepcificStatNum(p3, "avg"))
    p4 = getplayer(input[3], "season", "hitting")
    p4_stat = float(getSepcificStatNum(p4, "avg"))
    p5 = getplayer(input[4], "season", "hitting")
    p5_stat = float(getSepcificStatNum(p5, "avg"))
    p6 = getplayer(input[5], "season", "hitting")
    p6_stat = float(getSepcificStatNum(p6, "avg"))
    p7 = getplayer(input[6], "season", "hitting")
    p7_stat = float(getSepcificStatNum(p7, "avg"))
    differnce1 = (p1_stat - AVG) * 100
    differnce2 = (p2_stat - AVG) * 100
    differnce3 = (p3_stat - AVG) * 100
    differnce4 = (p4_stat - AVG) * 100
    differnce5 = (p5_stat - AVG) * 100
    differnce6 = (p6_stat - AVG) * 100
    differnce7 = (p7_stat - AVG) * 100
    p1_stat = float(getSepcificStatNum(p1, "baseOnBalls"))
    p2_stat = float(getSepcificStatNum(p2, "baseOnBalls"))
    p3_stat = float(getSepcificStatNum(p3, "baseOnBalls"))
    p4_stat = float(getSepcificStatNum(p4, "baseOnBalls"))
    p5_stat = float(getSepcificStatNum(p5, "baseOnBalls"))
    p6_stat = float(getSepcificStatNum(p6, "baseOnBalls"))
    p7_stat = float(getSepcificStatNum(p7, "baseOnBalls"))
    differnce1 = differnce1 + (p1_stat - BB)
    differnce2 = differnce2 + (p2_stat - BB)
    differnce3 = differnce3 + (p3_stat - BB)
    differnce4 = differnce4 + (p4_stat - BB)
    differnce5 = differnce5 + (p5_stat - BB)
    differnce6 = differnce6 + (p6_stat - BB)
    differnce7 = differnce7 + (p7_stat - BB)
    p1_stat = float(getSepcificStatNum(p1, "homeRuns"))
    p2_stat = float(getSepcificStatNum(p2, "homeRuns"))
    p3_stat = float(getSepcificStatNum(p3, "homeRuns"))
    p4_stat = float(getSepcificStatNum(p4, "homeRuns"))
    p5_stat = float(getSepcificStatNum(p5, "homeRuns"))
    p6_stat = float(getSepcificStatNum(p6, "homeRuns"))
    p7_stat = float(getSepcificStatNum(p7, "homeRuns"))
    differnce1 = differnce1 + (p1_stat)
    differnce2 += differnce2 + (p2_stat)
    differnce3 += differnce3 + (p3_stat)
    differnce4 = differnce4 + (p4_stat)
    differnce5 += differnce5 + (p5_stat)
    differnce6 += differnce6 + (p6_stat )
    differnce7 = differnce7 + (p7_stat )
    p1_stat = float(getSepcificStatNum(p1, "rbi"))
    p2_stat = float(getSepcificStatNum(p2, "rbi"))
    p3_stat = float(getSepcificStatNum(p3, "rbi"))
    p4_stat = float(getSepcificStatNum(p4, "rbi"))
    p5_stat = float(getSepcificStatNum(p5, "rbi"))
    p6_stat = float(getSepcificStatNum(p6, "rbi"))
    p7_stat = float(getSepcificStatNum(p7, "rbi"))
    differnce1 = differnce1 + (p1_stat - RBI)
    differnce2 += differnce2 + (p2_stat - RBI)
    differnce3 += differnce3 + (p3_stat - RBI)
    differnce4 = differnce4 + (p4_stat - RBI)
    differnce5 += differnce5 + (p5_stat - RBI)
    differnce6 += differnce6 + (p6_stat - RBI)
    differnce7 = differnce7 + (p7_stat - RBI)
    p1Count += (differnce1)
    p2Count += (differnce2)
    p3Count += (differnce3)
    p4Count += (differnce4)
    p5Count += (differnce5)
    p6Count += (differnce6)
    p7Count += (differnce7)
    playerDiffList = [p1Count, p2Count, p3Count, p4Count, p5Count, p6Count, p7Count]
    biggest = max(playerDiffList)
    first = playerDiffList.index(biggest)
    firstPerson = input[first]
    print(str(p1Count) + " " + str(p2Count) + " " + str(p3Count))
    i = 0
    j = 0
    for x in range(7):
        if (input[i] == firstPerson):
            i = i + 1
        else:
            editedList[j] = input[i]
            i = i + 1
            j = j + 1
        print(i)
    output[0] = editedList
    output[1] = firstPerson
    return output

def fourth(input):
    p1Count = 0
    p2Count = 0
    p3Count = 0
    p4Count = 0
    p5Count = 0
    p6Count = 0
    editedList = [None] * 5
    output = [editedList, "string"]
    p1 = getplayer(input[0], "season", "hitting")
    p1_stat = float(getSepcificStatNum(p1, "avg"))
    p2 = getplayer(input[1], "season", "hitting")
    p2_stat = float(getSepcificStatNum(p2, "avg"))
    p3 = getplayer(input[2], "season", "hitting")
    p3_stat = float(getSepcificStatNum(p3, "avg"))
    p4 = getplayer(input[3], "season", "hitting")
    p4_stat = float(getSepcificStatNum(p4, "avg"))
    p5 = getplayer(input[4], "season", "hitting")
    p5_stat = float(getSepcificStatNum(p5, "avg"))
    p6 = getplayer(input[5], "season", "hitting")
    p6_stat = float(getSepcificStatNum(p6, "avg"))
    differnce1 = (p1_stat - AVG) * 100
    differnce2 = (p2_stat - AVG) * 100
    differnce3 = (p3_stat - AVG) * 100
    differnce4 = (p4_stat - AVG) * 100
    differnce5 = (p5_stat - AVG) * 100
    differnce6 = (p6_stat - AVG) * 100
    p1_stat = float(getSepcificStatNum(p1, "baseOnBalls"))
    p2_stat = float(getSepcificStatNum(p2, "baseOnBalls"))
    p3_stat = float(getSepcificStatNum(p3, "baseOnBalls"))
    p4_stat = float(getSepcificStatNum(p4, "baseOnBalls"))
    p5_stat = float(getSepcificStatNum(p5, "baseOnBalls"))
    differnce1 = differnce1 + (p1_stat - BB)
    differnce2 = differnce2 + (p2_stat - BB)
    differnce3 = differnce3 + (p3_stat - BB)
    differnce4 = differnce4 + (p4_stat - BB)
    differnce5 = differnce5 + (p5_stat - BB)
    differnce6 = differnce6 + (p6_stat - BB)
    p1_stat = float(getSepcificStatNum(p1, "homeRuns"))
    p2_stat = float(getSepcificStatNum(p2, "homeRuns"))
    p3_stat = float(getSepcificStatNum(p3, "homeRuns"))
    p4_stat = float(getSepcificStatNum(p4, "homeRuns"))
    p5_stat = float(getSepcificStatNum(p5, "homeRuns"))
    p6_stat = float(getSepcificStatNum(p6, "homeRuns"))
    differnce1 = differnce1 + (p1_stat )
    differnce2 += differnce2 + (p2_stat)
    differnce3 += differnce3 + (p3_stat)
    differnce4 = differnce4 + (p4_stat)
    differnce5 += differnce5 + (p5_stat)
    differnce6 += differnce6 + (p6_stat)
    p1_stat = float(getSepcificStatNum(p1, "rbi"))
    p2_stat = float(getSepcificStatNum(p2, "rbi"))
    p3_stat = float(getSepcificStatNum(p3, "rbi"))
    p4_stat = float(getSepcificStatNum(p4, "rbi"))
    p5_stat = float(getSepcificStatNum(p5, "rbi"))
    p6_stat = float(getSepcificStatNum(p6, "rbi"))
    differnce1 = differnce1 + (p1_stat - RBI)
    differnce2 += differnce2 + (p2_stat - RBI)
    differnce3 += differnce3 + (p3_stat - RBI)
    differnce4 = differnce4 + (p4_stat - RBI)
    differnce5 += differnce5 + (p5_stat - RBI)
    differnce6 += differnce6 + (p6_stat - RBI)
    p1Count += (differnce1)
    p2Count += (differnce2)
    p3Count += (differnce3)
    p4Count += (differnce4)
    p5Count += (differnce5)
    p6Count += (differnce6)
    playerDiffList = [p1Count, p2Count, p3Count, p4Count, p5Count, p6Count]
    biggest = max(playerDiffList)
    first = playerDiffList.index(biggest)
    firstPerson = input[first]
    print(str(p1Count) + " " + str(p2Count) + " " + str(p3Count))
    i = 0
    j = 0
    for x in range(6):
        if (input[i] == firstPerson):
            i = i + 1
        else:
            editedList[j] = input[i]
            i = i + 1
            j = j + 1
        print(i)
    output[0] = editedList
    output[1] = firstPerson
    return output

def fith(input):
    p1Count = 0
    p2Count = 0
    p3Count = 0
    p4Count = 0
    p5Count = 0
    editedList = [None] * 4
    output = [editedList, "string"]
    p1 = getplayer(input[0], "season", "hitting")
    p1_stat = float(getSepcificStatNum(p1, "avg"))
    p2 = getplayer(input[1], "season", "hitting")
    p2_stat = float(getSepcificStatNum(p2, "avg"))
    p3 = getplayer(input[2], "season", "hitting")
    p3_stat = float(getSepcificStatNum(p3, "avg"))
    p4 = getplayer(input[3], "season", "hitting")
    p4_stat = float(getSepcificStatNum(p4, "avg"))
    p5 = getplayer(input[4], "season", "hitting")
    p5_stat = float(getSepcificStatNum(p5, "avg"))
    differnce1 = (p1_stat - AVG) * 100
    differnce2 = (p2_stat - AVG) * 100
    differnce3 = (p3_stat - AVG) * 100
    differnce4 = (p4_stat - AVG) * 100
    differnce5 = (p5_stat - AVG) * 100
    p1_stat = float(getSepcificStatNum(p1, "baseOnBalls"))
    p2_stat = float(getSepcificStatNum(p2, "baseOnBalls"))
    p3_stat = float(getSepcificStatNum(p3, "baseOnBalls"))
    p4_stat = float(getSepcificStatNum(p4, "baseOnBalls"))
    p5_stat = float(getSepcificStatNum(p5, "baseOnBalls"))
    differnce1 = differnce1 + (p1_stat - BB)
    differnce2 = differnce2 + (p2_stat - BB)
    differnce3 = differnce3 + (p3_stat - BB)
    differnce4 = differnce4 + (p4_stat - BB)
    differnce5 = differnce5 + (p5_stat - BB)
    p1_stat = float(getSepcificStatNum(p1, "homeRuns"))
    p2_stat = float(getSepcificStatNum(p2, "homeRuns"))
    p3_stat = float(getSepcificStatNum(p3, "homeRuns"))
    p4_stat = float(getSepcificStatNum(p4, "homeRuns"))
    p5_stat = float(getSepcificStatNum(p5, "homeRuns"))
    differnce1 = differnce1 + (p1_stat )
    differnce2 += differnce2 + (p2_stat)
    differnce3 += differnce3 + (p3_stat)
    differnce4 = differnce4 + (p4_stat)
    differnce5 += differnce5 + (p5_stat)
    p1_stat = float(getSepcificStatNum(p1, "rbi"))
    p2_stat = float(getSepcificStatNum(p2, "rbi"))
    p3_stat = float(getSepcificStatNum(p3, "rbi"))
    p4_stat = float(getSepcificStatNum(p4, "rbi"))
    p5_stat = float(getSepcificStatNum(p5, "rbi"))
    differnce1 = differnce1 + (p1_stat - RBI)
    differnce2 += differnce2 + (p2_stat - RBI)
    differnce3 += differnce3 + (p3_stat - RBI)
    differnce4 = differnce4 + (p4_stat - RBI)
    differnce5 += differnce5 + (p5_stat - RBI)
    p1Count += (differnce1)
    p2Count += (differnce2)
    p3Count += (differnce3)
    p4Count += (differnce4)
    p5Count += (differnce5)
    playerDiffList = [p1Count, p2Count, p3Count, p4Count, p5Count]
    biggest = max(playerDiffList)
    first = playerDiffList.index(biggest)
    firstPerson = input[first]
    print(str(p1Count) + " " + str(p2Count) + " " + str(p3Count))
    i = 0
    j = 0
    for x in range(5):
        if (input[i] == firstPerson):
            i = i + 1
        else:
            editedList[j] = input[i]
            i = i + 1
            j = j + 1
        print(i)
    output[0] = editedList
    output[1] = firstPerson
    return output

def six(input):
    p1Count = 0
    p2Count = 0
    p3Count = 0
    p4Count = 0
    p5Count = 0
    editedList = [None] * 3
    output = [editedList, "string"]
    p1 = getplayer(input[0], "season", "hitting")
    p1_stat = float(getSepcificStatNum(p1, "avg"))
    p2 = getplayer(input[1], "season", "hitting")
    p2_stat = float(getSepcificStatNum(p2, "avg"))
    p3 = getplayer(input[2], "season", "hitting")
    p3_stat = float(getSepcificStatNum(p3, "avg"))
    p4 = getplayer(input[3], "season", "hitting")
    p4_stat = float(getSepcificStatNum(p4, "avg"))
    differnce1 = (p1_stat - AVG) * 100
    differnce2 = (p2_stat - AVG) * 100
    differnce3 = (p3_stat - AVG) * 100
    differnce4 = (p4_stat - AVG) * 100
    p1_stat = float(getSepcificStatNum(p1, "baseOnBalls"))
    p2_stat = float(getSepcificStatNum(p2, "baseOnBalls"))
    p3_stat = float(getSepcificStatNum(p3, "baseOnBalls"))
    p4_stat = float(getSepcificStatNum(p4, "baseOnBalls"))
    differnce1 = differnce1 + (p1_stat - BB)
    differnce2 = differnce2 + (p2_stat - BB)
    differnce3 = differnce3 + (p3_stat - BB)
    differnce4 = differnce4 + (p4_stat - BB)
    p1_stat = float(getSepcificStatNum(p1, "homeRuns"))
    p2_stat = float(getSepcificStatNum(p2, "homeRuns"))
    p3_stat = float(getSepcificStatNum(p3, "homeRuns"))
    p4_stat = float(getSepcificStatNum(p4, "homeRuns"))
    differnce1 = differnce1 + (p1_stat)
    differnce2 += differnce2 + (p2_stat)
    differnce3 += differnce3 + (p3_stat)
    differnce4 = differnce4 + (p4_stat)
    p1_stat = float(getSepcificStatNum(p1, "rbi"))
    p2_stat = float(getSepcificStatNum(p2, "rbi"))
    p3_stat = float(getSepcificStatNum(p3, "rbi"))
    p4_stat = float(getSepcificStatNum(p4, "rbi"))
    differnce1 = differnce1 + (p1_stat - RBI)
    differnce2 += differnce2 + (p2_stat - RBI)
    differnce3 += differnce3 + (p3_stat - RBI)
    differnce4 = differnce4 + (p4_stat - RBI)
    p1Count += (differnce1)
    p2Count += (differnce2)
    p3Count += (differnce3)
    p4Count += (differnce4)
    playerDiffList = [p1Count, p2Count, p3Count, p4Count]
    biggest = max(playerDiffList)
    first = playerDiffList.index(biggest)
    firstPerson = input[first]
    print(str(p1Count) + " " + str(p2Count) + " " + str(p3Count))
    i = 0
    j = 0
    for x in range(4):
        if (input[i] == firstPerson):
            i = i + 1
        else:
            editedList[j] = input[i]
            i = i + 1
            j = j + 1
        print(i)
    output[0] = editedList
    output[1] = firstPerson
    return output

def seven(input):
    p1Count = 0
    p2Count = 0
    p3Count = 0
    editedList = [None] * 2
    output = [editedList,"string"]
    p1 = getplayer(input[0], "season", "hitting")
    p1_stat = float(getSepcificStatNum(p1, "avg"))
    p2 = getplayer(input[1], "season", "hitting")
    p2_stat = float(getSepcificStatNum(p2, "avg"))
    p3 = getplayer(input[2], "season", "hitting")
    p3_stat = float(getSepcificStatNum(p3, "avg"))
    differnce1 = (p1_stat - AVG) * 100
    differnce2 = (p2_stat - AVG) * 100
    differnce3 = (p3_stat - AVG) * 100
    p1_stat = float(getSepcificStatNum(p1, "baseOnBalls"))
    p2_stat = float(getSepcificStatNum(p2, "baseOnBalls"))
    p3_stat = float(getSepcificStatNum(p3, "baseOnBalls"))
    differnce1 = differnce1 + (p1_stat - BB)
    differnce2 += differnce2 + (p2_stat - BB)
    differnce3 += differnce3 + (p3_stat - BB)
    p1_stat = float(getSepcificStatNum(p1, "homeRuns"))
    p2_stat = float(getSepcificStatNum(p2, "homeRuns"))
    p3_stat = float(getSepcificStatNum(p3, "homeRuns"))
    differnce1 = differnce1 + (p1_stat - HR)
    differnce2 += differnce2 + (p2_stat - HR)
    differnce3 += differnce3 + (p3_stat - HR)
    p1_stat = float(getSepcificStatNum(p1, "rbi"))
    p2_stat = float(getSepcificStatNum(p2, "rbi"))
    p3_stat = float(getSepcificStatNum(p3, "rbi"))
    differnce1 = differnce1 + (p1_stat - RBI)
    differnce2 += differnce2 + (p2_stat - RBI)
    differnce3 += differnce3 + (p3_stat - RBI)
    p1Count += (differnce1)
    p2Count += (differnce2)
    p3Count += (differnce3)
    playerDiffList = [p1Count, p2Count, p3Count]
    biggest = max(playerDiffList)
    first = playerDiffList.index(biggest)
    firstPerson = input[first]
    print(str(p1Count) + " " + str(p2Count) + " " + str(p3Count))
    i = 0
    j = 0
    for x in range(3):
        if (input[i] == firstPerson):
            i = i + 1
        else:
            editedList[j] = input[i]
            i = i + 1
            j = j + 1
        print(i)
    output[0] = editedList
    output[1] = firstPerson
    return output

def eight(input):
    p1Count = 0
    p2Count = 0
    p3Count = 0
    editedList = [None] * 1
    output = [editedList,"string"]
    p1 = getplayer(input[0], "season", "hitting")
    p1_stat = float(getSepcificStatNum(p1, "avg"))
    p2 = getplayer(input[1], "season", "hitting")
    p2_stat = float(getSepcificStatNum(p2, "avg"))
##    p3 = getplayer(input[2], "season", "hitting")
  ##  p3_stat = float(getSepcificStatNum(p3, "avg"))
    differnce1 = (p1_stat - AVG) * 100
    differnce2 = (p2_stat - AVG) * 100
    ##differnce3 = p3_stat - AVG
    p1_stat = float(getSepcificStatNum(p1, "baseOnBalls"))
    p2_stat = float(getSepcificStatNum(p2, "baseOnBalls"))
    ##p3_stat = float(getSepcificStatNum(p3, "baseOnBalls"))
    differnce1 = differnce1 + (p1_stat - BB)
    differnce2 += differnce2 + (p2_stat - BB)
   ## differnce3 += differnce3 + (p3_stat - BB)
    p1_stat = float(getSepcificStatNum(p1, "homeRuns"))
    p2_stat = float(getSepcificStatNum(p2, "homeRuns"))
   ## p3_stat = float(getSepcificStatNum(p3, "homeRuns"))
    differnce1 = differnce1 + (p1_stat - HR)
    differnce2 += differnce2 + (p2_stat - HR)
   ## differnce3 += differnce3 + (p3_stat - HR)
    p1_stat = float(getSepcificStatNum(p1, "rbi"))
    p2_stat = float(getSepcificStatNum(p2, "rbi"))
  ## p3_stat = float(getSepcificStatNum(p3, "rbi"))
    differnce1 = differnce1 + (p1_stat - RBI)
    differnce2 += differnce2 + (p2_stat - RBI)
   ## differnce3 += differnce3 + (p3_stat - RBI)
    p1Count += (differnce1)
    p2Count += (differnce2)
  ##  p3Count += (differnce3)
    playerDiffList = [p1Count, p2Count]
    biggest = max(playerDiffList)
    first = playerDiffList.index(biggest)
    firstPerson = input[first]
    ##print(str(p1Count) + " " + str(p2Count) + " " + str(p3Count))
    i = 0
    j = 0
    for x in range(2):
        if (input[i] == firstPerson):
            i = i + 1
        else:
            editedList[j] = input[i]
            i = i + 1
            j = j + 1
        print(i)
    output[0] = editedList
    output[1] = firstPerson
    return output

def nine(input):
    p1Count = 0
    p2Count = 0
    p3Count = 0
    editedList = [None]
    output = [editedList,"string"]
    p1 = getplayer(input[0], "season", "hitting")
    p1_stat = float(getSepcificStatNum(p1, "avg"))
    ##p2 = getplayer(input[1], "season", "hitting")
   ## p2_stat = float(getSepcificStatNum(p2, "avg"))
   ## p3 = getplayer(input[2], "season", "hitting")
   ## p3_stat = float(getSepcificStatNum(p3, "avg"))
    differnce1 = (p1_stat - AVG) * 100
   ## differnce2 = p2_stat - AVG
   ## differnce3 = p3_stat - AVG
    p1_stat = float(getSepcificStatNum(p1, "baseOnBalls"))
   ## p2_stat = float(getSepcificStatNum(p2, "baseOnBalls"))
   ## p3_stat = float(getSepcificStatNum(p3, "baseOnBalls"))
    differnce1 = differnce1 + (p1_stat - BB)
    ##differnce2 += differnce2 + (p2_stat - BB)
    ##differnce3 += differnce3 + (p3_stat - BB)
    p1_stat = float(getSepcificStatNum(p1, "homeRuns"))
    ##p2_stat = float(getSepcificStatNum(p2, "homeRuns"))
    ##p3_stat = float(getSepcificStatNum(p3, "homeRuns"))
    differnce1 = differnce1 + (p1_stat - HR)
    ##differnce2 += differnce2 + (p2_stat - HR)
   ## differnce3 += differnce3 + (p3_stat - HR)
    p1_stat = float(getSepcificStatNum(p1, "rbi"))
   ## p2_stat = float(getSepcificStatNum(p2, "rbi"))
   ## p3_stat = float(getSepcificStatNum(p3, "rbi"))
    differnce1 = differnce1 + (p1_stat - RBI)
    ##differnce2 += differnce2 + (p2_stat - RBI)
   ##differnce3 += differnce3 + (p3_stat - RBI)
    p1Count += (differnce1)
    ##p2Count += (differnce2)
    ##p3Count += (differnce3)
    playerDiffList = [p1Count, p2Count, p3Count]
    biggest = max(playerDiffList)
    first = playerDiffList.index(biggest)
    print(input)
    firstPerson = input[0]
   ## print(str(p1Count) + " " + str(p2Count) + " " + str(p3Count))
    i = 0
    j = 0
    for x in range(1):
        if (input[i] == firstPerson):
            i = i + 1
        else:
            editedList[j] = input[i]
            i = i + 1
            j = j + 1
        print(i)
    output[0] = editedList
    output[1] = firstPerson
    return output
def createLinup(playerList):
    lineup = ["1", "1", "1","1","1","1","1","1","1"]
    holder = compareToAverage(playerList)
    playerList = holder[0]
    lineup[0] = holder[1]
    holder = second(playerList)
    playerList = holder[0]
    lineup[1] = holder[1]
    holder = third(playerList)
    playerList = holder[0]
    lineup[2] = holder[1]
    holder = fourth(playerList)
    playerList = holder[0]
    lineup[3] = holder[1]
    holder = fith(playerList)
    playerList = holder[0]
    lineup[4] = holder[1]
    holder = six(playerList)
    playerList = holder[0]
    lineup[5] = holder[1]
    holder = seven(playerList)
    playerList = holder[0]
    lineup[6] = holder[1]
    holder = eight(playerList)
    playerList = holder[0]
    lineup[7] = holder[1]
    holder = nine(playerList)
    playerList = holder[0]
    lineup[8] = holder[1]
    print(lineup)
    return lineup