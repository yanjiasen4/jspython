import numpy as np
import math
from sklearn.preprocessing import normalize


def feature_ppg(singal,segnum,winunit,fs):
    anotherfeatures = np.array([], dtype=float)
    anotherwindowsize=12
    value_peak, index_peak = search_peak(singal, winunit, segnum)
    # plt.plot(range(0, len(singal)), singal)
    # plt.scatter(index_peak, value_peak, marker='x', color='r', s=30)
    # plt.show()
    if len(value_peak)<13:
        # print('不可用：',fnum)
        return anotherfeatures
    PP_interval=[]
    for i in range(1,len(index_peak)):
        PP_interval.append((index_peak[i]-index_peak[i-1])/fs)
    # print('PP间隔如下：')
    # print(PP_interval)
    di_PP_interval=[]
    for i in range(1,len(PP_interval)):
        buf = abs(PP_interval[i] - PP_interval[i - 1])
        if buf<=0.04:
            buf=0
        di_PP_interval.append(math.sqrt(buf))
    di_PP_interval.append(sum(di_PP_interval))
    anotherfeatures=np.zeros((1,anotherwindowsize))
    anotherfeatures[0,:]=di_PP_interval[-12:]#+PP_interval[-12:]
    anotherfeatures=np.array(anotherfeatures)
    return  anotherfeatures
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
    return sum(n[:-4])/(minSegment-4),sum(m[1:])/(minSegment-1)
def search_peak(singal,winunit,segnum):

    value_peak=[]
    index_peak=[]
    thmin,th=findthrehold(singal,winunit,10)
    # print('阈值：',thmin,th)
    for i in range(segnum):
        Max,index=selfmax(i,singal[i*winunit:(i+1)*winunit],winunit)#此时是在峰值左侧，并不一定是在峰值上
        if index!=0 and singal[index-1]>Max:
            continue
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
        if len(index_peak)!=0:
            #print(index_peak[-1],index)
            if index_peak[-1]>=index:
                continue
            min = selfmin(singal[index_peak[-1]:index])
            #print(Max,min)
            if (Max>=th):
                #print('最大值满足')
                if min<thmin or index-index_peak[-1]>winunit:# and abs(Max-value_peak[-1])<th-thmin:
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
