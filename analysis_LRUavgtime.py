import matplotlib.pyplot as plt
import json
import numpy as np
def loadavgtimes(replicatype,activeType,totaltime):
    filename='./LRUtestData-'+str(replicatype)+'-'+str(activeType)+'-'+str(totaltime)+'-4032-200-200-10-1-4-6-1.txt'
    AvgTime=[]
    with open(filename, 'r') as datafile:
        i=0
        for dataline in datafile:
            if i ==0:
                datalineitem = dataline.split()
                # print(0,'-',datalineitem)
                begin=int(datalineitem[0])
                ends = int(datalineitem[1])
                step = int(datalineitem[2])
            elif i!=1:
                datalineitem=dataline.split()
                # print(1,'-',datalineitem)
                for i in range(0,len(datalineitem)):
                    AvgTime.append(float(datalineitem[i]))
            i+=1
        # print(AvgTime)
    return AvgTime,begin,ends,step
def plotAvg():
    replicatype = 0
    activeType = 1
    totaltime = 100
    begin = 4032
    end = 4431
    step = 1
    beginblock = 200
    Avgtime01, b01, e01, s01 = loadavgtimes(replicatype, activeType, totaltime)
    Avgtime02, b02, e02, s02 = loadavgtimes(0, 2, 100)
    Avgtime12, b12, e12, s12 = loadavgtimes(1, 2, 100)
    Avgtime22, b22, e22, s22 = loadavgtimes(2, 2, 100)
    Avgtime_12,b_12,e_12,s_12=loadavgtimes(-1,2,100)
    Avgtime_11,b_11,e_11,s_11=loadavgtimes(-1,1,100)
    Avgtime11,_,_,_=loadavgtimes(1,1,100)
    Avgtime21,_,_,_=loadavgtimes(2,1,100)
    Avgtime10,_,_,_=loadavgtimes(1,0,100)
    Avgtime20,_,_,_=loadavgtimes(2,0,100)
    Avgtime_10All,_,_,_=loadavgtimes(-1,0,100)
    if b01 != b01 or e01 != e02 or s01 != s02:
        exit(-1)
    if b12 != b22 or e12 != e22 or s12 != s22:
        exit(-1)
    if b01 != b12 or e01 != e12 or s01 != s12:
        exit(-1)
    if b12!=b_12 or e12!=e_12 or s12!=s_12:
        exit(-1)
    colors = ['blue', 'red', 'green', 'skyblue', 'pink', 'yellow', 'purple', 'black', 'cyan', 'orange']
    plt.plot(range(b01, e01, s01), Avgtime01, color=colors[0], label='01')
    plt.plot(range(b01, e01, s01), Avgtime02, color=colors[1], label='02')
    plt.plot(range(b01, e01, s01), Avgtime12, color=colors[2], label='12')
    # plt.plot(range(b01, e01, s01), Avgtime22, color=colors[3], label='22')
    # plt.plot(range(b01, e01, s01), Avgtime_12, color=colors[4], label='-12')
    # plt.plot(range(b01, e01, s01), Avgtime_11, color=colors[5], label='-11')
    plt.plot(range(b01,e01,s01),Avgtime11,color=colors[6],label='11')
    # plt.plot(range(b01, e01, s01), Avgtime21, color=colors[7], label='21')
    # plt.plot(range(b01, e01, s01), Avgtime10, color=colors[8], label='1-1')
    # plt.plot(range(b01, e01, s01), Avgtime20, color=colors[9], label='2-1')
    # plt.plot(range(b01,e01,s01),Avgtime_10All,color='grey',label='-10')
    plt.legend()
    plt.xlabel('blocks')
    plt.ylabel('avg time')
    # plt.ylim(ymin=0,ymax=5)
    plt.show()

def loadstorage(replicatype,activeType):
    totalblocksdynamic=200
    filename = './LRU-StorageSize-' + str(replicatype) + '-' + str(activeType) + '200-4432-4.txt'
    NodesSizeAll = np.array([.0]*totalblocksdynamic)
    BlockSize=[]
    with open(filename, 'r') as datafile:
        i = 0
        for dataline in datafile:
            if i == 0:
                datalineitem = dataline.split()
                # print(0,'-',datalineitem)
                begin = int(datalineitem[0])
                ends = int(datalineitem[1])
                step = int(datalineitem[2])
            elif i ==2:
                BlockSize=json.loads(dataline)
            elif i>=4:
                NodesSize=np.array(json.loads(dataline))
                NodesSizeAll+=NodesSize
                # if i==4:
                #     print(NodesSize)
            i += 1
        print('filename=', filename, '-------')
        print(NodesSizeAll)
        NodesSizeAll=NodesSizeAll/10
        print('filename=',filename,'-------')
        print(NodesSizeAll)
    return BlockSize,NodesSizeAll, begin, ends, step

def plotStorage():
    replicatype = 0
    activeType = 1
    Blocksize01,NodeSize01, b01, e01, s01 = loadstorage(replicatype, activeType)
    Blocksize02,NodeSize02, b02, e02, s02 = loadstorage(0, 2)
    Blocksize12,NodeSize12, b12, e12, s12 = loadstorage(1, 2)
    Blocksize22,NodeSize22, b22, e22, s22 = loadstorage(2, 2)
    # print(NodeSize01)
    # print('-----')
    # print(NodeSize02)
    # print('-----')
    # print(NodeSize12)
    # print('-----')
    # print(NodeSize22)
    # print('-----')
    if b01 != b01 or e01 != e02 or s01 != s02:
        exit(-1)
    if b12 != b22 or e12 != e22 or s12 != s22:
        exit(-1)
    if b01 != b12 or e01 != e12 or s01 != s12:
        exit(-1)
    colors = ['blue', 'red', 'green', 'skyblue', 'pink', 'yellow', 'purple', 'black', 'cyan', 'orange']
    plt.plot(range(b01, e01, s01),np.array(NodeSize01)/np.array(Blocksize01),color='gold')#,label='total')
    # plt.plot(range(b01, e01, s01), NodeSize01, color=colors[0], label='01')
    # plt.plot(range(b01, e01, s01), NodeSize02, color=colors[1], label='02')
    # plt.plot(range(b01, e01, s01), NodeSize12, color=colors[2], label='12')
    # plt.plot(range(b01, e01, s01), NodeSize22, color=colors[3], label='22')
    # plt.legend()
    plt.ylim(ymin=0.2,ymax=.5)
    plt.xlabel('blocks')
    plt.ylabel('per node storage size/total size')
    plt.show()

if __name__=='__main__':
    plotAvg()
    # plt.plot(range(begin+beginblock,end),RR[beginblock:],color='r',marker='.',label='needed-actual')
    # plt.bar(range(begin+beginblock,end),LL[beginblock:],color='grey',label='levels')
    # plt.plot(range(begin+beginblock,end),RN[beginblock:],label='needed',color='g')
    # plt.plot(range(begin+beginblock, end), RA[beginblock:], label='actual', color='b')
    # plt.axhline(y=0, color='grey')
    # plt.legend()
    # plt.title("REPLICANUMS: NEEDED-ACTUAL(lambdai="+str(lambdai))
    # plt.xlabel('numbers')
    # plt.ylabel('replicas\' amounts differences')
    # plt.show()