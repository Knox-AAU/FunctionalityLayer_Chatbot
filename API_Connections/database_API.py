import request

response = requests.get('http://localhost:8000/get', verify=False) #only works if you are connected to server: ssh <studiemail>@knox-kb01.srv.aau.dk -L 8000:localhost:8081.
print(response.status_code)
print(response.json())
