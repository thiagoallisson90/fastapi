import requests

headers = {
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzU3NTM1NjY4fQ.aTEn7IqDzTqh8l5lmmZLky8A4C1y0NgpMvysuo0WWKM"
}

requisicao = requests.get('http://127.0.0.1:8000/auth/refresh', headers=headers)
print(requisicao.status_code)
print(requisicao.json())