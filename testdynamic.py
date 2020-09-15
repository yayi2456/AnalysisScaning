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
RandomBlockStorage=[]

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

def calReplicas(blocklevel,piece):
    return pow(2,blocklevel-1)*piece

def generateNodesCommunicationCost_norm(nodesnums):
    mu=0.5
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
    #random
    blocklevel = BlockLists[blockID - beginID][0]
    r = calReplicas(blocklevel, piece)
    randnode = random.randint(0, nodesum-1)
    RandomBlockStorage.append({randnode})
    if r>nodesum:
        r=nodesum
    r-=1
    while r:
        randnode = random.randint(0, nodesum-1)
        if randnode not in RandomBlockStorage[blockID-beginID]:
            RandomBlockStorage[blockID-beginID].add(randnode)
            r-=1
    return

def initialNewComingBlock(beginID,blockID,nodesum,piece):
    randnode=random.randint(0,nodesum-1)
    RandomBlockStorage.append({randnode})
    print("LOG:new block is coming... blockid=",blockID,', randomnode=',randnode)

def printAssignRes(beginID,endID,piece):
    filename = './initialAssign-' + str(beginID) + '-' + str(endID) + '.txt'
    fileoutput = open(filename, 'w')
    for blockID in range(beginID,endID):
        print('blockID:',blockID,' , level:',BlockLists[blockID-beginID][0],', replicanums:', calReplicas(BlockLists[blockID-beginID][0],piece),',replicaactually:',len(RandomBlockStorage[blockID-beginID]), ',replicas:',RandomBlockStorage[blockID-beginID],file=fileoutput)
    fileoutput.close()

def init(beginID,endID,endIDpreassign,nodesums,assigntype,piece):#assigntype=001=只有新方法，011=level+新方法，111=random+level+新方法
    loadData(beginID,endID)
    maxlevel = buildBlockList(beginID, endID)
    generateCommunicationCost_1(nodesums)
    loadData_Sizes(beginID,endID)
    for blockID in range(beginID,endIDpreassign):
        initialAssignOneBlock(beginID,endID,blockID,nodesums,assigntype,piece)
    #printAssignRes(beginID,endID,piece)
    return maxlevel

def dynamicRep(nodesum,Chosen,mynodeid,beginID,endIDsince):
    allrepblocknums=int(len(Chosen)/nodesum)
    allrepblocks=random.sample(range(0,len(Chosen)),allrepblocknums)
    print("LOG:dynamic: mynodeid=",mynodeid,', blocks=')
    for blockid in allrepblocks:
        RandomBlockStorage[Chosen[blockid]-beginID].add(mynodeid)
        print('\t blockid=',Chosen[blockid],', nodeplace=',mynodeid)

def Time_togetBlocksNeededtoProve(m,beginID,endIDsince,maxlevel,mynodeid,assigntype,nodesum):
    assigntype=0b111
    if assigntype not in [0b1,0b11,0b111]:
        print("ERROR")
        exit(1)
        return 0
    Chosen = scanBlockList_noRepeat(m, beginID, endIDsince, maxlevel)
    AllTimeCost=[0]*nodesum
    if assigntype==0b111:
        RandomAllTimeCost=[0]*nodesum
        for blockID in Chosen:
            # minCommunicate=min(CommunicationCost[mynodeid])
            # minNode=np.argmin(CommunicationCost[mynodeid])
            storageNodes = RandomBlockStorage[blockID - beginID]
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
        if len(Chosen)!=0:
            timemax=max(RandomAllTimeCost)
        else:
            timemax=0
        dynamicRep(nodesum,Chosen,mynodeid,beginID,endIDSince)
    return timemax

def endIDAverageTime(m,beginID,endIDsince,maxlevel,nodesum,assigntype,lambdai):
    AllTimeMax=[]
    allaccessnodes=random.sample(range(0,nodesum),lambdai)
    for nodeid in allaccessnodes:
        timemax=Time_togetBlocksNeededtoProve(m,beginID,endIDsince,maxlevel,nodeid,assigntype,nodesum)
        #print(timemax)
        AllTimeMax.append(timemax)
    return AllTimeMax#np.mean(AllTimeMax,axis=1)###

if __name__=='__main__':
    #随链长度变化
    beginID=2016*2
    tailnodes=50
    beginnodes=200
    endID=beginnodes+beginID+tailnodes
    nodesum=10
    m=3
    assigntype=0b0
    piece=2
    lambdai=7
    maxlevel=init(beginID,endID,beginID+beginnodes,nodesum,assigntype,piece)
    AvgTime=[]
    step=1
    for endIDSince in range(beginID+beginnodes,endID,step):
        avgtime=endIDAverageTime(m,beginID,endIDSince,maxlevel,nodesum,assigntype,lambdai)
        AvgTime.append(avgtime)
        initialNewComingBlock(beginID,endIDSince,nodesum,piece)
    printAssignRes(beginID,endIDSince,1)
    AvgTime=np.array(AvgTime)

    filename='./testData-' + str(assigntype)+'-'+str(beginID) + '-' + str(endID)+'-'+str(step)+'-'+str(m)+'-'+str(nodesum)+'-'+str(piece) + '.txt'
    fileoutput=open(filename,'w')

    AvgTime=AvgTime.flatten()
    print(AvgTime)
    plt.plot(range(0,lambdai*tailnodes),AvgTime,color='r',marker='.')
    # plt.plot(range(0,lambdai),AvgTime[0],color='r')
    # plt.plot(range(lambdai, 2*lambdai), AvgTime[1], color='g')
    # plt.plot(range(lambdai*2, lambdai*3), AvgTime[2], color='b')
    # plt.plot(range(lambdai*3, 4*lambdai), AvgTime[3], color='y')
    for i in range(tailnodes):
        plt.axvline(x=lambdai*(i+1),color='g')
    print(range(beginID+m,endID,step),file=fileoutput)
    print(AvgTime,file=fileoutput)
    fileoutput.close()
    # plt.legend()
    plt.title('avgtime over length of chain')
    plt.xlabel('length of chain')
    plt.ylabel('avgtime')
    # plt.ylim(ymin=0,ymax=2)
    plt.show()
    #链长为2016时随r变化