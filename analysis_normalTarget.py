import re
import matplotlib.pyplot as plt
import numpy as np
Bits='1d00ffff'
Targets=0
BlockHashes=[]
BlockLists=[]
BlockSizes=[]
CapacityofNodes=[]
TotalStorageSpaceNeeded=0#=expandFactor*totalsize
expandFactor=500
CommunicationCost=[]#节点不变，只一次
WhichNodeistheBlockStored={}
LevelBlocks=[]
OnlyLevelBlocks=[]

def clearGlobal():
    global Targets
    Targets=0
    global BlockHashes
    BlockHashes=[]
    global BlockLists
    BlockLists=[]
    # global BlockSizes
    # BlockSizes=[]
    # global TotalStorageSpaceNeeded
    # TotalStorageSpaceNeeded= 0  # =expandFactor*totalsize
    global WhichNodeistheBlockStored
    WhichNodeistheBlockStored = {}
    global LevelBlocks
    LevelBlocks=[]
    global OnlyLevelBlocks
    OnlyLevelBlocks=[]


def loadData_Hashes(beginID, endID):
    filedataname = 'E:/CUB/bh.dat/bh.dat'
    with open(filedataname, 'r') as datafile:
        for dataline in datafile:
            datalineitem = dataline.split()
            # 只取height和hash
            datalineitem = datalineitem[:2]
            blockID = int(datalineitem[0])
            if blockID < beginID:
                continue
            if blockID >= endID:
                break
            blockHash = datalineitem[1]
            BlockHashes.append(blockHash)

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


def calTotalSpaceNeeded():
    totalsize=0
    global TotalStorageSpaceNeeded
    for blocksize in BlockSizes:
        totalsize+=blocksize
    TotalStorageSpaceNeeded=totalsize*expandFactor
    if TotalStorageSpaceNeeded != int(TotalStorageSpaceNeeded):
        TotalStorageSpaceNeeded=int(TotalStorageSpaceNeeded)+1
    return TotalStorageSpaceNeeded


#计算Target并赋值
def calTarget(blockBits):
    global Targets
    exp=int(blockBits[:2],16)
    coef=int(blockBits[2:8],16)
    Targets=coef*pow(256,exp-3)

#level从1开始
def calLevel(blockID,beginID,endID):
    if blockID>=endID or blockID<beginID:
        return 0
    #if blockID==beginID:
     #   return 256
    target=Targets
    blockHash=BlockHashes[blockID-beginID]
    blockHashwithno0 = re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", blockHash)
    blockHashValue=int(blockHashwithno0,16)
    level=1
    while blockHashValue<(target/pow(2,level)):
        level=level+1
    #print('blockhash=', blockHashValue, 'target=', target, 'level=',level)
    return level

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
def loadNodesCommunicationCost_norm(nodesnums):
    x=0


def generateNodesCapacity_norm(nodesnums):
    low=0
    high=1
    global CapacityofNodes
    tmpCapacitylist=np.random.uniform(low,high,nodesnums)
    tmpCapacitylist=tmpCapacitylist/sum(tmpCapacitylist)
    CapacityofNodes=tmpCapacitylist*TotalStorageSpaceNeeded



def initNodesCapacity(nodenums,beginID,endID,rege):
    loadData_Sizes(beginID,endID)
    # print("blocksize init done. len(blocksize)=",len(BlockSizes))
    calTotalSpaceNeeded()
    # print("total space needed cal is done, totalSpaceNeeded is ",TotalStorageSpaceNeeded)
    if rege:
        generateNodesCapacity_norm(nodenums)
    # print("generate nodes capacity is done.")

def buildBlockList(beginID,endID):
    calTarget(Bits)
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

def buildtLevelBlocks(beginID,endID):
    calTarget(Bits)
    MaxLevel=0
    Thislevel=[]
    for blockID in range(beginID,endID):
        level=calLevel(blockID,beginID,endID)
        Thislevel.append(level)
        if level>MaxLevel:
            MaxLevel=level
    global LevelBlocks
    for i in range(MaxLevel):
        LevelBlocks.append([])
        OnlyLevelBlocks.append([])
    for blockID in range(beginID,endID):
        level=Thislevel[blockID-beginID]
        OnlyLevelBlocks[level-1].append(blockID)
        for levelinput in range(level):
            LevelBlocks[levelinput].append(blockID)
        #print("at level",level-1,",append block ",blockID)
    return MaxLevel

def printLevelBlocks(beginID,endID,only):
    stronly="only"
    if not only:
        stronly="not-only"
    filename='./normalT_levelBlocks-'+str(beginID)+'-'+str(endID)+'-'+stronly+'-'+str(int(np.random.rand()*1000))+'.txt'
    fileoutput=open(filename,'w')
    level=0
    if not only:
        for levelblocks in LevelBlocks:
            level+=1
            print("level-",level,' blocks:',file=fileoutput)
            print(levelblocks,file=fileoutput)
    if only:
        for levelblocks in OnlyLevelBlocks:
            level+=1
            print("level-",level,' blocks:',file=fileoutput)
            print(levelblocks,file=fileoutput)
    fileoutput.close()

def scanLevelBlocks(m,beginID,endID,maxlevel):
    chosenBlocks=[]
    thislevel=0
    # filename = './normalT_scanlevelBlocks-' + str(beginID) + '-' + str(endID) + '-' + str(m) + '.txt'
    # fileoutput = open(filename, 'w')
    chosenblockthislevel=0
    for lowlevel in range(maxlevel):
        level=maxlevel-1-lowlevel
        thislevel+=1
        if len(LevelBlocks[level])<m:
            continue
        newblocksgot=0
        tmpchosenBlocks=[]
        for i in range(len(LevelBlocks[level])):
            chosenindex=len(LevelBlocks[level])-1-i
            chosenblock=LevelBlocks[level][chosenindex]
            if not(chosenblock in chosenBlocks):
                newblocksgot+=1
                tmpchosenBlocks.append(chosenblock)
                if newblocksgot==m:
                    # print('level-', level + 1, ',blocks:', file=fileoutput)
                    for chosenbs in tmpchosenBlocks:
                        chosenBlocks.append(chosenbs)
                        # print(chosenbs,file=fileoutput)
                    break
    # fileoutput.close()
    return chosenBlocks


def initBlockLevels(beginID,endID):
    loadData_Hashes(beginID,endID)
    #print("load hash is done.")
    maxlevel=buildtLevelBlocks(beginID,endID)
    #print("build blocklist is done,maxlevel=",maxlevel)
    return maxlevel

def print_BlockList(beginID,endID):
    filename='./normalT_blocklistdata-'+str(beginID)+'-'+str(endID)+'.txt'
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
    filename='./normalT_scannedinlevel-'+str(beginID)+'-'+str(endID)+'.txt'
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
    thisLevelbeginBlockID=beginID
    thisBlockID = beginID
    filename = './normalT_scannedinlevel-norepeat-' + str(beginID) + '-' + str(endID) + '.txt'
    fileoutput = open(filename, 'w')
    ChosenBlockIDs=[]
    while thisLevel > 0:
        thisLevelBlockNumbers = 0
        while thisBlockID != endID:
            BlockScannedTimes[thisBlockID - beginID] = BlockScannedTimes[thisBlockID - beginID] + 1
            print("scanned:", thisBlockID, " , in level ", thisLevel, " scannedTimes=",BlockScannedTimes[thisBlockID - beginID], file=fileoutput)
            if BlockScannedTimes[thisBlockID-beginID]<=1:
                thisLevelBlockNumbers = thisLevelBlockNumbers + 1
            thisBlockID = BlockLists[thisBlockID - beginID][thisLevel]
        thisBlockID = thisLevelbeginBlockID
        scannedBlockNumbers = 0
        # 取最后三个
        while scannedBlockNumbers < thisLevelBlockNumbers - m:
            thisBlockID = BlockLists[thisBlockID - beginID][thisLevel]
            if BlockScannedTimes[thisBlockID-beginID]<=1:
                scannedBlockNumbers = scannedBlockNumbers + 1
        #####
        chosenblockid=thisBlockID
        while chosenblockid != endID:
            if BlockScannedTimes[chosenblockid-beginID]<=1:
                ChosenBlockIDs.append(chosenblockid)
                print("in level-",thisLevel,",chosen block:",chosenblockid)
            chosenblockid = BlockLists[chosenblockid - beginID][thisLevel]
        #####
        thisLevel = thisLevel - 1
        print("==========================================================================",file=fileoutput)
        thisLevelbeginBlockID = thisBlockID
    fileoutput.close()
    return BlockScannedTimes,ChosenBlockIDs


def assignBlockswithBlockList(nodenums,beginID,endID):
    global WhichNodeistheBlockStored
    RemainingCapacityofNodes = []
    for capacity in CapacityofNodes:
        RemainingCapacityofNodes.append(capacity)
    for blockID in range(beginID,endID):
        targetlevel=BlockLists[blockID-beginID][0]
        targetNode=targetlevel%nodenums
        thisBlockSize=BlockSizes[blockID-beginID]
        print("target level=", targetlevel, 'targetnode-', targetNode,'this bloc size=',thisBlockSize,'targetstorage=',RemainingCapacityofNodes[targetNode])
        nodesscanned=0
        while thisBlockSize>RemainingCapacityofNodes[targetNode]:
            targetNode+=1
            targetNode=targetNode%nodenums
            nodesscanned+=1
            if nodesscanned>=nodenums:
                print("ERROR:no nodes can store block ",blockID," now!")
                exit(1)
        RemainingCapacityofNodes[targetNode]-=thisBlockSize
        WhichNodeistheBlockStored[blockID]=targetNode

def assignBlocksWithLevelBlocks(nodenums,beginID,endID):
    global WhichNodeistheBlockStored
    thislevel=0
    # filename='./normalT_assignRes-'+str(nodenums)+'-'+str(beginID)+'-'+str(endID)+'-'+str(int(np.random.rand()*1000))+'.txt'
    # fileoutput=open(filename,'w')
    RemainingCapacityofNodes = []
    for capacity in CapacityofNodes:
        RemainingCapacityofNodes.append(capacity)
    for thislevelControl in range(len(OnlyLevelBlocks)):
        uplevel=len(OnlyLevelBlocks)-1-thislevelControl
        levelblocks=OnlyLevelBlocks[uplevel]
        thislevel+=1
        for blocks in levelblocks:
            targetLevel=uplevel#已经使用了-1处理
            targetNode=targetLevel%nodenums
            thisBlocksize=BlockSizes[blocks-beginID]
            #print("target level=", targetLevel, ',targetnode-', targetNode, ',this bloc size=', thisBlocksize,',targetstorage=', RemainingCapacityofNodes[targetNode],file=fileoutput)
            nodesscanned = 0
            while thisBlocksize > RemainingCapacityofNodes[targetNode]:
                targetNode += 1
                targetNode = targetNode % nodenums
                nodesscanned += 1
                if nodesscanned >= nodenums:
                    print("assignBlocksWithLevelBlocks:ERROR:no nodes can store block ", blocks, " now!")
                    print("blocksize is ",thisBlocksize)
                    print("reamining is:",RemainingCapacityofNodes)
                    exit(1)
            # print("target level=", targetLevel, ',targetnode-', targetNode, 'this block is=',blocks,',this block size=', thisBlocksize,',targetstorage=', RemainingCapacityofNodes[targetNode], file=fileoutput)
            RemainingCapacityofNodes[targetNode] -= thisBlocksize
            WhichNodeistheBlockStored[blocks] = targetNode
    # for n in range(nodenums):
    #     print("in node ",n,file=fileoutput)
    #     for b in range(beginID,endID):
    #         if WhichNodeistheBlockStored[b-beginID]==n:
    #             print(b,file=fileoutput)
    # fileoutput.close()

def assignNormal(nodenums,beginID,endID):
    global WhichNodeistheBlockStored
    RemainingCapacityofNodes = []
    for capacity in CapacityofNodes:
        RemainingCapacityofNodes.append(capacity)
    for blockID in range(beginID,endID):
        targetNode=int(np.random.rand()*nodenums)
        #print(targetNode)
        thisBlocksize = BlockSizes[blockID - beginID]
        nodesscanned = 0
        while thisBlocksize > RemainingCapacityofNodes[targetNode]:
            targetNode += 1
            targetNode = targetNode % nodenums
            nodesscanned += 1
            if nodesscanned >= nodenums:
                print("assignBlocksWithLevelBlocks:ERROR:no nodes can store block ", blockID, " now!")
                print("blocksize is ", thisBlocksize)
                print("reamining is:", RemainingCapacityofNodes)
                exit(1)
        # print("target level=", targetLevel, ',targetnode-', targetNode, 'this block is=',blocks,',this block size=', thisBlocksize,',targetstorage=', RemainingCapacityofNodes[targetNode], file=fileoutput)
        RemainingCapacityofNodes[targetNode] -= thisBlocksize
        WhichNodeistheBlockStored[blockID] = targetNode


def getOneBlockfromOtherNode(blockID,beginID,endID,nodeid):
    if not(blockID in WhichNodeistheBlockStored):
        print("ERROR: block:",blockID," is not stored!")
    fromnodeid=WhichNodeistheBlockStored[blockID]
    timeconsumed=CommunicationCost[nodeid][fromnodeid]*BlockSizes[blockID-beginID]
    return timeconsumed,fromnodeid

def onceRunAtOneChainLength(nodenums,beginID,endID,m,islevel):
    maxlevel=initBlockLevels(beginID,endID)
    #printLevelBlocks(beginID,endID,0)
    #printLevelBlocks(beginID, endID, 1)
    if islevel:
        assignBlocksWithLevelBlocks(nodenums,beginID,endID)
    if not islevel:
        assignNormal(nodenums,beginID,endID)
    #print("assignblocks is done,blocks assigned =",len(WhichNodeistheBlockStored))
    timeConsumed=0
    chosenBlocks = scanLevelBlocks(m, beginID, endID, maxlevel)
    # filename='./normalT_communication-cost-'+str(nodenums)+'-'+str(beginID)+'-'+str(endID)+'-'+str(m)+'.txt'
    # fileoutput = open(filename, 'w')
    # print(nodenums," nodes is going to request for blockid...",file=fileoutput)
    # print(chosenBlocks,file=fileoutput)
    ###ver1
    # for nodeid in range(nodenums):
    #     # print("node[",nodeid,'] is requesting...',file=fileoutput)
    #     for blocks in chosenBlocks:
    #         timecom,fromnode=getOneBlockfromOtherNode(blocks,beginID,endID,nodeid)
    #         # print("blockID[",blocks,']...from node[',fromnode,']...timeconumption=',CommunicationCost[nodeid][fromnode],'*',BlockSizes[blocks-beginID],'=',timecom,file=fileoutput)
    #         timeConsumed+=timecom
    # #print("request done,total time consumed=",timeConsumed,"average consumption=",timeConsumed/nodenums,file=fileoutput)
    ###ver2
    for nodeid in range(nodenums):
        timesum = [0] * nodenums
        for blocks in chosenBlocks:
            timecom, fromnode = getOneBlockfromOtherNode(blocks, beginID, endID, nodeid)
            timesum[fromnode]+=timecom
        maxtime=max(timesum)
        timeConsumed += maxtime
    return timeConsumed/nodenums



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
    filename='./normalT_blockscannedtimes-'+str(beginID)+'-'+str(endID)+'.txt'
    fileoutput=open(filename,'w')
    for blockID in range(beginID,endID):
        if scannedTimes[blockID-beginID]!=0:
            print("{ID:",blockID," , scannedTimes =",scannedTimes[blockID-beginID]," }",file=fileoutput)
    fileoutput.close()

def plotPie(scannedTimes,beginID,endID):
    plt.pie(scannedTimes)
    plt.show()

def printLevel(beginID,endID,Maxlevel):
    filename = './normalT_levelofnodes-' + str(beginID) + '-' + str(endID) + '.txt'
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


def test_level_per_node(nodesnum):
    print("ok")


def onceTest():
    beginID = 0
    endID = 2016
    m = 3
    loadData_Hashes(beginID, endID)
    print("INFO: load done")
    maxlevel = buildBlockList(beginID, endID)
    print_BlockList(beginID, endID)
    print("INFO: build block list done")
    BlockScannedTimes = scanBlockList_noRepeat(m, beginID, endID, maxlevel)
    print("INFO: scan block list done")
    # printBlockScannedTimes(BlockScannedTimes,beginID,endID)
    # printLevel(beginID,endID,maxlevel)
    # plotBlockScannedTimes(BlockScannedTimes,beginID,endID)
    # plotHasBeenScanned(BlockScannedTimes,beginID,endID)
    #plotScannedTimesV(BlockScannedTimes, beginID, endID)

def StepGO():
    beginID = 0
    endID = 2016
    step = 2016
    MAXMUL=508032/2016#252
    maxendid = step*5  # 508032
    m = 3
    nodesnum = 10
    timereslist = []
    timereslistnotlevel = []
    generateNodesCommunicationCost_norm(nodesnum)
    initNodesCapacity(nodesnum, beginID, endID,1)
    XTimes=100
    times=XTimes
    while times!=0:#endID != maxendid:
        clearGlobal()
        times-=1
        initNodesCapacity(nodesnum, beginID, endID,0)
        timeres = onceRunAtOneChainLength(nodesnum, beginID, endID, m,1)
        endID += step
        timereslist.append(timeres)
    endID=2016
    times=XTimes
    while times!=0:#endID != maxendid:
        clearGlobal()
        times -= 1
        initNodesCapacity(nodesnum, beginID, endID,0)
        timeres = onceRunAtOneChainLength(nodesnum, beginID, endID, m,0)
        endID += step
        timereslistnotlevel.append(timeres)
    print(timereslist)
    print('\n')
    print(timereslistnotlevel)
    plt.xlabel('blocknumbers (*2016)')
    titlestr = "Communication cost under different length of chain \n(m={them},beginID={begin},nodesnum={nodes})".format(
        them=m, begin=beginID, nodes=nodesnum)
    plt.ylabel('communication cost')
    plt.title(titlestr)
    plt.plot(range(int(beginID/step),int(len(timereslist)+int(beginID/step))), timereslist,color='red',label='with level')
    plt.plot(range(int(beginID/step),int(len(timereslistnotlevel)+int(beginID/step))), timereslistnotlevel,color='green',label='with random')
    plt.legend()
    plt.show()
    #capacity重新生成对每一次时间开销影响很大，因此如果统计块数增长带来的开销，如何设置capacity，排除它带来的影响是一个问题。还是说就只是预留足够空间？
    #通信开销重新生成也如是：通过请求快的响应时间长短来作为一项是否replicate的标准？
    #我其实没太懂把一个level对应的块全分配到一个节点会有什么改进，因为通信开销是变化的，而且每个节点也都会从其他节点拿块？感觉level对确定副本数量的作用会更大一些。
    #目前看来，和随机其实相差不大
    #如果一定要用level确定一个节点，应该是根据高层确定通信能力更强的节点，底层则处于通信能力偏弱的节点？
    #快的分配位置其实应该更应该是看节点对块的需求，但在现在的模型下，节点不会有特数的偏好，在某个时间点下，所有节点偏好的块都是同一批。
    #这批快的特点是：高层、最近生成。（level，blockid）
    #因此为了改进系统的平均通信开销，是否应该令这些块在与其他节点进行通信时长更小的节点。
    #当有一段时间收不到对某个块B的请求的时候，或者自己在做验证的时候需求的块全是id大于该块B的块，那么B大概率再也不会被请求来做验证了
    #
    #目前只有给足存储空间，因此当连数目比较小的时候，几乎全是分在targetnode上
    #因为分配是确定的，比较怀疑是不是比特币本身的数据集存在一些特点，会导致出现转折

def MoreTimes():
    beginID = 0
    endID = 2016
    times=10
    m = 3
    nodesnum = 10
    timereslist = []
    initNodesCapacity(nodesnum, beginID, endID)
    generateNodesCommunicationCost_norm(nodesnum)
    # print("generate nodes communication cost is done.")
    for i in range(times):
        clearGlobal()
        timeres = onceRunAtOneChainLength(nodesnum, beginID, endID, m)
        timereslist.append(timeres)
    plt.plot(range(len(timereslist)), timereslist)
    plt.xlabel('excution times')
    titlestr="Communication cost under multiple executions\n(m={them},beginID={begin},endID={end},nodesnum={nodes})".format(them=m, begin=beginID,end=endID,nodes=nodesnum)
    plt.ylabel('communication cost')
    plt.title(titlestr)
    print(timereslist)
    plt.show()


if __name__ == '__main__':
    StepGO()