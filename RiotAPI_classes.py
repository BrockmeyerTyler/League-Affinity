
class Summoner:

    # CONSTRUCTOR
    def __init__(self, summ_json):
        """
        :members:
            string      name        //code-name of the summoner
            string      idealized   //display-name of the summoner
            int         id          //indexable id of the summoner
            int         icon        //id of the icon for this summoner
            int         level       //summoner level of this summoner
        """

        if list(summ_json.keys())[0] != 'status':
            self.name = list(summ_json.keys())[0]
            self.idealized = summ_json[self.name]['name']
            self.id = summ_json[self.name]['id']
            self.icon = summ_json[self.name]['profileIconId']
            self.level = summ_json[self.name]['summonerLevel']
        else:
            self.name = self.idealized = ''
            self.id = self.icon = self.level = 0


class ChampionMastery:

    # CONSTRUCTOR
    def __init__(self, champ_mastery_json):
        """
        :members:
            int         id              //id of the champion
            int         points          //total amount of champ mastery points
            int         pts_next_level  //points to get to the next level for this champ
            int         pts_last_level  //points gained since leveling up last
            int         level           //level of this champion
            bool        chest           //has gotten a chest with this champ
        """

        if list(champ_mastery_json.keys())[0] != 'status':
            self.id = champ_mastery_json['championId']
            self.points = champ_mastery_json['championPoints']
            self.pts_next_level = champ_mastery_json['championPointsUntilNextLevel']
            self.pts_last_level = champ_mastery_json['championPointsSinceLastLevel']
            self.level = champ_mastery_json['championLevel']
            self.chest = champ_mastery_json['chestGranted']
        else:
            self.id = self.points = self.pts_next_level = self.pts_next_level = self.level = 0
            self.chest = False


class Champion:

    # CONSTRUCTOR
    def __init__(self, champion_json):
        """
        :members:
            string      name        //code-name of the champ
            string      idealized   //display name for the champion
            int         id          //code-id of the champ
            string      title       //champion's title
        """

        if list(champion_json.keys())[0] != 'status':
            self.id = champion_json['id']
            self.name = champion_json['key']
            self.idealized = champion_json['name']
            self.title = champion_json['title']
        else:
            self.name = self.idealized = self.title = ''
            self.id = 0
