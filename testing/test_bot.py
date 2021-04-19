import datetime
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
from utils import database_utils

load_dotenv()
DISCORD_EMAIL = os.getenv("TEST_EMAIL")
DISCORD_PASSWORD = os.getenv("TEST_PASSWORD")
REQUEST_WAIT_TIME = 5
COMMAND_WAIT_TIME = 70

UNIT_TEST_CHANNEL_URL = 'https://discord.com/channels/@me/832128070194036736'  # 'https://discord.com/channels/801966497235730472/828825916573745185'
# DM_CHANNEL_URL = 'https://discord.com/channels/@me/832084348760752159'  # CHANGE

DM_TEXT_INPUT_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div[3]/div[2]/div'  # '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div[3]/div[2]/div'

# TEXT_INPUT_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div/div/div[3]/div[2]'
MESSAGE_CONTAINER_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/div[1]/div/div/div'

TEXT_MESSAGE_CLASS = 'message-2qnXI6'
TEXT_MESSAGE_BODY_CLASS = 'markup-2BOw-j'

EMBED_MESSAGE_CLASS = 'grid-1nZz7S'  # original'grid-1nZz7S'
EMBED_MESSAGE_BODY_CLASS = 'embedDescription-1Cuq9a'
EMBED_TITLE_CLASS = 'embedTitle-3OXDkz'
EMBED_FIELD_VALUE = 'embedFieldValue-nELq2s'


@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
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

'''
# Tests command and creation of one-time repeated reminders
def test_create_reminder(driver: webdriver.Chrome):
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('b!sr' + Keys.RETURN)
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
'''

'''
# Tests command and creation of user defined number of repeated reminders
def test_create_repeating_reminder(driver: webdriver.Chrome):
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('b!srr' + Keys.RETURN)
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
'''

'''
# Tests command and creation of infinite repeated reminders
def test_create_infinite_reminder(driver: webdriver.Chrome):
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('b!sir' + Keys.RETURN)
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
'''


# Tests instantiation of reminder is one week from day of creation
def test_next_reminder_date(driver: webdriver.Chrome):
    _days_abbr = ['m', 't', 'w', 'th', 'f', 's', 'su']

    # get next date and format
    next_date = datetime.datetime.now() + datetime.timedelta(days=6)
    formatted_date = next_date.strftime("%a %b %d")

    # get current day to set reminder
    current_date = datetime.datetime.now()

    # set week_day
    week_day = _days_abbr[current_date.weekday()]

    # set hour
    hour = datetime.datetime.now().hour

    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('b!sr' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys(week_day + Keys.RETURN)

    time.sleep(REQUEST_WAIT_TIME)
    minute = datetime.datetime.now().minute + 1
    str_time = str(hour) + ' ' + str(minute)

    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys(str_time + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(DM_TEXT_INPUT_XPATH).send_keys('Set Reminder Test' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    time.sleep(COMMAND_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_FIELD_VALUE).text
    print(message_text)
    assert formatted_date in message_text


'''
# Tests query execution
def test_database_utils_exec():
    statement = 'SELECT COUNT(*) FROM NOTES'
    result = database_utils.exec(statement)
    print(result, result[0])
    assert result[0][0] > 0


# Tests sql database connectivity
def test_database_connection():
    assert database_utils.connection() != None
'''
