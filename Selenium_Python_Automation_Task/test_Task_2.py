import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def setup():
    chr_option = Options()
    chr_option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chr_option)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_product_search_using_contains(setup):
    driver = setup  # Assuming 'setup' initializes the WebDriver
    url = "https://www.amazon.in/"

    # Check if the current URL matches the target URL
    if driver.current_url != url:
        driver.get(url)  # Navigate to the target URL

    # Locate the Amazon search box and perform a search for "mobiles"
    amazon_search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
    assert amazon_search_box.is_displayed(), 'Failed: Amazon Search Box is not Present'
    amazon_search_box.click()
    amazon_search_box.send_keys("iphone")

    # Click on the search button
    amazon_search_btn = driver.find_element(By.ID, "nav-search-submit-button")
    amazon_search_btn.click()

    # Wait for the Amazon result page to load
    wait = WebDriverWait(driver, 30)
    verify_amazon_result_page = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='a-color-state a-text-bold']")))
    assert verify_amazon_result_page.is_displayed(), 'Failed: Searched Keyword is not present in Amazon result page'

    # Extract and process the list of mobiles
    mobile_list = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
    count = 0
    for item in mobile_list:
        item_name = item.text
        if "128" in item_name:
            count += 1
            assert item_name, "Product title is empty"
            print(item_name)

    print("Total count:", count)