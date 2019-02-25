from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import common
import config


def print_notifications(unread_count):
    browser.find_element_by_id('fbNotificationsJewel').click()
    try:
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_fyy']")))
        notifications = browser.find_elements_by_xpath("//li[@class='_33c jewelItemNew']")
        text = [notifications[i].text for i in range(unread_count)]
        for notification in text:
            print("  ->         %s" % common.parse_text(notification))
    except TimeoutException:
        pass


def check_notifications():
    if config.facebook_checks['notification_check']:
        unread_count = browser.find_element_by_id('notificationsCountValue')
        if len(unread_count.text) > 0:
            print("You have %s new notification(s)" % unread_count.text)
            print_notifications(int(unread_count.text))
        else:
            print("0 notifications")


def print_messages(unread_count):
    browser.find_element_by_id('u_0_e').click()
    try:
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='_1sdi _1sde _1sdd mrm']")))
        messages = browser.find_elements_by_xpath("//a[@class='messagesContent']")
        unread_messages = [messages[i].text for i in range(unread_count)]
        for unread in unread_messages:
            print("  -> Message     %s" % unread.split('\n')[0])
    except TimeoutException:
        pass


def check_messages():
    if config.facebook_checks['message_check']:
        unread_count = browser.find_element_by_id('mercurymessagesCountValue')
        if len(unread_count.text) > 0:
            print("You have %s new message(s)" % unread_count.text)
            print_messages(int(unread_count.text))
        else:
            print("0 messages")


def check_friend_request():
    if config.facebook_checks['friend_request_check']:
        unread_count = browser.find_element_by_id('requestsCountValue')
        if len(unread_count.text) > 0:
            print("You have %s friend request(s))" % unread_count.text)
        else:
            print("0 friend requests")


option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--headless")
browser = webdriver.Chrome(executable_path=config.chrome_driver_path, chrome_options=option)

browser.get("https://www.facebook.com")

common.login(browser, 'facebook')
timeout = 8
try:
    # Wait until the final element [Avatar link] is loaded.
    # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
    # the last things to be loaded.
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='_2qgu _54rt img']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    print("Please check the password and the email in config.py")
    browser.quit()
    sys.exit(1)

try:
    name_element = browser.find_element_by_xpath("//div[@class='linkWrap noCount']")
    print('')
    print("Hello %s, checking for Facebook:" % name_element.text)
    print('')
except:
    print("An error occured")

print('----------------------')
check_notifications()
check_messages()
check_friend_request()
print('----------------------')
browser.quit()
