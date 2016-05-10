

import os
from RiotAPI import RiotAPI
from SummonerCard import *
from flask import Flask, render_template, request
from Skills import *


'''
    League Affinity
        https://league-affinity.herokuapp.com/
'''

API_KEY = "your-api-key-here"

app = Flask(__name__)
api = RiotAPI(API_KEY)


@app.route("/")
def index():
    return render_template('index.html', info_head="Search for a summoner to see their playing card!")


@app.route("/search", methods=['GET'])
def search():
    api.region = request.args['region']
    s_card = SummonerCard(api, request.args['summoner'])

    if s_card.build_card(api):
        info = {
            'info_head': 'About {summoner}:'.format(summoner=s_card.summoner.idealized),
            'info': ""
        }

        if s_card.main_affinity != "None":
            maininfo = "They have {mainpts}k points with {main} champions.".format(
                mainpts=int(s_card.affinities[s_card.main_affinity]['points'] / 1000), main=s_card.main_affinity)
        else:
            maininfo = ""
        if s_card.sub_affinity != "None":
            subinfo = "They have {subpts}k points with {sub} champions."\
                .format(subpts=int(s_card.affinities[s_card.sub_affinity]['points'] / 1000), sub=s_card.sub_affinity)
        else:
            subinfo = ""
        info['info'] = "This summoner has a main affinity of {main}. Their sub-affinity is {sub}. {maininfo} {subinfo}"\
                       " They have {pts}k total points and a total level of {lvl}"\
            .format(main=s_card.main_affinity, sub=s_card.sub_affinity, maininfo=maininfo, subinfo=subinfo,
                    pts=int(s_card.points / 1000), lvl=s_card.level)

        card_fill = {
            'name': s_card.summoner.idealized,
            'class_lvl': s_card.affinities[s_card.main_affinity]['level'],
            'class': s_card.main_affinity,
            'class_icon': api.get_summoner_icon(AFFINITY_ICONS[SPEC_CONVERSION[s_card.main_affinity]]),
            'icon': s_card.icon_image
        }
        if s_card.sub_affinity is "None":
            card_fill['spec'] = SPEC_SYNONYMS[s_card.main_affinity]
        else:
            card_fill['spec'] = SPEC_SYNONYMS[s_card.sub_affinity]

        # sc: skill cost
        # sci: skill cost image
        # sn: skill name
        # sd: skill description
        if s_card.sub_affinity is "None":
            sub = s_card.main_affinity
        else:
            sub = s_card.sub_affinity
        card_skills = {
            'sc1': SKILL_LIST[SKILLS[s_card.main_affinity][sub][0]]['cost'],
            'sc2': SKILL_LIST[SKILLS[s_card.main_affinity][sub][1]]['cost'],
            'sc3': SKILL_LIST[SKILLS[s_card.main_affinity][sub][2]]['cost'],
            'sci1': api.get_item_img(3070),
            'sci2': api.get_item_img(3070),
            'sci3': api.get_item_img(3070),
            'sn1': SKILLS[s_card.main_affinity][sub][0],
            'sn2': SKILLS[s_card.main_affinity][sub][1],
            'sn3': SKILLS[s_card.main_affinity][sub][2],
            'sd1': SKILL_LIST[SKILLS[s_card.main_affinity][sub][0]]['desc'],
            'sd2': SKILL_LIST[SKILLS[s_card.main_affinity][sub][1]]['desc'],
            'sd3': SKILL_LIST[SKILLS[s_card.main_affinity][sub][2]]['desc'],
        }

        return render_template('search.html', **card_fill, **card_skills, **info)

    else:
        return render_template('notfound.html', info_head=
                               '"{summoner}" does not exist in the {region} server. Please check the name and region.'
                               .format(summoner=request.args['summoner'], region=request.args['region']))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
