from dotenv import load_dotenv
from selenium import webdriver
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
        
        # Chrome 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=0")
        
        # ChromeDriver 서비스 설정
        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("BOJ 로그인 페이지 접속 중...")
        driver.get('https://www.acmicpc.net/login?next=%2F')
        
        # 명시적 대기 사용 (time.sleep 대신)
        wait = WebDriverWait(driver, 10)
        
        # ID 입력 (pyperclip 대신 직접 입력)
        print("로그인 정보 입력 중...")
        id_box = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_form"]/div[2]/input')))
        id_box.clear()
        id_box.send_keys(BOJ_ID)
        
        # 비밀번호 입력
        password_box = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[3]/input')
        password_box.clear()
        password_box.send_keys(BOJ_PASSWORD)
        
        # 로그인 버튼 클릭
        login_button = driver.find_element(By.XPATH, '//*[@id="submit_button"]')
        login_button.click()
        
        print("로그인 완료, 그룹 관리 페이지로 이동 중...")
        time.sleep(3)  # 로그인 처리 대기
        
        # 그룹 관리 페이지로 이동
        driver.get('https://www.acmicpc.net/group/admin/member/24084')
        
        # 초대 입력란에 사용자 ID 입력
        print(f"사용자 {boj_id} 초대 중...")
        invite_box = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="add-member-form"]/div/div/input')))
        invite_box.clear()
        invite_box.send_keys(boj_id)
        invite_box.submit()  # Enter 키 대신 submit 사용
        
        print("초대 완료!")
        return "성공"
        
    except Exception as e:
        print(f"오류 발생: {e}")
        
        if return_cnt >= 3:
            print("최대 재시도 횟수 초과")
            return "실패"
        else:
            return_cnt += 1
            print(f"재시도 {return_cnt}/3")
            time.sleep(2)  # 재시도 전 잠시 대기
            return invite(boj_id)
            
    finally:
        if driver is not None:
            driver.quit()
            print("Chrome 드라이버 종료")
