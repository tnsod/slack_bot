from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        print(f"BOJ ID {boj_id} 초대 프로세스 시작...")
        
        chrome_options = Options()
        
        # headless
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        
        # 창 및 디스플레이 설정
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-web-security")
        
        # DevToolsActivePort 에러 해결
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        
        # User-Agent 설정
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        service = Service('/usr/bin/chromedriver')
        
        print("Chrome 드라이버 초기화 중...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 페이지 로드 타임아웃 설정
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        
        print("BOJ 로그인 페이지 접속 중...")
        driver.get('https://www.acmicpc.net/login?next=%2F')
        time.sleep(3)
        
        wait = WebDriverWait(driver, 15)
        
        print("로그인 정보 입력 중...")
        # ID 입력
        id_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login_form"]/div[2]/input')))
        id_box.clear()
        id_box.send_keys(BOJ_ID)
        time.sleep(1)
        
        # 비밀번호 입력
        password_box = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[3]/input')
        password_box.clear()
        password_box.send_keys(BOJ_PASSWORD)
        time.sleep(1)
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit_button"]')))
        login_button.click()
        
        print("로그인 처리 대기 중...")
        time.sleep(5)
        
        # 그룹 관리 페이지로 이동
        print("그룹 관리 페이지로 이동 중...")
        driver.get('https://www.acmicpc.net/group/admin/member/24084')
        time.sleep(3)
        
        # 초대 입력란 대기 및 입력
        print(f"사용자 {boj_id} 초대 중...")
        invite_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="add-member-form"]/div/div/input')))
        if invite_box:
            print("입력칸 찾음")
        invite_box.clear()
        invite_box.send_keys(boj_id)
        invite_box.send_keys(Keys.RETURN)
        
        print("초대 완료!")
        time.sleep(2)
        
        return "성공"
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        
        if return_cnt >= 3:
            print("최대 재시도 횟수 초과")
            return "실패"
        else:
            return_cnt += 1
            print(f"재시도 {return_cnt}/3 시작...")
            time.sleep(5)  # 재시도 전 충분한 대기
            return invite(boj_id)
            
    finally:
        if driver is not None:
            try:
                driver.quit()
                print("Chrome 드라이버 정상 종료")
            except:
                print("Chrome 드라이버 종료 중 오류 (무시됨)")