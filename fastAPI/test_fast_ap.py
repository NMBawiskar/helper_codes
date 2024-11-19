from fastapi import FastAPI, File, UploadFile
import os


from threading import Thread
import requests
from requests.auth import HTTPProxyAuth, HTTPDigestAuth, HTTPBasicAuth
import uvicorn


app = FastAPI()

UPLOAD_IMG_DIR_PATH = "uploadedImages"



@app.post("/testEndPoint/")
async def create_upload_file():
    #################################### Image 1 ################################################
    print("Received API call.")   
    # fileNameUploaded1 = file.filename
    # contents = await file.read()     
    # npimg1 = np.fromstring(contents, np.uint8)
    # # convert numpy array to image
   

    # if os.path.exists(resultFilePath):
    return {"Status":"Upload Successful","test": 'test'}
    # else:
    #     return {"Status":"Failed","filename":None}

if __name__ == "__main__":
    
    uvicorn.run("test_fast_ap:app", host="0.0.0.0", port=8000, reload=True)


