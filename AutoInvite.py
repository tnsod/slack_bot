from dotenv import load_dotenv
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
    driver = None  # driver 초기화
    
    try:
        # undetected-chromedriver 전용 옵션 설정
        options = uc.ChromeOptions()
        
        # 기본 설정
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        # 봇 탐지 우회 (문제가 되는 옵션들 제거)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        # excludeSwitches와 useAutomationExtension 옵션 제거 (호환성 문제)
        
        # User-Agent 설정
        options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # undetected-chromedriver로 생성 (version_main=None으로 자동 감지)
        driver = uc.Chrome(options=options, version_main=None)
        
        # 수동으로 webdriver 속성 숨기기
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # stealth 적용 (선택사항, 문제 발생 시 주석 처리)
        try:
            stealth(driver,
                languages=["ko-KR", "ko", "en-US", "en"],
                vendor="Google Inc.",
                platform="Linux x86_64",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
        except Exception as stealth_error:
            print(f"Stealth 적용 실패 (무시하고 진행): {stealth_error}")
 
        driver.get('https://www.acmicpc.net/login?next=%2F')
        time.sleep(3)

        # 로그인
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

        time.sleep(2)
        print(f"✅ {boj_id} 초대 완료")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        if return_cnt >= 3:
            print("최대 재시도 횟수 초과")
            return False
        else:
            return_cnt += 1
            return invite(boj_id)
            
    finally:
        # driver가 None이 아닐 때만 quit() 호출
        if driver is not None:
            try:
                driver.quit()
            except Exception as quit_error:
                print(f"드라이버 종료 중 에러 (무시): {quit_error}")