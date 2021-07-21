
import pytest

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

 

 

@pytest.fixture(scope='session')

def browser():

    options = Options()

    options.add_argument('--headless')

    options.add_argument('--disable-gpu')  # Last I checked this was necessary.

    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)

    return driver

 

 

def find_locators(browser, xpath):

    """a teszt során felhasznált xpath lokátorok egy locators dictionary-be rendezve"""

    locators = {"register": '//a[@href="#/register"]', 

    "Username": '//input[@placeholder="Username"]',

    "Email":'//input[@placeholder="Email"',

    "Password":'//input[@placeholder="Password"]',

    "Okbutton":'//button[@class="btn btn-lg btn-primary pull-xs-right"]',

    "Modalbutton":"//div[@class='swal-button-container']",

    "logout":'//a[@active-class="active"]'}

    return browser.find_element_by_xpath(locators[xpath])

 

def wait_for_element(xpath):

    return WebDriverWait(browser, 10).until(

        EC.visibility_of_element_located((By.XPATH, xpath)))

 

 

def test_register(browser):

    browser.get('http://localhost:1667/#/')

    find_locators(browser, "register").click()

    find_locators(browser, "Username").send_keys("Jani")

    find_locators(browser, "Email").send_keys("jani@jani.com")

    find_locators(browser,"Email").send_keys("Jani1234")

    find_locators(browser,"Okbutton").click()

    #wait = WebDriverWait(browser, 10).until(

    #    EC.visibility_of_element_located((By.XPATH, "//div[@class='swal-button-container']")))

    wait_for_element("//div[@class='swal-button-container']").click()

    find_locators(browser, "logout").click()

 

 

def test_login(browser):

    browser.find_element_by_xpath('//a[@href="#/login"]').click()

    browser.find_element_by_xpath('//input[@placeholder="Email"]').send_keys("jani@jani.com")

    browser.find_element_by_xpath('//input[@placeholder="Password"]').send_keys("Jani1234")

    browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]').click()

    assert WebDriverWait(browser, 10).until(

        EC.visibility_of_element_located((By.XPATH, "//a[@href='#/@Jani/']"))).text == "Jani"

    browser.find_element_by_xpath('//a[@active-class="active"]').click()

