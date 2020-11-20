from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

options = webdriver.ChromeOptions()
# options.add_argument("headless")
chrome = webdriver.Chrome(executable_path="drivers/chromedriver.exe", options=options)
chrome.get("https://facebook.com")
try:
    WebDriverWait(chrome, 100).until(expected_conditions.element_to_be_clickable((By.ID, "email")))
    chrome.find_element_by_id("email").send_keys("hieutm123")
    WebDriverWait(chrome, 100).until(expected_conditions.element_to_be_clickable((By.ID, "pass")))
    chrome.find_element_by_id("pass").send_keys("vuivetrekhoe")
    WebDriverWait(chrome, 100).until(expected_conditions.element_to_be_clickable((By.ID, "u_0_b")))
    chrome.find_element_by_id("u_0_b").click()
    time.sleep(3)
except Exception:
    print(Exception)