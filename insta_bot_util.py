from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from fake_useragent import UserAgent
from random import choice
from time import sleep

from web_element import web_element, click_on_element, element_exsist
from log_handle import *
from report import Stats
from misc import hashtag_list_to_follow_per_hashtag_list

info = Stats()
report = getattr(info, "report")


def login(d, username, password):
    # delete cookies
    js = "var element = document.getElementsByClassName(\"RnEpo\")[0];element.remove();"
    d.execute_script(js)
    username_xpath = "//*[@id='loginForm']/div/div[1]/div/label/input"
    password_xpath = "//*[@id='loginForm']/div/div[2]/div/label/input"
    login_button_xpath = "//*[@id='loginForm']/div/div[3]/button"
    not_now_cookies_xpath = "//*[@id='react-root']/section/main/div/div/div/div/button"
    not_now_privacy_xpath = "/html/body/div[5]/div/div/div/div[3]/button[2]"

    web_element(d, username_xpath, xpath=True, send_keys=username)
    web_element(d, password_xpath, xpath=True, send_keys=password)
    web_element(d, login_button_xpath, xpath=True).click()
    web_element(d, not_now_cookies_xpath, xpath=True).click()
    web_element(d, not_now_privacy_xpath, xpath=True).click()


def like_util(d):
    for element in web_element(d, "_8-yf5", class_name=True, elements=True):  # find Like button
        try:
            if element.get_attribute("aria-label") == "Like" and int(element.get_attribute("height")) > 13:
                # dont like comments
                click_on_element(d, element=element)
                report(liked=True)
                break
            elif element.get_attribute("aria-label") == "Unlike" and int(element.get_attribute("height")) > 13:
                report(skipped=True)
        except NoSuchElementException or StaleElementReferenceException:
            print("Skipping...Like or Unlike button missing")
            continue


def scroll_collect_site(d, amount, skip_top_posts=True, collect_by_hashtag=False, hashtag=None):
    other_posts = set()  # TODO implement amount calculation
    top_posts = set()

    if element_exsist(d, "EZdmt"):  # then grab top posts data and add that to set elements_grabbed
        for ele in web_element(d, "EZdmt", elements=True, class_name=True):
            top_posts.add(web_element(ele, "a", tag_name=True, attribute="href"))

    if element_exsist(d, "g47SY"):
        avaliable_posts = web_element(d, "g47SY", class_name=True, elements=True)[0].text
        avaliable_posts = int(avaliable_posts.replace(",", ""))
        if amount > avaliable_posts:
            amount = avaliable_posts

    previous_elements = None

    if element_exsist(d, "v1Nh3"):
        actions = ActionChains(d)
        while len(other_posts) < amount:
            current_elements = web_element(d, "v1Nh3", class_name=True, elements=True)
            if current_elements == previous_elements:  # i'm at the end
                break
            for ele in current_elements:
                link = web_element(ele, "a", tag_name=True, attribute="href")
                if collect_by_hashtag:
                    if hashtag in my_dict:
                        if link not in my_dict[hashtag]:
                            other_posts.add(link)
                    else:
                        other_posts.add(link)
                else:
                    other_posts.add(link)

            actions.send_keys(Keys.END).perform()
            previous_elements = current_elements.copy()

    if collect_by_hashtag:
        if hashtag in my_dict:
            my_dict[hashtag] = my_dict[hashtag] | other_posts
        else:
            my_dict[hashtag] = other_posts
    if skip_top_posts:
        all_posts = other_posts
    else:
        all_posts = other_posts | top_posts
    return list(all_posts)[:amount]


def like_posts(d, amount, interact=False, interact_amount_like=3, interact_percentage=10,
               follow=False, follow_crit=1, follow_amount=0, like_by_hashtag=False, tag=None):
    try:
        posts = scroll_collect_site(d, amount, collect_by_hashtag=like_by_hashtag, hashtag=tag)
        to_interact = set()
        for post in posts:
            sleep(1)
            d.get(post)
            if interact:
                human = web_element(d, "o-MQd", class_name=True).text.split("•")[0]
                if human not in to_interact:
                    to_interact.add(human)
            like_util(d)  # click Like button

        if interact:
            interact_with_list(d, to_interact, interact_amount_like, interact_percentage,
                               follow, follow_crit, follow_amount)
    except NoSuchElementException:
        print("Element wasn't found...Skipping")
    sleep(2)


def extract_follower_following_info(d):
    try:
        followers = web_element(d, "g47SY", elements=True, class_name=True, attribute="title", index=1)
        followers = int(followers.replace(",", ""))
        following = web_element(d, "g47SY", elements=True, class_name=True)[2].text
        following = int(following.replace(",", ""))
        return following, followers
    except ValueError:
        return 0, 0


def follow_util(d, follow_crit):
    following, followers = extract_follower_following_info(d)
    if followers == 0 or following == 0:
        return 0
    if following / followers >= follow_crit:
        try:
            if (ele := web_element(d, "_5f5mN", class_name=True, elements=True)[0]).text == "Follow":
                ele.click()
                report(followed=True)
            elif not ele.text:
                report(already_follow=True)
        except IndexError:
            print("Exception happened on url: ", d.current_url)
            raise NoSuchElementException
    sleep(1)


def interact_with_list(driver, people, amount, percentage,
                       follow=False, follow_crit=1, follow_amount=0, my_followers=False):
    if my_followers:
        follow = False
    amount_of_people = round(len(people) / 100 * percentage)
    peoples = []
    if len(people) < 5:
        amount_of_people = 0
        peoples = people
    for _ in range(amount_of_people):
        peoples.append(choice(list(people)))
    peoples = list(set(peoples))
    for human in [h.replace("\n", "") for h in peoples]:
        followed_actual = info.followed_on_session()
        print(followed_actual)
        sleep(1)
        if "www.instagram" in human:
            driver.get(human.replace("Verified", ""))
        else:
            driver.get(f"http://www.instagram.com/{human}")
        if follow and followed_actual <= follow_amount:
            follow_util(driver, follow_crit)
            followed_actual_after_visit = info.followed_on_session()
            if followed_actual_after_visit == followed_actual:
                continue

        report(interact=True)
        like_posts(driver, amount)
    sleep(2)


def like_feed(d, amount, interact=False, interact_percent=10, like_interact_amount=3):
    actually_liked = 0
    to_interact = []
    while amount > actually_liked:
        articles = web_element(d, "article", elements=True, tag_name=True)
        slicen = len(articles) // 2
        for a in articles[slicen:]:
            sleep(2)
            action = ActionChains(d)
            # move to article
            action.move_to_element(a)
            action.perform()
            if interact:
                to_interact.append(web_element(a, "a", tag_name=True, attribute="href"))
            for element in web_element(a, "_8-yf5", elements=True, class_name=True):  # find Like button
                try:
                    if element.get_attribute("aria-label") == "Like" and int(element.get_attribute("height")) > 13:
                        # dont like comments
                        actually_liked += 1
                        click_on_element(d, element=element)
                        report(liked=True)
                        break
                    elif element.get_attribute("aria-label") == "Unlike" and int(element.get_attribute("height")) > 13:
                        report(skipped=True)
                except NoSuchElementException or StaleElementReferenceException:
                    print("Skipping...Something went wrong with liking feed")
                    continue
    if interact:
        interact_with_list(d, to_interact, like_interact_amount, interact_percent)
