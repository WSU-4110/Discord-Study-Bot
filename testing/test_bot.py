import asyncio
import os
import time
import datetime as dt
from datetime import timedelta as td
import pytest
from typing import Tuple, List
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

from models import timer
from utils import config as cfg

load_dotenv()
DISCORD_EMAIL = os.getenv('TEST_USER')
DISCORD_PASSWORD = os.getenv('TEST_PASS')

LOAD_WAIT_TIME = 5
REQUEST_WAIT_TIME = 2
COMMAND_WAIT_TIME = 60

UNIT_TEST_CHANNEL_URL = 'https://discord.com/channels/801966497235730472/832299823020769351'
DM_CHANNEL_URL = 'https://discord.com/channels/@me/832079906300624966'

TEXT_INPUT_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div/div/div[3]/div[2]'
MESSAGE_CONTAINER_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/div[1]/div/div/div'

TEXT_MESSAGE_CLASS = 'message-2qnXI6'
TEXT_MESSAGE_BODY_CLASS = 'markup-2BOw-j'

EMBED_MESSAGE_CLASS = 'grid-1nZz7S'
EMBED_MESSAGE_BODY_CLASS = 'embedDescription-1Cuq9a'
EMBED_MESSAGE_TITLE_CLASS = "embedTitle-3OXDkz"
EMBED_MESSAGE_FIELD_CLASS = "embedFieldValue-nELq2s"

USERID = '832075762458558544'
NAME = "gv7006"
MENTION = "@" + NAME


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()  # initiate a webdriver instance through Selenium
    driver.get('https://discord.com/app')  # go to Discord's login page
    # enter email
    driver.find_element_by_xpath(
        '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[1]/div/div[2]/input').send_keys(
        DISCORD_EMAIL)
    # enter password
    driver.find_element_by_xpath(
        '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[2]/div/input').send_keys(
        DISCORD_PASSWORD)
    # click login button
    driver.find_element_by_xpath(
        '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]').click()
    time.sleep(REQUEST_WAIT_TIME)  # wait for request to process
    yield driver  # allow for tests to run
    driver.quit()  # teardown by quitting the webdriver instance


'''
def test_unit_test_channel(driver: webdriver.Chrome):
    text = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/div[1]/div/div/div/div[1]/h1').text
    assert text == 'Welcome to #unit-testing!'
'''


def send_text_input(driver: webdriver.Chrome, command: str):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys(command + Keys.RETURN)


def get_latest_message_text(driver: webdriver.Chrome) -> str:
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(TEXT_MESSAGE_BODY_CLASS).text
    return message_text


def get_latest_embed_text(driver: webdriver.Chrome) -> str:
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_BODY_CLASS).text
    return message_text


def get_latest_titled_embed_text(driver: webdriver.Chrome) -> Tuple[str, str]:
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_title = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_TITLE_CLASS).text
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_BODY_CLASS).text
    return message_title, message_text


def get_latest_titled_embed_field_text(driver: webdriver.Chrome) -> Tuple[str, List[str]]:
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_title = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_TITLE_CLASS).text
    message_field_text = [x.text for x in
                          messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_elements_by_class_name(
                              EMBED_MESSAGE_FIELD_CLASS)]
    return message_title, message_field_text


# def test_set_timer(driver: webdriver.Chrome):
#     driver.get(UNIT_TEST_CHANNEL_URL)
#     time.sleep(LOAD_WAIT_TIME)
#
#     # Clear timers
#     send_text_input(driver, 'ss!unset-all-timers')
#     time.sleep(REQUEST_WAIT_TIME)
#
#     # Test non numeric duration input
#     send_text_input(driver, 'ss!set-timer hi not-a-number')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_text = get_latest_embed_text(driver)
#     assert embed_text == "Non-numeric timer duration given!"
#
#     # Test numeric duration input out of range
#     send_text_input(driver, 'ss!set-timer 300 toolong')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_text = get_latest_embed_text(driver)
#     assert embed_text == "Timer duration not in acceptable range! [1 .. 120]"
#
#     # Test correct input
#     send_text_input(driver, 'ss!set-timer 1 working')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_text = get_latest_embed_text(driver)
#     assert embed_text == "Timer created!"
#
#     # Testing that timer fired properly (not required for this unit test, responsibility falls on async_tasks)
#     # driver.get(DM_CHANNEL_URL)
#     # time.sleep(REQUEST_WAIT_TIME)
#     # time.sleep(COMMAND_WAIT_TIME)
#     # message_text = get_latest_message_text(driver)
#     # embed_title, embed_text = get_latest_titled_embed_text(driver)
#     # assert all([text in message_text for text in ("Alerting", MENTION)])
#     # assert embed_title == "Timer Expired!"
#     # assert embed_text == "working"
#
#
# def test_highest_timer(driver: webdriver.Chrome):
#     driver.get(UNIT_TEST_CHANNEL_URL)
#     time.sleep(LOAD_WAIT_TIME)
#
#     # Clear timers
#     send_text_input(driver, 'ss!unset-all-timers')
#     time.sleep(REQUEST_WAIT_TIME)
#
#     # Test for empty queue
#     send_text_input(driver, 'ss!highest-timer')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_text = get_latest_embed_text(driver)
#     assert embed_text == "No timers found!"
#
#     # Add timers to queue
#     send_text_input(driver, 'ss!set-timer 3 three')
#     time.sleep(REQUEST_WAIT_TIME)
#     send_text_input(driver, 'ss!set-timer 2 two')
#     time.sleep(REQUEST_WAIT_TIME)
#     send_text_input(driver, 'ss!set-timer 1 one')
#     time.sleep(REQUEST_WAIT_TIME)
#
#     # Test correctness
#     send_text_input(driver, 'ss!highest-timer')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_title, embed_field_text = get_latest_titled_embed_field_text(driver)
#     assert embed_title == "Detailed Timer Information"
#     assert embed_field_text[0] == "one"
#
#
# def test_list_timers(driver: webdriver.Chrome):
#     driver.get(UNIT_TEST_CHANNEL_URL)
#     time.sleep(LOAD_WAIT_TIME)
#
#     # Clear timers
#     send_text_input(driver, 'ss!unset-all-timers')
#     time.sleep(REQUEST_WAIT_TIME)
#
#     # Test for empty queue
#     send_text_input(driver, 'ss!list-timers')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_text = get_latest_embed_text(driver)
#     assert embed_text == "No timers found!"
#
#     # Add timers to queue
#     send_text_input(driver, 'ss!set-timer 3 three')
#     time.sleep(REQUEST_WAIT_TIME)
#     send_text_input(driver, 'ss!set-timer 2 two')
#     time.sleep(REQUEST_WAIT_TIME)
#     send_text_input(driver, 'ss!set-timer 1 one')
#     time.sleep(REQUEST_WAIT_TIME)
#
#     # Test for empty queue
#     send_text_input(driver, 'ss!list-timers')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_title, embed_field_text = get_latest_titled_embed_field_text(driver)
#     assert embed_title == "Active Timers"
#     assert all([embed_field_text[i] == t for i, t in zip(range(0, 9, 3), ("one", "two", "three"))])
#
#     send_text_input(driver, 'ss!list-timers 2')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_title, embed_field_text = get_latest_titled_embed_field_text(driver)
#     assert embed_title == "Active Timers"
#     assert all([embed_field_text[i] == t for i, t in zip(range(0, 6, 3), ("one", "two"))])
#
#     send_text_input(driver, 'ss!list-timers -2')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_title, embed_field_text = get_latest_titled_embed_field_text(driver)
#     assert embed_title == "Active Timers"
#     assert all([embed_field_text[i] == t for i, t in zip(range(0, 3, 3), ("one",))])
#
#
# def test_unset_timer(driver: webdriver.Chrome):
#     driver.get(UNIT_TEST_CHANNEL_URL)
#     time.sleep(REQUEST_WAIT_TIME)
#
#     # Clear timers
#     send_text_input(driver, 'ss!unset-all-timers')
#     time.sleep(REQUEST_WAIT_TIME)
#
#     # Test for empty queue
#     send_text_input(driver, 'ss!unset-timer 1')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_text = get_latest_embed_text(driver)
#     assert embed_text == "No timers found!"
#
#     # Add timers to queue
#     send_text_input(driver, 'ss!set-timer 3 three')
#     time.sleep(REQUEST_WAIT_TIME)
#     send_text_input(driver, 'ss!set-timer 2 two')
#     time.sleep(REQUEST_WAIT_TIME)
#     send_text_input(driver, 'ss!set-timer 1 one')
#     time.sleep(REQUEST_WAIT_TIME)
#
#     # Test non numeric duration input
#     send_text_input(driver, 'ss!unset-timer not-a-number')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_text = get_latest_embed_text(driver)
#     assert embed_text == "Non-numeric index given!"
#
#     # Test numeric duration input out of range
#     send_text_input(driver, 'ss!unset-timer 300')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_text = get_latest_embed_text(driver)
#     assert embed_text == "Index input not in range! Range [1 .. 3], got 300"
#
#     # Test correctness
#     send_text_input(driver, 'ss!unset-timer 2')
#     time.sleep(REQUEST_WAIT_TIME)
#     embed_text = get_latest_embed_text(driver)
#     assert embed_text == "Timer deleted!"


def test_time_remaining():
    my_timer = timer.Timer(USERID, 300, '', None)
    target_diff = td(minutes=4)
    time.sleep(COMMAND_WAIT_TIME)
    assert my_timer.time_remaining() - target_diff < td(seconds=5)


def test_colhex():
    ...
