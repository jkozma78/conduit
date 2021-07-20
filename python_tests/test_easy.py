from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest

@pytest.fixture(scope="session")
def browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get('http://localhost:1667/#/')
    return driver

def test_one(browser):
    browser.find_element_by_xpath('//a[@href="#/login"]').click()

    assert browser.find_element_by_tag_name('h1').text == 'Sign in'