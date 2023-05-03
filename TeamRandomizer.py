import random
import numpy as np
from Team import Team

def print_teams(teams):
    for i, team in enumerate(teams):
        print(f'Team {i+1}:')
        for position, player in team.items():
            print(f'\t{position} - {player}')
        print()

def generate_teams(players_list, teams_needed):

    POSITIONS = ['Top', 'Jungle', 'Mid', 'Bot', 'Support']
    teams = [Team(i+1) for i in range(teams_needed)]

    random.shuffle(POSITIONS)

    for i, position in enumerate(POSITIONS):

        sorted_players_list = dict(sorted(players_list.items(), key=lambda item: len(item[1])))
        candidates = [player for player, roles in sorted_players_list.items() if position in roles]

        if len(candidates) < teams_needed:
            return f'Nie mozna wypelnic wszystkich druzyn. Za malo graczy na pozycji: {position}'

        teams_indexes = [num for num in range(teams_needed)]
        random.shuffle(teams_indexes)
        for idx, team_idx in enumerate(teams_indexes):
            teams[team_idx].add_player_at(candidates[idx], position)
            del players_list[candidates[idx]]
    return teams

