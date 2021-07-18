from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def test_one():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get('http://localhost:1667')
    assert driver.title == 'Conduit'
