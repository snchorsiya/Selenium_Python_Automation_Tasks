import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture()
def setup():
    chr_option = Options()
    chr_option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chr_option)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_amazonSearch(setup):
    driver = setup
    url = "https://www.amazon.in/"
    driver.get(url)

    amazonSearchBox = driver.find_element(By.ID, 'twotabsearchtextbox')
    assert amazonSearchBox.is_displayed(), 'Failed: Amazon Search Box is not Present'
    amazonSearchBox.click()
    amazonSearchBox.send_keys("mobiles")
    amazonSearchBtn = driver.find_element(By.ID, 'nav-search-submit-button')
    amazonSearchBtn.click()
    wait = WebDriverWait(driver, 30)
    verifyAmazonResultPage = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='a-color-state "
                                                                                    "a-text-bold']")))
    # verifyAmazonResultPage = driver.find_element(By.XPATH, "//span[@class='a-color-state a-text-bold']")
    assert verifyAmazonResultPage.is_displayed(), 'Failed: Searched Keyword is not present in Amazon result page'
    mobile_list = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")

    for i in range(min(5, len(mobile_list))):
        list_item = mobile_list[i].text
        assert list_item, "Product list is empty"
        print("Product Title:", list_item)


