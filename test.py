import requests

response=requests.post('http://vaxraxd.tech/encrypt-data', json={'data':'carl'})
print(response.text)