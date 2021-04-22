import time
from collections import Counter
from unittest.mock import Mock, MagicMock

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from utils import timer_priority_queue
from models import timer
import os

try:
    IS_TRAVIS = os.environ['TRAVIS'] # https://docs.travis-ci.com/user/environment-variables/
except:
    IS_TRAVIS = False

DISCORD_EMAIL = 'go2977@wayne.edu'
DISCORD_PASSWORD = 'alph@bet@123'
DISCORD_USER_ID = 831306913819394068
BOT_PREFIX = 'lb'
REQUEST_WAIT_TIME = 5
COMMAND_WAIT_TIME = 60

UNIT_TEST_CHANNEL_URL = 'https://discord.com/channels/801966497235730472/828825916573745185'
DM_CHANNEL_URL = 'https://discord.com/channels/@me/831667630145536030'

TEXT_INPUT_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div/div/div[3]/div[2]'
MESSAGE_CONTAINER_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/div[1]/div/div/div'

TEXT_MESSAGE_CLASS = 'message-2qnXI6'
TEXT_MESSAGE_BODY_CLASS = 'markup-2BOw-j'

EMBED_MESSAGE_CLASS = 'grid-1nZz7S'
EMBED_MESSAGE_BODY_CLASS = 'embedDescription-1Cuq9a'


@pytest.fixture(scope="session")
def driver():
    if IS_TRAVIS:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=chrome_options)  # initiate a headless webdriver instance through Selenium with no-sandbox
    else:
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
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(REQUEST_WAIT_TIME)
    yield driver  # allow for tests to run
    driver.quit()  # teardown by quitting the webdriver instance


'''
def test_unit_test_channel(driver: webdriver.Chrome):
    text = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/div[1]/div/div/div/div[1]/h1').text
    assert text == 'Welcome to #unit-testing!'
'''


def test_ping_command(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys(f'{BOT_PREFIX}!ping' + Keys.RETURN)
    if IS_TRAVIS:
        print(driver.current_url)
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(TEXT_MESSAGE_BODY_CLASS).text
    assert message_text == 'pong!'


def test_create_todo(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys(f'{BOT_PREFIX}!create-item 1 test' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(EMBED_MESSAGE_BODY_CLASS).text
    assert message_text == 'ToDoList Item created!'
    driver.get(DM_CHANNEL_URL)
    time.sleep(REQUEST_WAIT_TIME)
    time.sleep(COMMAND_WAIT_TIME)
    messages = driver.find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(TEXT_MESSAGE_BODY_CLASS).text
    assert 'To Do Item' in message_text
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(REQUEST_WAIT_TIME)


def test_timer_pqueue_singleton_instance():
    instance = timer_priority_queue.TimerPriorityQueue.get_instance()
    assert instance is not None
    instance_2 = timer_priority_queue.TimerPriorityQueue.get_instance()
    assert instance_2 is not None
    assert instance == instance_2


# pytest runs as a separate process, and therefore the following must be mocked since the memory space is different
def test_timer_pqueue_user_map():
    def mock_dict(d):  # https://stackoverflow.com/questions/38299103/how-to-mock-a-dictionary-in-python
        m = MagicMock()
        m.__getitem__.side_effect = d.__getitem__
        return m
    timer_priority_queue.TimerPriorityQueue.get_instance().user_map = mock_dict({DISCORD_USER_ID: ['Test']})
    user_map = timer_priority_queue.TimerPriorityQueue.get_instance().user_map
    assert user_map[DISCORD_USER_ID] is not None


def test_timer_pqueue_alarm_map():
    # a Counter is just a dict
    def mock_counter(c):  # https://stackoverflow.com/questions/38299103/how-to-mock-a-dictionary-in-python
        m = MagicMock()
        m.__getitem__.side_effect = c.__getitem__
        return m
    timer_priority_queue.TimerPriorityQueue.get_instance().alarm_map = mock_counter(Counter({DISCORD_USER_ID: 1}))
    alarm_map = timer_priority_queue.TimerPriorityQueue.get_instance().alarm_map
    assert alarm_map[DISCORD_USER_ID] is not None


def test_timer_pqueue_peek():
    timer_priority_queue.TimerPriorityQueue.get_instance().peek = Mock(return_value=timer.Timer)  # https://realpython.com/python-mock-library/#configuring-your-mock
    assert timer_priority_queue.TimerPriorityQueue.get_instance().peek().__name__ == 'Timer'
