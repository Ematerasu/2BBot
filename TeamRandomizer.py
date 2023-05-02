import random
import numpy as np

def print_teams(teams):
    for i, team in enumerate(teams):
        print(f'Team {i+1}:')
        for position, player in team.items():
            print(f'\t{position} - {player}')
        print()

def generate_teams(players_list, teams_needed):

    POSITIONS = ['Top', 'Jungle', 'Mid', 'Bot', 'Support']
    teams = [{'Top': '', 'Jungle': '', 'Mid': '', 'Bot': '', 'Support': ''} for _ in range(teams_needed)]

    random.shuffle(POSITIONS)

    for i, position in enumerate(POSITIONS):
        print(f'Role: {position}')
        sorted_players_list = dict(sorted(players_list.items(), key=lambda item: len(item[1])))
        print(sorted_players_list)
        candidates = [player for player, roles in sorted_players_list.items() if position in roles]
        print(candidates)
        if len(candidates) < teams_needed:
            return f'Nie mozna wypelnic wszystkich druzyn. Za malo graczy na pozycji: {position}'
        teams_indexes = [num for num in range(teams_needed)]
        random.shuffle(teams_indexes)
        for idx, team_idx in enumerate(teams_indexes):
            teams[team_idx][position] = candidates[idx]
            del players_list[candidates[idx]]
    return teams

