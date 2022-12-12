# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 16:03:45 2022

@author: 푸른나무
"""

raise Exception('블록쳐서 F9 눌러서 실행바랍니다.')

import cv2
import numpy as np
import pandas as pd
import os
import itertools

img = cv2.imread(r"C:\2\survived\train\Urticaria Hives\hives-Urticaria-Acute-31.jpg")

# 워터마크를 구하기 위해서 평균값 추출

files = os.listdir(r"C:\2\survived\train\Seborrheic Keratoses and other Benign Tumors"+"\\")

N = len(files)
wms = np.empty((N, 48,350,3))

for i, fn in itertools.islice(enumerate(files),N):
    img = cv2.imread(r"C:\2\survived\train\Seborrheic Keratoses and other Benign Tumors"+"\\"+fn)
    cy, cx = (img.shape[i]//2 for i in range(2))
    wm = img[cy-24:cy+24,cx-175:cx+175]
    wms[i] = wm


mini = np.minimum(wms.min(axis=0).round() * 4,255).astype('uint8')
maxi = np.maximum(wms.max(axis=0).round() * 4,255).astype('uint8')

cv2.imshow('',mini)
cv2.waitKey()
cv2.imwrite('minvalue.png',mini)

cv2.imshow('',maxi)
cv2.waitKey()
cv2.imwrite('maxvalue.png',maxi)


# 그림자관련


# 평균값 추출함
# [0]행을 기준으로 해서 뺄셈하여 양수 반영
# 그림자도 뺄셈을 해야 함


# 화이트마스크
meani = wms.mean(axis=0)
meani = meani.mean(axis=2)[...,np.newaxis]

wm = meani[:,:,:] > meani[0,:,:] + 3
wmask = np.where(wm, 255, 0).astype('uint8')
cv2.imwrite('wmask.png',wmask)


# 블랙마스크
meani = wms.mean(axis=0)
meani = meani.mean(axis=2)[...,np.newaxis]

bm = meani[:,:,:] < meani[0,:,:] - 2
bmask = np.where(bm, 255, 0).astype('uint8')
cv2.imwrite('bmask.png',bmask)


shadow = meani[0,:,:] - meani[:,:,:]

# 마스크 영역에서는 특정색으로 대체


img = cv2.imread(r"C:\2\survived\train\Urticaria Hives\dermagraphism-34.jpg")

cy, cx = (img.shape[i]//2 for i in range(2))

beta = 0.10
img[cy-24:cy+24,cx-175:cx+175] = np.where(wm, np.minimum((img[cy-24:cy+24,cx-175:cx+175]-255*beta)/(1-beta),255), img[cy-24:cy+24,cx-175:cx+175]).astype('uint8')
beta = shadow * 0.0085
img[cy-24:cy+24,cx-175:cx+175] = np.where(bm, np.minimum(np.maximum((img[cy-24:cy+24,cx-175:cx+175]-0*beta)/(1-beta),0),255), img[cy-24:cy+24,cx-175:cx+175])

cv2.imshow('',img)
cv2.waitKey()



# 하나의 디렉토리 각각 루프해서 dewater 디렉토리에 추가
with open(r"C:\2\dewater\error_reporting.txt", "at") as f:
    for dn in os.listdir(r"C:\2\archive\test"):
        print(dn)
        os.makedirs(r"C:\2\dewater\test"+"\\"+dn, exist_ok=True)
        for fn in os.listdir(r"C:\2\archive\test"+"\\"+dn+"\\"):
            try:
                print(fn)
                img = cv2.imread(r"C:\2\archive\test"+"\\"+dn+"\\"+fn)
                cy, cx = (img.shape[i]//2 for i in range(2))
                beta = 0.10
                img[cy-24:cy+24,cx-175:cx+175] = np.where(wm, np.minimum((img[cy-24:cy+24,cx-175:cx+175]-255*beta)/(1-beta),255), img[cy-24:cy+24,cx-175:cx+175]).astype('uint8')
                beta = shadow * 0.0085
                img[cy-24:cy+24,cx-175:cx+175] = np.where(bm, np.minimum(np.maximum((img[cy-24:cy+24,cx-175:cx+175]-0*beta)/(1-beta),0),255), img[cy-24:cy+24,cx-175:cx+175])
                cv2.imwrite(r"C:\2\dewater\test"+"\\"+dn+"\\"+fn,img)
            except Exception as e:
                f.write(dn)
                f.write('\n')
                f.write(fn)
                f.write('\n')
                f.write(str(e))
                f.write('\n\n')
                print(dn, fn, e)
            
        print(dn, 'Done!')





