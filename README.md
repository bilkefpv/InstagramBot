# Instagram Bot
Replace "username" and "password" in example_script.py

## requirements: selenium, webdriver_manager, fake_useragent  
pip install selenium  
pip install webdriver-manager  
pip install fake-useragent

## Bot init
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

Now that we have initliazed our Bot class let's see what it can do.  

