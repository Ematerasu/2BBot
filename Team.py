import json

class Team:

    POSITIONS = ['Top', 'Jungle', 'Mid', 'Bot', 'Support']

    def __init__(self, team_id):
        self.team_id = team_id
        self.top = None
        self.jungle = None
        self.mid = None
        self.bot = None
        self.support = None
    
    def add_player_at(self, player, position):
        if position not in self.POSITIONS:
            raise ValueError('Position value invalid')
        if position == 'Top':
            self.top = player
        elif position == 'Jungle':
            self.jungle = player
        elif position == 'Mid':
            self.mid = player
        elif position == 'Bot':
            self.bot = player
        elif position == 'Support':
            self.support = player
        return
    
    def print_teams(self) -> str:
        string_builder = f'Team {self.team_id}:\n'
        string_builder += f'.\t Top: {self.top}\n'
        string_builder += f'.\t Jungle: {self.jungle}\n'
        string_builder += f'.\t Mid: {self.mid}\n'
        string_builder += f'.\t Bot: {self.bot}\n'
        string_builder += f'.\t Support: {self.support}'
        return string_builder
    
    def get_players(self) -> list:
        return [self.top, self.jungle, self.mid, self.bot, self.support]

    def get_teams_elo(self, ranking):
        if not all(self.get_players()):
            raise AttributeError("Nie ma wypelnionych wszystkich pozycji")
        elo = 0
        for player in self.get_players():
            if player in ranking:
                elo += ranking[player]["elo"]
            else:
                elo += 500
        return int(round(elo/5))
