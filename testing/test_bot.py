import time
import datetime as dt
from collections import Counter
from typing import Tuple, List
from unittest.mock import Mock, MagicMock
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from utils import timer_priority_queue, time_utils, database_utils, config as cfg
from models import timer
import os

try:
    IS_TRAVIS = os.environ['TRAVIS']  # https://docs.travis-ci.com/user/environment-variables/
except:
    IS_TRAVIS = False

DISCORD_EMAIL = 'go2977@wayne.edu'
DISCORD_PASSWORD = 'alph@bet@123'
DISCORD_USER_ID = 831306913819394068
BOT_PREFIX = 'lb'
USERID = str(DISCORD_USER_ID)
NAME = "go2977"
MENTION = "@" + NAME

LOAD_WAIT_TIME = 6
REQUEST_WAIT_TIME = 2
COMMAND_WAIT_TIME = 60
LONG_COMMAND_WAIT_TIME = 75

UNIT_TEST_CHANNEL_URL = 'https://discord.com/channels/801966497235730472/828825916573745185'
DM_CHANNEL_URL = 'https://discord.com/channels/@me/831667630145536030'

TEXT_INPUT_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div/div/div[3]/div[2]'
MESSAGE_CONTAINER_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/div[1]/div/div/div'
DM_TEXT_INPUT_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div[3]/div[2]/div'  # '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div[3]/div[2]/div'

TEXT_MESSAGE_CLASS = 'message-2qnXI6'
TEXT_MESSAGE_BODY_CLASS = 'markup-2BOw-j'
EMBED_MESSAGE_CLASS = 'grid-1nZz7S'
EMBED_MESSAGE_BODY_CLASS = 'embedDescription-1Cuq9a'
EMBED_MESSAGE_TITLE_CLASS = 'embedTitle-3OXDkz'
EMBED_TITLE_CLASS = EMBED_MESSAGE_TITLE_CLASS
EMBED_MESSAGE_FIELD_CLASS = "embedFieldValue-nELq2s"
EMBED_LINKED_TITLE_CLASS = 'anchor-3Z-8Bb'
EMBED_FIELD_VALUE = EMBED_MESSAGE_FIELD_CLASS
EMBED_FIELD_NAME_CLASS = "embedFieldName-NFrena"
REACTION_CLASS = "reactions-12N0jA"
INDIVIDUAL_REACTION_CLASS = "reaction-1hd86g"


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
    def enter_credentials():
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
        time.sleep(LOAD_WAIT_TIME)  # wait for request to process
    enter_credentials()
    try:  # I AM HUMAN
        # time.sleep(2 * LOAD_WAIT_TIME)
        hCaptcha = '/html/body/div[1]/div[2]/div/section/div/div[3]/div'
        driver.find_element_by_xpath(hCaptcha).click()
        time.sleep(2 * LOAD_WAIT_TIME)
        enter_credentials()
    except:
        pass
    # enter 2fa via backup token
    tokens = ['3sbw-z8sw', 'f0bp-v6fo', 'f7d9-riy1', 'fml8-tv9z', 'ydq1-q23r', 'zspb-ruzs']
    token = tokens[0]
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/form/div/div[3]/div/div/input').send_keys(token)
    # click login button (again)
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/form/div/div[3]/button[1]').click()
    time.sleep(LOAD_WAIT_TIME)
    try:  # sometimes we have to login again
        print(driver.page_source)
        enter_credentials()
    except:
        pass
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(LOAD_WAIT_TIME)
    yield driver  # allow for tests to run
    driver.quit()  # teardown by quitting the webdriver instance


'''
def test_unit_test_channel(driver: webdriver.Chrome):
    text = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/div[1]/div/div/div/div[1]/h1').text
    assert text == 'Welcome to #unit-testing!'
'''


# ADI'S TESTS:
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
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_BODY_CLASS).text
    assert message_text == 'ToDoList Item created!'
    driver.get(DM_CHANNEL_URL)
    time.sleep(LOAD_WAIT_TIME)
    messages = driver.find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(TEXT_MESSAGE_BODY_CLASS).text
    assert 'To Do Item' in message_text
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(LOAD_WAIT_TIME)


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
    timer_priority_queue.TimerPriorityQueue.get_instance().peek = Mock(
        return_value=timer.Timer)  # https://realpython.com/python-mock-library/#configuring-your-mock
    assert timer_priority_queue.TimerPriorityQueue.get_instance().peek().__name__ == 'Timer'


# NATALY'S TESTS:
def test_create_note(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys(
        f'{BOT_PREFIX}!create-note test1' + Keys.RETURN)  # creating the note using command
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_TITLE_CLASS).text
    assert message_text == 'Note Created!'  # checking if it matches


def test_list_notes(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys(
        f'{BOT_PREFIX}!list-notes' + Keys.RETURN)  # listing notes command
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_TITLE_CLASS).text
    assert message_text == 'Notes'  # checking if it matches


def test_delete_note(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys(
        f'{BOT_PREFIX}!delete-note' + Keys.RETURN)  # creating the note using command
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('1' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_TITLE_CLASS).text
    assert message_text == 'Note Deleted!'  # checking if it matches


def test_curr_est_offset():
    offset = time_utils.curr_est_offset()  # calling method
    assert offset == -4  # checking if it matches


def test_orig_to_utc():
    a_time = dt.datetime.now()
    a_time_2 = time_utils.orig_to_utc(a_time)
    assert a_time_2 <= dt.datetime.utcnow()  # checking if it matches


def test_utc_to_dest():
    a_time = dt.datetime.now()
    a_time_2 = time_utils.orig_to_utc(a_time)
    assert time_utils.utc_to_dest(a_time_2, 'EST') == a_time  # checking if it matches


# SAFWAAN'S TESTS
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


def test_set_timer(driver: webdriver.Chrome):
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(LOAD_WAIT_TIME)

    # Clear timers
    send_text_input(driver, f'{BOT_PREFIX}!unset-all-timers')
    time.sleep(REQUEST_WAIT_TIME)

    # Test non numeric duration input
    send_text_input(driver, f'{BOT_PREFIX}!set-timer hi not-a-number')
    time.sleep(REQUEST_WAIT_TIME)
    embed_text = get_latest_embed_text(driver)
    assert embed_text == "Non-numeric timer duration given!"

    # Test numeric duration input out of range
    send_text_input(driver, f'{BOT_PREFIX}!set-timer 300 toolong')
    time.sleep(REQUEST_WAIT_TIME)
    embed_text = get_latest_embed_text(driver)
    assert embed_text == "Timer duration not in acceptable range! [1 .. 120]"

    # Test correct input
    send_text_input(driver, f'{BOT_PREFIX}!set-timer 1 working')
    time.sleep(REQUEST_WAIT_TIME)
    embed_text = get_latest_embed_text(driver)
    assert embed_text == "Timer created!"

    # Testing that timer fired properly (not required for this unit test, responsibility falls on async_tasks)
    # driver.get(DM_CHANNEL_URL)
    # time.sleep(REQUEST_WAIT_TIME)
    # time.sleep(COMMAND_WAIT_TIME)
    # message_text = get_latest_message_text(driver)
    # embed_title, embed_text = get_latest_titled_embed_text(driver)
    # assert all([text in message_text for text in ("Alerting", MENTION)])
    # assert embed_title == "Timer Expired!"
    # assert embed_text == "working"


def test_highest_timer(driver: webdriver.Chrome):
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(LOAD_WAIT_TIME)

    # Clear timers
    send_text_input(driver, f'{BOT_PREFIX}!unset-all-timers')
    time.sleep(REQUEST_WAIT_TIME)

    # Test for empty queue
    send_text_input(driver, f'{BOT_PREFIX}!highest-timer')
    time.sleep(REQUEST_WAIT_TIME)
    embed_text = get_latest_embed_text(driver)
    assert embed_text == "No timers found!"

    # Add timers to queue
    send_text_input(driver, f'{BOT_PREFIX}!set-timer 3 three')
    time.sleep(REQUEST_WAIT_TIME)
    send_text_input(driver, f'{BOT_PREFIX}!set-timer 2 two')
    time.sleep(REQUEST_WAIT_TIME)
    send_text_input(driver, f'{BOT_PREFIX}!set-timer 1 one')
    time.sleep(REQUEST_WAIT_TIME)

    # Test correctness
    send_text_input(driver, f'{BOT_PREFIX}!highest-timer')
    time.sleep(REQUEST_WAIT_TIME)
    embed_title, embed_field_text = get_latest_titled_embed_field_text(driver)
    assert embed_title == "Detailed Timer Information"
    assert embed_field_text[0] == "one"


def test_list_timers(driver: webdriver.Chrome):
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(LOAD_WAIT_TIME)

    # Clear timers
    send_text_input(driver, f'{BOT_PREFIX}!unset-all-timers')
    time.sleep(REQUEST_WAIT_TIME)

    # Test for empty queue
    send_text_input(driver, f'{BOT_PREFIX}!list-timers')
    time.sleep(REQUEST_WAIT_TIME)
    embed_text = get_latest_embed_text(driver)
    assert embed_text == "No timers found!"

    # Add timers to queue
    send_text_input(driver, f'{BOT_PREFIX}!set-timer 3 three')
    time.sleep(REQUEST_WAIT_TIME)
    send_text_input(driver, f'{BOT_PREFIX}!set-timer 2 two')
    time.sleep(REQUEST_WAIT_TIME)
    send_text_input(driver, f'{BOT_PREFIX}!set-timer 1 one')
    time.sleep(REQUEST_WAIT_TIME)

    # Test for empty queue
    send_text_input(driver, f'{BOT_PREFIX}!list-timers')
    time.sleep(REQUEST_WAIT_TIME)
    embed_title, embed_field_text = get_latest_titled_embed_field_text(driver)
    assert embed_title == "Active Timers"
    assert all([embed_field_text[i] == t for i, t in zip(range(0, 9, 3), ("one", "two", "three"))])

    send_text_input(driver, f'{BOT_PREFIX}!list-timers 2')
    time.sleep(REQUEST_WAIT_TIME)
    embed_title, embed_field_text = get_latest_titled_embed_field_text(driver)
    assert embed_title == "Active Timers"
    assert all([embed_field_text[i] == t for i, t in zip(range(0, 6, 3), ("one", "two"))])

    send_text_input(driver, f'{BOT_PREFIX}!list-timers -2')
    time.sleep(REQUEST_WAIT_TIME)
    embed_title, embed_field_text = get_latest_titled_embed_field_text(driver)
    assert embed_title == "Active Timers"
    assert all([embed_field_text[i] == t for i, t in zip(range(0, 3, 3), ("one",))])


def test_unset_timer(driver: webdriver.Chrome):
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(REQUEST_WAIT_TIME)

    # Clear timers
    send_text_input(driver, f'{BOT_PREFIX}!unset-all-timers')
    time.sleep(REQUEST_WAIT_TIME)

    # Test for empty queue
    send_text_input(driver, f'{BOT_PREFIX}!unset-timer 1')
    time.sleep(REQUEST_WAIT_TIME)
    embed_text = get_latest_embed_text(driver)
    assert embed_text == "No timers found!"

    # Add timers to queue
    send_text_input(driver, f'{BOT_PREFIX}!set-timer 3 three')
    time.sleep(REQUEST_WAIT_TIME)
    send_text_input(driver, f'{BOT_PREFIX}!set-timer 2 two')
    time.sleep(REQUEST_WAIT_TIME)
    send_text_input(driver, f'{BOT_PREFIX}!set-timer 1 one')
    time.sleep(REQUEST_WAIT_TIME)

    # Test non numeric duration input
    send_text_input(driver, f'{BOT_PREFIX}!unset-timer not-a-number')
    time.sleep(REQUEST_WAIT_TIME)
    embed_text = get_latest_embed_text(driver)
    assert embed_text == "Non-numeric index given!"

    # Test numeric duration input out of range
    send_text_input(driver, f'{BOT_PREFIX}!unset-timer 300')
    time.sleep(REQUEST_WAIT_TIME)
    embed_text = get_latest_embed_text(driver)
    assert embed_text == "Index input not in range! Range [1 .. 3], got 300"

    # Test correctness
    send_text_input(driver, f'{BOT_PREFIX}!unset-timer 2')
    time.sleep(REQUEST_WAIT_TIME)
    embed_text = get_latest_embed_text(driver)
    assert embed_text == "Timer deleted!"


def test_time_remaining():
    my_timer = timer.Timer(USERID, 300, '', None)
    target_diff = dt.timedelta(minutes=4)
    time.sleep(COMMAND_WAIT_TIME)
    assert abs(my_timer.time_remaining() - target_diff) < dt.timedelta(seconds=5)


def test_hex_to_int():
    assert cfg.hex_to_int('#552cae') == 0x552cae
    assert cfg.hex_to_int('#e55186') == 0xe55186
    assert cfg.hex_to_int('#ccfd9d') == 0xccfd9d
    assert cfg.hex_to_int('#59ef14') == 0x59ef14
    assert cfg.hex_to_int('#e6855b') == 0xe6855b
    assert cfg.hex_to_int('#cd89af') == 0xcd89af
    assert cfg.hex_to_int('#eeafac') == 0xeeafac
    assert cfg.hex_to_int('#670d1f') == 0x670d1f
    assert cfg.hex_to_int('#34bfa7') == 0x34bfa7
    assert cfg.hex_to_int('#22f91e') == 0x22f91e


# BRYAN'S TESTS:
# Tests command and creation of one-time repeated reminders
def test_create_reminder(driver: webdriver.Chrome):
    # Clear timers
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(LOAD_WAIT_TIME)
    send_text_input(driver, f'{BOT_PREFIX}!unset-all-timers')
    time.sleep(REQUEST_WAIT_TIME)
    driver.get(DM_CHANNEL_URL)
    time.sleep(LOAD_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys(f'{BOT_PREFIX}!sr' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('th' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('17 10' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('Set Reminder Test' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).text
    print(message_text)
    time.sleep(REQUEST_WAIT_TIME)
    assert message_text == 'Reminder Created!'


# Tests command and creation of user defined number of repeated reminders
def test_create_repeating_reminder(driver: webdriver.Chrome):
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys(f'{BOT_PREFIX}!srr' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('th' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('17 24' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('Set Reminder Test' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('3' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).text
    print(message_text)
    time.sleep(REQUEST_WAIT_TIME)
    assert message_text == 'Reminder Created!'


# Tests command and creation of infinite repeated reminders
def test_create_infinite_reminder(driver: webdriver.Chrome):
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys(f'{BOT_PREFIX}!sir' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('th' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('17 31' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('Set Reminder Test' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).text
    print(message_text)
    time.sleep(REQUEST_WAIT_TIME)
    assert message_text == 'Reminder Created!'


# Tests instantiation of reminder is one week from day of creation
def test_next_reminder_date(driver: webdriver.Chrome):
    _days_abbr = ['m', 't', 'w', 'th', 'f', 's', 'su']

    # get next date and format
    next_date = dt.datetime.now() + dt.timedelta(days=7)
    formatted_date = next_date.strftime("%a %b %d")

    # get current day to set reminder
    current_date = dt.datetime.now()

    # set week_day
    week_day = _days_abbr[current_date.weekday()]

    # set hour
    hour = dt.datetime.now().hour

    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys(f'{BOT_PREFIX}!sr' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys(week_day + Keys.RETURN)

    time.sleep(REQUEST_WAIT_TIME)
    minute = dt.datetime.now().minute + 1
    str_time = str(hour) + ' ' + str(minute)

    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys(str_time + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('Set Reminder Test' + Keys.RETURN)
    time.sleep(LONG_COMMAND_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_FIELD_VALUE).text
    print(message_text)
    assert formatted_date in message_text


# Tests query execution
def test_database_utils_exec():
    statement = 'SELECT COUNT(*) FROM NOTES'
    result = database_utils.exec(statement)
    print(result, result[0])
    assert result[0][0] >= 0


# Tests sql database connectivity
def test_database_connection():
    assert database_utils.connection() != None


# SAIM'S TESTS:
def test_default_search(driver: webdriver.Chrome):
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(LOAD_WAIT_TIME)
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys(f'{BOT_PREFIX}!search banana' + Keys.RETURN)
    time.sleep(LOAD_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)

    message_text1 = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_BODY_CLASS).text
    message_text2 = messages[-2].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_BODY_CLASS).text
    message_text3 = messages[-3].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_BODY_CLASS).text
    message_text4 = messages[-4].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_BODY_CLASS).text
    message_text5 = messages[-5].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_BODY_CLASS).text

    assert 'banana' in message_text1.lower()
    assert 'banana' in message_text2.lower()
    assert 'banana' in message_text3.lower()
    assert 'banana' in message_text4.lower()
    assert 'banana' in message_text5.lower()


def test_search_site(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys(f'{BOT_PREFIX}!search-site' + Keys.RETURN)
    time.sleep(LOAD_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).text
    assert 'Which website do you want to search?' in message_text

    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('youtube.com' + Keys.RETURN)
    time.sleep(LOAD_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).text
    assert 'What do you want to find?' in message_text

    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('banana' + Keys.RETURN)
    time.sleep(LOAD_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)

    message_text1 = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).find_element_by_class_name(EMBED_LINKED_TITLE_CLASS).text
    message_text2 = messages[-2].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).find_element_by_class_name(EMBED_LINKED_TITLE_CLASS).text
    message_text3 = messages[-3].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).find_element_by_class_name(EMBED_LINKED_TITLE_CLASS).text
    message_text4 = messages[-4].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).find_element_by_class_name(EMBED_LINKED_TITLE_CLASS).text
    message_text5 = messages[-5].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).find_element_by_class_name(EMBED_LINKED_TITLE_CLASS).text

    assert 'banana' in message_text1.lower()
    assert 'banana' in message_text2.lower()
    assert 'banana' in message_text3.lower()
    assert 'banana' in message_text4.lower()
    assert 'banana' in message_text5.lower()


def test_big_search(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys(f'{BOT_PREFIX}!big-search banana' + Keys.RETURN)
    time.sleep(LOAD_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).find_element_by_class_name(EMBED_LINKED_TITLE_CLASS).get_attribute('href')
    assert 'https://letmegooglethat.com/?q=banana' in message_text.lower()


def test_eight_ball(driver: webdriver.Chrome):
    responses = [
        'It is certain.',
        'It is decidedly so.',
        'Without a doubt',
        'Yes - definetly',
        'You may rely on it.',
        'As I see it, yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',
        'Reply hazy, try again',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now',
        'Concentrate and ask again.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.'
    ]
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys(f'{BOT_PREFIX}!8-ball did this work' + Keys.RETURN)
    time.sleep(LOAD_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_FIELD_NAME_CLASS).text
    assert message_text in responses


def test_rock_paper_scissors(driver: webdriver.Chrome):
    valid_responses = [
        "Yay! you won.",
        "Oh no! you lost.",
        "Tied!"
    ]

    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys(f'{BOT_PREFIX}!rock-paper-scissors' + Keys.RETURN)
    time.sleep(LOAD_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).text
    assert message_text == "Choose rock paper or scissors!"

    time.sleep(LOAD_WAIT_TIME / 2)
    messages[-1].find_element_by_class_name(REACTION_CLASS).find_element_by_class_name(
        INDIVIDUAL_REACTION_CLASS).click()
    time.sleep(LOAD_WAIT_TIME / 2)

    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).text
    assert message_text in valid_responses


def test_guessing_game(driver: webdriver.Chrome):
    valid_responses = [
        "You gave up!",
        "You guessed wrong! Try again.",
        "Guess the number!",
    ]

    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys(f'{BOT_PREFIX}!guessing-game' + Keys.RETURN)
    time.sleep(LOAD_WAIT_TIME)

    flag = True
    while flag:
        messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
        message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
            EMBED_TITLE_CLASS).text

        if message_text == "Yay! you won.":
            assert message_text == "Yay! you won."
            flag = False
        elif message_text == "Oh no! you lost.":
            assert message_text == "Oh no! you lost."
            flag = False
        else:
            assert message_text in valid_responses

            time.sleep(LOAD_WAIT_TIME / 2)
            messages[-1].find_element_by_class_name(REACTION_CLASS).find_element_by_class_name(
                INDIVIDUAL_REACTION_CLASS).click()
            time.sleep(LOAD_WAIT_TIME)
