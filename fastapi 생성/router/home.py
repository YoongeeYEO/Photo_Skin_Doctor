from fastapi import APIRouter
from fastapi import UploadFile
import os, sys
from service import homeservice
import cv2 as cv

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)

router = APIRouter()

@router.get("/")
def home():
    return "hello world"

@router.post("/file")
async def upload_file(file: UploadFile):
    if (os.path.isdir("uploads/") == False):
        os.mkdir("uploads/")
    file_dir = "uploads/" + file.filename
    with open(file_dir, "wb+") as f:
        f.write(file.file.read())
            
    pred_class = homeservice.predict(file_dir)   
    # temp = pred_class.tolist()
    return {
        "statusCode": 200,
        "Prediect_class": pred_class
        }

@router.post("/cam")
async def upload_cam():
    if (os.path.isdir("uploads/") == False):
        os.mkdir("uploads/")
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("camera open failed")
        exit()
    while True:
        ret, img = cap.read()
        if not ret:
            print("Can't read camera")
            break
        
        file_dir = "uploads/img_captured.png"    
        cv.imshow('PC_camera', img)
        if cv.waitKey(1) == ord('c'):
            img_captured = cv.imwrite('uploads/img_captured.png', img)
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
        
    pred_class = homeservice.predict(file_dir)   
    # temp = pred_class.tolist()
    return {
        "statusCode": 200,
        "Prediect_class": pred_class
        }