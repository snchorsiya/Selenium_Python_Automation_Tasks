import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture()
def step():
    chr_option=Options()
    chr_option.add_experimental_option("detach", True)
    driver=webdriver.Chrome(options=chr_option)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_product_price(step):
    driver=step
    url="https://www.jcpenney.com/"
    driver.get(url)
    title=driver.title
    print("title")
    deals_menu=driver.find_element(By.XPATH, "//div[@id='flyoutMenuBlock']//li[1]")
    ActionChains(driver).move_to_element(deals_menu).perform()

    deals_under_15=driver.find_element(By.XPATH, "//a[normalize-space()='$15 & Under']")
    deals_under_15.click()

    time.sleep(3)

    driver.execute_script("window.scrollBy(0,950)")

    time.sleep(5)

    products=driver.find_elements(By.XPATH, "//li[@class='pAB7b D2LxB gQ4Qt QLk4z false RQ2ya false false']")
    print(products)
    product_map_price={}

    for product in products:
        product_title=product.find_element(By.XPATH, ".//a[@data-automation-id='product-title']").text
        product_price=product.find_element(By.XPATH, ".//span[@class='DXCCO _2Bk5a wrap']']").text
        product_map_price[product_title]=product_price

    for product, price in product_map_price.item():
        if float(price.replace("$", "")) < 15.0:
            print(f"{product}-{price}")
