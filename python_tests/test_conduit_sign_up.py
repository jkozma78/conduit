import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope='session')
def browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get("http://localhost:1667/")
    driver.implicitly_wait(10)
    return driver


def test_registration(browser):
    
    browser.find_element_by_xpath('//a[@href="#/register"]').click()
    browser.find_element_by_xpath('//input[@placeholder="Username"]').send_keys('Jani')
    browser.find_element_by_xpath('//input[@placeholder="Email"]').send_keys('jani@jani.hu')
    browser.find_element_by_xpath('//input[@placeholder="Password"]').send_keys('Jani.1234')
    browser.find_element_by_tag_name("button").click()

    splash = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="swal-text"]')))
    assert browser.find_element_by_xpath('//div[@class="swal-text"]').text == "Your registration was successful!"
    assert splash.text == "Email already taken."
    browser.find_element_by_xpath('//div[@class="swal-text"]').click()




def test_login(browser):
    browser.get('http://localhost:1667/')
    browser.find_element_by_xpath('//a[@href="#/login"]').click()
    browser.find_element_by_xpath('//input[@placeholder="Email"]').send_keys('jani@jani.hu')
    browser.find_element_by_xpath('//input[@placeholder="Password"]').send_keys('Jani.12346')
    browser.find_element_by_tag_name("button").click()
