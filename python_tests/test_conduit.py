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
    """a teszt során felhasznált xpath lokátorok egy locators dictionary-be rendezve"""
    locators = {"register": '//a[@href="#/register"]',
                "Username": '//input[@placeholder="Username"]',
                "Email": '//input[@placeholder="Email"]',
                "Password": '//input[@placeholder="Password"]',
                "Okbutton": '//button[@class="btn btn-lg btn-primary pull-xs-right"]',
                "Modalbutton": "//div[@class='swal-button-container']",
                "logout": '//a[@active-class="active"]',
                "login": '//a[@href="#/login"]',
                "accept": '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]'}
    return browser.find_element_by_xpath(locators[xpath])


def wait_for_element(browser, xpath):
    """waiting for an xpath element to be visible"""
    return WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))


def test_accept_cookies():
    """accept cookies"""
    find_locators(browser, "accept").click()


def test_register(browser):
    """a user registration"""
    browser.get('http://localhost:1667/#/')
    find_locators(browser, "register").click()
    find_locators(browser, "Username").send_keys("Jani")
    find_locators(browser, "Email").send_keys("jani@jani.com")
    find_locators(browser, "Password").send_keys("Jani1234")
    find_locators(browser, "Okbutton").click()
    wait_for_element(browser, "//div[@class='swal-button-container']").click()
    find_locators(browser, "logout").click()


def test_login(browser):
    """login with a registered user"""
    find_locators(browser, "login").click()
    find_locators(browser, "Email").send_keys("jani@jani.com")
    find_locators(browser, "Password").send_keys("Jani1234")
    find_locators(browser, "Okbutton").click()
    assert wait_for_element(browser, "//a[@href='#/@Jani/']").text == "Jani"
    find_locators(browser, "logout").click()
