import requests
import os
from dotenv import load_dotenv

load_dotenv(".secrets")
apiKey = os.getenv("key")
region = os.getenv("region")

#region Function to retrieve player points
def getPlayerPoints(playerName):
    summonerUrl = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{playerName}?api_key={apiKey}"
    response = requests.get(summonerUrl).json()

    if "status" in response:
        print(f"Error retrieving data for {playerName}.")
        return None

    summonerId = response['id']

    leagueUrl = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerId}?api_key={apiKey}"
    leagueResponse = requests.get(leagueUrl).json()

    if not leagueResponse:
        print(f"{playerName} has no league data.")
        return 0

    points = 0
    for entry in leagueResponse:
        if entry['queueType'] == 'RANKED_SOLO_5x5':
            points = entry['leaguePoints']
            break
    
    return points
#endregion

#region Collect player names from input
playerNames = input("Enter player names separated by a comma (,): ").split(',')

presentPlayers = {}
for name in playerNames:
    cleanName = name.strip()
    points = getPlayerPoints(cleanName)
    if points is not None:
        presentPlayers[cleanName] = points
    else:
        print(f"{cleanName} was not found.")
#endregion

#region Calculate total points
totalPoints = sum(presentPlayers.values())
print(f"Total points: {totalPoints}")

if len(presentPlayers) < 2:
    print("At least 2 players are required to play.")
elif len(presentPlayers) > 10:
    print("A maximum of 10 players can play.")
else:
    teamBlue = []
    teamRed = []
    teamBluePoints = 0
    teamRedPoints = 0
    averagePoints = totalPoints / 2

    # Balance
    for player, points in sorted(presentPlayers.items(), key=lambda item: item[1], reverse=True):
        if teamBluePoints <= teamRedPoints:
            teamBlue.append(player)
            teamBluePoints += points
        else:
            teamRed.append(player)
            teamRedPoints += points

    # Teasm
    print(f"Team Blue: {', '.join(teamBlue)} - Points: {teamBluePoints}")
    print(f"Team Red: {', '.join(teamRed)} - Points: {teamRedPoints}")
#endregion