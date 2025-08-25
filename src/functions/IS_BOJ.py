import requests

def check_id(BOJ_id):
    url = f'https://solved.ac/api/v3/user/show?handle={BOJ_id}'
    response = requests.head(url, timeout=10)
    try:
        if response.status_code == 200:
            return True
                
        else:
            return check2(BOJ_id)
    except Exception as e:
        print(f'Failed : {e}')
        return check2(BOJ_id)

def check2(BOJ_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    url = f'https://www.acmicpc.net/user/{BOJ_id}'
    response = requests.head(url, headers=headers, timeout=10)
    try:
        if response.status_code == 200:
            return True

        else:
            print('error')
            return False
    except Exception as e:
        print(f'Failed2 : {e}')
        return False