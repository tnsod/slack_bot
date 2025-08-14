from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import undetected_chromedriver as uc
import time
import os

load_dotenv()
BOJ_ID = os.getenv('BOJ_ID')
BOJ_PASSWORD = os.getenv('BOJ_PASSWORD')

return_cnt = 0
def invite(boj_id):
    global return_cnt
    driver = None
    try:
        options = webdriver.ChromeOptions()
        
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        driver = uc.Chrome(options=options)
        
        stealth(driver,
            languages=["ko-KR", "ko", "en-US", "en"],
            vendor="Google Inc.",
            platform="Linux x86_64",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver.get('https://www.acmicpc.net/login?next=%2F')
        time.sleep(3)

        id_box = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[2]/input')
        id_box.click()
        id_box.send_keys(BOJ_ID)
        time.sleep(1)

        password_box = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[3]/input')
        password_box.click()
        password_box.send_keys(BOJ_PASSWORD)
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