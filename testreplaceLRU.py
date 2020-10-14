import logging
import math
import re
import random
import json
import matplotlib.pyplot as plt
import numpy as np

Bits=[]#每2016存1个
Targets=[]#通过Bits计算得到
BlockHashes=[]
BlockLists=[]
CommunicationCost=[]
BlockSizes=[]
StorageOwned=[]
#静态块存储
ExpBlockStorage=[]
# ExpBlockLiveTime=[]
ExpSqrtBlockStorage=[]
# ExpSqrtBlockLiveTime=[]
LevelBlockStorage=[]
# LevelBlockLiveTime=[]
LevelSqrtBlockStorage=[]
# LevelSqrtBlockLiveTime=[]
PERIOD=np.inf
#热度统计
ExpNodesBlocksPopularity=[]
#最大存储使用量
ExpNodeStorageUsed=[]

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
    storageOwned=0
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
            storageOwned=storageOwned+blocksize
    return storageOwned

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
    for i in range(nodesum):
        ExpNodesBlocksPopularity.append({})
    #exp
    nodeid=blockID%nodesum
    blocklevel=BlockLists[blockID-beginID][0]
    timelived=calReplicas_exp(blocklevel, PERIOD)
    if assigntype&0b1:
        replicates = calReplicas_exp(blocklevel, piece)
        if nodesum<replicates:
            replicates=nodesum
        nodereplicas=random.sample(range(0,nodesum),replicates)
        ExpBlockStorage.append({})
        for nodeid in nodereplicas:
            ExpBlockStorage[blockID - beginID][nodeid]=timelived
            if nodeid in ExpBlockStorage[blockID - beginID]:
                ExpNodeStorageUsed[nodeid]+=BlockSizes[blockID-beginID]
            ExpNodesBlocksPopularity[nodeid][blockID]=0
    #expsqrt
    if assigntype&0b10:
        replicates = calReplicas_expsqrt(blocklevel, piece)
        if nodesum < replicates:
            replicates = nodesum
        nodereplicas = random.sample(range(0, nodesum), replicates)
        ExpSqrtBlockStorage.append({})
        for nodeid in nodereplicas:
            ExpSqrtBlockStorage[blockID - beginID][nodeid]=timelived
    #level
    if assigntype&0b100:
        replicates = calReplicas_level(blocklevel, piece)
        if nodesum < replicates:
            replicates = nodesum
        nodereplicas = random.sample(range(0, nodesum), replicates)
        LevelBlockStorage.append({})
        for nodeid in nodereplicas:
            LevelBlockStorage[blockID - beginID][nodeid]=timelived
    if assigntype&0b1000:
        replicates = calReplicas_levelsqrt(blocklevel, piece)
        if nodesum < replicates:
            replicates = nodesum
        nodereplicas = random.sample(range(0, nodesum), replicates)
        LevelSqrtBlockStorage.append({})
        for nodeid in nodereplicas:
            LevelSqrtBlockStorage[blockID - beginID][nodeid]=timelived
    return

def initialNewComingBlock_1(beginID,blockID,nodesum,assigntype,piece):
    if assigntype==0b0 or assigntype>0b1111:
        print("ERROR")
        exit(1)
    blocklevel = BlockLists[blockID - beginID][0]
    randnode = random.randint(0, nodesum - 1)
    timelived=calReplicas_exp(blocklevel,PERIOD)
    if assigntype & 0b1:
        ExpBlockStorage.append({})
        ExpBlockStorage[blockID-beginID][randnode]=timelived
        if randnode not in ExpBlockStorage[blockID - beginID]:
            ExpNodeStorageUsed[randnode] += BlockSizes[blockID - beginID]
        ExpNodesBlocksPopularity[randnode][blockID] = 0
    if assigntype & 0b10:
        ExpSqrtBlockStorage.append({})
        ExpSqrtBlockStorage[blockID-beginID][randnode]=timelived
    if assigntype & 0b100:
        LevelBlockStorage.append({})
        LevelBlockStorage[blockID-beginID][randnode]=timelived
    if assigntype&0b1000:
        LevelSqrtBlockStorage.append({})
        LevelSqrtBlockStorage[blockID-beginID][randnode]=timelived

def initialNewComingBlock_2_n(beginID,blockID,nodesum,assigntype,piece):
    initialAssignOneBlock(beginID,0,blockID,nodesum,assigntype,piece)
def initialNewComingBlock_All(beginID,blockID,nodesum,assigntype,piece):
    if assigntype==0b0 or assigntype>0b1111:
        print("ERROR")
        exit(1)
    for i in range(nodesum):
        ExpNodesBlocksPopularity.append({})
    #all
    nodeid=blockID%nodesum
    blocklevel=BlockLists[blockID-beginID][0]
    timelived=calReplicas_exp(blocklevel, PERIOD)
    replicates=nodesum
    nodereplicas=random.sample(range(0,nodesum),replicates)
    ExpBlockStorage.append({})
    for nodeid in nodereplicas:
        ExpBlockStorage[blockID - beginID][nodeid]=timelived
        if nodeid in ExpBlockStorage[blockID - beginID]:
            ExpNodeStorageUsed[nodeid]+=BlockSizes[blockID-beginID]
        ExpNodesBlocksPopularity[nodeid][blockID]=0
    return

def dynamicRep(nodesum,Chosen,mynodeid,beginID,assigntype):
    allrepblocknums=int(len(Chosen)/(nodesum))
    allrepblocks=random.sample(range(0,len(Chosen)),allrepblocknums)
    #print("LOG:dynamic: mynodeid=",mynodeid,', blocks=')
    for blockid in allrepblocks:
        blocklevel=BlockLists[Chosen[blockid]-beginID][0]
        timelived=calReplicas_exp(blocklevel, PERIOD)
        if assigntype & 0b1:
            ExpBlockStorage[Chosen[blockid]-beginID][mynodeid] = timelived ###
            if mynodeid not in ExpBlockStorage[Chosen[blockid] - beginID]:
                ExpNodeStorageUsed[mynodeid] += BlockSizes[Chosen[blockid] - beginID]
            if Chosen[blockid] not in ExpNodesBlocksPopularity[mynodeid]:
                ExpNodesBlocksPopularity[mynodeid][Chosen[blockid]]=0
        if assigntype & 0b10:
            ExpSqrtBlockStorage[Chosen[blockid]-beginID][mynodeid] = timelived  ###
        if assigntype & 0b100:
            LevelBlockStorage[Chosen[blockid]-beginID][mynodeid] = timelived ###
        if assigntype & 0b1000:
            LevelSqrtBlockStorage[Chosen[blockid]-beginID][mynodeid] = timelived  ###
    logging.info('node %d received %d blocks, %d blocks are stored.', mynodeid, len(Chosen), len(allrepblocks))

def dynamicRep_propularity(nodesum,Chosen,mynodeid,beginID,assigntype,chosenPopularity):
    if assigntype&0b1110!=0:
        exit(-1)
    allrepblocknums = int(len(Chosen) / (nodesum))
    allrepblocks=[]
    #按照key的大小排序，大的在前
    kvs = sorted(chosenPopularity.items(), key=lambda x: x[1], reverse=True)
    kvs = kvs[:allrepblocknums]
    for blocks in kvs:
        allrepblocks.append(blocks[0])
    # allrepblocks = random.sample(range(0, len(Chosen)), allrepblocknums)
    # print("LOG:dynamic: mynodeid=",mynodeid,', blocks=')
    for blockID in allrepblocks:
        blocklevel = BlockLists[blockID - beginID][0]
        timelived = calReplicas_exp(blocklevel, PERIOD)
        ExpBlockStorage[blockID - beginID][mynodeid] = timelived  ###
        if mynodeid not in ExpBlockStorage[blockID - beginID]:
            ExpNodeStorageUsed[mynodeid] += BlockSizes[blockID - beginID]
        if blockID not in ExpNodesBlocksPopularity[mynodeid]:
            ExpNodesBlocksPopularity[mynodeid][blockID] = 0
def dynamicRep_cost(nodesum,Chosen,mynodeid,beginID,assigntype,chosenCost):
    if assigntype&0b1110!=0:
        exit(-1)
    allrepblocknums = int(len(Chosen) / (nodesum))
    allrepblocks=[]
    #按照key的大小排序，大的在前
    kvs = sorted(chosenCost.items(), key=lambda x: x[1], reverse=True)
    kvs = kvs[:allrepblocknums]
    for blocks in kvs:
        allrepblocks.append(blocks[0])
    # allrepblocks = random.sample(range(0, len(Chosen)), allrepblocknums)
    # print("LOG:dynamic: mynodeid=",mynodeid,', blocks=')
    for blockID in allrepblocks:
        blocklevel = BlockLists[blockID - beginID][0]
        timelived = calReplicas_exp(blocklevel, PERIOD)
        ExpBlockStorage[blockID - beginID][mynodeid] = timelived  ###
        if mynodeid not in ExpBlockStorage[blockID - beginID]:
            ExpNodeStorageUsed[mynodeid] += BlockSizes[blockID - beginID]
        if blockID not in ExpNodesBlocksPopularity[mynodeid]:
            ExpNodesBlocksPopularity[mynodeid][blockID] = 0
def activeDynamicRep(nodesum,beginID,assigntype,times,topnumbers,nodenumbers):
    if assigntype&0b1110!=0:
        exit(-1)
    for nodeid in range(nodesum):
        kvs = sorted(ExpNodesBlocksPopularity[nodeid].items(), key=lambda x: x[1], reverse=True)
        kvs=kvs[:topnumbers]
        nodesreplicas=random.sample(range(nodesum),nodenumbers)
        for nodes in nodesreplicas:
            for blocks in kvs:
                blocklevel = BlockLists[blocks[0] - beginID][0]
                timelived = calReplicas_exp(blocklevel, PERIOD)
                ExpBlockStorage[blocks[0]-beginID][nodes]=timelived
                if nodes not in ExpBlockStorage[blocks[0]-beginID]:
                    ExpNodeStorageUsed[nodes] += BlockSizes[blocks[0] - beginID]
                if blocks[0] not in ExpNodesBlocksPopularity[nodes]:
                    ExpNodesBlocksPopularity[nodes][blocks[0]] = 0
    logging.info('active-dynamic OK.')

def activedynamic_calculate(nodesum,beginID,assigntype,times,topnumbers):
    if assigntype&0b1110!=0:
        exit(-1)
    for nodeid in range(nodesum):
        kvs = sorted(ExpNodesBlocksPopularity[nodeid].items(), key=lambda x: x[1], reverse=True)
        kvs=kvs[:topnumbers]
        # nodesreplicas=random.sample(range(nodesum),nodenumbers)
        nodesreplicas={}
        for blocks in kvs:
            maximprove=0
            maxiprovenode=nodeid
            blockID = blocks[0]
            for nodes in range(nodesum):
                allsavedcost=0
                for allnodesaved in range(nodesum):
                    nodesavedcost=0
                    storageNodes = ExpBlockStorage[blockID - beginID].keys()
                    minCommunicate = 100
                    minNode = -1
                    for nodesstore in storageNodes:
                        commuicate = CommunicationCost[allnodesaved][nodesstore]
                        if commuicate < minCommunicate:
                            minCommunicate = commuicate
                            minNode = nodes
                    if minCommunicate>CommunicationCost[allnodesaved][nodes]:
                        nodesavedcost+=BlockSizes[blockID-beginID]*(minCommunicate-CommunicationCost[allnodesaved][nodes])
                        allsavedcost+=nodesavedcost
                if allsavedcost>maximprove:
                    maximprove=allsavedcost
                    maxiprovenode=nodes
            # print("maxiprove node=",maxiprovenode,', maxiprove=',maximprove,'singing node=',nodeid,', processing block=',blockID)
            #得到block的最佳位置
            blocklevel = BlockLists[blockID - beginID][0]
            timelived = calReplicas_exp(blocklevel, PERIOD)
            ExpBlockStorage[blocks[0] - beginID][maxiprovenode] = timelived
            if maxiprovenode not in ExpBlockStorage[blocks[0] - beginID]:
                ExpNodeStorageUsed[maxiprovenode] += BlockSizes[blocks[0] - beginID]
            if blockID not in ExpNodesBlocksPopularity[maxiprovenode]:
                ExpNodesBlocksPopularity[maxiprovenode][blocks[0]] = 0
    logging.info('active-dynamic-calculate OK.')

def updateLiveTimeandExpel(beginID,endSince,nodesum,assigntype,step):
    if assigntype==0b0 or assigntype>0b1111:
        print("ERROR")
        exit(1)
    #更新剩余生命期限
    ExpDeadBlocks=[]
    ExpSqrtDeadBlocks=[]
    LevelDeadBlocks = []
    LevelSqrtDeadBlocks = []
    for blockID in range(beginID,endSince):
        if assigntype & 0b1:
            ExpDeadBlocks.append([])
            for kv in ExpBlockStorage[blockID-beginID].items():
                if kv[1]<=step:
                    ExpDeadBlocks[blockID-beginID].append(kv[0])
                ExpBlockStorage[blockID-beginID][kv[0]]-=step
        if assigntype & 0b10:
            ExpSqrtDeadBlocks.append([])
            for kv in ExpSqrtBlockStorage[blockID-beginID].items():
                if kv[1]<=step:
                    ExpSqrtDeadBlocks[blockID-beginID].append(kv[0])
                ExpSqrtBlockStorage[blockID-beginID][kv[0]]-=step
        if assigntype & 0b100:
            LevelDeadBlocks.append([])
            for kv in LevelBlockStorage[blockID - beginID].items():
                if kv[1]<=step:
                    LevelDeadBlocks[blockID-beginID].append(kv[0])
                LevelBlockStorage[blockID-beginID][kv[0]]-=step
        if assigntype & 0b1000:
            LevelSqrtDeadBlocks.append([])
            for kv in LevelSqrtBlockStorage[blockID - beginID].items():
                if kv[1]<=step:
                    LevelSqrtDeadBlocks[blockID-beginID].append(kv[0])
                LevelSqrtBlockStorage[blockID-beginID][kv[0]]-=step
    logging.info('all blocks\' age updated.')
    #清除死块
    strexp=''
    for blockID in range(beginID,endSince):
        if assigntype&0b1:
            strexpchild=''
            for i in ExpDeadBlocks[blockID-beginID]:
                if len(ExpBlockStorage[blockID-beginID])>1:
                    ExpNodesBlocksPopularity[i].pop(blockID)
                    ExpBlockStorage[blockID-beginID].pop(i)
                    if i in ExpBlockStorage[blockID-beginID]:
                        ExpNodeStorageUsed[i] -= BlockSizes[blockID - beginID]
                    # print(ExpNodesBlocksPopularity[i])
                    strexpchild+=str(i)+','
            if strexpchild:
                strexp+='['+str(blockID)+']:'+strexpchild
        if assigntype & 0b10:
            for i in ExpSqrtDeadBlocks[blockID-beginID]:
                if len(ExpSqrtBlockStorage[blockID - beginID]) > 1:
                    ExpSqrtBlockStorage[blockID-beginID].pop(i)
        if assigntype&0b100:
            for i in LevelDeadBlocks[blockID-beginID]:
                if len(LevelBlockStorage[blockID - beginID]) > 1:
                    LevelBlockStorage[blockID-beginID].pop(i)
        if assigntype&0b1000:
            for i in LevelDeadBlocks[blockID-beginID]:
                if len(LevelSqrtBlockStorage[blockID - beginID]) > 1:
                    LevelSqrtBlockStorage[blockID-beginID].pop(i)
    logging.info('dead blocks:{} sweeped.'.format(strexp))



def printAssignRes(beginID,endID,assigntype,piece):
    filename = './LRUAssign-' + str(beginID) + '-' + str(endID) + '.txt'
    fileoutput = open(filename, 'w')
    for blockID in range(beginID,endID):
        stractually=',replicaactually:'
        if assigntype&0b1:
            stractually+='exp: '+str(len(ExpBlockStorage[blockID-beginID]))+','
        if assigntype&0b10:
            stractually += 'expsqrt: ' + str(len(ExpSqrtBlockStorage[blockID - beginID])) + ','
        if assigntype&0b100:
            stractually+='level: '+str(len(LevelBlockStorage[blockID-beginID]))+','
        if assigntype&0b1000:
            stractually += 'levelsqrt: ' + str(len(LevelSqrtBlockStorage[blockID - beginID])) + ','

        print('blockID:',blockID,' , level:',BlockLists[blockID-beginID][0],', replicanums-exp\expsqrt\level\levelsqrt:', calReplicas_exp(BlockLists[blockID-beginID][0],piece),',', calReplicas_expsqrt(BlockLists[blockID-beginID][0],piece),
              ',', calReplicas_level(BlockLists[blockID-beginID][0],piece),',', calReplicas_levelsqrt(BlockLists[blockID-beginID][0],piece),
              stractually,
              file=fileoutput)
    fileoutput.close()

def init(beginID,endID,endIDpreassign,nodesums,assigntype,piece):
    loadData(beginID,endID)
    maxlevel = buildBlockList(beginID, endID)
    generateCommunicationCost_1(nodesums)
    storageOwned=loadData_Sizes(beginID,endID)
    global StorageOwned
    StorageOwned=[storageOwned/(nodesums)]*nodesums
    global ExpNodeStorageUsed
    ExpNodeStorageUsed=[0]*nodesum
    return maxlevel

def assignBlcoksStatically(beginID,endID,nodesums,assigntype,piece):
    for blockID in range(beginID,endID):
        initialAssignOneBlock(beginID,endID,blockID,nodesums,assigntype,piece)
    printAssignRes(beginID,endID,assigntype,piece)

def Time_togetBlocksNeededtoProve(m,beginID,endIDsince,maxlevel,mynodeid,assigntype,nodesum,replicatype):
    if assigntype not in [0b1,0b11,0b111,0b1111]:
        print("ERROR")
        exit(1)
        return 0
    ReturnTimeCost=[]
    Chosen = scanBlockList_noRepeat(m, beginID, endIDsince, maxlevel)
    # print(Chosen)
    logging.info('AT endIDsince={}, node {} is requesting {:}...'.format(endIDsince,mynodeid,Chosen))
    ExpChosenPopularity = {}
    ExpChosenCost = {}
    if assigntype&0b1:
        AllTimeCost=[0]*nodesum
        for blockID in Chosen:
            storageNodes=ExpBlockStorage[blockID-beginID].keys()
            minCommunicate=100
            minNode=-1
            for nodes in storageNodes:
                commuicate=CommunicationCost[mynodeid][nodes]
                if commuicate<minCommunicate:
                    minCommunicate=commuicate
                    minNode=nodes
            TimeCost=minCommunicate*BlockSizes[blockID-beginID]
            AllTimeCost[minNode]+=TimeCost
            #更新存储空间记录
            if minNode!=mynodeid:
                ExpNodesBlocksPopularity[minNode][blockID]+=1
            #记录popularity
            ExpChosenPopularity[blockID]=ExpNodesBlocksPopularity[minNode][blockID]
            #记录cost
            ExpChosenCost[blockID]=TimeCost
        ##并行的接受
        # if len(Chosen) != 0:
        #     timemax = max(AllTimeCost)
        # else:
        #     timemax = 0
        #串行的接受
        timemax=0
        for i in AllTimeCost:
            timemax=timemax+i
        ReturnTimeCost.append(timemax)
    if assigntype&0b10:
        LevelAllTimeCost=[0]*nodesum
        for blockID in Chosen:
            storageNodes = ExpSqrtBlockStorage[blockID - beginID].keys()
            # first = storageNodes.pop()
            # minCommunicate = CommunicationCost[mynodeid][first]
            # minNode = first
            # storageNodes.add(first)
            minCommunicate = 100
            minNode = 0
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
            storageNodes = LevelBlockStorage[blockID - beginID].keys()
            # first = storageNodes.pop()
            # minCommunicate = CommunicationCost[mynodeid][first]
            # minNode = first
            # storageNodes.add(first)
            minCommunicate = 100
            minNode = 0
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
            storageNodes = LevelSqrtBlockStorage[blockID - beginID].keys()
            # first = storageNodes.pop()
            # minCommunicate = CommunicationCost[mynodeid][first]
            # minNode = first
            # storageNodes.add(first)
            minCommunicate = 100
            minNode = 0
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
    logging.info('request processed. blocks got.')
    # print(ReturnTimeCost)
    if replicatype==0:
        #随机的requester复制
        dynamicRep(nodesum, Chosen, mynodeid, beginID, assigntype)#(nodesum,Chosen,mynodeid,beginID,assigntype):
    elif replicatype==1:
        #使用热度的requester复制
        dynamicRep_propularity(nodesum,Chosen,mynodeid,beginID,assigntype,ExpChosenPopularity)
    elif replicatype==2:
        #使用负载的requester复制
        dynamicRep_propularity(nodesum, Chosen, mynodeid, beginID, assigntype, ExpChosenCost)

    return ReturnTimeCost

def endIDAverageTime(m,beginID,endIDsince,maxlevel,nodesum,assigntype,lambdai,replicatype):
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
    # for nodeid in range(nodesum):
    #     timemax=Time_togetBlocksNeededtoProve(m,beginID,endIDsince,maxlevel,nodeid,assigntype,nodesum)
    #     #print(timemax)
    #     for i in range(len(timemax)):
    #         AllTimeMax[i].append(timemax[i])
    #随机选择lambdai个
    allaccessnodes = []
    for i in range(lambdai):
        allaccessnodes.append(random.randint(0,nodesum-1))
    for nodeid in allaccessnodes:
        timemax=Time_togetBlocksNeededtoProve(m,beginID,endIDsince,maxlevel,nodeid,assigntype,nodesum,replicatype)
        #print(timemax)
        for i in range(len(timemax)):
            AllTimeMax[i].append(timemax[i])
    logging.info('{} nodes have finished their request, with time cost {:}'.format(lambdai,AllTimeMax))
    return AllTimeMax#np.mean(AllTimeMax,axis=1)###

def preAssign(beginID,endID,endIDpreassign,nodesums,assigntype,piece):
    for blockID in range(beginID,endIDpreassign):
        initialAssignOneBlock(beginID,endID,blockID,nodesums,assigntype,piece)

if __name__=='__main__':
    # 随链长度变化
    beginID = 2016
    tailnodes = 200
    beginnodes = 200
    endID = beginnodes + beginID + tailnodes
    nodesum = 10
    m = 3
    assigntype = 0b1
    piece = 1
    lambdai = 4
    replicatype=-1
    activeReplicaType=0#1A2AC0关闭
    ##
    logfilename = './LRU' +str(beginID)+'-'+str(beginnodes)+'-'+str(tailnodes)+'-'+str(nodesum)+'-'+str(piece)+'-'+str(lambdai)+'-'+str(PERIOD)+ '.log'
    logging.basicConfig(filename=logfilename, level=logging.INFO,filemode='w')
    maxlevel = init(beginID, endID, beginID + beginnodes, nodesum, assigntype, piece)#(beginID,endID,nodesums,assigntype,piece):
    AvgTime = []
    step = 1
    totaltimes = 1  # 减小所得点的波动
    for runtimes in range(0, totaltimes):
        logging.info(('runtime %d begin...'),runtimes)
        AvgTime.append([])
        ExpBlockStorage.clear()
        ExpSqrtBlockStorage.clear()
        LevelBlockStorage.clear()
        LevelSqrtBlockStorage.clear()
        preAssign(beginID, endID, beginID + beginnodes, nodesum, assigntype, piece)
        logging.info('preAssign done. blcok %d to %d have been assigned.',beginID,beginID+beginnodes)
        EachNodeStorageChange=[]
        EachBlockInStorage=[0]
        for i in range(beginID,beginID+beginnodes):
            EachBlockInStorage[0]+=BlockSizes[i-beginID]
        fname = 'LRU-ExpNodeStorageUsed.txt'
        foutput = open(fname, 'w')
        print('blocksSize:', StorageOwned[0] * nodesum, file=foutput)
        for endIDSince in range(beginID + beginnodes, endID, step):
            avgtime = endIDAverageTime(m, beginID, endIDSince, maxlevel, nodesum, assigntype, lambdai,replicatype)
            AvgTime[runtimes].append(avgtime)
            updateLiveTimeandExpel(beginID, endIDSince, nodesum, assigntype,step)
            for allblocks in range(step):
                # initialNewComingBlock_All(beginID,endIDSince+allblocks,nodesum,assigntype,piece)
                initialNewComingBlock_2_n(beginID, endIDSince+allblocks, nodesum,assigntype, piece)#(beginID,blockID,nodesum,assigntype,piece):
            if activeReplicaType==1:
                activeDynamicRep(nodesum,beginID,assigntype,0,3,1)
            elif activeReplicaType==2:
                activedynamic_calculate(nodesum,beginID,assigntype,0,3)
            #清空
            for nodes in range(nodesum):
                for key in ExpNodesBlocksPopularity[nodes].keys():
                    ExpNodesBlocksPopularity[nodes][key]=0
            ######storage record
    #         print('blockID=',endIDSince,':',BlockSizes[endIDSince-beginID],':',ExpNodeStorageUsed,file=foutput)
    #         nodesshow=10
    #         for i in range(nodesshow):
    #             EachNodeStorageChange.append([])
    #             EachNodeStorageChange[i].append(ExpNodeStorageUsed[i])
    #         addstorage=0
    #         for i in range(step):
    #             addstorage+=BlockSizes[endIDSince-beginID+i]
    #         EachBlockInStorage.append(EachBlockInStorage[len(EachBlockInStorage)-1]+addstorage)
    # colors = ['r', 'g', 'b', 'grey', 'purple', 'yellow', 'pink', 'orange', 'black', 'gold']
    # labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    # filenamestoragesize='./LRU-StorageSize-'+str(replicatype)+'-'+str(activeReplicaType)+str(beginnodes)+'-'+str(endID)+'-'+str(lambdai)+'.txt'
    # with open(filenamestoragesize,'w') as filestorage:
    #     print(beginnodes+beginID,' ',endID,' ',step,file=filestorage)
    #     print('ALL',file=filestorage)
    #     print(json.dumps(EachBlockInStorage[:len(EachBlockInStorage)-1]),file=filestorage)
    #     print("EACH",file=filestorage)
    #     for i in range(nodesshow):
    #         print(json.dumps(EachNodeStorageChange[i]),file=filestorage)
    ###plotstorageActual
    # plt.plot(range(beginID+beginnodes,endID,step),EachBlockInStorage[:len(EachBlockInStorage)-1],color='r',label='chain size')#,marker='.')
    # plt.plot(range(beginID + beginnodes, endID, step), EachNodeStorageChange[0], color='b', label='node 0 storage size')#, marker='+')
    # plt.plot(range(beginID + beginnodes, endID, step), EachNodeStorageChange[1], color='y',
    #          label='node 1 storage size')  # , marker='+')
    # plt.plot(range(beginID + beginnodes, endID, step), EachNodeStorageChange[2], color='g',
    #          label='node 2 storage size')  # , marker='+')
    # plt.plot(range(beginID + beginnodes, endID, step), EachNodeStorageChange[3], color='purple',
    #          label='node 3 storage size')  # , marker='+')
    # plt.plot(range(beginID + beginnodes, endID, step), EachNodeStorageChange[4], color='grey',
    #          label='node 4 storage size')  # , marker='+')
    # plt.plot(range(beginID + beginnodes, endID, step), EachNodeStorageChange[5], color='pink',
    #          label='node 5 storage size')  # , marker='+')
    # plt.legend()
    # plt.xlabel('blocks')
    # plt.ylabel('storage sizes')
    # plt.show()
    # exit(1)
    #plotstoragePercetile
    # for i in range(nodesshow):
    #     plt.plot(range(beginID+beginnodes,endID,step),np.array(EachNodeStorageChange[i])/np.array(EachBlockInStorage[:len(EachBlockInStorage)-1]),color=colors[i],label=labels[i])
    # plt.legend()
    # plt.xlabel('blocks')
    # plt.ylabel('node storage size/all blocksize')
    # plt.ylim(ymin=0,ymax=.5)
    # plt.show()
    # exit(2)
    ###plot avgtime
    printAssignRes(beginID, endID,assigntype, piece)
    AvgTime = np.array(AvgTime)
    ResContainer = AvgTime[0]
    for runtimes in range(1, totaltimes):
        ResContainer = ResContainer + AvgTime[runtimes]
    ResContainer = ResContainer / totaltimes
    filename = './LRUtestData-' + str(replicatype)+'-'+str(activeReplicaType)+'-'+str(totaltimes)+'-'+str(PERIOD)+'-'+str(beginID)+'-'+str(beginnodes)+'-'+str(tailnodes)+'-'+str(nodesum)+'-'+str(piece)+'-'+str(lambdai)+'-'+str(PERIOD)+'-'+str(step)+  '.txt'
    fileoutput = open(filename, 'w')
    #求平均：
    ResContainer=np.mean(ResContainer,axis=2)
    # ResContainer = ResContainer.flatten()
    i=0
    print(beginID + beginnodes,' ', endID,' ', step, file=fileoutput)
    if assigntype&0b1:
        plt.plot(range(beginID+beginnodes,endID,step),ResContainer[:,i],marker='.',color='r')
        print('exp:', file=fileoutput)
        print(ResContainer[:,i], file=fileoutput)
        i+=1
    if assigntype & 0b10:
        plt.plot(range(beginID + beginnodes, endID,step), ResContainer[:, i], marker='+',color='g')
        print('expsqrt:', file=fileoutput)
        print(ResContainer[:, i], file=fileoutput)
        i += 1
    if assigntype & 0b100:
        plt.plot(range(beginID + beginnodes, endID,step), ResContainer[:, i], marker='^',color='b')
        print('level:', file=fileoutput)
        print(ResContainer[:, i], file=fileoutput)
        i += 1
    if assigntype & 0b1000:
        plt.plot(range(beginID + beginnodes, endID,step), ResContainer[:, i], marker='s',color='y')
        print('levelsqrt:', file=fileoutput)
        print(ResContainer[:, i], file=fileoutput)
        i += 1
    # for i in range(tailnodes):
    #     plt.plot(range(lambdai * i, lambdai * (i + 1)), ResContainer[i], color='r', marker='.')
    # 分割线
    # for i in range(-1,tailnodes):
    #     plt.axvline(x=lambdai*(i+1),color='grey')
    fileoutput.close()
    # plt.legend()
    plt.title('avgtime over length of chain (lambda=' + str(lambdai))
    plt.xlabel('length of chain')
    plt.ylabel('avgtime')
    # plt.ylim(ymin=0,ymax=2)
    plt.show()
    exit(3)
    # 链长为2016时随r变化

    """
    1. 脱离了NIPOPOW，在某个具体的块访问热度模型下，算法的表现
    2. 在算法运行过程中，每个epoch内，块的副本利用率(该epoch内该块被需求次数/该块的副本个数）
    3. 不考虑FC的尾巴，测一下在其概率分布下，算法的表现
    4. 重新获取驱逐策略的数据
    """