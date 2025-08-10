from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import pyperclip
import time
import os

load_dotenv()
BOJ_ID = os.getenv('BOJ_ID')
BOJ_PASSWORD = os.getenv('BOJ_PASSWORD')

return_cnt = 0
def invite(boj_id):
    global return_cnt
    try:
        driver = webdriver.Chrome()
        driver.get('https://www.acmicpc.net/login?next=%2F')
        time.sleep(3)

        id_box = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[2]/input')
        id_box.click()
        pyperclip.copy(BOJ_ID)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        time.sleep(1)

        password_box = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[3]/input')
        password_box.click()
        pyperclip.copy(BOJ_PASSWORD)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        actions.key_down(Keys.RETURN)
        time.sleep(1)

        login_box = driver.find_element(By.XPATH, '//*[@id="submit_button"]')
        login_box.click()
        time.sleep(3)

        driver.get('https://www.acmicpc.net/group/admin/member/24084')

        invite_box = driver.find_element(By.XPATH, '//*[@id="add-member-form"]/div/div/input')
        invite_box.click()
        invite_box.send_keys(boj_id)
        invite_box.send_keys(Keys.RETURN)

        driver.quit()
    except:
        if return_cnt == 3:
            driver.quit()
            exit()
        else:
            return_cnt += 1
            return (invite(boj_id))