import time

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random_generator import RandomData

"""xpath locators and used variables in locators dictionary"""
locators = {"register": '//a[@href="#/register"]',  # sing up link
            "username": '//input[@placeholder="Username"]',  # username input field
            "email": '//input[@placeholder="Email"]',  # email input field
            "password": '//input[@placeholder="Password"]',  # password input field
            "okbutton": '//button[@class="btn btn-lg btn-primary pull-xs-right"]',  # singn up, sing in button
            "submit": '//button[@type="submit"]',  # article ok button
            "modalbutton": "//div[@class='swal-button-container']",  # modal-ok-button
            "logout": '//a[@active-class="active"]',  # logout link
            "login": '//a[@href="#/login"]',  # login link
            "accept": '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]',
            # accept cookie button
            "edit": '//a[@class="btn btn-sm btn-outline-secondary"]',  # edit article button
            "pages": '//a[@class="page-link"]',  # page number button
            "new": '//a[@href="#/editor"]',  # new article button
            "delete": '//button[@class="btn btn-outline-danger btn-sm"]',  # delete article button
            "modal-text": '//div[@class="swal-title"]',  # modal text
            "rnduname": RandomData.uname(),  # random generated username
            "rndemail": RandomData.email(),  # random generated email
            "input_fields": ['(//input[@type="text"])[1]', '(//input[@ type="text"])[2]', '//textarea',
                             '//input[@placeholder="Enter tags"]']
            # new article input fields(title, about, article, tags)
            }


@pytest.fixture(scope='session')
def browser():
    """init webbrowser with selenium"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

# @pytest.fixture(scope='session')
# def browser():
#     driver = webdriver.Chrome()
#     driver.implicitly_wait(10)
#     return driver


def find_locators(browser, xpath):
    """find element by xpath from locations dictionary"""
    return browser.find_element_by_xpath(locators[xpath])


def wait_for_element(browser, xpath):
    """waiting for an xpath element to be visible"""
    return WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))


def test_login_with_empty_fields(browser):
    """try to login without email and password"""
    browser.get('http://localhost:1667/')
    find_locators(browser, "login").click()
    find_locators(browser, "okbutton").click()
    assert wait_for_element(browser, '//div[@class="swal-title"]').text == "Login failed!"


def test_register(browser):
    """a user registration"""
    browser.get('http://localhost:1667/')
    find_locators(browser, "register").click()
    find_locators(browser, "username").send_keys(locators['rnduname'])
    find_locators(browser, "email").send_keys(locators["rndemail"])
    find_locators(browser, "password").send_keys("Jani1234")
    find_locators(browser, "okbutton").click()
    wait_for_element(browser, locators["modalbutton"]).click()
    usern = locators['rnduname']
    assert browser.find_elements_by_xpath(f'//a[@href="#/@{usern}/"]')


def test_logout(browser):
    """logout after successful registration"""
    find_locators(browser, "logout").click()


def test_login(browser):
    """login with a registered user"""
    browser.get('http://localhost:1667/')
    find_locators(browser, "login").click()
    find_locators(browser, "email").send_keys(locators["rndemail"])
    find_locators(browser, "password").send_keys("Jani1234")
    find_locators(browser, "okbutton").click()
    usern = locators['rnduname']
    assert wait_for_element(browser, f'//a[@href="#/@{usern}/"]')


# @pytest.mark.skip(reason="no way of currently testing this")
def test_save_data(browser):
    """Save data from articles"""

    articles = browser.find_elements_by_xpath("//a[contains(@href, 'article')]")
    for i in range(0, len(articles)):
        articles2 = browser.find_elements_by_xpath("//a[contains(@href, 'article')]")

        articles2[i].click()
        time.sleep(1)
        with open("article.txt", "a") as articlefile:
            tetx = browser.find_element_by_tag_name('h1').text
            articlefile.write(f'{tetx} \n')
        browser.back()


def test_accept_cookies(browser):
    """accept cookies"""

    find_locators(browser, "accept").click()
    browser.refresh()
    try:
        find_locators(browser, "accept").click()
    except:
        print('Adatkezelés elfogadva')


def test_pagination(browser):
    """select last page and assert if it is 'page-item active' """

    wait_for_element(browser, '//a[@class="page-link"]')
    pages = browser.find_elements_by_xpath('//a[@class="page-link"]')
    pages[-1].click()

    assert int(browser.find_element_by_xpath('//li[@class="page-item active"]/a').get_property("text")) == len(pages)


def test_new_article(browser):
    find_locators(browser, "new").click()

    for i in locators["input_fields"]:
        browser.find_element_by_xpath(i).send_keys(RandomData.uname())
    find_locators(browser, "submit").click()


@pytest.mark.skip(reason="no way of currently testing this")
def test_new_article_from_file(browser):
    find_locators(browser, "new").click()

    with open("testdata.csv", "r") as csvfile:
        next(csvfile)
        for words in csvfile.readlines():
            split_words = words.split(',')
            find_locators(browser, "new").click()
            for i in range(len(locators["input_fields"])):
                time.sleep(5)
                browser.find_element_by_xpath(locators["input_fields"][i]).clear()
                browser.find_element_by_xpath(locators["input_fields"][i]).send_keys(split_words[i])
            find_locators(browser, "submit").click()
    csvfile.close()


def test_edit_article(browser):
    find_locators(browser, 'edit').click()
    wait_for_element(browser, '//textarea[@class="form-control"]')
    browser.find_element_by_xpath('//textarea[@class="form-control"]').send_keys("másvalami")
    find_locators(browser, 'submit').click()


def test_delete_article(browser):
    find_locators(browser, 'delete').click()
