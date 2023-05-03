import json
from Team import Team

class Referee:

    def __init__(self):
        self.current_teams = dict()

    def register_teams(self, team: Team):

        if team.team_id in self.current_teams:
            return
        self.current_teams[team.team_id] = team
        return
    
    def update_leaderboard(self, winnerTeamID: int, loserTeamID: int):
        if winnerTeamID not in self.current_teams:
            raise ValueError("Winner team is not registered")
        if loserTeamID not in self.current_teams:
            raise ValueError("Loser team is not registered")
        
        with open('ranking.json', 'r') as f:
            ranking = json.load(f)

        winnerTeam = self.current_teams[winnerTeamID]

        for player in winnerTeam.get_players():
            if player in ranking:
                ranking[player]["wins"] += 1
            else:
                ranking[player] = {"wins": 1, "losses": 0}

        loserTeam = self.current_teams[loserTeamID]
        
        for player in loserTeam.get_players():
            if player in ranking:
                ranking[player]["losses"] += 1
            else:
                ranking[player] = {"wins": 0, "losses": 1}

        with open('ranking.json', 'w') as f:
            json.dump(ranking, f)
        
        del self.current_teams[winnerTeamID]
        del self.current_teams[loserTeamID]
        
    def clear_register(self):
        self.current_teams = dict()
