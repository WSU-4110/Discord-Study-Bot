import asyncio
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

UNIT_TEST_CHANNEL_URL = 'https://discord.com/channels/801966497235730472/828825916573745185'
TEXT_INPUT_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div/div/div[3]/div[2]'
MESSAGE_CONTAINER_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/div[1]/div/div/div'
MESSAGE_CLASS = 'message-2qnXI6'

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()  # initiate a webdriver instance through Selenium
    driver.get('https://discord.com/app')  # go to Discord's login page
    # enter email
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[1]/div/div[2]/input').send_keys('go2977@wayne.edu')
    # enter password
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[2]/div/input').send_keys('alph@bet@123')
    # click login button
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]').click()
    time.sleep(5)  # wait for request to process
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(10)  # wait for request to process
    yield driver  # allow for tests to run
    driver.quit()  # teardown by quitting the webdriver instance


'''
@pytest.mark.asyncio
async def test_some_asyncio_code():
    async def func():
        return 2
    res = await func()
    assert res == 2
'''


def test_unit_test_channel(driver: webdriver.Chrome):
    text = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/div[1]/div/div/div/div[1]/h1').text
    assert text == 'Welcome to #unit-testing!'


def test_ping_command(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('lb!ping' + Keys.RETURN)
    time.sleep(5)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name('markup-2BOw-j').text
    assert message_text == 'pong!'
