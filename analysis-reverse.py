
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
        #将我的level之下指向上一个本level节点
        for level in range(blockLevel):
            BlockLists[blockID-beginID][level+1]=levelLastNodeID[level]
        # 上一个列表更新
        for leveli in range(blockLevel):
            levelLastNodeID[leveli] = blockID
    return MaxLevel,levelLastNodeID

def print_BlockList(beginID,endID):
    filename='./blocklistdata-'+str(beginID)+'-'+str(endID)+'.txt'
    fileoutput=open(filename,'w')
    for blockID in range(beginID,endID):
        mylevel=BlockLists[blockID-beginID][0]
        print("{ID:",blockID," , mylevel =",mylevel," , [",end="",file=fileoutput)
        for i in range(mylevel-1):
            print("pre-level-",i+1,":",BlockLists[blockID-beginID][i+1]," , ",end="",file=fileoutput)
        print("pre-level-",mylevel,":",BlockLists[blockID-beginID][mylevel]," ]} ",file=fileoutput)
    fileoutput.close()

def scanBlockList_noRepeat(m,beginID,endID,Maxlevel,LevelLastNodeID):
    BlockScannedTimes=[0]*(endID-beginID)
    thisLevel=Maxlevel
    filename = './scannedinlevel-norepeat-reverse-' + str(beginID) + '-' + str(endID) + '.txt'
    fileoutput = open(filename, 'w')
    ScannedBlockIDS=[]
    BlockChosen=[0]*(endID-beginID)
    while thisLevel>0:
        thisBlockID = LevelLastNodeID[thisLevel - 1]
        print('in level ',thisLevel,file=fileoutput)
        ScannedthisLevelBlockID=[]
        while len(ScannedthisLevelBlockID)<m and thisBlockID>=beginID:
            # if BlockLists[thisBlockID-beginID][0]==thisLevel or (thisBlockID==beginID and (not beginIDchosen)):
            if BlockChosen[thisBlockID-beginID]==0:
                ScannedthisLevelBlockID.append(thisBlockID)
            if thisBlockID==beginID:
                break
            thisBlockID=BlockLists[thisBlockID-beginID][thisLevel]
        if len(ScannedthisLevelBlockID)==m:
            for value in ScannedthisLevelBlockID:
                print('block ',value,file=fileoutput)
                ScannedBlockIDS.append(value)
                BlockChosen[value-beginID]=1
        thisLevel-=1
        print("==========================================================================",file=fileoutput)
    fileoutput.close()
    return BlockScannedTimes


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

def runonce(beginID,endID,m):
    loadData(beginID,endID)
    ml,llbi=buildBlockList(beginID,endID)
    print_BlockList(beginID,endID)
    chosen=scanBlockList_noRepeat(m,beginID,endID,ml,llbi)



def every2016BlocksPlot(beginID,endID,m):
    if endID-beginID!=2016:
        return 0,[]
    loadData(beginID,endID)
    x=[]
    y=[]
    filename='./every2016plot-'+str(beginID)+'-'+str(endID)+'.txt'
    fileoutput=open(filename,'w')
    for times in range(beginID,endID):
        maxlevel, levellastblockid = buildBlockList(beginID, beginID+times+1)
        ChosenBlocks=scanBlockList_noRepeat(m,beginID,beginID+times+1,maxlevel,levellastblockid)
        print('=================scan times=',times,'==========================',file=fileoutput)
        for x1s in ChosenBlocks:
            print('blockid=',x1s+beginID,',level=',BlockLists[x1s][0],file=fileoutput)
            x.append(x1s+beginID)
            y.append(times+1)
    plt.scatter(x,y)
    plt.xlabel('blockID')
    plt.ylabel('scantime')
    plt.show()
    fileoutput.close()



if __name__=='__main__':
    # every2016BlocksPlot(0,2016,3)
    runonce(0,2016,3)


