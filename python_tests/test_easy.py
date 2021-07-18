from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def test_one():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get('http://localhost:1667/#/')
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]')))
    # driver.find_element_by_xpath('//a[@href="#/login"]').click()
    element.click()
    assert driver.find_element_by_tag_name('h1').text == 'Sign in'