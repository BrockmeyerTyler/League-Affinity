Disclaimer: This project is very old in terms of my coding ability. Very, very old.

# League-Affinity
My submission to Riot Games' API Contest for April 2016. It uses Champion Mastery to produce a playing card based around that summoner's particular play style and interests. Built with Python 3 using the requests and Flask modules, and hosted by Heroku.  
ACTIVE SITE: https://league-affinity.herokuapp.com/  
Because of the way that Heroku works, be aware that the site may take several seconds to load, and when it does come up, the initial load may be void of formatting. If this is the case, a simple refresh will fix it.

# BRIEF SUMMARY
Hello. My name is Tyler Brockmeyer, and this is my web app, League Affinity. As stated, it will create a playing card using the searched summoner's champion mastery info. The card provides the following:  
1. The summoner's name.  
2. The summoner's affinity. (Assassin / Mage / etc.)  
3. The summoner's level in their main affinity. (Not the same as their champion mastery score for that affinity!)  
4. The summoner's icon as an image to represent them.  
5. The summoner's sub-affinity. (Similar to affinity, but it will be the second-best, if within half of the main's total points)  
6. Three skills to go along with the summoner's main and sub affinities.  
7. Some other minor additions.  
8. To the right of the card, other details about the summoner's affinities.  
All will be explained in detail further down.


# TO LAUNCH LOCALLY
This is NOT required, as there is a live site up right now.  
That being said, it is very simple. All you have to do is (after downloading all of the files obviously) set the API_KEY constant in main.py to your own API key and run main.py using the Python 3 console. Then simply navigate to localhost:5000 in your web browser to see the site. And you're done! To turn off the server, press CTRL+C in your Python 3 console.


# THE DETAILS
League Affinity is not a very complicated app, but I would like to believe it is interesting and fun. To explain what happens, there is a bit that should be known from behind the scenes. One big one is what the affinities are, and why some of them may not seem so familliar to us. Well, not too long ago, Riot released a post detailing the way that they are planning to reclassify champions in League of Legends. No longer would they simply be mage, assassin, tank, etc, but now it would be a bit more in-depth. Some good examples inlcude burst mages, control mages, enchanters, vanguards, wardens and divers. I used this currently unimplemented idea and applied it to every champion (it is by my own personal opinion that I classified each champion, and some were very difficult to decide on, so I apologize if you do not agree). I changed the system around a bit in manners that I saw fit and came up with what is represented here, and that can be seen in RiotAPI_consts.py. The new classifications have been defined in my app as 'affinities.' 

When a summoner is searched for, they are given a main and sub affinity. The main affinity is simply the summoner's highest scoring affinity. For example: Annie Bot, a famous 'only Annie' player, easily gets the main affinity of 'Burst Mage' because of his absurd amount of games played on Annie. 

Following this, the sub-affinity is the player's second highest scoring affinity -- unless their second highest has less than 50% of the main's score. Going back to the example with Annie Bot, because Annie has only one affinity assigned to her, Annie Bot will not have a sub-affinity. The app will treat this as if his sub-affinity is the same as his main, and it will move on. For another example: if a player has 100k points on Marksman, and 51k points on Warden (defensive tank: Braum, Thresh...), they will have the sub-affinity of Warden, but if they only had 49k points, they would not. This is because their sub-affinity must have at least half of the amount of points that their main affinity has.

The way that the affinities are represented on the card is with the main affinity and its level up at the top-right, and a synonym for the sub-affinity just below the summoner's icon. The level is not the same as the champion mastery level used in the client right now. Any levels used in this app are actually (total points / points required for level 4). I found this to be a more accurate result for showing how invested a summoner is in each role.

And finally, the skill list. I created a list of skills that can be seen in Skills.py. There are quite a few, but they have to cover all combinations of roles. The overall idea with the usage of these skills would be a card game that involved moving your cards through a grid. The cards are not (and may never) be play-ready, but I think the skills bring them more to life. The skills are NOT random. I wanted to be sure that the skills would hold meaning instead of just being silly space-taker-uppers on the card. This way, if you search yourself twice or if other people search you, they will find the same stats and skills that you did. (Try searching for someone that has no champion mastery!)


# HOW IT WORKS
So without further ado, a condensed an more mathematical presentation. League Affinity works using the following method:  
1. Get a list of all champions that the searched summoner has mastery points for.  
2. Takes the amount of champion mastery points for each individual champion, and splits it among that champion's affinities, adding each amount to the summoner's totals. This includes their overall total points and their points for each affinity.  
3. Once finished with all champions, find the summoner's total level by dividing their total points by the amount of points required to get to champion mastery level 4. Do the same for each affinity.  
4. Decide which affinity is their main simply by which one has the most points. Follow this with a decision on a sub affinity by finding the second highest that has more than 50% of the main affinity's total points.  
5. Prepare all trivial information that will be displayed on the card: Name, affinity, level, sub-affinity, icons, etc.  
6. Decide on skills by indexing the SKILLS dictionary with the main affinity, skill number (1-3), and sub-affinity.  
7. Display all information into the appropriate place on the card. This uses HTML and much more so, the CSS file.  
8. Also display other information about the summoner's affinity in the right-hand column. This is mostly information that does not appear on the card, but would be interesting to the user. (all affinity levels, total level, total points, etc.)
  

# ABOUT ME AND BUILDING THE PROJECT
Thank you for taking the time to read over my project. This was the first time I had used Python, and I kind of like it now, but at the same time, I kind of don't. Haha. I have really only used C++ or C# up until now and Python was a very interesting change from those two. I only used Python because when I was first interested in taking part in this competition, I learned about the 'requests' module and the ease with which it can get and send data over the net. Thanks to that and its SUPER easy json <--> dictionary conversions make it simple to write a class to access Riot's API. This is also the first time I have worked with any internet program whatsoever, and therefore it was also my first time building a website and deploying to a web host. Everything seemed so daunting at first, but after doing some research, I learned a simple method to get everything done using Flask for a webserver and Heroku for hosting. This has been an awesome adventure for me and it was an incredible opportunity to get some experience in that I probably would not have otherwise.

I, myself, Tyler Brockmeyer, wrote 100% of the code for this project. I have one sole friend who helped, Alex Ambrose, who designed the layout of the website, and drew, painted, and arranged the layout of the playing card. I had no other help outside of him, and this idea was purely my own.
