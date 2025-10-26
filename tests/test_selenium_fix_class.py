from selenium import webdriver

def test_homepage_chrome():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000/")
    assert "Welcome" in driver.page_source
    driver.quit()

def test_homepage_firefox():
    driver = webdriver.Firefox()
    driver.get("http://127.0.0.1:5000/")
    assert "Welcome" in driver.page_source
    driver.quit()
