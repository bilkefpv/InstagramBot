# Instagram Bot
Hey! I've written this automation tool for Instagram for fun and practice.

If you are searching for a good automation tool for Instagram take a look at [InstaPy](https://github.com/timgrossmann/InstaPy).  
This tool is inspired by InstaPy, but is not a fork of InstaPy.  
All of the code written here is mine.

The easiest way to start the bot after downloading requierments is to  
Replace "username" and "password" with your credentials in `Bot("username", "password") as bot:` in [example_script.py](example_script.py)  
And just run the script :)

## requirements:
pip install selenium  
pip install webdriver-manager  
pip install fake-useragent

## Bot Arguments
In [example_script.py](example_script.py) we use class ` Bot("username", "password") as bot:`  
Here you can additionally declare variables  

1.`mute_audio = True`By default audio is off.  
Let's say you want to use `bot.watch_stories` function and want audio, declare bot like this  
`Bot("username", "password", mute_audio=False). `

2.`headless = False`By default headless mode is off.    
If you want the webdriver to work headless just init bot like this:  
`Bot("username", "password", headless=True). `

3.`fake_agent=False`By default fake agent is off  
If you want the chromedriver to run on a random fake agent just declare it like
`Bot("username", "password", fake_agent=True).`  

For example, I want to setup bot with fake agent on headless mode:  
`Bot("username", "password", fake_agent=True, headless=True).`

## Avaliable functions

Now that you have initliazed Bot class let's see what it can do.  
In [example_script.py](example_script.py) on line 8 we have our first action function
### like_by_feed  
`bot.like_by_feed(amount=10)`
This will scrool on your home feed and like posts for the choosen amount.
### setup_interact
In this case when liking on our feed it will not interact with profiles whos pictures it liked, because on line 7 we setup bot `bot.setup_interact(interact=False)`.  
If we decalred instead ` bot.setup_interact(interact=True, interact_percentage=50,  interact_amount_like=4)` above `like_by_feed` on Line 8  
Then because `interact_percentage=50` bot would visit 5 profiles and like 4 posts on each profile, because `interact_amount_like=4`
### setup_follow
In [example_script.py](example_script.py) we used `bot.setup_follow(do_follow=True, follow_criteria=1.05, follow_people=15)`  
This means that when interacting with profile it will check  `if following / followers >= follow_crit:`  
Let's say bot is on a profile that has 1000 followers and is following 1005 people. Then the criteria will be 1.05 and we will follow that profile.  
`follow_people=15` means that bot will repeat looking for profiles until it follows 15 people. But how? Which profiles? Well firstly both `setup_interact(interact=True)` and `setup_follow(do_follow=True)` need to be set and then you have only 1 action (like_by_hashtags) avaliable from where bot will collect profile links and visit(interact) with them and follow if met with critiera.
### like_by_hashtags
In [example_script.py](example_script.py) we used `bot.like_by_hashtag(hashtag=["computerscience", "python"], amount=50)`  
This means it will like 50 posts on each hashtag. Because we set `interact_percentage= 50%` and `interact = True` it will save 25 profile links and visit them. Because we set `follow = True` and `follow_people=15` it will <b>try to </b> follow 8 new people out of 25 visited. Why try to? Because of `follow_criteria=1.05` it's not guaranteed that out of 25 profiles 8 of them will match our criteria. Because of that bot will repeat the process of liking 50 posts on hashtag until it will follow 8 people in total for that hashtag. Then it will move to the next hashtag and repeat the process. Like 50 posts, visit 50%. Now it will try to follow 7 new people in total, because we set follow_people=15 and we have 2 hashtags.
### view_stories
In [example_script.py](example_script.py) we used `bot.view_stories(for_minutes_long=2, seconds_between_stories=3)`
This one is self explanitory. In this case bot will watch stories for 2 minutes and click on next story every 3 seconds. In this case,because of line 9 and 10 bot has a setup to follow and interact. In this case, because stories (same with feed) are your followers it will only interact with some profiles and won't try to follow anyone.
   
