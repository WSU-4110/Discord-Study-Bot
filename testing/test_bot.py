import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


DISCORD_EMAIL = 'gz0715@wayne.edu'
DISCORD_PASSWORD = 'f3MTSwYJW6hTVrG'
REQUEST_WAIT_TIME = 5
COMMAND_WAIT_TIME = 60

UNIT_TEST_CHANNEL_URL = 'https://discord.com/channels/801966497235730472/832302247277756447'#'https://discord.com/channels/801966497235730472/828825916573745185'
DM_CHANNEL_URL = 'https://discord.com/channels/@me/832084681670787073'

TEXT_INPUT_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div/div/div[3]/div[2]'
MESSAGE_CONTAINER_XPATH = '/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/div[1]/div/div/div'

TEXT_MESSAGE_CLASS = 'message-2qnXI6'
TEXT_MESSAGE_BODY_CLASS = 'markup-2BOw-j'

EMBED_MESSAGE_CLASS = 'grid-1nZz7S'
EMBED_TITLE_CLASS = 'embedTitle-3OXDkz'
EMBED_LINKED_TITLE_CLASS = 'anchor-3Z-8Bb'
EMBED_MESSAGE_BODY_CLASS = 'embedDescription-1Cuq9a'
EMBED_FIELD_NAME_CLASS = "embedFieldName-NFrena"

REACTION_CLASS = "reactions-12N0jA"
INDIVIDUAL_REACTION_CLASS = "reaction-1hd86g"


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()  # initiate a webdriver instance through Selenium
    driver.get('https://discord.com/app')  # go to Discord's login page
    # enter email
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[3]/div/div/form/div/div/div[1]/div[3]/div[1]/div/div[2]/input').send_keys(DISCORD_EMAIL)
    # enter password
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[3]/div/div/form/div/div/div[1]/div[3]/div[2]/div/input').send_keys(DISCORD_PASSWORD)
    # click login button
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[3]/div/div/form/div/div/div[1]/div[3]/button[2]').click()
    time.sleep(REQUEST_WAIT_TIME)  # wait for request to process
    driver.get(UNIT_TEST_CHANNEL_URL)
    time.sleep(REQUEST_WAIT_TIME)
    yield driver  # allow for tests to run
    driver.quit()  # teardown by quitting the webdriver instance


def test_default_search(driver: webdriver.Chrome):
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('sb!search banana' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
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
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('sb!search-site' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).text
    assert 'Which website do you want to search?' in message_text

    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('youtube.com' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).text
    assert 'What do you want to find?' in message_text

    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('banana' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
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
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('sb!big-search banana' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
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
    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('sb!8-ball did this work' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
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

    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('sb!rock-paper-scissors' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)
    messages = driver.find_element_by_xpath(MESSAGE_CONTAINER_XPATH).find_elements_by_class_name(TEXT_MESSAGE_CLASS)
    message_text = messages[-1].find_element_by_class_name(EMBED_MESSAGE_CLASS).find_element_by_class_name(
        EMBED_TITLE_CLASS).text
    assert message_text == "Choose rock paper or scissors!"

    time.sleep(REQUEST_WAIT_TIME/2)
    messages[-1].find_element_by_class_name(REACTION_CLASS).find_element_by_class_name(
        INDIVIDUAL_REACTION_CLASS).click()
    time.sleep(REQUEST_WAIT_TIME/2)

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

    driver.find_element_by_xpath(TEXT_INPUT_XPATH).send_keys('sb!guessing-game' + Keys.RETURN)
    time.sleep(REQUEST_WAIT_TIME)

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

            time.sleep(REQUEST_WAIT_TIME / 2)
            messages[-1].find_element_by_class_name(REACTION_CLASS).find_element_by_class_name(
                INDIVIDUAL_REACTION_CLASS).click()
            time.sleep(REQUEST_WAIT_TIME)
