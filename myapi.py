#Libraries for api
from fastapi import FastAPI,status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse,Response
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel
#Libraries for encryption & decryption
from cryptography.fernet import Fernet

#Code for encryption & decryption 
def dataEncryption(data):
    key=Fernet.generate_key()
    token=Fernet(key).encrypt(bytes(data,'utf-8'))
    return [token.decode('utf-8'),key.decode('utf-8')]

def dataDecrption(key,token):
    f=Fernet(bytes(key,'utf-8'))
    data=f.decrypt(bytes(token,'utf-8'))
    return data.decode('utf-8')

#Code for api
class Payload(BaseModel):
     key: str
     data: str

app=FastAPI(docs_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs")
def overridden_swagger():
	return get_swagger_ui_html(openapi_url="/openapi.json", title="SecureChatApi", swagger_favicon_url="/static/app.ico")

@app.get("/favicon.ico")
def favicon():
    return FileResponse('./static/app.ico')

@app.get("/")
def home():
    return Response(status_code=status.HTTP_200_OK)

@app.post("/encrypt-data")
def encryptPlayload(data : str):
     keydata=dataEncryption(data)
     crypto={'key':keydata[0],'data':keydata[1]}
     return crypto