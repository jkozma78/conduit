import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope='session')
def browser():
    """init webbrowser with selenium"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver


def find_locators(browser, xpath):
    """xpath locators in locators dictionary"""
    locators = {"register": '//a[@href="#/register"]',
                "username": '//input[@placeholder="Username"]',
                "email": '//input[@placeholder="Email"]',
                "password": '//input[@placeholder="Password"]',
                "okbutton": '//button[@class="btn btn-lg btn-primary pull-xs-right"]',
                "modalbutton": "//div[@class='swal-button-container']",
                "logout": '//a[@active-class="active"]',
                "login": '//a[@href="#/login"]',
                "accept": '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]',
                "pages": '//a[@class="page-link"]'}

    return browser.find_element_by_xpath(locators[xpath])


def wait_for_element(browser, xpath):
    """waiting for an xpath element to be visible"""
    return WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))


@pytest.mark.skip(reason="no way of currently testing this")
def test_register(browser):
    """a user registration"""
    browser.get('http://localhost:1667/')
    find_locators(browser, "register").click()
    find_locators(browser, "username").send_keys("Jani")
    find_locators(browser, "email").send_keys("jani@jani.com")
    find_locators(browser, "password").send_keys("Jani1234")
    find_locators(browser, "okbutton").click()
    wait_for_element(browser, "//div[@class='swal-button-container']").click()
    find_locators(browser, "logout").click()


def test_login(browser):
    """login with a registered user"""
    browser.get('http://localhost:1667/')
    find_locators(browser, "login").click()
    find_locators(browser, "email").send_keys("jani@jani.com")
    find_locators(browser, "password").send_keys("Jani1234")
    find_locators(browser, "okbutton").click()
    assert wait_for_element(browser, "//a[@href='#/@Jani/']").text == "Jani"
    find_locators(browser, "logout").click()


def test_accept_cookies(browser):
    """accept cookies"""
    browser.get('http://localhost:1667/#/')
    find_locators(browser, "accept").click()


def test_pagination(browser):
    """select last page and assert if it is 'page-item active' """
    test_login(browser)
    pages = browser.find_elements_by_xpath('//a[@class="page-link"]')
    pages[-1].click()
    assert int(browser.find_element_by_xpath('//li[@class="page-item active"]/a').get_property("text")) == len(pages)
