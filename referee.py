import json
import math
from Team import Team

class Referee:

    K_FACTOR = 30
    SCALE = 400
    def __init__(self):
        self.current_teams = dict()

    def register_teams(self, team: Team):
        if team.team_id in self.current_teams:
            return
        self.current_teams[team.team_id] = team
        return
    
    def calculate_elo(self, old_elo, opponent_elo, result):
        expected_score = 1 / (1 + math.pow(10, (opponent_elo - old_elo) / self.SCALE))
        new_elo = old_elo + self.K_FACTOR * (result - expected_score)
        return int(round(new_elo))
    
    def update_leaderboard(self, winnerTeamId: int, loserTeamId: int):
        if winnerTeamId not in self.current_teams:
            raise ValueError("Winner team is not registered")
        if loserTeamId not in self.current_teams:
            raise ValueError("Loser team is not registered")
        
        with open('ranking.json', 'r') as f:
            ranking = json.load(f)

        winnerTeam = self.current_teams[winnerTeamId]
        winnerTeamElo = winnerTeam.get_teams_elo(ranking)

        loserTeam = self.current_teams[loserTeamId]
        loserTeamElo = loserTeam.get_teams_elo(ranking)

        for player in winnerTeam.get_players():
            if player in ranking:
                ranking[player]["elo"] = self.calculate_elo(ranking[player]["elo"], loserTeamElo, 1)
                ranking[player]["wins"] += 1
            else:
                ranking[player] = {
                    "elo": self.calculate_elo(500, loserTeamElo, 1),
                    "wins": 1,
                    "losses": 0
                }

        for player in loserTeam.get_players():
            if player in ranking:
                ranking[player]["elo"] = self.calculate_elo(ranking[player]["elo"], winnerTeamElo, 0)
                ranking[player]["losses"] += 1
            else:
                ranking[player] = {
                    "elo": self.calculate_elo(500, winnerTeamElo, 0),
                    "wins": 0,
                    "losses": 1
                }

        with open('ranking.json', 'w') as f:
            json.dump(ranking, f, sort_keys=True, indent=4)
        
        del self.current_teams[winnerTeamId]
        del self.current_teams[loserTeamId]
        
    def clear_register(self):
        self.current_teams = dict()
