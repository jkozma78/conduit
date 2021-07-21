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
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver


elemek = ('//a[@href="#/register"]', '//input[@placeholder="Username"]')


def test_register(browser):
    browser.get('http://localhost:1667/#/')
    # browser.find_element_by_xpath('//a[@href="#/register"]').click()
    browser.find_element_by_xpath(elemek[0]).click()
    browser.find_element_by_xpath(elemek[1]).send_keys("Jani")
    browser.find_element_by_xpath('//input[@placeholder="Email"]').send_keys("jani@jani.com")
    browser.find_element_by_xpath('//input[@placeholder="Password"]').send_keys("Jani1234")
    browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]').click()
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='swal-button-container']"))).click()

    browser.find_element_by_xpath('//a[@active-class="active"]').click()


def test_login(browser):
    browser.find_element_by_xpath('//a[@href="#/login"]').click()
    browser.find_element_by_xpath('//input[@placeholder="Email"]').send_keys("jani@jani.com")
    browser.find_element_by_xpath('//input[@placeholder="Password"]').send_keys("Jani1234")
    browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]').click()
    assert WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='#/@Jani/']"))).text == "Jani"
    browser.find_element_by_xpath('//a[@active-class="active"]').click()
