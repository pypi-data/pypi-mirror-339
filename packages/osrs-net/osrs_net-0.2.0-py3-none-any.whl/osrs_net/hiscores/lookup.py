import requests
from osrs_net.hiscores.stat import Stat
from osrs_net.hiscores.skill import Skill, skills_list
from osrs_net.hiscores.account import Account


def lookup_player(player_name):
    player_stats = dict()
    url = f'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={player_name}'
    text = requests.get(url).text
    if text[0] == '<':
        return None
    text = text.split('\n')

    for i, skill in enumerate(skills_list):
        skill_enum = Skill.from_string(skill)
        curr_text = text[i].split(',')
        rank, level, exp = curr_text
        curr_skill = Stat(skill_enum, int(level), int(exp), int(rank))
        player_stats[skill] = curr_skill

    return Account(player_name, player_stats)
