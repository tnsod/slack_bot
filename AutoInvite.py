from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import os

load_dotenv()
BOJ_ID = os.getenv('BOJ_ID')
BOJ_PASSWORD = os.getenv('BOJ_PASSWORD')

return_cnt = 0

def human_delay(min_delay=2, max_delay=5):
    """인간적인 랜덤 대기 시간"""
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

def setup_stealth_chrome():
    """reCAPTCHA 탐지를 최대한 회피하는 Chrome 설정"""
    chrome_options = Options()
    
    # === 필수 EC2 옵션들 ===
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # === 봇 탐지 방지 핵심 옵션들 ===
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # === 자연스러운 브라우저 환경 시뮬레이션 ===
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")  # 이미지 로드 비활성화로 속도 향상
    chrome_options.add_argument("--disable-javascript")  # reCAPTCHA 스크립트 차단
    
    # === 메모리 및 성능 최적화 ===
    chrome_options.add_argument("--memory-pressure-off")
    chrome_options.add_argument("--max_old_space_size=4096")
    
    # === 자연스러운 창 크기 (일반적인 해상도) ===
    chrome_options.add_argument("--window-size=1366,768")
    
    # === 봇 방지 추가 옵션들 ===
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    
    # === 자연스러운 User-Agent (일반 사용자) ===
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # === 언어 및 지역 설정 ===
    chrome_options.add_argument("--lang=ko-KR")
    chrome_options.add_experimental_option('prefs', {
        'intl.accept_languages': 'ko-KR,ko,en-US,en'
    })
    
    return chrome_options

def setup_driver_stealth(driver):
    """WebDriver 속성을 숨겨서 봇 탐지 회피"""
    # navigator.webdriver 속성 제거
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # Chrome 자동화 관련 속성 숨김
    driver.execute_script("""
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
    """)
    
    # 자연스러운 화면 해상도 설정
    driver.execute_script("""
        Object.defineProperty(screen, 'width', {get: () => 1366});
        Object.defineProperty(screen, 'height', {get: () => 768});
    """)

def human_typing(element, text, typing_speed=0.1):
    """인간적인 타이핑 시뮬레이션"""
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, typing_speed))

def invite(boj_id):
    global return_cnt
    driver = None
    
    try:
        print(f"BOJ ID {boj_id} 초대 프로세스 시작...")
        
        # reCAPTCHA 방지 Chrome 옵션 설정
        chrome_options = setup_stealth_chrome()
        service = Service('/usr/bin/chromedriver')
        
        print("Chrome 드라이버 초기화 중...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 브라우저 Stealth 설정 적용
        setup_driver_stealth(driver)
        
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        
        # === 자연스러운 브라우징 패턴 시뮬레이션 ===
        
        # 1단계: 메인 페이지 방문 (일반 사용자처럼)
        print("BOJ 메인 페이지 방문 중...")
        driver.get('https://www.acmicpc.net/')
        human_delay(3, 6)
        
        # 스크롤 동작으로 자연스러움 연출
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        human_delay(1, 2)
        driver.execute_script("window.scrollTo(0, 0);")
        human_delay(1, 2)
        
        # 2단계: 로그인 페이지로 이동
        print("로그인 페이지로 이동 중...")
        driver.get('https://www.acmicpc.net/login')
        human_delay(3, 5)
        
        wait = WebDriverWait(driver, 20)
        
        print("로그인 정보 입력 중...")
        
        # ID 입력 (자연스러운 타이핑)
        try:
            id_box = wait.until(EC.element_to_be_clickable((By.NAME, "login_user_id")))
        except:
            id_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login_form"]/div[2]/input')))
        
        # 클릭 전 마우스 이동 시뮬레이션
        driver.execute_script("arguments[0].focus();", id_box)
        human_delay(0.5, 1)
        
        human_typing(id_box, BOJ_ID, 0.15)  # 인간적인 타이핑 속도
        human_delay(1, 2)
        
        # 비밀번호 입력
        try:
            password_box = driver.find_element(By.NAME, "login_password")
        except:
            password_box = driver.find_element(By.XPATH, '//*[@id="login_form"]/div[3]/input')
        
        driver.execute_script("arguments[0].focus();", password_box)
        human_delay(0.5, 1)
        
        human_typing(password_box, BOJ_PASSWORD, 0.12)
        human_delay(2, 3)
        
        # 로그인 버튼 클릭 (자연스러운 클릭)
        try:
            login_button = driver.find_element(By.CLASS_NAME, "btn-primary")
        except:
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit_button"]')))
        
        # 마우스 이동 시뮬레이션
        driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
        human_delay(0.5, 1)
        login_button.click()
        
        print("로그인 처리 중...")
        human_delay(5, 8)  # 충분한 대기 시간
        
        # 로그인 성공 확인
        current_url = driver.current_url
        print(f"현재 URL: {current_url}")
        
        # if "login" in current_url or "signin" in current_url:
        #     print("❌ 로그인 실패 - reCAPTCHA 또는 자격증명 문제")
        #     return "로그인 실패"
        
        # print("✅ 로그인 성공!")
        
        # 그룹 관리 페이지로 이동
        print("그룹 관리 페이지로 이동 중...")
        driver.get('https://www.acmicpc.net/group/admin/member/24084')
        print(driver.current_url)
        human_delay(4, 7)
        
        # 페이지 접근 권한 확인
        page_title = driver.title
        print(f"페이지 제목: {page_title}")
        
        if "Forbidden" in page_title or "403" in page_title or "접근" in page_title:
            print("❌ 그룹 관리 권한이 없습니다.")
            return "권한 없음"
        
        # 초대 기능 실행
        print(f"사용자 {boj_id} 초대 중...")
        
        # 여러 XPATH 옵션 시도
        xpath_options = [
            '//*[@id="add-member-form"]/div/div/input',
            '//input[@placeholder="사용자명"]',
            '//input[contains(@name, "username")]',
            '//form[@id="add-member-form"]//input[@type="text"]',
            '//div[@class="form-group"]//input'
        ]
        
        invite_box = None
        for xpath in xpath_options:
            try:
                invite_box = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                break
            except:
                continue
        
        if invite_box is None:
            raise Exception("초대 입력란을 찾을 수 없습니다.")
        
        # 자연스러운 입력
        driver.execute_script("arguments[0].focus();", invite_box)
        human_delay(1, 2)
        
        human_typing(invite_box, boj_id, 0.1)
        human_delay(1, 2)
        
        invite_box.send_keys(Keys.RETURN)
        
        print("초대 완료!")
        human_delay(3, 5)
        
        return "성공"
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        
        if driver:
            try:
                print(f"현재 URL: {driver.current_url}")
                print(f"페이지 제목: {driver.title}")
                
                # reCAPTCHA 탐지
                page_source = driver.page_source.lower()
                if "recaptcha" in page_source or "captcha" in page_source:
                    print("🤖 reCAPTCHA 탐지됨!")
                    
            except:
                pass
        
        if return_cnt >= 3:
            print("최대 재시도 횟수 초과")
            return "실패"
        else:
            return_cnt += 1
            print(f"재시도 {return_cnt}/3 (더 긴 대기 후)")
            # 재시도 시 더 긴 대기 (IP 쿨다운)
            time.sleep(random.uniform(30, 60))
            return invite(boj_id)
            
    finally:
        if driver is not None:
            try:
                driver.quit()
                print("Chrome 드라이버 정상 종료")
            except:
                print("Chrome 드라이버 종료 중 오류 (무시됨)")