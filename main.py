import random

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    driver.quit()


def test_purchase_of_good(driver):
    driver.get('https://www.saucedemo.com')

    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, 'user-name')))
    username_field = driver.find_element(value='user-name')
    username_field.send_keys('standard_user')
    password_field = driver.find_element(value='password')
    password_field.send_keys('secret_sauce')
    login_button = driver.find_element(value='login-button')
    login_button.click()

    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
        (By.XPATH, '//button[contains(text(), "Add to cart")]')))
    cart_buttons = driver.find_elements(by=By.XPATH, value='//button[contains(text(), "Add to cart")]')
    random.choices(cart_buttons)[0].click()

    assert driver.find_element(by=By.CLASS_NAME, value='shopping_cart_badge').text == '1'

    cart_link = driver.find_element(by=By.CLASS_NAME, value='shopping_cart_link')
    cart_link.click()

    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, 'continue-shopping')))
    assert driver.find_element(by=By.CLASS_NAME, value='cart_item')

    checkout_button = driver.find_element(value='checkout')
    checkout_button.click()

    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, 'cancel')))
    first_name = driver.find_element(value='first-name')
    first_name.send_keys('first-name')
    last_name = driver.find_element(value='last-name')
    last_name.send_keys('last-name')
    postal_code = driver.find_element(value='postal-code')
    postal_code.send_keys('postal-code')

    continue_ = driver.find_element(value='continue')
    continue_.click()

    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, 'finish')))
    finish = driver.find_element(value='finish')
    finish.click()

    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'title')))
    complete = driver.find_element(by=By.CLASS_NAME, value='title')
    assert 'Complete!' in complete.text
