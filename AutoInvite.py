from dotenv import load_dotenv
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import os

load_dotenv()
BOJ_ID = os.getenv('BOJ_ID')
BOJ_PASSWORD = os.getenv('BOJ_PASSWORD')

def invite(boj_id):
    driver = None
    try:
        options = uc.ChromeOptions()
        
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--single-process")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")

        options.add_argument("--memory-pressure-off")
        options.add_argument("--max_old_space_size=4096")
        
        driver = uc.Chrome(
            options=options, 
            version_main=None,
            driver_executable_path=None
        )
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ 드라이버 생성 성공")
        
        # 로그인 과정
        driver.get('https://www.acmicpc.net/login?next=%2F')
        time.sleep(5)  # Amazon Linux에서는 더 긴 대기 시간 필요
        
        # 로그인
        wait = WebDriverWait(driver, 20)
        
        id_box = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_form"]/div[2]/input')))
        id_box.click()
        id_box.send_keys(BOJ_ID)
        time.sleep(2)
        
        password_box = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[3]/input')
        password_box.click()
        password_box.send_keys(BOJ_PASSWORD)
        time.sleep(2)
        
        login_button = driver.find_element(By.XPATH, '//*[@id="submit_button"]')
        login_button.click()
        time.sleep(5)
        
        # 그룹 페이지 이동
        driver.get('https://www.acmicpc.net/group/admin/member/24084')
        time.sleep(5)
        
        # 여러 방법으로 초대 입력란 찾기
        invite_selectors = [
            '//*[@id="add-member-form"]/div/div/input',
            '//input[contains(@placeholder, "사용자")]',
            '//input[contains(@name, "member")]',
            'input[type="text"]'
        ]
        
        invite_box = None
        for selector in invite_selectors:
            try:
                if selector.startswith('//') or selector.startswith('//*'):
                    invite_box = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                else:
                    invite_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                print(f"✅ 초대 입력란 발견: {selector}")
                break
            except:
                continue
        
        if not invite_box:
            raise Exception("초대 입력란을 찾을 수 없습니다")
        
        invite_box.clear()
        invite_box.send_keys(boj_id)
        invite_box.send_keys(Keys.RETURN)
        time.sleep(3)
        
        print(f"✅ {boj_id} 초대 완료")
        return True
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return False
        
    finally:
        if driver:
            try:
                driver.quit()
                print("드라이버 종료 완료")
            except:
                pass