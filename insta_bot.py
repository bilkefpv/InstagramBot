from insta_bot_util import *
import timeit


class Bot:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # print(exc_type, exc_value, exc_traceback)
        write_dict()
        self.driver.quit()

    def __init__(self, username, password, mute_audio=True, fake_agent=False, headless=False):
        self.interact_percent = 10
        self.interact = False
        self.like_interact_amount = 3
        self.driver = None
        self.like_posts = True
        self.comment_posts = False
        self.follow = False
        self.follow_crit = 1.3
        self.comments = []
        self.comment_pecentage = 0
        self.amount_to_follow = 4
        read_dict()
        options = Options()
        options.headless = headless
        if fake_agent:
            options.add_argument(f'user-agent={UserAgent().random}')
        if mute_audio:
            options.add_argument("--mute-audio")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.implicitly_wait(20)
        self.driver.get("http://www.instagram.com")
        login(self.driver, username, password)

    def setup(self, do_like=True, do_comment=False, comments_percentage=0, comments=None):
        self.like_posts = do_like
        self.comment_posts = do_comment
        self.comments = comments
        self.comment_pecentage = comments_percentage
        if self.comment_posts:
            self.comment_pecentage = 10

    def setup_follow(self, do_follow, follow_criteria=1.3, follow_people=4):
        self.follow = do_follow
        self.follow_crit = follow_criteria  # following / followers
        self.amount_to_follow = follow_people

    def setup_interact(self, interact_percentage=10, interact=False, interact_amount_like=3):
        self.interact_percent = interact_percentage
        self.interact = interact
        self.like_interact_amount = interact_amount_like
        if interact_percentage < 10:
            self.interact_percent = 10
            self.interact = False

    def view_stories(self, for_minutes_long, seconds_between_stories=2):
        self.driver.get("https://www.instagram.com/")
        click_on_element(self.driver, "OE3OK ")  # Click on first story
        start = timeit.default_timer()
        stop = start
        to_interact = set()
        while stop - start < for_minutes_long * 60:
            if self.interact:
                story_profile = self.driver.find_element_by_class_name("FPmhX").text
                if story_profile not in to_interact:
                    to_interact.add(story_profile)
            click_on_element(self.driver, "FhutL")  # scroll next story
            sleep(seconds_between_stories)
            stop = timeit.default_timer()
        if self.interact:
            interact_with_list(self.driver, to_interact, self.like_interact_amount, self.interact_percent,my_followers=True)

    def like_by_hashtag(self, hashtag, amount):
        if not isinstance(hashtag, list):
            hashtags = [hashtag]
        else:
            hashtags = hashtag
        follow_per_hashtag = hashtag_list_to_follow_per_hashtag_list(hashtags, self.amount_to_follow)
        for tag in hashtags:
            link = "https://www.instagram.com/explore/tags/" + tag
            self.driver.get(link)
            sleep(1)
            this_hashtag_to_follow_people = next(follow_per_hashtag)
            if self.follow:
                followed_on_session = info.followed_actual
                while followed_on_session < this_hashtag_to_follow_people:
                    link = "https://www.instagram.com/explore/tags/" + tag
                    self.driver.get(link)
                    like_posts(self.driver, amount, self.interact, self.like_interact_amount, self.interact_percent,
                               self.follow, self.follow_crit, this_hashtag_to_follow_people, like_by_hashtag=True,
                               tag=tag)
                    followed_on_session = info.followed_actual
            else:
                like_posts(self.driver, amount, self.interact, self.like_interact_amount, self.interact_percent,
                           self.follow, self.follow_crit, this_hashtag_to_follow_people, like_by_hashtag=True, tag=tag)

    def like_by_feed(self, amount):
        self.driver.get("https://www.instagram.com")
        like_feed(self.driver, amount, self.interact, self.interact_percent, self.like_interact_amount)
