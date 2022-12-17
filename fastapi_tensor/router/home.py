from fastapi import APIRouter
import os, sys
from service import homeservice
import cv2 as cv

from fastapi import Request, UploadFile, File
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse
from service.helpers import *

import shutil
from pydantic.main import BaseModel

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return  templates.TemplateResponse("page.html", {"request": request})

class UploadedData(BaseModel):
    img_path: str
    thumb_path: str
    pred_class: str
    pred_name: str


@router.post("/upload/new/", response_model=UploadedData)
async def post_upload(request: Request, imgdata: tuple, file: UploadFile = File(...)):
    data_dict = eval(imgdata[0])
    winWidth, imgWidth, imgHeight = data_dict["winWidth"], data_dict["imgWidth"], data_dict["imgHeight"]

    # create the full path
    workspace = create_workspace()
    # filename
    file_path = Path(file.filename)
    # image full path
    img_full_path = workspace / file_path
    with open(str(img_full_path), 'wb') as myfile:
        contents = await file.read()
        myfile.write(contents)
    # create a thumb image and save it
    thumb(img_full_path, winWidth, imgWidth, imgHeight)
    # create the thumb path
    # ext is like .png or .jpg
    filepath, ext = os.path.splitext(img_full_path)
    thumb_path = filepath + ".thumbnail"+ext
            
    pred_class, pred_name = homeservice.predict(img_full_path)   
    
    print(UploadedData(
        img_path=str(img_full_path),
        thumb_path=str(thumb_path),
        pred_class=str(pred_class),
        pred_name=str(pred_name)
    ))

    return UploadedData(
        img_path=str(img_full_path),
        thumb_path=str(thumb_path),
        pred_class=str(pred_class),
        pred_name=str(pred_name)
    )
    
@router.get("/cam")
async def get_cam(request: Request):
    return templates.TemplateResponse("cam.html", {"request": request})


@router.post("/file")
async def upload_file(file: UploadFile):
    if (os.path.isdir("static/uploads/") == False):
        os.mkdir("static/uploads/")
    file_dir = "static/uploads/" + file.filename
    with open(file_dir, "wb+") as f:
        f.write(file.file.read())
            
    pred_class, pred_name = homeservice.predict(file_dir)   
    # temp = pred_class.tolist()
    return {
        "statusCode": 200,
        "Predicted_class": pred_class,
        "Predicted_name": pred_name
        }

@router.post("/cam")
async def upload_cam():
    if (os.path.isdir("static/uploads/") == False):
        os.mkdir("static/uploads/")
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("camera open failed")
        exit()
    while True:
        ret, img = cap.read()
        if not ret:
            print("Can't read camera")
            break
        
        file_dir = "static/uploads/img_captured.png"    
        cv.imshow('PC_camera', img)
        if cv.waitKey(1) == ord('c'):
            img_captured = cv.imwrite('static/uploads/img_captured.png', img)
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
        
    pred_class, pred_name = homeservice.predict(file_dir)
    print(pred_class)
    print(pred_name)   
    # temp = pred_class.tolist()
    return {
        "statusCode": 200,
        "Predicted_class": str(pred_class),
        "Predicted_name": str(pred_name),
        "thumb_path": file_dir
        }