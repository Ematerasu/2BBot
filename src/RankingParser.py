
class RankingParser:

    IRON_THOLD = 0
    BRONZE_THOLD = 300
    SILVER_THOLD = 400
    GOLD_THOLD = 500
    PLATINUM_THOLD = 600
    DIAMOND_THOLD = 800
    MASTER_THOLD = 900
    GRANDMASTER_THOLD = 1100
    CHALLENGER_THOLD = 1300

    RANKS = {
        'Iron': 0,
        'Bronze': 300,
        'Silver': 400,
        'Gold': 500,
        'Platinum': 600,
        'Diamond': 800,
        'Master': 900,
        'Grandmaster': 1100,
        'Challenger': 1300
    }

    @classmethod
    def assign_division(cls, elo):
        curr_rank = 'Iron'
        for rank_name, elo_needed in cls.RANKS.items():
            if elo >= elo_needed:
                curr_rank = rank_name
            else:
                break
        return curr_rank