import requests

response=requests.post('http://vaxraxd.tech/encrypt-data', {'data':'carl'})
print(response.text)