class Account:
    def __init__(self, username, stats):
        self.name = username
        self.stats = stats

    def get_stat(self, stat_name):
        try:
            return self.stats[stat_name.lower()]
        except KeyError:
            return None

    def get_total(self):
        try:
            return self.stats['total']
        except KeyError:
            return None

    def get_level(self, stat_name):
        try:
            return self.stats[stat_name.lower()].level
        except KeyError:
            return None

    def get_xp(self, stat_name):
        try:
            return self.stats[stat_name.lower()].experience
        except KeyError:
            return None

    def get_rank(self, stat_name):
        try:
            return self.stats[stat_name.lower()].rank
        except KeyError:
            return None
