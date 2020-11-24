import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

node_sum=10

def plot_popularity(epoch):
    popu_dicts=[]
    for nodeid in range(node_sum):
        fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\access3-llu8-popularity-node'+str(nodeid)+'.txt')
        # fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\calculate3-llu8-popularity-node'+str(nodeid)+'.txt')
        # popu_dicts.append({})
        with open(fname, 'r') as datafile:
            j=0
            for dataline in datafile:
                datalineitem = dataline.split('$')
                epoch_id=int(datalineitem[0])
                if epoch_id==epoch and j==1:
                # print(datalineitem[1])
                    popu_dicts.append(json.loads(datalineitem[1]))
                elif epoch_id==epoch and j==0:
                    j=1
    #
    # print(popu_dicts[1])
    #node_sum
    fig = plt.figure()
    ax3=plt.axes(projection='3d')
    # ax = Axes3D(fig)
    # for i in range(len(use_ratio01)):
    #     ax.scatter([i+b01-begin_static for j in range(b01,e01,s01)], [j for j in range(b01,e01,s01)], use_ratio01[i])
    x=range(0,node_sum)
    y=range(654000,epoch+1)
    X,Y=np.meshgrid(y,x)
    X_,Y_=X.ravel(),Y.ravel()#flatten
    plot_array_array=[]
    for nid in range(node_sum):
        plot_array_array.append([])
        for bid in range(0,epoch-654000+1):
            plot_array_array[nid].append(-1)
        for kvs in popu_dicts[nid].items():
            plot_array_array[nid][int(kvs[0])]=kvs[1][0]+kvs[1][1]
            # print(kvs[0])
    fname_store='D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\excel-paint.txt'
    with open(fname_store,'w')as datafile:
        for i in x:
            pstring=''
            for j in range(0,epoch-654000+1):
                this_str=str(plot_array_array[i][j])
                if plot_array_array[i][j]==-1:
                    this_str='0'
                if j!=epoch-654000:
                    pstring+=this_str+','
                else:
                    pstring+=this_str
            print(pstring,file=datafile)
    
    blocks_in_which_node=[]
    for i in range(0,epoch-654000+1):
        blocks_in_which_node.append([])
    for nid in range(node_sum):
        for kvs in popu_dicts[nid].items():
            blocks_in_which_node[int(kvs[0])].append(nid)

    # ax3.plot_surface(X,Y,np.array(plot_array_array))#,cmap='rainbow')
    bar_color=['grey','darkblue','blue','lightblue','mistyrose','lightcoral','orangered','red','darkred','orchid','mediumpurple','blueviolet','purple','indigo']
    width=1# thick in x label
    depth=1#thick in y label
    for i in range(node_sum):
        for j in range(0,epoch-654000+1):
            z=plot_array_array[i][j]
            this_color=bar_color[z+1]
            if len(blocks_in_which_node[j])==2:
                this_color='grey'
            ax3.bar3d(j,i,0,width,depth,z,color=this_color)
    
    

    ax3.set_xlabel('Blocks')
    ax3.set_ylabel('Nodes')
    ax3.set_zlabel("Popu")
    plt.show()

# global memo to decrease runing time of `generalized_harmonic_number`
Generalized_harmonic_number={}

def generalized_harmonic_number(N,s):
    """(float,float) -> float

    used in zipf PMF.which F(K=k)=1/ghn(N,s)*k^s
    """
    if N in Generalized_harmonic_number:
        return Generalized_harmonic_number[N]
    elif N-1 in Generalized_harmonic_number:
        sum_up=Generalized_harmonic_number[N-1]
        sum_up+=pow(1/N,s)
        Generalized_harmonic_number[N]=sum_up
        return sum_up
    else:
        sum_up=0
        for i in range(1,N+1):
            sum_up+=pow(1/i,s)
        Generalized_harmonic_number[N]=sum_up
    return sum_up



def plot_distribution_replia_nums(epoch):
    popu_dicts=[]
    for nodeid in range(node_sum):
        # fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\calculate3-llu8-popularity-node'+str(nodeid)+'.txt')
        fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\access3-llu8-popularity-node'+str(nodeid)+'.txt')
        # popu_dicts.append({})
        with open(fname, 'r') as datafile:
            j=0
            for dataline in datafile:
                datalineitem = dataline.split('$')
                epoch_id=int(datalineitem[0])
                if epoch_id==epoch and j==1:
                # print(datalineitem[1])
                    popu_dicts.append(json.loads(datalineitem[1]))
                elif epoch_id==epoch and j==0:
                    j=1
    ####
    # plot_array_array=[]
    # for nid in range(node_sum):
    #     plot_array_array.append([])
    #     for bid in range(0,epoch-654000+1):
    #         plot_array_array[nid].append(-1)
    #     for kvs in popu_dicts[nid].items():
    #         plot_array_array[nid][int(kvs[0])]=kvs[1][0]+kvs[1][1]
    ###
    blocks_in_which_node=[]
    for i in range(0,epoch-654000+1):
        blocks_in_which_node.append([])
    for nid in range(node_sum):
        for kvs in popu_dicts[nid].items():
            blocks_in_which_node[int(kvs[0])].append(nid)

    replica_nums=[0]*(epoch-654000+1)
    for blockid in range(epoch-654000+1):
        replica_nums[blockid]=len(blocks_in_which_node[blockid])
        # print('block id=',blockid,', replica num=',len(blocks_in_which_node[blockid]))
    
    allsum=sum(replica_nums)
    replica_ratio=np.array(replica_nums)/allsum

    probabllity=[0]*(epoch-654000+1)
    s=1.2

    for i in range(len(probabllity)):
            probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number((epoch-654000),s)*pow(i+1,s))
    
    sqrt_prob=[]
    for i in range(len(probabllity)):
        sqrt_prob.append(math.sqrt(probabllity[i]))

    sqrt_prob_ratio=np.array(sqrt_prob)/sum(sqrt_prob)

    plt.figure()

    X=range(epoch-654000+1)
    
    # plt.scatter(X,replica_ratio,marker='*',color='red',label='replica_ratio')
    # plt.scatter(X,probabllity,marker='.',color='green',label='probabllity')
    # plt.scatter(X,sqrt_prob_ratio,marker='+',color='blue',label='sqrt_prob_ratio')

    plt.plot(X,replica_ratio,color='red',label='replica_ratio')
    plt.plot(X,probabllity,color='green',label='probabllity')
    plt.plot(X,sqrt_prob_ratio,color='blue',label='sqrt_prob_ratio')

    plt.xlabel('block')
    plt.ylabel('num')
    plt.show()


def plot_distribution_replia_nums_v2(epoch):
    # popu_dicts=[]
    epoch=654400
    replica_nums=[0]*(epoch-654000)
    for nodeid in range(node_sum):
        # fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\calculate3-llu8-popularity-node'+str(nodeid)+'-100.txt')
        fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\access3-llu8-popularity-node'+str(nodeid)+'-100.txt')
        # popu_dicts.append({})
        with open(fname, 'r') as datafile:
            for dataline in datafile:
                datalineitem = dataline.split('$')
                runtime=int(datalineitem[0])
                popu_dicts=(json.loads(datalineitem[1]))
                for kvs in popu_dicts.items():
                    replica_nums[int(kvs[0])]+=1
    

    for i in range(epoch-654000):
        print('blockid=',i,',replicas=',replica_nums[i])
    allsum=sum(replica_nums)
    replica_ratio=np.array(replica_nums)/(allsum)

    probabllity=[0]*(epoch-654000)
    s=1.2

    for i in range(len(probabllity)):
            probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number((epoch-654000),s)*pow(i+1,s))
    
    sqrt_prob=[]
    for i in range(len(probabllity)):
        sqrt_prob.append(math.sqrt(probabllity[i]))

    sqrt_prob_ratio=np.array(sqrt_prob)/sum(sqrt_prob)

    plt.figure()

    X=range(epoch-654000)
    
    # plt.scatter(X,replica_ratio,marker='*',color='red',label='replica_ratio')
    # plt.scatter(X,probabllity,marker='.',color='green',label='probabllity')
    # plt.scatter(X,sqrt_prob_ratio,marker='+',color='blue',label='sqrt_prob_ratio')

    plt.plot(X,replica_ratio,color='red',label='replica_ratio')
    plt.plot(X,probabllity,color='green',label='probabllity')
    plt.plot(X,sqrt_prob_ratio,color='blue',label='sqrt_prob_ratio')

    plt.xlabel('block')
    plt.ylabel('num')
    plt.show()

def plot_distribution_replia_nums_v3(epoch):
    # popu_dicts=[]
    epoch=654400
    replica_nums_1=[0]*(epoch-654000)
    for nodeid in range(node_sum):
        # fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\calculate3-llu8-popularity-node'+str(nodeid)+'-100.txt')
        fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\calculate3-curve3-popularity-node'+str(nodeid)+'-100.txt')
        # popu_dicts.append({})
        with open(fname, 'r') as datafile:
            for dataline in datafile:
                datalineitem = dataline.split('$')
                runtime=int(datalineitem[0])
                popu_dicts=(json.loads(datalineitem[1]))
                for kvs in popu_dicts.items():
                    replica_nums_1[int(kvs[0])]+=1

    replica_nums_2=[0]*(epoch-654000)
    for nodeid in range(node_sum):
        fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\calculate3-llu8-popularity-node'+str(nodeid)+'-100.txt')
        # fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\access3-llu8-popularity-node'+str(nodeid)+'-100.txt')
        # popu_dicts.append({})
        with open(fname, 'r') as datafile:
            for dataline in datafile:
                datalineitem = dataline.split('$')
                runtime=int(datalineitem[0])
                popu_dicts=(json.loads(datalineitem[1]))
                for kvs in popu_dicts.items():
                    replica_nums_2[int(kvs[0])]+=1
    

    for i in range(epoch-654000):
        print('blockid=',i,',A-replicas=',replica_nums_1[i])
    allsum_1=sum(replica_nums_1)
    replica_ratio_1=np.array(replica_nums_1)/100#(allsum_1)#np.array(replica_nums_1)/100#

    for i in range(epoch-654000):
        print('blockid=',i,',C-replicas=',replica_nums_2[i])
    allsum_2=sum(replica_nums_2)
    replica_ratio_2=np.array(replica_nums_2)/100#(allsum_2)#np.array(replica_nums_2)/100#

    probabllity=[0]*(epoch-654000)
    s=1.2

    for i in range(len(probabllity)):
            probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number((epoch-654000),s)*pow(i+1,s))
    
    sqrt_prob=[]
    for i in range(len(probabllity)):
        sqrt_prob.append(math.sqrt(probabllity[i]))

    sqrt_prob_ratio=np.array(sqrt_prob)/sum(sqrt_prob)

    plt.figure()

    X=range(epoch-654000)

    TAIL_BLOCKS=5
    
    plt.scatter(X,replica_ratio_1,marker='*',color='red',label='CC-replica_ratio_1')
    plt.scatter(X,replica_ratio_2,marker='.',color='black',label='CL-replica_ratio_2')
    # plt.scatter(X[0:len(X)-TAIL_BLOCKS],sqrt_prob_ratio[0:len(X)-TAIL_BLOCKS],marker='+',color='blue',label='sqrt-probability')

    # plt.plot(X,replica_ratio_1,color='red',label='A-replica_ratio_1')
    # plt.plot(X,replica_ratio_2,color='black',label='C-replica_ratio_2')
    # plt.plot(X,probabllity,color='green',label='probabllity')
    # plt.plot(X[0:len(X)-8],sqrt_prob_ratio[0:len(X)-8],color='blue',label='sqrt_prob_ratio')
    plt.legend()

    plt.xlabel('block')
    plt.ylabel('num')
    plt.show()



# datasize of blocksize
FILESIZENAME='E:/CUB/bh.dat/blocksize-654000.csv'


### open
def load_blocksizes(beginID,endID):
    """(int,int) -> (list of float, float)

    Return blocksizes of blocks whose height are between [bgeinID,endID) base on file FILESIZENAME.
    Return total size of blocks whose height is in [beginID,endID)
    """

    blocksizes=[]

    # size sum of all blocks between [beginID,endID)
    storage_of_all_blocks=0

    with open(FILESIZENAME,'r') as size_file:
        for size_line in size_file:
            size_line_item=size_line.split(',')
            # get block height
            blockID=int(size_line_item[0])
            # skip blocks lower than beginID and no lower than endID
            if blockID<beginID:
                continue
            if blockID>=endID:
                break
            block_size=float(size_line_item[1])/1000000
            blocksizes.append(block_size)
            # sum this size up to storage_of_all_blocks
            storage_of_all_blocks+=block_size

    return blocksizes,storage_of_all_blocks

def plot_size():
    beginID=654000
    endID=654000+400
    blocksizes,_=load_blocksizes(beginID,endID)
    X=range(0,len(blocksizes))
    plt.plot(X,blocksizes)
    plt.show()


def load_load(chosen_block_distribution,piece,passive_item,active_item,expel_item,total_times):
    file_load='./finalTest/finalRes/debug/load-'+chosen_block_distribution+'-'+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.csv'
    node_load=[]
    with open(file_load, 'r') as datafile:
        i = 0
        for dataline in datafile:
            node_load.append(json.loads(dataline))
            i += 1
    return node_load

def plot_load():
    distribution='zipf'
    replica_sum=3
    passive_item='load10'
    active_item='random3'
    expel_item='llu8'
    run_times=100
    node_load = load_load(distribution,replica_sum,passive_item,active_item,expel_item,run_times)
    
    colors = ['blue', 'red', 'green', 'skyblue', 'pink', 'yellow', 'purple', 'black', 'cyan', 'orange','gold','brown','grey','lime']
    
    for i in range(10):
        plt.plot(range(len(node_load[i])),np.array(node_load[i]),color=colors[i],label=str(i))
    # plt.plot(range(b01, e01, s01),np.array(NodeSize04)/np.array(Blocksize01),color=colors[2],label='llu4')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize05)/np.array(Blocksize01),color=colors[3],label='llu5')
    # # # plt.plot(range(b01, e01, s01),np.array(NodeSize05r)/np.array(Blocksize01),color=colors[4],label='5r')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize06)/np.array(Blocksize01),color=colors[4],label='llu6')

    # plt.plot(range(b01, e01, s01),np.array(NodeSize011)/np.array(Blocksize01),color=colors[5],label='curve-11')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize022)/np.array(Blocksize01),color=colors[6],label='22')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize033)/np.array(Blocksize01),color=colors[7],label='lru8')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize033r)/np.array(Blocksize01),color=colors[8],label='33r')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize044)/np.array(Blocksize01),color=colors[8],label='44')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize055)/np.array(Blocksize01),color=colors[9],label='55')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize066)/np.array(Blocksize01),color=colors[10],label='66')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize077)/np.array(Blocksize01),color=colors[11],label='77')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize_no)/np.array(Blocksize01),color=colors[12],label='no-expel')
    # plt.plot(range(b01, e01, s01), NodeSize01, color=colors[0], label='01')
    # plt.plot(range(b01, e01, s01), NodeSize02, color=colors[1], label='02')
    # plt.plot(range(b01, e01, s01), NodeSize12, color=colors[2], label='12')
    # plt.plot(range(b01, e01, s01), NodeSize22, color=colors[3], label='22')
    plt.legend()
    # plt.ylim(ymin=0.2,ymax=.5)
    plt.xlabel('epoch')
    plt.ylabel('load=[block num]*[access time]')
    title_name=distribution+'-'+str(replica_sum)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(run_times)
    plt.title(title_name)
    # plt.title('s-'+distribution+str(replica_sum)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(run_times))
    plt.show()


if __name__=='__main__':
    begin_epoch=654010
    # plot_popularity(begin_epoch+30)
    # plot_size()
    # plot_distribution_replia_nums_v3(begin_epoch+390)
    plot_load()