
import re
import matplotlib.pyplot as plt
Bits=[]#每2016存1个
Targets=[]#通过Bits计算得到
BlockHashes=[]
BlockLists=[]
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


def every2016BlocksPlot(beginID,endID,m):
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
    for times in range(beginID-beginID,endID-beginID):
        Chosen=scanBlockList_noRepeat_withoutm(m,beginID,beginID+times+1,maxlevel)
        print('=================scan times=',times,'==========================',file=fileoutput)
        for x1s in Chosen:
            print('blockid=',x1s,',level=',BlockLists[x1s-beginID][0],file=fileoutput)
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
    plt.scatter(x,y,c='r',s=0.5,label='level:[1,4]')
    plt.scatter(x1,y1,c='g',s=0.5,label='level:[5,6]')
    plt.scatter(x2, y2, c='y', s=0.5, label='level:[7,8]')
    plt.scatter(x3,y3,c='b',s=0.5,label='level:[9,∞)')
    plt.xlabel('blockID')
    plt.ylabel('scantime')
    plt.legend()
    plt.show()
    fileoutput.close()
    #接下来对数据进行分析
    #该层级节点平均被选中的次数
    LevelAveBlockChosenTimes=[0]*maxlevel
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
    xlevel=range(1,maxlevel+1)
    PlotXLevel=[]
    PlotLevelAveBlockChosenTimes=[]
    for i in range(maxlevel):
        xp=xlevel[i]
        yp=LevelAveBlockChosenTimes[i]
        if yp!=0:
            plt.text(xp + 0.01, yp + 20, '(%d ,\n %.2f,\n %d)' % (xp,yp,LevelChosenBlocks[i]), ha='center', va='top')
            PlotLevelAveBlockChosenTimes.append(yp)
            PlotXLevel.append(xp)
    plt.plot(PlotXLevel,PlotLevelAveBlockChosenTimes)
    plt.xlabel('levels')
    plt.ylabel('avg-scantimes')
    plt.title('beginID=%d,endID=%d'%(beginID,endID))
    plt.show()
    return LevelAveBlockChosenTimes

def runonce(beginID,endID,m):
    loadData(beginID,endID)
    ml=buildBlockList(beginID,endID)
    print_BlockList(beginID,endID)
    chosen=scanBlockList_noRepeat(m,beginID,endID,ml)

if __name__=='__main__':
    x=1#12
    every2016BlocksPlot(2016*x,2016*(x+1),3)


