import ppg_featureversion2 as p2
import pickle
from scipy import signal
import sys
import os
def run(file_dir,fs):
    step=4
    k=16
    fs = int(fs)
    # svm_model = joblib.load('15rbfSVM.joblib.pkl')
    svm_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'svm.txt')
    f = open(svm_path, 'rb')
    svm_model=pickle.load(f)
    f.close()
    try:
        f = open(file_dir, 'r')
    except Exception as e:
        print(e)
        return None
    signals = []
    si = f.readlines()
    for row in si:
        if row.split()[0]!='':
            signals.append(int(row.split()[1]))
    lenth=len(signals)
    if (lenth < k*fs):
        print('Insufficient data!')
        return None
    elif (lenth > 61 * fs):
        print('Excessive data!')
        return None
    else:
        winunit = int(fs / 2) - 1
        segnum = int(k*fs / winunit)-1
        fc = 5
        wn = 2 * fc / fs
        [b, a] = signal.butter(3, wn, 'low')
        sf = signal.filtfilt(b, a, signals)
        j = 0
        invaidnum = 0
        ncount = 0
        count = 0
        tag = False
        gg=int((int(lenth/(step*fs))-3)/3)
        while (j + k*fs < lenth):
            feature = p2.feature_ppg(sf[j:j + k*fs], segnum, winunit, fs)
            if (len(feature) != 0):
                ppgpred = svm_model.predict(feature)
                if (ppgpred[0] == 1):  # 房颤
                    # print('af')
                    count = count + 1
                    j = j + step*fs
                else:
                    # print('norm')
                    ncount = ncount + 1
                    j = j + step*fs
            elif invaidnum <= gg:
                invaidnum = invaidnum + 1
                j = j + step*fs
            else:
                tag = True
                break
        if tag == False:
            rate = count / (ncount + count)
            # rfrate = rfcount / (rfcount + rfncount)
        if tag == False and rate >= 0.6:
            # print(i,0)
            print('AFIB')
        elif tag == False and rate < 0.6 and rate >= 0.2:
            print('Suspected AFIB')

        elif tag == False and rate < 0.2:
            print('Normal')
        else:
            print('Noisy')

if __name__ == '__main__':
    '''
     the test dataset
    '''
    run(sys.argv[1],sys.argv[2])
    fs=64
#    for i in range(1,7):
#        run('E:\PPG\\'+str(i)+'.txt',fs)
