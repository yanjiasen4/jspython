import ppg_featureversion1 as p1
import numpy as np
from sklearn.externals import joblib
import os
from sklearn import svm
import sys
import xlwt
import time
# def next_batch(singals):
#     ppgfeatures = []
#     winunit = int(25 / 2)-1
#     segnum = int(400 / winunit)+1
#     j=50
#     tag=False
#     invaidnum=0
#     lenth=len(singals)
#     gg = int((int(lenth / 100) - 3) / 3)
#     while(j+400<lenth):
#         feature = p1.feature_ppg(singals[j:j+400], segnum, winunit,1)
#         if(len(feature)!=0):
#             j=j+100
#             ppgfeatures.append(feature)
#         elif invaidnum<=gg:
#             invaidnum=invaidnum+1
#             j = j + 100
#         else:
#             tag=True
#             ppgfeatures = []
#             break
#     ppgfeatures=np.array(ppgfeatures, dtype=float)
#     return ppgfeatures
def run(file_dir,fs):
    step=4
    k=16
    fs = int(fs)
    winunit = int(fs / 2) - 1
    ppgfeatures = np.array([], dtype=float)
    ppglabels = np.array([], dtype=np.int32)
    savename='default'
    L = []
    svm_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'svm.joblib.pkl')
    rf_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'RF.joblib.pkl')
    svm_model = joblib.load(svm_path)
    rf_model = joblib.load(rf_path)
    #listfile = os.listdir(file_dir)

    for root, _, listfile in os.walk(file_dir):
        listfile.sort(key=lambda x: int(x[:-8]))
        for file in listfile:
            if os.path.splitext(file)[1] == '.txt':
                L.append(os.path.join(root, file))
    savename=file_dir.split('/')[-2]
    filelist = []
    filelabel = []
    rffilelabel = []
    svmstarttime=time.time()

    for l in L:
        print(l)
        f = open(l, 'r')
        singals = []
        singal = f.readlines()
        #print(len(singal[1].split()))
            #continue
        for row in singal:
            singals.append(int(row.split()[1]))
        lenth = len(singals)
        if (lenth < k*fs+50):
            continue
        filelist.append(os.path.basename(l))
        segnum = int(k*fs / winunit)+1
        j = 40
        invaidnum = 0
        # bukeyong=[]
        ncount = 0
        count = 0
        tag = False
        gg=int((int(lenth/(step*fs))-3)/3)
        while (j + k*fs < lenth):
            feature = p1.feature_ppg(singals[j:j + k*fs], segnum, winunit, 1)
            if (len(feature) != 0):
                ppgpred = svm_model.predict(feature)
                #rfppgpred = rf_model.predict(feature)
                # prob = svm_model.predict_proba(feature)
                # prob=round(prob,3)
                # if rfppgpred[0] == 1:
                #     rfcount += 1
                # else:
                #     rfncount += 1
                if (ppgpred[0] == 1):  # 房颤
                    # pro.append(['afib', round(float(prob[:, 1][0]), 4)])
                    # buff.append('afib')
                    count = count + 1
                    j = j + step*fs
                else:
                    # pro.append(['norm', round(float(prob[:, 0][0]), 4)])
                    # buff.append('normal')
                    ncount = ncount + 1
                    j = j + step*fs
            elif invaidnum <= gg:
                # tag=True
                # bukeyong=bukeyong+1
                # print('第', i, '个文件的第', j, '到', j + 400, '检测为不可用片段')
                invaidnum = invaidnum + 1
                j = j + step*fs
            else:
                tag = True
                # bukeyong.append(i)
                # print('第', i, '个文件判定为不可用')

                # print(i,'~')
                # plt.plot(singals[j:j+400])
                # plt.scatter(index_peak, value_peak, marker='x', color='r', s=30)
                # plt.show()
                break
        if tag == False:
            rate = count / (ncount + count)
            # rfrate = rfcount / (rfcount + rfncount)
        if tag == False and rate >= 0.6:
            # print(i,0)
            filelabel.append('AFIB')
        elif tag == False and rate < 0.6 and rate >= 0.2:
            filelabel.append('Suspected AFIB ')

        elif tag == False and rate < 0.2:
            filelabel.append('Normal')
        else:
            filelabel.append('Noisy')

    # rfstarttime=time.time()
    # for l in L:
    #     #print(l)
    #     f = open(l, 'r')
    #     singals = []
    #     singal = f.readlines()
    #     #print(len(singal[1].split()))
    #         #continue
    #     for row in singal:
    #         singals.append(int(row.split()[1]))
    #     lenth = len(singals)
    #     if (lenth < 20*fs+50):
    #         continue
    #     filelist.append(os.path.basename(l))
    #     segnum = int(400 / winunit)+1
    #     j = 40
    #     invaidnum = 0
    #     # bukeyong=[]
    #     rfncount = 0
    #     rfcount = 0
    #     tag = False
    #     gg=int((int(lenth/100)-3)/3)
    #     while (j + 400 < lenth):
    #         feature = p1.feature_ppg(singals[j:j + 400], segnum, winunit, 1)
    #         if (len(feature) != 0):
    #             #ppgpred = svm_model.predict(feature)
    #             rfppgpred = rf_model.predict(feature)
    #             # prob = svm_model.predict_proba(feature)
    #             # prob=round(prob,3)
    #             if rfppgpred[0] == 1:
    #                 rfcount += 1
    #                 j = j + 100
    #             else:
    #                 rfncount += 1
    #                 j = j + 100
    #             # if (ppgpred[0] == 1):  # 房颤
    #             #     # pro.append(['afib', round(float(prob[:, 1][0]), 4)])
    #             #     # buff.append('afib')
    #             #     count = count + 1
    #             #     j = j + 100
    #             # else:
    #             #     # pro.append(['norm', round(float(prob[:, 0][0]), 4)])
    #             #     # buff.append('normal')
    #             #     ncount = ncount + 1
    #             #     j = j + 100
    #         elif invaidnum <= gg:
    #             # tag=True
    #             # bukeyong=bukeyong+1
    #             # print('第', i, '个文件的第', j, '到', j + 400, '检测为不可用片段')
    #             invaidnum = invaidnum + 1
    #             j = j + 100
    #         else:
    #             tag = True
    #             # bukeyong.append(i)
    #             # print('第', i, '个文件判定为不可用')
    #
    #             # print(i,'~')
    #             # plt.plot(singals[j:j+400])
    #             # plt.scatter(index_peak, value_peak, marker='x', color='r', s=30)
    #             # plt.show()
    #             break
    #     if tag == False:
    #         rfrate = rfcount / (rfcount + rfncount)
    #     # if tag == False and rate >= 0.6:
    #     #     # print(i,0)
    #     #     filelabel.append('AFIB')
    #     # elif tag == False and rate < 0.6 and rate >= 0.2:
    #     #     filelabel.append('Suspected AFIB ')
    #     #
    #     # elif tag == False and rate < 0.2:
    #     #     filelabel.append('Normal')
    #     # else:
    #     #     filelabel.append('Noisy')
    #
    #     if tag == False and rfrate >= 0.6:
    #         # print(i,0)
    #         rffilelabel.append('AFIB')
    #     elif tag == False and rfrate < 0.6 and rfrate >= 0.2:
    #         rffilelabel.append('Suspected AFIB ')
    #
    #     elif tag == False and rfrate < 0.2:
    #         rffilelabel.append('Normal')
    #     else:
    #         rffilelabel.append('Noisy')
    # rftime=time.time()-rfstarttime

    # 初始化并创建一个工作簿
    book1 = xlwt.Workbook()
    # 创建一个名为sheetname的表单
    sheet1 = book1.add_sheet('sheet1')
    sheet1.write(0, 0, 'filename')
    sheet1.write(0, 1, 'Model')
    # book2 = xlwt.Workbook()
    # # 创建一个名为sheetname的表单
    # sheet2 = book2.add_sheet('sheet1')
    # sheet2.write(0, 0, 'filename')
    # sheet2.write(0, 1, 'Model2')
    # sheet2.write(0, 2, rftime)
    # book3 = xlwt.Workbook()
    # # 创建一个名为sheetname的表单
    # sheet3 = book3.add_sheet('sheet1')
    # sheet3.write(0, 0, 'filename')
    # sheet3.write(0, 1, 'Model3')
    # sheet3.write(0, 2, nntime)
    # 将工作簿以bookname命名并保存
    for i in range(len(filelabel)):
        sheet1.write(i + 1, 0, filelist[i])
        # sheet2.write(i + 1, 0, filelist[i])
        # sheet3.write(i + 1, 0, filelist[i])
        sheet1.write(i + 1, 1, filelabel[i])
    savePath = os.path.abspath(os.path.join(os.getcwd(), '../public/download/'))
    book1.save(os.path.join(savePath, savename + '-Statistics.xls'))
if __name__ == '__main__':
    #path1 = 'F:\zhanhlaoshi\\cinictest\A08521'
    '''
     the test dataset
    '''
    # print (sys.argv[0], sys.argv[1])
    run(sys.argv[1],sys.argv[2])
    # fs=25
    # run('E:/200/',fs)

