import matplotlib.pyplot as plt
import numpy as np
def loadreplicanums(begin,end,lambdai):
    filename='./initialAssign-'+str(begin)+'-'+str(end)+'-L'+str(lambdai)+'.txt'
    Replicaneeded=[]
    ReplicaActual=[]
    Levels=[]
    with open(filename, 'r') as datafile:
        for dataline in datafile:
            datalineitem = dataline.split()
            #4/7/9有用
            Levels.append(int(datalineitem[4]))
            Replicaneeded.append(int(datalineitem[7]))
            ReplicaActual.append(int(datalineitem[9]))
    return Replicaneeded,ReplicaActual,Levels



if __name__=='__main__':
    begin=4032
    end=4431
    lambdai=10
    beginblock=200
    RN,RA,LL=loadreplicanums(begin,end,lambdai)
    RR=[]
    for i in range(len(RN)):
        RR.append(int(RN[i])-int(RA[i]))
    RR[0]=0
    maxlevel=0
    for i in range(begin+beginblock,end):
        if maxlevel<LL[i-begin]:
            maxlevel=LL[i-begin]
    EveryLevel=[]
    for i in range(maxlevel):
        EveryLevel.append([])
    for i in range(begin+beginblock,end):
        thislevel=LL[i-begin]
        rr=RR[i-begin]
        EveryLevel[thislevel-1].append(rr)

    colors=['blue','red','green','skyblue','pink','yellow','purple','black','cyan','orange']
    labels=['1','2','3','4','5','6','7','8','9','10']
    maxpltlevel=maxlevel
    if maxlevel>10:
        maxpltlevel=10
    for i in range(maxpltlevel):
        plt.plot(range(0,len(EveryLevel[i])),EveryLevel[i],color=colors[i],label=labels[i],marker='.')
    # plt.plot(range(begin+beginblock,end),RR[beginblock:],color='r',marker='.',label='needed-actual')
    # plt.bar(range(begin+beginblock,end),LL[beginblock:],color='grey',label='levels')
    # plt.plot(range(begin+beginblock,end),RN[beginblock:],label='needed',color='g')
    # plt.plot(range(begin+beginblock, end), RA[beginblock:], label='actual', color='b')
    plt.axhline(y=0, color='grey')
    plt.legend()
    plt.title("REPLICANUMS: NEEDED-ACTUAL(lambdai="+str(lambdai))
    plt.xlabel('numbers')
    plt.ylabel('replicas\' amounts differences')
    plt.show()