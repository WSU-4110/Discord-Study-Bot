import time
import datetime as dt

import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from utils.time_utils import curr_est_offset, orig_to_utc, utc_to_dest

DISCORD_EMAIL = 'natric90@gmail.com'
DISCORD_PASSWORD = 'iLoveRexy21!!'
REQUEST_WAIT_TIME = 5
COMMAND_WAIT_TIME = 60

UNIT_TEST_CHANNEL_URL = 'https://discord.com/channels/801966497235730472/828825916573745185'
DM_CHANNEL_URL = 'https://discord.com/channels/@me/832101393649238036'

TEXT_INPUT_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div/div/div[3]/div[2]'
MESSAGE_CONTAINER_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/div[1]/div/div/div'

TEXT_MESSAGE_CLASS = 'message-2qnXI6'
TEXT_MESSAGE_BODY_CLASS = 'markup-2BOw-j'

EMBED_MESSAGE_CLASS = 'grid-1nZz7S'
EMBED_MESSAGE_BODY_CLASS = 'embedDescription-1Cuq9a'
EMBED_MESSAGE_TITLE_CLASS = 'embedTitle-3OXDkz'


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()  # initiating a webdriver instance through Selenium
    driver.get('https://discord.com/app')  # Discord's log in page

    driver.find_element_by_xpath(
        '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[1]/div/div[2]/input').send_keys(
        DISCORD_EMAIL)  # Email field

    driver.find_element_by_xpath(
        '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[2]/div/input').send_keys(
        DISCORD_PASSWORD)  # Password field

    driver.find_element_by_xpath(
        '/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]').click()  # click log in button
    time.sleep(REQUEST_WAIT_TIME)  # waiting for request to process
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(REQUEST_WAIT_TIME)
    yield driver  # allowing for tests to run
    driver.quit()  # tearing down by quitting the webdriver instance


def test_create_note(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('na!create-note test1' + Keys.RETURN)  # creating the note using command
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_TITLE_CLASS).text
    assert message_text == 'Note Created!'  # checking if it matches


def test_list_notes(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('na!list-notes' + Keys.RETURN)  # listing notes command
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_TITLE_CLASS).text
    assert message_text == 'Notes'  # checking if it matches


def test_delete_note(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('na!delete-note' + Keys.RETURN)  # creating the note using command
    time.sleep(REQUEST_WAIT_TIME)
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('1' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_MESSAGE_TITLE_CLASS).text
    assert message_text == 'Note Deleted!'  # checking if it matches


def test_curr_est_offset():
    curr_est_offset()  # calling method
    assert -4  # checking if it matches


def test_orig_to_utc():
    a_time = dt.datetime.now()
    a_time_2 = orig_to_utc(a_time)
    assert a_time_2 == dt.datetime.utcnow()  # checking if it matches


def test_utc_to_dest():
    a_time = dt.datetime.now()
    a_time_2 = orig_to_utc(a_time)
    assert utc_to_dest(a_time_2, 'EST') == a_time  # checking if it matches
