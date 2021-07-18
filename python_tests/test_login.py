import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope='session')
def browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(10)
    driver.get('http://localhost:1667')
    time.sleep(10)
    return driver


def test_login(browser):
    assert browser.title == 'Conduit'
    browser.find_element_by_xpath('//*[@href="#/login"]').click()


if __name__ == "__main__":
    test_login()
