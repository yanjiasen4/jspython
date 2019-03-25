import ppg_featureversion1 as p1
import numpy as np
from sklearn.externals import joblib
import os
from sklearn import svm
from sklearn.model_selection import train_test_split
#导入xlwt库用于写excel文件
import xlwt
import sys
import time
def next_batch(singals):

    #print()
    ppgfeatures = []
    winunit = int(25 / 2)-1
    segnum = int(400 / winunit)+1
    j=50
    tag=False
    invaidnum=0
    lenth=len(singals)
    gg = int((int(lenth / 100) - 3) / 3)
    while(j+400<lenth):
        feature = p1.feature_ppg(singals[j:j+400], segnum, winunit,1)
        if(len(feature)!=0):
            j=j+100
            ppgfeatures.append(feature)
        elif invaidnum<=gg:
            invaidnum=invaidnum+1
            j = j + 100
        else:
            tag=True
            ppgfeatures = []
            break
    ppgfeatures=np.array(ppgfeatures, dtype=float)
    return ppgfeatures
def run(file_dir):
    winunit = int(25 / 2) - 1
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
        if (lenth <= 460):
            continue
        filelist.append(os.path.basename(l))
        segnum = int(400 / winunit)+1
        j = 40
        invaidnum = 0
        # bukeyong=[]
        ncount = 0
        count = 0
        tag = False
        gg=int((int(lenth/100)-3)/3)
        while (j + 400 < lenth):
            feature = p1.feature_ppg(singals[j:j + 400], segnum, winunit, 1)
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
                    j = j + 100
                else:
                    # pro.append(['norm', round(float(prob[:, 0][0]), 4)])
                    # buff.append('normal')
                    ncount = ncount + 1
                    j = j + 100
            elif invaidnum <= gg:
                # tag=True
                # bukeyong=bukeyong+1
                # print('第', i, '个文件的第', j, '到', j + 400, '检测为不可用片段')
                invaidnum = invaidnum + 1
                j = j + 100
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

        # if tag == False and rfrate >= 0.6:
        #     # print(i,0)
        #     rffilelabel.append('AFIB')
        # elif tag == False and rfrate < 0.6 and rfrate >= 0.2:
        #     rffilelabel.append('Suspected AFIB ')
        #
        # elif tag == False and rfrate < 0.2:
        #     rffilelabel.append('Normal')
        # else:
        #     rffilelabel.append('Noisy')
    svmtime=time.time()-svmstarttime
    rfstarttime=time.time()
    for l in L:
        #print(l)
        f = open(l, 'r')
        singals = []
        singal = f.readlines()
        #print(len(singal[1].split()))
            #continue
        for row in singal:
            singals.append(int(row.split()[1]))
        lenth = len(singals)
        if (lenth <= 460):
            continue
        filelist.append(os.path.basename(l))
        segnum = int(400 / winunit)+1
        j = 40
        invaidnum = 0
        # bukeyong=[]
        rfncount = 0
        rfcount = 0
        tag = False
        gg=int((int(lenth/100)-3)/3)
        while (j + 400 < lenth):
            feature = p1.feature_ppg(singals[j:j + 400], segnum, winunit, 1)
            if (len(feature) != 0):
                #ppgpred = svm_model.predict(feature)
                rfppgpred = rf_model.predict(feature)
                # prob = svm_model.predict_proba(feature)
                # prob=round(prob,3)
                if rfppgpred[0] == 1:
                    rfcount += 1
                    j = j + 100
                else:
                    rfncount += 1
                    j = j + 100
                # if (ppgpred[0] == 1):  # 房颤
                #     # pro.append(['afib', round(float(prob[:, 1][0]), 4)])
                #     # buff.append('afib')
                #     count = count + 1
                #     j = j + 100
                # else:
                #     # pro.append(['norm', round(float(prob[:, 0][0]), 4)])
                #     # buff.append('normal')
                #     ncount = ncount + 1
                #     j = j + 100
            elif invaidnum <= gg:
                # tag=True
                # bukeyong=bukeyong+1
                # print('第', i, '个文件的第', j, '到', j + 400, '检测为不可用片段')
                invaidnum = invaidnum + 1
                j = j + 100
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
            rfrate = rfcount / (rfcount + rfncount)
        # if tag == False and rate >= 0.6:
        #     # print(i,0)
        #     filelabel.append('AFIB')
        # elif tag == False and rate < 0.6 and rate >= 0.2:
        #     filelabel.append('Suspected AFIB ')
        #
        # elif tag == False and rate < 0.2:
        #     filelabel.append('Normal')
        # else:
        #     filelabel.append('Noisy')

        if tag == False and rfrate >= 0.6:
            # print(i,0)
            rffilelabel.append('AFIB')
        elif tag == False and rfrate < 0.6 and rfrate >= 0.2:
            rffilelabel.append('Suspected AFIB ')

        elif tag == False and rfrate < 0.2:
            rffilelabel.append('Normal')
        else:
            rffilelabel.append('Noisy')
    rftime=time.time()-rfstarttime
    nnstarttime=time.time()
    import tensorflow as tf
    #tf.reset_default_graph()
    n_inputs = 12
    time_steps = 1
    num_layers = 4  # 层数
    hidden_size = 60  # 隐藏节点个数
    n_classes = 2
    time_steps = 1
    lenth = 12

    nnfilelabel = []
    #saver=tf.train.Saver()

    #x = tf.placeholder(tf.float32, [None, time_steps, lenth])
    #_batchsize = tf.placeholder(tf.int32, [])
    #pred = nninference.lstm_model(x,_batchsize)
    #predict_prob = tf.argmax(tf.nn.softmax(pred), 1)


    with tf.Session() as sess:
        # check_point_path='saver_model/'
        # ckpt = tf.train.get_checkpoint_state(checkpoint_dir=check_point_path)
        meta_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'saver_model/model.ckpt.meta')
        store_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'saver_model/')
        saver=tf.train.import_meta_graph(meta_path)
        # saver.restore(sess, ckpt.model_checkpoint_path)
        saver.restore(sess, tf.train.latest_checkpoint(store_path))
        graph = tf.get_default_graph()
        for l in L:
            f = open(l, 'r')
            singals = []
            singal = f.readlines()
            for row in singal:
                singals.append(int(row.split()[1]))
            if len(singals)<=460:
                continue
            testx = next_batch(singals)
            predict_prob=graph.get_tensor_by_name('predict_prob:0')
            _batchsize=graph.get_tensor_by_name('batchsize:0')
            x=graph.get_tensor_by_name('x:0')
            if testx.shape[0] != 0:
                predl = sess.run(predict_prob, feed_dict={x: testx, _batchsize: testx.shape[0]})
                if sum(predl) / len(predl) > 0.6:
                    nnfilelabel.append('AFIB')
                elif sum(predl) / len(predl) > 0.2:
                    nnfilelabel.append('Suspected AFIB')
                else:
                    nnfilelabel.append('Normal')
            else:
                nnfilelabel.append('Noisy')
    nntime=time.time()-nnstarttime
    # 初始化并创建一个工作簿
    book1 = xlwt.Workbook()
    # 创建一个名为sheetname的表单
    sheet1 = book1.add_sheet('sheet1')
    sheet1.write(0, 0, 'filename')
    sheet1.write(0, 1, 'Model1')
    sheet1.write(0, 2, 'Model2')
    sheet1.write(0, 3, 'Model3')
    sheet1.write(0, 4, 'Model4')
    sheet1.write(0, 5, 'T-model1')
    sheet1.write(0, 6, 'T-model2')
    sheet1.write(0, 7, 'T-model3')
    sheet1.write(0, 8, 'T-model4')
    sheet1.write(1,5,svmtime)
    sheet1.write(1, 6, rftime)
    sheet1.write(1, 7, nntime)
    sheet1.write(1,8,svmtime+rftime+nntime)

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
        sheet1.write(i + 1, 2, rffilelabel[i])
        sheet1.write(i + 1, 3, nnfilelabel[i])
        if filelabel[i]==rffilelabel[i]==nnfilelabel[i]:
            sheet1.write(i+1,4,filelabel[i])
        else:
            sheet1.write(i+1,4,'N/A')
    savePath = os.path.abspath(os.path.join(os.getcwd(), '../public/download/'))
    book1.save(os.path.join(savePath, savename + '-Statistics.xls'))
if __name__ == '__main__':
    #path1 = 'F:\zhanhlaoshi\\cinictest\A08521'
    '''
     the test dataset
    '''
    run(sys.argv[1])
    #run('E:/2000/200/')

