from fastapi import FastAPI, File, UploadFile
import os
import cv2
import numpy as np

from threading import Thread
import time

from threading import Thread
import requests
from requests.auth import HTTPProxyAuth, HTTPDigestAuth, HTTPBasicAuth
import uvicorn
import numpy as np

app = FastAPI()

UPLOAD_IMG_DIR_PATH = "uploadedImages"



@app.post("/uploadImage/")
async def create_upload_file(file: UploadFile):
    #################################### Image 1 ################################################
    print("Received API call.")   
    fileNameUploaded1 = file.filename
    contents = await file.read()     
    npimg1 = np.fromstring(contents, np.uint8)
    # convert numpy array to image
    img1 = cv2.imdecode(npimg1, cv2.IMREAD_UNCHANGED)    
    uploaded_img_file_path1 = os.path.join(UPLOAD_IMG_DIR_PATH,fileNameUploaded1)
    cv2.imwrite(uploaded_img_file_path1, img1)


    if os.path.exists(resultFilePath):
        return {"Status":"Upload Successful","filename_1": file.filename}
    else:
        return {"Status":"Failed","filename":None}

if __name__ == "__main__":
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


