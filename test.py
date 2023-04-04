import requests
BASE_URL = 'http://127.0.0.1:8080'
response = requests.put(f"{BASE_URL}//api/v2/news/1")
print(response.json())