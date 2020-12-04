import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import time
import os

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
        fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\zipfr-calculate3-popularity10-curve3-PL-node'+str(nodeid)+'-100.txt')
        # fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\calculate3-curve3-popularity-node'+str(nodeid)+'-100.txt')
        # popu_dicts.append({})
        last_time=time.ctime(os.stat(fname).st_mtime)
        print('file modify time: ',last_time,', file: ',fname)
        with open(fname, 'r') as datafile:
            for dataline in datafile:
                datalineitem = dataline.split('$')
                runtime=int(datalineitem[0])
                popu_dicts=(json.loads(datalineitem[1]))
                for kvs in popu_dicts.items():
                    replica_nums_1[int(kvs[0])]+=1

    replica_nums_2=[0]*(epoch-654000)
    for nodeid in range(node_sum):
        # fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\calculate3-llu8-popularity-node'+str(nodeid)+'-100.txt')
        fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\access3-llu8-popularity-node'+str(nodeid)+'-100.txt')
        # popu_dicts.append({})
        last_time=time.ctime(os.stat(fname).st_mtime)
        print('file modify time: ',last_time,', file: ',fname)
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
    replica_ratio_1=np.array(replica_nums_1)/(allsum_1)#np.array(replica_nums_1)/100#

    for i in range(epoch-654000):
        print('blockid=',i,',C-replicas=',replica_nums_2[i])
    allsum_2=sum(replica_nums_2)
    replica_ratio_2=np.array(replica_nums_2)/(allsum_2)#np.array(replica_nums_2)/100#

    # index is rank
    # value is block number
    pzr=[239, 39, 161, 24, 383, 46, 26, 249, 365, 108, 103, 17, 60, 276, 278, 345, 11, 360, 338, 320, 208, 327, 394, 262, 30, 90, 86, 375, 187, 396, 156, 101, 306, 176, 225, 168, 369, 47, 132, 340, 332, 123, 378, 374, 169, 299, 317, 6, 71, 255, 343, 361, 15, 14, 295, 21, 309, 63, 92, 265, 200, 246, 43, 177, 280, 251, 197, 364, 385, 190, 217, 57, 70, 134, 186, 329, 154, 363, 9, 219, 302, 16, 304, 127, 328, 314, 235, 288, 289, 181, 391, 357, 193, 386, 58, 189, 195, 149, 324, 260, 135, 85, 293, 204, 237, 271, 236, 59, 172, 290, 226, 50, 245, 2, 392, 141, 160, 116, 95, 115, 352, 336, 285, 277, 207, 150, 66, 286, 209, 107, 96, 284, 
        61, 220, 113, 224, 316, 339, 145, 34, 287, 252, 201, 238, 397, 387, 110, 93, 175, 227, 322, 20, 27, 362, 88, 341, 51, 303, 128, 118, 202, 359, 82, 67, 167, 199, 194, 35, 33, 274, 376, 157, 379, 233, 390, 28, 106, 19, 389, 48, 292, 354, 178, 358, 163, 162, 8, 247, 382, 221, 281, 0, 125, 3, 121, 393, 97, 367, 351, 13, 153, 29, 38, 148, 54, 349, 335, 36, 89, 12, 69, 250, 143, 133, 313, 1, 347, 104, 155, 269, 272, 78, 
        308, 5, 170, 398, 99, 142, 94, 355, 234, 353, 166, 384, 261, 112, 231, 399, 268, 174, 137, 230, 371, 102, 242, 373, 147, 315, 380, 337, 310, 395, 91, 223, 140, 105, 45, 25, 79, 388, 52, 22, 87, 350, 55, 68, 158, 348, 248, 139, 72, 283, 184, 264, 298, 62, 49, 173, 192, 258, 381, 323, 77, 130, 129, 73, 138, 41, 7, 171, 279, 243, 203, 56, 211, 80, 307, 10, 244, 205, 83, 84, 109, 164, 377, 206, 240, 23, 273, 146, 18, 229, 311, 366, 37, 301, 64, 326, 372, 346, 81, 183, 126, 275, 53, 370, 111, 185, 291, 256, 297, 241, 144, 159, 331, 270, 282, 215, 4, 344, 228, 100, 305, 210, 198, 180, 131, 254, 259, 40, 42, 267, 75, 151, 333, 330, 368, 214, 120, 325, 318, 266, 300, 32, 321, 294, 31, 342, 334, 188, 296, 136, 222, 98, 213, 182, 76, 152, 257, 216, 196, 212, 356, 191, 117, 124, 65, 232, 74, 218, 312, 122, 165, 179, 119, 114, 253, 44, 
        263, 319]

    probabllity=[0]*(epoch-654000)
    probabllity_uni=[0]*(epoch-654000)
    probabllity_r=[0]*(epoch-654000)
    s=1.2
    for i in range(len(probabllity)):
        probabllity_uni[i]=allsum_1/len(probabllity_uni)
        probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number((epoch-654000),s)*pow(i+1,s))
        probabllity_r[pzr[i]]=1/(generalized_harmonic_number((epoch-654000),s)*pow(i+1,s))
    probabllity=np.array(probabllity)
    probabllity_r=np.array(probabllity_r)

    

    
    
    # sqrt_prob=[]
    # sqrt_prob_uni=[]
    # for i in range(len(probabllity)):
    #     sqrt_prob.append(math.sqrt(probabllity[i]))
    #     sqrt_prob_uni.append(math.sqrt(probabllity_uni[i]))

    # sqrt_prob_ratio=np.array(sqrt_prob)/sum(sqrt_prob)
    # sqrt_prob_ratio_uni=np.array(sqrt_prob_uni)/sum(sqrt_prob_uni)

    # plt.figure()

    # X=range(epoch-654000)

    # TAIL_BLOCKS=0
    
    # replica_ratio_1=[math.log10(i) for i in replica_ratio_1]
    # plt.scatter(X,replica_ratio_1,marker='*',color='red',label='CL-replica_ratio_1')
    # plt.scatter(X,replica_ratio_2,marker='.',color='black',label='AL-replica_ratio_2')
    # plt.scatter(X[0:len(X)-TAIL_BLOCKS],sqrt_prob_ratio[0:len(X)-TAIL_BLOCKS],marker='+',color='blue',label='sqrt-probability')
    # probabllity=[math.log10(i) for i in probabllity]
    # plt.scatter(X[0:len(X)-TAIL_BLOCKS],probabllity[0:len(X)-TAIL_BLOCKS],marker='+',color='green',label='probability')
    # plt.scatter(X[0:len(X)-TAIL_BLOCKS],probabllity_r[0:len(X)-TAIL_BLOCKS],marker='+',color='green',label='probability')
    # plt.ylim(150,400)

    # plt.plot(X,replica_ratio_1,color='red',label='A-replica_ratio_1')
    # # plt.plot(X,replica_ratio_2,color='black',label='C-replica_ratio_2')
    # plt.plot(X,probabllity_r,color='green',label='probabllity')
    # # plt.plot(X[0:len(X)-8],sqrt_prob_ratio[0:len(X)-8],color='blue',label='sqrt_prob_ratio')
    # plt.legend()

    # plt.xlabel('block')
    # plt.ylabel('num')
    # plt.show()

    store_file_name_1='./P-list1.txt'
    store_file_name_zipf='./P-zipf.txt'
    with open(store_file_name_1,'w')as w_f:
        pstring=str(epoch)+' '+str(epoch+400)+' 1'
        print(pstring,file=w_f)
        print(json.dumps(replica_ratio_1.tolist()),file=w_f)
    with open(store_file_name_zipf,'w')as w_f:
        pstring=str(epoch)+' '+str(epoch+400)+' 1'
        print(pstring,file=w_f)
        print(json.dumps(probabllity_r.tolist()),file=w_f)
    return probabllity_r



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

def plot_pro(distribution_type):
    chain_length=400
    # probability of each node to be chosen.
    probabllity=[0]*(chain_length)
    # sum()=1


    if distribution_type=='uniform':
        for i in range(len(probabllity)):
            probabllity[i]=1/(chain_length)
    elif distribution_type=='zipf':
        #zipf PMF=F(K=k)=1/ghn(N,s)*k^s. k is the rank, N is the total number, 
        # s is a parameter to describe zipf curve
        #s is a parameter used in zipf distribution
        s=1.2
        for i in range(len(probabllity)):
            probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number(chain_length,s)*pow(i+1,s))
    elif distribution_type=='zipf8':
        s8=.8
        for i in range(len(probabllity)):
            probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number(chain_length,s8)*pow(i+1,s8))
    # elif distribution_type=='zipfr':
    #     szr=1.2
    #     # new block: endID-1 is coming
    #     new_dict={}
    #     # key: block number
    #     # value: rank
    #     for i in range(chain_length):
    #         new_dict[i]=CONSTANT_RANK[i]
    #     new_dict_rank=sorted(new_dict.items(),key=lambda x:x[1])
    #     rank_now=1
    #     for i in range(len(probabllity)):
    #         probabllity[new_dict_rank[i][0]]=1/(generalized_harmonic_number(chain_length,szr)*pow(rank_now,szr))
    #         rank_now+=1
    elif distribution_type=='flyclient':
        # c and k are 2 params of flyclient, c\in (0,1],k\in N
        # delta=c^k
        c=0.5
        k=10
        neg_small=pow(c,k)
        #PDF of flyclient is g(x)=1/((x-1)*ln(δ)), δ is c^k. c\in (0,1],k\in N
        # in their test, δ=2^{-10}
        # flyclient use difficult percentage.
        # here we consider unchanged target only.
        # P(x=k)=F_{k+1/N}-F{k}=(1/ln(δ))*(ln|k+1/N-1|-ln|k-1|)
        ### math.log1p(x), Return the natural logarithm of 1+x (base e). 
        ln_delta=1/math.log1p(pow(c,k)-1)
        for i in range(len(probabllity)):
            percentage_k=i/(chain_length)
            percentage_k_step_forward=percentage_k+1/(chain_length)
            if i==len(probabllity)-1:
                percentage_k_step_forward-=neg_small
            probabllity[i]=ln_delta*(math.log1p(-percentage_k_step_forward)-math.log1p(-percentage_k))
    
    return probabllity


if __name__=='__main__':
    # plot_popularity(begin_epoch+30)
    # plot_size()
    plot_distribution_replia_nums_v3(654010+390)
    # plot_load()
    # p_zipf=plot_pro('zipf')
    # p_fly=plot_pro('flyclient')

    # plt.figure()

    # plt.plot(range(400),p_zipf,color='r',label='zipf',marker='*')
    # plt.plot(range(400),p_fly,color='g',label='fly',marker='*')
    # plt.legend()
    # plt.show()