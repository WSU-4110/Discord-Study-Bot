import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


DISCORD_EMAIL = 'go2977@wayne.edu'
DISCORD_PASSWORD = 'alph@bet@123'
REQUEST_WAIT_TIME = 10
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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()  # initiate a webdriver instance through Selenium
    driver.get('https://discord.com/app')  # go to Discord's login page
    # enter email
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[1]/div/div[2]/input').send_keys(DISCORD_EMAIL)
    # enter password
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[2]/div/input').send_keys(DISCORD_PASSWORD)
    # click login button
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]').click()
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
    time.sleep(REQUEST_WAIT_TIME)
    print(driver.current_url)
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('lb!ping' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(TEXT_MESSAGE_BODY_CLASS).text
    assert message_text == 'pong!'


def test_create_todo(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('lb!create-item 1 test' + Keys.RETURN)
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

