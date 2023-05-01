#Libraries for api
from fastapi import FastAPI,UploadFile,status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse,Response
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum
import uvicorn
#Libraries for encryption & decryption
from cryptography.fernet import Fernet
import string,base64

#Code for encryption & decryption 
def dataEncryption(data):
    key=Fernet.generate_key()
    token=Fernet(key).encrypt(bytes(data,'utf-8'))
    return [token.decode('utf-8'),key.decode('utf-8')]

def dataDecryption(key,token):
    f=Fernet(bytes(key,'utf-8'))
    data=f.decrypt(bytes(token,'utf-8'))
    return data.decode('utf-8')

#Code for api
class Payload(BaseModel):
     key: str
     data: str

app=FastAPI(docs_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
handler=Mangum(app)

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
    crypto={'key':keydata[1],'data':keydata[0]}
    return crypto

@app.post("/decrypt-data")
def decrpytoPlayload(data:Payload):
    token=dataDecryption(data.key,data.data)
    crypto={'message':token}
    return crypto     

@app.post("/encrypt-img")
async def encryptImage(file: UploadFile):
    data=await file.read()
    data=base64.b64encode(data)
    byte=data.decode('utf-8')
    token=str()
    for char in byte:
        if char in string.ascii_letters:
            token+=string.ascii_letters[len(string.ascii_letters)-1-string.ascii_letters.index(char)]
        else:
            token+=char
    with open("token.txt", "w") as f:
        f.write(token)
    return FileResponse("token.txt", media_type="text/plain")

@app.post("/decrypt-img")
async def decryptImage(file: UploadFile):
    token= await file.read()
    token=token.decode('utf-8')
    byte=str()
    for char in token:
        if char in string.ascii_letters:
            byte+=string.ascii_letters[len(string.ascii_letters)-1-string.ascii_letters.index(char)]
        else:
            byte+=char
    byte=bytes(byte,'utf-8')
    img=open('store.png','wb')
    img.write(base64.b64decode((byte)))
    img.close()
    return FileResponse("store.png", media_type="image/jpeg")

if __name__ == '__main__':
    uvicorn.run(app, port=80, host='0.0.0.0')