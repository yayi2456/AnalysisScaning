import math
import re
import random

import matplotlib.pyplot as plt
import numpy as np

Bits=[]#每2016存1个
Targets=[]#通过Bits计算得到
BlockHashes=[]
BlockLists=[]
CommunicationCost=[]
BlockSizes=[]

ExpBlockStorage=[]
ExpSqrtBlockStorage=[]
LevelBlockStorage=[]
LevelSqrtBlockStorage=[]

def loadData(beginID,endID):#不包括endID
    filedataname='E:/CUB/bh.dat/bh.dat'
    filebitsname='E:/CUB/bh.dat/btc.com_diff_2020-07-02_08_27_40.csv'
    with open(filedataname,'r') as datafile:
        for dataline in datafile:
            datalineitem=dataline.split()
            #只取height和hash
            datalineitem=datalineitem[:2]
            blockID=int(datalineitem[0])
            if blockID<beginID:
                continue
            if blockID>=endID:
                break
            blockHash = datalineitem[1]
            BlockHashes.append(blockHash)
    with open(filebitsname,'r') as bitsfile:
        Bits.append('1d00ffff')#0-2015
        Targets.append(calTarget(Bits[0]))
        bitsfile.readline()
        for dataline in bitsfile:
            dataline=dataline.replace('\n','')
            datalineitem=dataline.split(',')
            #只取height和Bits
            datalineitem=datalineitem[0:5:4]
            #blockID=int(datalineitem[0])
            blockBits=datalineitem[1][2:]#去掉0x
            Bits.append(blockBits)
            Targets.append(calTarget(blockBits))

def calTarget(blockBits):
    exp=int(blockBits[:2],16)
    coef=int(blockBits[2:8],16)
    target=coef*pow(256,exp-3)
    return target

#level从1开始
def calLevel(blockID,beginID,endID):
    if blockID>=endID or blockID<beginID:
        return 0
    if blockID==beginID:
        return 256
    blockRow_blockBits=int(blockID/2016)
    target=Targets[blockRow_blockBits]
    blockHash=BlockHashes[blockID-beginID]
    blockHashwithno0 = re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", blockHash)
    blockHashValue=int(blockHashwithno0,16)
    level=1
    while blockHashValue<(target/pow(2,level)):
        level=level+1
    #print('blockhash=', blockHashValue, 'target=', target, 'level=',level)
    return level
#BlockList:[[mylevel,nextlevel1,nextlevel2,...,nextmylevel],...]
def buildBlockList(beginID,endID):
    MaxLevel=0
    levelLastNodeID=[beginID]*256
    for blockID in range(beginID,endID):
        BlockLists.append([])
        blockLevel=calLevel(blockID,beginID,endID)
        if blockLevel==0:
            print("error occured at blockID = ",blockID," , beginID = ",beginID," , endID = ",endID)
        if blockLevel>MaxLevel and blockID!=beginID:
            MaxLevel=blockLevel
        #先放入我的层级
        BlockLists[blockID-beginID].append(blockLevel)
        #我应该有mylevel个next字段
        for i in range(blockLevel):
            BlockLists[blockID-beginID].append(endID)
            # BlockLists[blockID-beginID].append(levelLastNodeID[i])
        #更新所有层级小于我节点的level=mylevel的next字段
        if blockID != beginID:
            for i in range(blockLevel):
                levelilastmodeid=levelLastNodeID[i]
                BlockLists[levelilastmodeid-beginID][i+1]=blockID
        # 上一个列表更新
        for leveli in range(blockLevel):
            levelLastNodeID[leveli] = blockID
    return MaxLevel

def print_BlockList(beginID,endID):
    filename='./blocklistdata-'+str(beginID)+'-'+str(endID)+'.txt'
    fileoutput=open(filename,'w')
    for blockID in range(beginID,endID):
        mylevel=BlockLists[blockID-beginID][0]
        print("{ID:",blockID," , mylevel =",mylevel," , [",end="",file=fileoutput)
        for i in range(mylevel-1):
            print("next-level-",i+1,":",BlockLists[blockID-beginID][i+1]," , ",end="",file=fileoutput)
        print("next-level-",mylevel,":",BlockLists[blockID-beginID][mylevel]," ]} ",file=fileoutput)
    fileoutput.close()

def scanBlockList(m,beginID,endID,Maxlevel):
    BlockScannedTimes=[0]*(endID-beginID)
    thisLevel=Maxlevel
    thisLevelbeginBlockID=beginID
    thisBlockID=beginID
    filename='./scannedinlevel-'+str(beginID)+'-'+str(endID)+'.txt'
    fileoutput=open(filename,'w')
    while thisLevel>0:
        thisLevelBlockNumbers = 0
        while thisBlockID!=endID:
            BlockScannedTimes[thisBlockID-beginID]=BlockScannedTimes[thisBlockID-beginID]+1
            print("scanned:",thisBlockID," , in level ",thisLevel," scannedTimes=",BlockScannedTimes[thisBlockID-beginID],file=fileoutput)
            thisBlockID=BlockLists[thisBlockID-beginID][thisLevel]
            thisLevelBlockNumbers=thisLevelBlockNumbers+1
        thisBlockID=thisLevelbeginBlockID
        scannedBlockNumbers=0
        while scannedBlockNumbers<thisLevelBlockNumbers-m:
            thisBlockID=BlockLists[thisBlockID-beginID][thisLevel]
            scannedBlockNumbers=scannedBlockNumbers+1
        thisLevel = thisLevel - 1
        print("==========================================================================", file=fileoutput)
        thisLevelbeginBlockID=thisBlockID
    fileoutput.close()
    return BlockScannedTimes

def scanBlockList_noRepeat(m,beginID,endID,Maxlevel):
    BlockScannedTimes=[0]*(endID-beginID)
    thisLevel=Maxlevel
    thisBlockID = beginID
    ChosenBlocks=[]
    # filename = './scannedinlevel-norepeat-' + str(beginID) + '-' + str(endID) + '.txt'
    # fileoutput = open(filename, 'w')
    while thisLevel > 0:
        # print('in level ',thisLevel,file=fileoutput)
        thisLevelBlockNumbers = 0
        while thisBlockID < endID:
            if BlockScannedTimes[thisBlockID-beginID]==0:
                thisLevelBlockNumbers = thisLevelBlockNumbers + 1
#            print(thisBlockID,' ',beginID,' endID: ',endID,' thisLevel: ',thisLevel,' ',len(BlockLists),' ',len(BlockLists[thisBlockID-beginID]))
            thisBlockID = BlockLists[thisBlockID - beginID][thisLevel]
        thisBlockID = beginID
        # 是否加层级块数小于m的
        if thisLevelBlockNumbers<m:
            thisLevel-=1
            thisBlockID=beginID
            # print("==========================================================================", file=fileoutput)
            continue
        scannedBlockNumbers = 0
        while scannedBlockNumbers < thisLevelBlockNumbers - m:
            if BlockScannedTimes[thisBlockID-beginID]==0:
                scannedBlockNumbers = scannedBlockNumbers + 1
            thisBlockID = BlockLists[thisBlockID - beginID][thisLevel]
        while scannedBlockNumbers<thisLevelBlockNumbers:
            if BlockScannedTimes[thisBlockID-beginID]==0:
                BlockScannedTimes[thisBlockID - beginID] = 1
                scannedBlockNumbers = scannedBlockNumbers + 1
                ChosenBlocks.append(thisBlockID)
                # print('block ', thisBlockID, file=fileoutput)
            thisBlockID=BlockLists[thisBlockID-beginID][thisLevel]
        thisLevel = thisLevel - 1
        # print("==========================================================================",file=fileoutput)
        thisBlockID=beginID
    # fileoutput.close()
    return ChosenBlocks



def scanBlockList_noRepeat_withoutm(m,beginID,endID,Maxlevel):
    BlockScannedTimes=[0]*(endID-beginID)
    thisLevel=Maxlevel
    thisBlockID = beginID
    ChosenBlocks=[]
    # filename = './scannedinlevel-norepeat-' + str(beginID) + '-' + str(endID) + '.txt'
    # fileoutput = open(filename, 'w')
    while thisLevel > 0:
        # print('in level ',thisLevel,file=fileoutput)
        thisLevelBlockNumbers = 0
        while thisBlockID < endID:
            if BlockScannedTimes[thisBlockID-beginID]==0:
                thisLevelBlockNumbers = thisLevelBlockNumbers + 1
#            print(thisBlockID,' ',beginID,' endID: ',endID,' thisLevel: ',thisLevel,' ',len(BlockLists),' ',len(BlockLists[thisBlockID-beginID]))
            thisBlockID = BlockLists[thisBlockID - beginID][thisLevel]
        thisBlockID = beginID
        # 是否加层级块数小于m的
        scannedBlockNumbers = 0
        while scannedBlockNumbers < thisLevelBlockNumbers - m:
            if BlockScannedTimes[thisBlockID-beginID]==0:
                scannedBlockNumbers = scannedBlockNumbers + 1
            thisBlockID = BlockLists[thisBlockID - beginID][thisLevel]
        while scannedBlockNumbers<thisLevelBlockNumbers:
            if BlockScannedTimes[thisBlockID-beginID]==0:
                BlockScannedTimes[thisBlockID - beginID] = 1
                scannedBlockNumbers = scannedBlockNumbers + 1
                ChosenBlocks.append(thisBlockID)
                # print('block ', thisBlockID, file=fileoutput)
            thisBlockID=BlockLists[thisBlockID-beginID][thisLevel]
        thisLevel = thisLevel - 1
        # print("==========================================================================",file=fileoutput)
        thisBlockID=beginID
    # fileoutput.close()
    return ChosenBlocks


def plotBlockScannedTimes(scannedTimes,beginID,endID):
    blockIDs = range(beginID, endID)
    plt.bar(blockIDs, scannedTimes)
    plt.xlabel('BlockID')
    plt.ylabel('scannedTimes')
    plt.show()

def plotHasBeenScanned(scannedTimes,beginID,endID):
    blockIDrange=range(beginID,endID)
    scanned=[0]*(endID-beginID)
    for blockID in range(beginID,endID):
        if scannedTimes[blockID-beginID]!=0:
            scanned[blockID-beginID]=1
    plt.bar(blockIDrange,scanned)
    plt.xlabel('BlockID')
    plt.ylabel('scannedTimes')
    plt.show()

def printBlockScannedTimes(scannedTimes,beginID,endID):
    filename='./blockscannedtimes-'+str(beginID)+'-'+str(endID)+'.txt'
    fileoutput=open(filename,'w')
    for blockID in range(beginID,endID):
        if scannedTimes[blockID-beginID]!=0:
            print("{ID:",blockID," , scannedTimes =",scannedTimes[blockID-beginID]," }",file=fileoutput)

def plotPie(scannedTimes,beginID,endID):
    plt.pie(scannedTimes)
    plt.show()

def printLevel(beginID,endID,Maxlevel):
    filename = './levelofnodes-' + str(beginID) + '-' + str(endID) + '.txt'
    fileoutput = open(filename, 'w')
    for thisLevel in range(Maxlevel):
        print("\n====================================================================Level-",thisLevel+1,file=fileoutput)
        for blockID in range(beginID, endID):
            if BlockLists[blockID-beginID][0]==thisLevel+1:
                print("{ID:", blockID, " }", file=fileoutput)

def plotScannedTimesV(scanned,beginID,endID):
    ChoosenID={beginID}
    for blockID in range(beginID,endID):
        if scanned[blockID-beginID]!=0:
            ChoosenID.add(blockID)
    y=list(ChoosenID)
    y.sort()
    x=range(len(y))
    plt.plot(x,y)
    plt.show()





def runme():
    beginID=0
    endID=2016#508032
    m=3
    loadData(beginID,endID)
    print("INFO: load done")
    maxlevel=buildBlockList(beginID,endID)
    print_BlockList(beginID,endID)
    print("INFO: build block list done")
    BlockScannedTimes=scanBlockList(m,beginID,endID,maxlevel)
    print("INFO: scan block list done")
    #printBlockScannedTimes(BlockScannedTimes,beginID,endID)
    #printLevel(beginID,endID,maxlevel)
    #plotBlockScannedTimes(BlockScannedTimes,beginID,endID)
    #plotHasBeenScanned(BlockScannedTimes,beginID,endID)
    plotScannedTimesV(BlockScannedTimes,beginID,endID)


def every2016BlocksPlot(beginID,endID,m,withoutm):
    if (endID-beginID)%2016!=0:
        exit(1)
    loadData(beginID,endID)
    maxlevel=buildBlockList(beginID,endID)
    print_BlockList(beginID, endID)
    print('maxlevel=',maxlevel)
    x=[]
    y=[]
    levelLine=5
    levelLine1=7
    levelLine2=9
    x1=[]
    y1=[]
    x2=[]
    y2=[]
    x3=[]
    y3=[]
    ReturnChosenTimes=[0]*(endID-beginID)
    filename='./every2016plot-'+str(beginID)+'-'+str(endID)+'.txt'
    fileoutput=open(filename,'w')
    stepmove=1#int((endID-beginID)/2016)
    for times in range(beginID-beginID+1,endID-beginID,stepmove):
        ##
        if withoutm:
            Chosen=scanBlockList_noRepeat_withoutm(m,beginID,beginID+times,maxlevel)
        if not withoutm:
            Chosen = scanBlockList_noRepeat(m, beginID, beginID + times, maxlevel)
        # print('=================scan times=',times,'==========================',file=fileoutput)
        for x1s in Chosen:
            # print('blockid=',x1s,',level=',BlockLists[x1s-beginID][0],file=fileoutput)
            ReturnChosenTimes[x1s-beginID]+=1
            if BlockLists[x1s-beginID][0]<levelLine:
                x.append(x1s)
                y.append(times+1)
            if BlockLists[x1s-beginID][0]>=levelLine and BlockLists[x1s-beginID][0]<levelLine1:
                x1.append(x1s)
                y1.append(times + 1)
            if BlockLists[x1s-beginID][0] >= levelLine1 and BlockLists[x1s-beginID][0] < levelLine2:
                x2.append(x1s)
                y2.append(times + 1)
            if BlockLists[x1s-beginID][0]>=levelLine2:
                x3.append(x1s)
                y3.append(times + 1)
    # plt.scatter(x,y,c='r',s=0.5,label='level:[1,4]')
    # plt.scatter(x1,y1,c='g',s=0.5,label='level:[5,6]')
    # plt.scatter(x2, y2, c='y', s=0.5, label='level:[7,8]')
    # plt.scatter(x3,y3,c='b',s=0.5,label='level:[9,∞)')
    # plt.xlabel('blockID')
    # plt.ylabel('scantime')
    # plt.legend()
    # plt.show()

    #接下来对数据进行分析
    #该层级节点平均被选中的次数
    LevelAveBlockChosenTimes=[0]*maxlevel
    LevelFangCha=[0]*maxlevel
    LevelChosenBlocks=[0]*maxlevel
    for thisblkID in range(beginID,endID):
        hislevel=BlockLists[thisblkID-beginID][0]
        if thisblkID==beginID:
            hislevel=maxlevel
        LevelChosenBlocks[hislevel-1]+=1
        LevelAveBlockChosenTimes[hislevel-1]+=(ReturnChosenTimes[thisblkID-beginID])
    print(LevelAveBlockChosenTimes)
    print(LevelChosenBlocks)
    for i in range(maxlevel):
        if LevelChosenBlocks[i]==0:
            LevelAveBlockChosenTimes[i]=0
            continue
        LevelAveBlockChosenTimes[i]=LevelAveBlockChosenTimes[i]/LevelChosenBlocks[i]
    #作图：
    # xlevel=range(1,maxlevel+1)
    # PlotXLevel=[]
    # PlotLevelAveBlockChosenTimes=[]
    # for i in range(maxlevel):
    #     xp=xlevel[i]
    #     yp=LevelAveBlockChosenTimes[i]
    #     if yp!=0:
    #         plt.text(xp + 0.01, yp + 90, '(%d ,\n %d,\n %d)' % (xp,yp,LevelChosenBlocks[i]), ha='center', va='top')
    #         PlotLevelAveBlockChosenTimes.append(yp)
    #         PlotXLevel.append(xp)
    # plt.plot(PlotXLevel,PlotLevelAveBlockChosenTimes)
    # plt.xlabel('levels')
    # plt.ylabel('avg-scantimes')
    # plt.title('beginID=%d,endID=%d'%(beginID,endID))
    # plt.show()
    #方差计算
    for thisblkID in range(beginID, endID):
        hislevel = BlockLists[thisblkID - beginID][0]
        if thisblkID == beginID:
            hislevel = maxlevel
        chazhi=ReturnChosenTimes[thisblkID - beginID]-LevelAveBlockChosenTimes[hislevel-1]
        LevelFangCha[hislevel - 1] += chazhi*chazhi
    for i in range(maxlevel):
        if LevelChosenBlocks[i]==0:
            LevelFangCha[i]=0
            continue
        LevelFangCha[i]=(math.sqrt(LevelFangCha[i]/LevelChosenBlocks[i]))
    print(LevelFangCha)
    #接下来是每一层的单独分析
    #因为level大的话节点很少，因此只统计[1,9]
    SortedLevelTimes=[]
    for i in range(9):
        SortedLevelTimes.append([])
    for blockID in range(beginID,endID):
        hislevel=BlockLists[blockID-beginID][0]
        if hislevel<=9:
            SortedLevelTimes[hislevel-1].append(ReturnChosenTimes[blockID-beginID])
            print('level=',hislevel,', blockid=',blockID,', times=',ReturnChosenTimes[blockID-beginID],file=fileoutput)
    #若需要有序，把下面取消注释
    for i in range(9):
        SortedLevelTimes[i]=np.sort(SortedLevelTimes[i])
    #多图
    # fig = plt.figure()
    # for i in range(9):
    #     if i<9:
    #         xplot=330+i+1
    #     else:
    #         xplot=3300+i+1
    #     if len(SortedLevelTimes[i])!=0:
    #         ax = fig.add_subplot(xplot)
    #         ax.set_title('level=%d'%(i+1))
    #         ax.scatter(range(len(SortedLevelTimes[i])),SortedLevelTimes[i],s=1,c='gray')
    #         ax.axhline(y=LevelFangCha[i]+LevelAveBlockChosenTimes[i], color='g')
    #         ax.axhline(y=-LevelFangCha[i] + LevelAveBlockChosenTimes[i], color='g')
    #         ax.axhline(y=LevelAveBlockChosenTimes[i],color='y')
    #         ax.text(0.5,LevelFangCha[i]+LevelAveBlockChosenTimes[i],'y=%.2f'%(LevelFangCha[i]+LevelAveBlockChosenTimes[i]))
    #         ax.text(0.5, -LevelFangCha[i] + LevelAveBlockChosenTimes[i],  'y=%.2f' % (-LevelFangCha[i] + LevelAveBlockChosenTimes[i]))
    #         ax.text(0.5,LevelAveBlockChosenTimes[i], 'average=%.2f' % (LevelAveBlockChosenTimes[i]))
    #
    # plt.show()
    #下面针对前9层计算扫描次数在x的块数
    BlocksByScanTimes =[]
    for i in range(9):
        BlocksByScanTimes.append([])
        begintimes=SortedLevelTimes[i][0]
        endtimes=SortedLevelTimes[i][len(SortedLevelTimes[i])-1]+1
        BlocksByScanTimes[i]=[0]*(endtimes-begintimes)
        for times in SortedLevelTimes[i]:
            BlocksByScanTimes[i][times-begintimes]+=1
    fig1=plt.figure()
    for i in range(9):
        xplot=330+i+1
        ax=fig1.add_subplot(xplot)
        ax.set_title('level=%d,avg=%.2f,s=%.2f' % (i + 1,LevelAveBlockChosenTimes[i],LevelFangCha[i]))
        ax.bar(range(SortedLevelTimes[i][0],SortedLevelTimes[i][len(SortedLevelTimes[i])-1]+1),BlocksByScanTimes[i],color='gray')
        ax.axvline(x=int(LevelAveBlockChosenTimes[i]),color='r')
        ax.axvline(x=int(LevelFangCha[i] + LevelAveBlockChosenTimes[i])+1, color='g')
        ax.axvline(x=int(-LevelFangCha[i] + LevelAveBlockChosenTimes[i]), color='g')
    plt.show()
    fileoutput.close()
    return ReturnChosenTimes

def runonce(beginID,endID,m):
    loadData(beginID,endID)
    ml=buildBlockList(beginID,endID)
    print_BlockList(beginID,endID)
    chosen=scanBlockList_noRepeat(m,beginID,endID,ml)

#块size
def loadData_Sizes(beginID,endID):
    # blocknums=endID-beginID
    # mu=1.2
    # sigma=0.2
    # global BlockSizes
    # BlockSizes=abs(np.random.normal(mu,sigma,blocknums))
    # #print((BlockSizes))
    global BlockSizes
    BlockSizes=[]
    filename='E:/CUB/bh.dat/blocksize.txt'
    with open(filename, 'r') as datafile:
        for dataline in datafile:
            datalineitem = dataline.split()
            # 只取height和hash
            blockID = int(datalineitem[0])
            if blockID < beginID:
                continue
            if blockID >= endID:
                break
            blocksize = float(datalineitem[1])
            BlockSizes.append(blocksize)

def calReplicas_exp(blocklevel,piece):
    return pow(2,blocklevel-1)*piece
def calReplicas_expsqrt(blocklevel,piece):
    return pow(2,(int)((blocklevel-1)/2))*piece
def calReplicas_level(blocklevel,piece):
    return piece*(blocklevel)
    #暂时替换：
    # return 8
#IMPORTANT: 那么我们知道大约7的时候和exp性能接近
def calReplicas_levelsqrt(blocklevel,piece):
    return piece*((int)(math.sqrt(blocklevel)))
    # 暂时替换：
    # return 7
    # numreverse=8-blocklevel-1
    # if numreverse<0:
    #     numreverse=0
    # return pow(2,numreverse)*piece

def generateNodesCommunicationCost_norm(nodesnums):
    mu=1
    sigma=0.5
    pairsofCostnums=int(nodesnums*(nodesnums-1)/2)
    Costtmp=np.random.normal(mu,sigma,pairsofCostnums)
    position=0
    for nodeid1 in range(nodesnums):
        CommunicationCost.append([])
        for nodeid2 in range(nodeid1):
            CommunicationCost[nodeid1].append(CommunicationCost[nodeid2][nodeid1])
        CommunicationCost[nodeid1].append(0)#自己与自己没有通信开销
        for nodeid2 in range(nodeid1+1,nodesnums):
            CommunicationCost[nodeid1].append(abs(Costtmp[position]))
            position=position+1

def generateCommunicationCost_1(nodesnums):
    position = 0
    for nodeid1 in range(nodesnums):
        CommunicationCost.append([])
        for nodeid2 in range(nodeid1):
            CommunicationCost[nodeid1].append(1)
        CommunicationCost[nodeid1].append(0)#自己与自己没有通信开销
        for nodeid2 in range(nodeid1+1,nodesnums):
            CommunicationCost[nodeid1].append(1)
            position=position+1


def initialAssignOneBlock(beginID,endID,blockID,nodesum,assigntype,piece):
    if assigntype==0b0 or assigntype>0b1111:
        print("ERROR")
        exit(1)
    #exp
    nodeid=blockID%nodesum
    blocklevel=BlockLists[blockID-beginID][0]
    thisnode=nodeid
    if assigntype&0b1:
        replicates = calReplicas_exp(blocklevel, piece)
        if nodesum<replicates:
            replicates=nodesum
        nodereplicas=random.sample(range(0,nodesum),replicates)
        ExpBlockStorage.append({nodereplicas[0]})
        for nodeid in nodereplicas[1:]:
            ExpBlockStorage[blockID - beginID].add(nodeid)
    #expsqrt
    if assigntype&0b10:
        replicates = calReplicas_expsqrt(blocklevel, piece)
        if nodesum < replicates:
            replicates = nodesum
        nodereplicas = random.sample(range(0, nodesum), replicates)
        ExpSqrtBlockStorage.append({nodereplicas[0]})
        for nodeid in nodereplicas[1:]:
            ExpSqrtBlockStorage[blockID - beginID].add(nodeid)
    #level
    if assigntype&0b100:
        replicates = calReplicas_level(blocklevel, piece)
        if nodesum < replicates:
            replicates = nodesum
        nodereplicas = random.sample(range(0, nodesum), replicates)
        LevelBlockStorage.append({nodereplicas[0]})
        for nodeid in nodereplicas[1:]:
            LevelBlockStorage[blockID - beginID].add(nodeid)
    if assigntype&0b1000:
        replicates = calReplicas_levelsqrt(blocklevel, piece)
        if nodesum < replicates:
            replicates = nodesum
        nodereplicas = random.sample(range(0, nodesum), replicates)
        LevelSqrtBlockStorage.append({nodereplicas[0]})
        for nodeid in nodereplicas[1:]:
            LevelSqrtBlockStorage[blockID - beginID].add(nodeid)
    return

def printAssignRes(beginID,endID,piece):
    filename = './DifferentinitialAssign-' + str(beginID) + '-' + str(endID) + '.txt'
    fileoutput = open(filename, 'w')
    for blockID in range(beginID,endID):
        print('blockID:',blockID,' , level:',BlockLists[blockID-beginID][0],', replicanums-exp\expsqrt\level\levelsqrt:', calReplicas_exp(BlockLists[blockID-beginID][0],piece),',', calReplicas_expsqrt(BlockLists[blockID-beginID][0],piece),
              ',', calReplicas_level(BlockLists[blockID-beginID][0],piece),',', calReplicas_levelsqrt(BlockLists[blockID-beginID][0],piece),
              ',replicaactually:',len(ExpBlockStorage[blockID-beginID]),',',len(ExpSqrtBlockStorage[blockID-beginID]),',',len(LevelBlockStorage[blockID-beginID]),',',len(LevelSqrtBlockStorage[blockID-beginID]),
              file=fileoutput)
    fileoutput.close()

def init(beginID,endID,nodesums,assigntype,piece):
    loadData(beginID,endID)
    maxlevel = buildBlockList(beginID, endID)
    generateCommunicationCost_1(nodesums)
    loadData_Sizes(beginID,endID)
    return maxlevel
def assignBlcoksStatically(beginID,endID,nodesums,assigntype,piece):
    for blockID in range(beginID,endID):
        initialAssignOneBlock(beginID,endID,blockID,nodesums,assigntype,piece)
    printAssignRes(beginID,endID,piece)

def Time_togetBlocksNeededtoProve(m,beginID,endIDsince,maxlevel,mynodeid,assigntype,nodesum):
    if assigntype not in [0b1,0b11,0b111,0b1111]:
        print("ERROR")
        exit(1)
        return 0
    ReturnTimeCost=[]
    Chosen = scanBlockList_noRepeat(m, beginID, endIDsince, maxlevel)
    if assigntype&0b1:
        AllTimeCost=[0]*nodesum
        for blockID in Chosen:
            storageNodes=ExpBlockStorage[blockID-beginID]
            first=storageNodes.pop()
            minCommunicate=CommunicationCost[mynodeid][first]
            minNode=first
            storageNodes.add(first)
            for nodes in storageNodes:
                commuicate=CommunicationCost[mynodeid][nodes]
                if commuicate<minCommunicate:
                    minCommunicate=commuicate
                    minNode=nodes
            TimeCost=minCommunicate*BlockSizes[blockID-beginID]
            AllTimeCost[minNode]+=TimeCost
            # print("new:minnode",minNode)
        # if len(Chosen) != 0:
        #     timemax = max(AllTimeCost)
        # else:
        #     timemax = 0
        timemax=0
        for i in AllTimeCost:
            timemax=timemax+i
        ReturnTimeCost.append(timemax)
    if assigntype&0b10:
        LevelAllTimeCost=[0]*nodesum
        for blockID in Chosen:
            storageNodes = ExpSqrtBlockStorage[blockID - beginID]
            first = storageNodes.pop()
            minCommunicate = CommunicationCost[mynodeid][first]
            minNode = first
            storageNodes.add(first)
            for nodes in storageNodes:
                # print(mynodeid,',,,',nodes)
                commuicate = CommunicationCost[mynodeid][nodes]
                if commuicate < minCommunicate:
                    minCommunicate = commuicate
                    minNode = nodes
            TimeCost = minCommunicate * BlockSizes[blockID - beginID]
            LevelAllTimeCost[minNode]+=(TimeCost)
            # print("level:minnode", minNode)
        # if len(Chosen)!=0:
        #     timemax=max(LevelAllTimeCost)
        # else:
        #     timemax=0
        timemax = 0
        for i in LevelAllTimeCost:
            timemax = timemax + i
        ReturnTimeCost.append(timemax)
    if assigntype&0b100:
        RandomAllTimeCost=[0]*nodesum
        for blockID in Chosen:
            storageNodes = LevelBlockStorage[blockID - beginID]
            first = storageNodes.pop()
            minCommunicate = CommunicationCost[mynodeid][first]
            minNode = first
            storageNodes.add(first)
            for nodes in storageNodes:
                #print(mynodeid,',,,',nodes)
                commuicate = CommunicationCost[mynodeid][nodes]
                if commuicate < minCommunicate:
                    minCommunicate = commuicate
                    minNode = nodes
            TimeCost = minCommunicate * BlockSizes[blockID - beginID]
            RandomAllTimeCost[minNode]+=(TimeCost)
            #print("random:minnode", minNode)
        # if len(Chosen)!=0:
        #     timemax=max(RandomAllTimeCost)
        # else:
        #     timemax=0
        timemax = 0
        for i in RandomAllTimeCost:
            timemax = timemax + i
        ReturnTimeCost.append(timemax)
    if assigntype&0b1000:
        Random1AllTimeCost=[0]*nodesum
        for blockID in Chosen:
            storageNodes = LevelSqrtBlockStorage[blockID - beginID]
            first = storageNodes.pop()
            minCommunicate = CommunicationCost[mynodeid][first]
            minNode = first
            storageNodes.add(first)
            for nodes in storageNodes:
                #print(mynodeid,',,,',nodes)
                commuicate = CommunicationCost[mynodeid][nodes]
                if commuicate < minCommunicate:
                    minCommunicate = commuicate
                    minNode = nodes
            TimeCost = minCommunicate * BlockSizes[blockID - beginID]
            Random1AllTimeCost[minNode]+=(TimeCost)
            #print("random:minnode", minNode)
        # if len(Chosen)!=0:
        #     timemax=max(RandomAllTimeCost)
        # else:
        #     timemax=0
        timemax = 0
        for i in Random1AllTimeCost:
            timemax = timemax + i
        ReturnTimeCost.append(timemax)
    # print(ReturnTimeCost)
    return ReturnTimeCost

def endIDAverageTime(m,beginID,endIDsince,maxlevel,nodesum,assigntype):
    AllTimeMax=[]
    if assigntype not in [0b1,0b11,0b111,0b1111]:
        print("ERROR")
        exit(1)
        return 0
    if assigntype &0b1:
        AllTimeMax.append([])
    if assigntype&0b10:
        AllTimeMax.append([])
    if assigntype&0b100:
        AllTimeMax.append([])
    if assigntype&0b1000:
        AllTimeMax.append([])
    #随机选择一个
    # nodeme=random.randint(0,nodesum-1)
    # timemax=Time_togetBlocksNeededtoProve(m,beginID,endIDsince,maxlevel,nodeme,assigntype,nodesum)
    # for i in range(len(timemax)):
    #     AllTimeMax[i].append(timemax[i])
    #全选求平均
    for nodeid in range(nodesum):
        timemax=Time_togetBlocksNeededtoProve(m,beginID,endIDsince,maxlevel,nodeid,assigntype,nodesum)
        #print(timemax)
        for i in range(len(timemax)):
            AllTimeMax[i].append(timemax[i])
    return np.mean(AllTimeMax,axis=1)

if __name__=='__main__':
    #随链长度变化
    beginID=2016*2
    endID=2016*2+400
    nodesum=10
    m=3
    #低位为1：正比2^n
    #第二位是1：正比2^(n/2)
    #第三位是1：正比level
    #第四位是1：正比\sqrt{level}
    assigntype=0b1111#0b1111=只有ranndom
    piece=1
    maxlevel=init(beginID,endID,nodesum,assigntype,piece)
    assignBlcoksStatically(beginID,endID,nodesum,assigntype,piece)
    AvgTime=[]
    step=50
    totaltimes=10
    MBEGIN=m*15
    for runtimes in range(0, totaltimes):
        AvgTime.append([])
        for endIDSince in range(beginID+MBEGIN,endID,step):
            avgtime=endIDAverageTime(m,beginID,endIDSince,maxlevel,nodesum,assigntype)
            avgtime=np.array(avgtime)
            avgtime=avgtime.flatten()
            AvgTime[runtimes].append(avgtime)#[1,2,3,4]
    AvgTime=np.array(AvgTime)
    ResContainer = AvgTime[0]
    for runtimes in range(1, totaltimes):
        ResContainer = ResContainer + AvgTime[runtimes]
    ResContainer = ResContainer / totaltimes
    filename='./testData-' + str(assigntype)+'-'+str(beginID) + '-' + str(endID)+'-'+str(step)+'-'+str(m)+'-'+str(nodesum)+'-'+str(piece) + '.txt'
    fileoutput=open(filename,'w')
    if assigntype&0b1:
        plt.plot(range(beginID+MBEGIN,endID,step),ResContainer[:,0],color='r',label='exp')
        print(range(beginID+MBEGIN,endID,step),file=fileoutput)
        print('exp',file=fileoutput)
        print(ResContainer[:,0],file=fileoutput)
    if assigntype&0b10:
        plt.plot(range(beginID + MBEGIN, endID,step), ResContainer[:, 1], color='g',label='expsqrt')
        print('expsqrt', file=fileoutput)
        print(ResContainer[:, 1], file=fileoutput)
    if assigntype&0b100:
        plt.plot(range(beginID + MBEGIN, endID,step), ResContainer[:, 2], color='b',label='level')
        print('level', file=fileoutput)
        print(ResContainer[:, 2], file=fileoutput)
    if assigntype&0b1000:
        plt.plot(range(beginID + MBEGIN, endID,step), ResContainer[:, 3], color='y',label='levelsqrt')
        print('levelsqrt', file=fileoutput)
        print(ResContainer[:, 0], file=fileoutput)
    fileoutput.close()
    plt.legend()
    plt.title('avgtime over length of chain')
    plt.xlabel('length of chain')
    plt.ylabel('avgtime')
    #plt.ylim(ymin=1,ymax=3)
    plt.show()
    #链长为2016时随r变化