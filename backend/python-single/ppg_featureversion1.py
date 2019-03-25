import operator
import csv
import numpy as np
from scipy.fftpack import fft,ifft
import scipy.io as sio
import matplotlib.pyplot as plt
import pywt
import pyfftw
import seaborn
import math
import scipy.signal as singal
from scipy.signal import butter,lfilter
from sklearn.preprocessing import normalize
import sys
import pandas as pd

nn50=18
max_interval=500##心跳间隔大于 500 认为是数据错误 不要 心跳低于
min_interval=200 ##心跳间隔小于 120 认为是数据错误 不要  心跳超过180/s

def computer_rmssd_hr(index_peak,fs):
    rmssd = []
    hr = []
    nowsumuti = 0.0
    for i in range(2, len(index_peak)):
        rr1 = (index_peak[i - 1] - index_peak[i - 2])/fs
        rr2 = (index_peak[i] - index_peak[i - 1])/fs
        nowsumuti = nowsumuti + (rr1 - rr2) ** 2
        rmssd.append(math.sqrt(nowsumuti / (i - 1)))
        hr.append(60/((index_peak[i]-index_peak[i-1])/(fs)))
    hr.append(rmssd[-1])
    hr.append(sum(rmssd)/len(rmssd))
    return rmssd,hr



def feature_ppg(singal,segnum,winunit,tag):
    features = np.array([], dtype=float)
    anotherfeatures = np.array([], dtype=float)
    windowsize=12
    anotherwindowsize=12
    value_peak, index_peak = search_peak(singal, winunit, segnum)
    if len(value_peak)<13:
        # print('不可用：',fnum)
        # plt.plot(range(0, len(singal)), singal)
        # plt.scatter(index_peak, value_peak, marker='x', color='r', s=30)
        # plt.show()
        return anotherfeatures
    PP_interval=[]
    for i in range(1,len(index_peak)):
        PP_interval.append((index_peak[i]-index_peak[i-1])/25)
    # print('PP间隔如下：')
    # print(PP_interval)
    di_PP_interval=[]
    for i in range(1,len(PP_interval)):
        buf = abs(PP_interval[i] - PP_interval[i - 1])
        if buf<=0.04:
            buf=0
        di_PP_interval.append(math.sqrt(buf))
        # buf = abs(PP_interval[i] - PP_interval[i - 1])
        # if buf>=0.2:
        #     di_PP_interval.append(20*buf)
        # elif buf>=0.15:
        #     di_PP_interval.append(10*buf)
        # else:
        #     di_PP_interval.append(1*buf)
    di_PP_interval.append(sum(di_PP_interval))
    #np.savetxt('PP_interval.csv',PP_interval,delimiter=',')
    #csv.writer()
    #data1 = pd.DataFrame(PP_interval)
    #data1.to_csv('PP_interval.csv')

    if(len(index_peak)<13):
        #print('不规律文件',fnum)
        tag=tag
    else:
        #print()
        rmssd, hr = computer_rmssd_hr(index_peak, 25)
        #print(len(rmssd),len(hr))
        #print(rmssd[:10],hr[:10])

        group=int(len(rmssd)/windowsize)
        #anothergroup = int(len(rmssd) / anotherwindowsize)
        anotherfeatures=np.zeros((1,anotherwindowsize))
        a=[]
        #a.append(sum(di_PP_interval[0:11]))

        for i in range(12):
           a.append(math.sqrt(PP_interval[i]))
        anotherfeatures[0,:]=di_PP_interval[-12:]#+PP_interval[-12:]
        anotherfeatures=np.array(anotherfeatures)



        # features = np.zeros((group,2+windowsize))
        # rm_ = np.array(rmssd[: group * windowsize])
        # hr_ = np.array(hr[: group * (windowsize+2)])
        # rm_=rm_.reshape((group,windowsize))
        # hr_=hr_.reshape((group,windowsize+2))
        #
        # #print('共有心跳：',len(index_peak))
        # for i in range(group):
        #     #features[i,0,:]=rm_[i]
        #     features[i,:]=hr_[i]
        # features=features.reshape((group,windowsize+2))
    return  anotherfeatures
# def compute_rmssd(f_RR):
#     rmssd = 0
#     for i in range(len(f_RR)-1):
#         rmssd = rmssd+math.fabs(f_RR[i]-f_RR[i+1])**2
#     rmssd = math.sqrt(rmssd/(len(f_RR)-1))
#     return rmssd

# def RR_interval(RR_sample,ann):
#     interval=[]
#     for i in range(len(RR_sample)-1):
#         value=RR_sample[i+1]-RR_sample[i]
#         if ann=='O':
#             interval.append(value)
#         elif(value>max_interval):
#             interval=[]
#             break
#         else:
#             interval.append(value)
#     return  interval
def findthrehold(singal,winunit,minSegment):
    m=[]
    n=[]
    for i in range(minSegment):
        Max,index=selfmax(i,singal[i*winunit:(i+1)*winunit],winunit)
        Min=selfmin(singal[i*winunit:(i+1)*winunit])
        m.append(Max)
        n.append(Min)
    m.sort(reverse=True)
    n.sort(reverse=True)
    return sum(n[-7:-2])/(minSegment-2),sum(m[1 :-3])/(minSegment+5)
def search_peak(singal,winunit,segnum):

    value_peak=[]
    index_peak=[]
    thmin,th=findthrehold(singal,winunit,10)
    #print('阈值：',thmin,th)
    for i in range(segnum):
        Max,index=selfmax(i,singal[i*winunit:(i+1)*winunit],winunit)#此时是在峰值左侧，并不一定是在峰值上
        if index!=0 and singal[index-1]>Max:
            continue
        # if index+3<len(singal) and Max<singal[index+1]:
        #     if singal[index+1]<singal[index+2]:
        #         if singal[index+2]<singal[index+3]:
        #             Max=singal[index+3]
        #             index=index+3
        #         else:
        #             Max=singal[index+2]
        #             index = index + 2
        #     else:
        #         Max=singal[index+1]
        #         index = index + 1
        buindex=index+1
        while(buindex<len(singal)):
            if singal[index]<singal[buindex]:
                index=buindex
                buindex+=1
            else:
                break
        Max=singal[index]
        if len(index_peak)!=0 and index-index_peak[-1]>winunit*4.6:
            #print("jiangeda",index)
            value_peak = []
            index_peak = []
            break

        #print('最开始的下标和值：',index,Max)
        # if(len(index_peak)!=0 and index-index_peak[-1]>(1+winunit)*4.5):
        #     print('间隔：',index-index_peak[-1])
        #     #plt.plot(range(0, len(singal)), singal)
        #     #plt.scatter(index_peak, value_peak, marker='x', color='r', s=30)
        #     #plt.show()
        #     value_peak=[]
        #     index_peak=[]
        #     break
        # if (len(index_peak)!=0) and singal[index]<int(0.5*(singal[index-1]+singal[index-3])):
        #     continue
        # if(Max>th):
        #     if(len(index_peak)!=0 and index-index_peak[-1]<=winunit+1):#相邻rr间隔不得小于8个采样点
        #         if(value_peak[-1]<Max):
        #             value_peak[-1]=Max
        #             index_peak[-1]=index
        #     else:
        #         index_peak.append(index)
        #         value_peak.append(Max)
        # elif(len(index_peak)!=0 and Max>0.6*th and Max>0.5*value_peak[-1] and index-index_peak[-1]>=winunit+1):
        #     index_peak.append(index)
        #     value_peak.append(Max)
        if len(index_peak)!=0:
            #print(index_peak[-1],index)
            if index_peak[-1]>=index:
                continue
            min = selfmin(singal[index_peak[-1]:index])
            #print(Max,min)
            if (Max>=th):
                #print('最大值满足')
                if min<thmin:# and abs(Max-value_peak[-1])<th-thmin:
                    #print('最小值满足')
                    index_peak.append(index)
                    value_peak.append(Max)
                else:
                    #print('伪波')
                    if (value_peak[-1] < Max):
                        value_peak[-1] = Max
                        index_peak[-1] = index
                    else:
                        continue
            else:
                #print('最大值不满足')
                if min<thmin and Max>thmin:
                    #print('但最小值满足')
                    index_peak.append(index)
                    value_peak.append(Max)
                else:
                    #print('最小值也不满足')
                    if (value_peak[-1] < Max):
                        value_peak[-1] = Max
                        index_peak[-1] = index
                    else:
                        continue
        elif Max>th:
            index_peak.append(index)
            value_peak.append(Max)
    return value_peak,index_peak
def selfmax(seg,singal,winunit):

    #max=float(singal[0])
    max = (singal[0])
    # min = (singal[0])
    index=seg*winunit
    for i in range(len(singal)):
        #if(float(singal[i])>max):
        if (singal[i] > max):
            max=singal[i]
            index=i+seg*winunit
        # if (singal[i] < min):
        #     min=singal[i]
    return max,index
def selfmin(singal):
    #max=float(singal[0])
    min = (singal[0])
    for i in range(len(singal)):
        #if(float(singal[i])>max):
        if (singal[i] < min):
            min=singal[i]
    return min
