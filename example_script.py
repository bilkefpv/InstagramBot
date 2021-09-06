from insta_bot import *
import timeit

start = timeit.default_timer()
try:
    with Bot("username", "password") as bot:
        bot.setup_interact(interact=False)
        bot.like_by_feed(amount=10)
        bot.setup_interact(interact=True, interact_percentage=50, interact_amount_like=4)
        bot.setup_follow(do_follow=True, follow_criteria=1.05, follow_people=15)
        bot.like_by_hashtag(hashtag=["computerscience", "python"], amount=50)
        bot.view_stories(for_minutes_long=2, seconds_between_stories=3)
        print("Instabot finished...")

finally:
    stop = timeit.default_timer()
    print(f'Time:  {(stop - start) // 60} minutes ')
    report(ret=True)
