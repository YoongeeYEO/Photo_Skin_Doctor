# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 22:21:30 2022

@author: 푸른나무
"""

import cv2
import numpy as np
import pandas as pd
import os
import time
import shutil


MAX_SURVIVES = 676

# 모든 디렉토리에 대해서 처리함

def drop_similar_train_imgs(directory):

    imgnames = []

    #directory = "Urticaria Hives"
    
    imgnames = os.listdir(r"C:\2\archive\train"+"\\"+directory)
    
    os.makedirs(r"C:\2\survived\train"+"\\"+directory, exist_ok=True)
    
    if len(imgnames) <= MAX_SURVIVES: # 기준 개수 이내로는 무사 통과
        print('All Survived!')
        for i, fn in enumerate(imgnames):
            shutil.copy(r"C:\2\archive\train"+"\\"+directory+"\\"+fn, \
                  r"C:\2\survived\train"+"\\"+directory+"\\"+fn, )
        return # 아래 실행 방지
    
    hists = []
    for i, fn in enumerate(imgnames): # 메모리 문제로 바로 히스토그램 실행
        img = (cv2.imread(r"C:\2\archive\train"+"\\"+directory+"\\"+fn))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
        hists.append(hist)
    
    
    
    
    sim_mat = pd.DataFrame()
    sim_rav = pd.DataFrame(columns=['image1', 'image2', 'inequality'])
    
    start_time = time.time_ns()
    
    index = 0
    for i, h1 in enumerate(hists):
        for j, h2 in enumerate(hists):
            if i > j: continue
            ret = cv2.compareHist(h1, h2, 3)
            
            sim_mat.loc[imgnames[i], imgnames[j]] = ret
            if i!=j:
                sim_mat.loc[imgnames[j], imgnames[i]] = ret
            
            if i < j:
                sim_rav.loc[index] = [imgnames[i], imgnames[j], ret]
                index += 1
        elapsed_time = time.time_ns() - start_time
        remain_time = (elapsed_time / (i+1) * len(hists) - elapsed_time) * 1e-9
        print(i+1, '/', len(hists), remain_time, 'sec remaining')
    print()
    
    del hists
    
    
    mean_sim = sim_mat.mean(axis=1)
    
    survives = set(mean_sim.index)
    total_count = len(survives)
    
    sim_rav.sort_values(by=['inequality'], inplace=True, ignore_index=True)
    
    
    for ei in range(total_count-MAX_SURVIVES): # 100개 생존
        
        fn1, fn2, ine = sim_rav.iloc[0,:]
        print(f'{ei+1:>4}', ': ', fn1, ('*' if mean_sim.loc[fn1] > mean_sim.loc[fn2] else ' '))
        print('    ', '  ', fn2, (' ' if mean_sim.loc[fn1] > mean_sim.loc[fn2] else '*'))
        print('    ', '  ', ine)
        print()
        
        # 둘 중 어느 것을 탈락시킬지는 평균 불일치도에 따라서 높은 것을 탈락시킴
        if mean_sim.loc[fn1] > mean_sim.loc[fn2]:
            sim_rav = sim_rav[ (sim_rav['image1']!=fn1) & (sim_rav['image2']!=fn1)]
            survives.remove(fn1)
        else:
            sim_rav = sim_rav[ (sim_rav['image1']!=fn2) & (sim_rav['image2']!=fn2)]
            survives.remove(fn2)
    
    # 최종 리스트 출력
    print(' == SURVIVES ==')
    for survivor in survives:
        print(survivor)
        # 최종 결과는 복사
        shutil.copy(r"C:\2\archive\train"+"\\"+directory+"\\"+survivor, \
              r"C:\2\survived\train"+"\\"+directory+"\\"+survivor, )
        

for dn in os.listdir(r"C:\2\archive\train"):
    print(dn)
    drop_similar_train_imgs(dn)
    print(dn, 'Complete!!!\n')
    print('='*30)
