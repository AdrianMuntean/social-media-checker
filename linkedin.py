from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import common
import config


def print_notifications(unread_count):
    browser.find_element_by_id('notifications-nav-item').click()
    try:
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[@class='t-16 t-black t-bold']")))
        notifications = browser.find_elements_by_xpath("//button[@class='nt-card__headline nt-card__text--3-line "
                                                       "nt-card__text--align-start nt-card__text--word-wrap t-14 "
                                                       "t-black t-normal']")
        text = [notifications[i].text for i in range(unread_count)]
        for notification in text:
            print("  ->         %s" % common.parse_text(notification))
    except TimeoutException:
        pass


def check_notifications():
    if config.linkedin_checks['notification_check']:
        unread = browser.find_elements_by_xpath("//a[@data-link-to='notifications']//span[@class='nav-item__badge-count']")
        unread_count_text = [x.text for x in unread]
        if len(unread_count_text) > 0:
            print("You have %s new notification(s)" % unread_count_text[0])
            print_notifications(int(unread_count_text[0]))
        else:
            print("0 notifications")


def print_messages(unread_count):
    browser.find_element_by_id('messaging-nav-item').click()
    try:
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1[@class='flex-grow-1 ph4 t-16 t-black t-bold']")))
        messages_sender = browser.find_elements_by_xpath("//h3[@class='msg-conversation-listitem__participant-names msg-conversation-card__participant-names truncate pr1 t-16 t-black--light t-normal']")
        senders = [messages_sender[i].text for i in range(unread_count)]
        for sender in senders:
            print("  -> From     %s" % common.parse_text(sender))
    except TimeoutException:
        pass


def check_messages():
    if config.linkedin_checks['message_check']:
        unread = browser.find_elements_by_xpath("//a[@data-link-to='messaging']//span[@class='nav-item__badge-count']")
        unread_count_text = [x.text for x in unread]
        if len(unread_count_text) > 0:
            print("You have %s new message(s)" % unread_count_text[0])
            print_messages(int(unread_count_text[0]))
        else:
            print("0 messages")


def approve_all_invites_if_needed(param):
    if config.linkedin_actions['accept_all_invites']:
        browser.find_element_by_id('mynetwork-nav-item').click()
        try:
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[@class='flex-1 t-18 t-black t-normal']")))
            accept_button = browser.find_elements_by_xpath("//button[@class='invitation-card__action-btn button-secondary-medium ']")
            for button in accept_button:
                print("  **** Accepted %s" % button.text[14:])
                button.click()
        except TimeoutException:
            print("   ****Could not approve %s invites****" % param)


def check_connection_invite():
    if config.linkedin_checks['connection_invitation_check']:
        unread = browser.find_elements_by_xpath("//a[@data-link-to='mynetwork']//span[@class='nav-item__badge-count']")
        unread_count_text = [x.text for x in unread]
        if len(unread_count_text) > 0:
            print("You have %s new invite(s))" % unread_count_text[0])
            approve_all_invites_if_needed(int(unread_count_text[0]))
        else:
            print("0 invites")


option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--headless")
browser = webdriver.Chrome(executable_path=config.chrome_driver_path, chrome_options=option)

browser.get("https://www.linkedin.com")

common.login(browser, 'linkedin')
timeout = 8
try:
    # Wait until the final element [Avatar link] is loaded.
    # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
    # the last things to be loaded.
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='lazy-image "
                                                                                      "loaded "
                                                                                      "feed-identity-module__member"
                                                                                      "-photo "
                                                                                      "profile-rail-card__member"
                                                                                      "-photo "
                                                                                      "EntityPhoto-circle-5']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    print("Please check the password and the email in config.py")
    browser.quit()
    sys.exit(1)

try:
    name_element = browser.find_element_by_xpath("//span[@class='t-16 t-black t-bold']")
    print('')
    print("Hello %s, checking for Linkedin:" % name_element.text)
    print('')
except:
    print("An error occured")

print('----------------------')
check_notifications()
check_messages()
check_connection_invite()
print('----------------------')
browser.quit()
