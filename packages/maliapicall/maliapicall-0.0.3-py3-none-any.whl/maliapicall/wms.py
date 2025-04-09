import requests


def get_token(auth_url: str, user_name: str, user_password: str) -> str:
    """
    Get the access token through login authentication.
    """        
    proxies = {"http": None, "https": None}
    params = {'username': user_name, 'password': user_password, 'applicationId':1}
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Authorization":'Basic bWFsbGVlLXNhYXMtdWFjOm1hbGlTb2FDbGllbnRTZWNyZXQ=',
        'Content-Length':'0',
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9,en;q=0.8'
        }
    query = requests.post(auth_url, params = params, headers = headers, proxies=proxies)
    return query.json()['result']['access_token']
