
from RiotAPI_classes import ChampionMastery, Summoner
from RiotAPI_consts import CHAMPIONS

CHAMP_MASTERY_REQUIREMENT = [0, 0, 1800, 6000, 12600, 21600, 33000, 46800]
AFFINITY_ICONS = {
    'None': 0,

    'Assassin': 657,
    'Fighter': 658,
    'Mage': 659,
    'Marksman': 660,
    'Support': 661,
    'Tank': 662
}
SPEC_RATIO = 0.5
SPEC_CONVERSION = {
    'None': 'None',

    'Utility': 'Support',
    'Healer': 'Support',
    'Vanguard': 'Tank',
    'Warden': 'Tank',
    'Juggernaut': 'Fighter',
    'Diver': 'Fighter',
    'Burst Mage': 'Mage',
    'Battle Mage': 'Mage',
    'Artillery Mage': 'Mage',
    'Control Mage': 'Mage',
    'Assassin': 'Assassin',
    'Skirmisher': 'Assassin',
    'Marksman': 'Marksman'
}
SPEC_SYNONYMS = {
    'None': 'None',

    'Utility': 'Utility',
    'Healer': 'Healing',
    'Vanguard': 'Lockdown',
    'Warden': 'Protection',
    'Juggernaut': 'Battle Endurance',
    'Diver': 'Carry Diving',
    'Burst Mage': 'Burst',
    'Battle Mage': 'Close Quarters',
    'Artillery Mage': 'Long Range',
    'Control Mage': 'Zone Control',
    'Assassin': 'Assassination',
    'Skirmisher': 'High DPS',
    'Marksman': 'Sharpshooting'
}


class SummonerCard:

    # CONSTRUCTOR
    def __init__(self, riot_api, summoner_name):
        """
        :member vars:
            int         points          //total number of champ mastery points. (Treat as int)
            int         level           //total [DEFINED HERE] level of this summoner. level != champ mastery level.
            string      main_affinity   //the highest ranked affinity
            string      sub_affinity    //the second highest affinity within the SUB_AFFINITY_RATIO
            Dict(str, Dict(str, int))
                        affinities      //the points and level of all of the champion classes.
            Summoner    summoner        //the summoner whose stats build this card.
            string      icon_image      //a link to the icon image of this summoner
        """

        self.points = 0
        self.level = 1
        self.main_affinity = 'None'
        self.sub_affinity = 'None'
        self.affinities = {
            'None': {'points': 0, 'level': 0},

            'Utility': {'points': 0, 'level': 0},
            'Healer': {'points': 0, 'level': 0},
            'Vanguard': {'points': 0, 'level': 0},
            'Warden': {'points': 0, 'level': 0},
            'Juggernaut': {'points': 0, 'level': 0},
            'Diver': {'points': 0, 'level': 0},
            'Burst Mage': {'points': 0, 'level': 0},
            'Battle Mage': {'points': 0, 'level': 0},
            'Artillery Mage': {'points': 0, 'level': 0},
            'Control Mage': {'points': 0, 'level': 0},
            'Assassin': {'points': 0, 'level': 0},
            'Skirmisher': {'points': 0, 'level': 0},
            'Marksman': {'points': 0, 'level': 0}
        }
        self.summoner = Summoner(riot_api.get_summoner(summoner_name))
        self.icon_image = riot_api.get_summoner_icon(self.summoner.icon)

    def __str__(self):

        if self.summoner.name is '':
            return 'Summoner does not exist.'

        if self.main_affinity != 'None':
            main_details = ', pts: {pts}, lvl: {lvl}'.format(pts=self.affinities[self.main_affinity]['points'],
                                                             lvl=self.affinities[self.main_affinity]['level'])
        else:
            main_details = ''

        if self.sub_affinity != 'None':
            sub_details = ', pts: {pts}, lvl: {lvl}'.format(pts=self.affinities[self.sub_affinity]['points'],
                                                            lvl=self.affinities[self.sub_affinity]['level'])
        else:
            sub_details = ''

        return 'Summoner: ' + self.summoner.idealized + \
            '\n Affinity: ' + self.main_affinity + main_details + \
            '\n Specialzation: ' + self.sub_affinity + sub_details + \
            '\n Total points: {points}; Total level: {level}'.format(points=self.points, level=self.level)

    def build_card(self, riot_api):

        if self.summoner.name is '':
            print(self)
            return False

        all_champ_mastery = riot_api.get_all_champion_mastery(self.summoner.id)
        all_champ_data = dict(riot_api.get_all_champion_data())['data']

        # For each champ mastery out of all champ masteries for this summoner...
        for cm in all_champ_mastery:
            champ_mast = ChampionMastery(cm)

            # For each champion, find the champion mastery to match it, and retrieve its tags and classes
            for champ_name, data in all_champ_data.items():
                if data['id'] == champ_mast.id:
                    name = champ_name
                    affinity = CHAMPIONS[data['name']]['classes']
                    break
            else:
                print("Error: Cannot find champ: " + champ_mast.id)
                continue

            # if more than one tag for champ, only add half of champ points to affinity points for tags
            modifier = 1 / len(affinity)

            # Add champ points to total points, add modifier * champ points to affinity points for champ tags.
            # print error if there was an issue getting a tag.
            self.points += champ_mast.points
            for aff in affinity:
                if aff in self.affinities.keys():
                    self.affinities[aff]['points'] += int(champ_mast.points * modifier)
                else:
                    print('Error getting tag: \"{aff}\", from champion: '.format(aff=aff) + name)

        # Calculate the level for each affinity, Calculate total level, Assign main_affinity
        self.level = int(self.points / CHAMP_MASTERY_REQUIREMENT[4]) + 1
        highest = 0
        for aff_name, aff_data in self.affinities.items():
            aff_data['level'] = int(aff_data['points'] / CHAMP_MASTERY_REQUIREMENT[4]) + 1
            if aff_data['points'] > highest:
                highest = aff_data['points']
                self.main_affinity = aff_name

        # Calculate the level for each class, Assign main_class
        highest = 0
        if self.main_affinity is not "None":
            for aff_name, aff_data in self.affinities.items():
                aff_data['level'] = int(aff_data['points'] / CHAMP_MASTERY_REQUIREMENT[4]) + 1
                if aff_data['points'] > highest and aff_name is not self.main_affinity and\
                        aff_data['points'] > self.affinities[self.main_affinity]['points'] * SPEC_RATIO:
                    highest = aff_data['points']
                    self.sub_affinity = aff_name

        return True
