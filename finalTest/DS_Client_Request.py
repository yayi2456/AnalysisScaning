import time
import numpy as np
import random
import math
import DS_init as dsinit
import DS_ReplicaAlgs as dsrpal
import json

# 记录最大超时时间设置，
MAX_TIME=0
# 记录解码时间
DECODE_TIME1=0
DECODE_TIME2=0
# 记录失败类型与失败节点
CRASH_TYPE='nocrash'
CRASH_NODES=0
# 记录数据分片个数和编码分片个数
DATA_SHARD=4
CODE_SHARD=2

crash_nodesid=[]

# dict which is to accelerate runing time of jiecheng
Jie_Cheng={}
def jiecheng(N):
    '''(int) -> int
    Return N!
    '''
    # 0!=1
    if N==0:
        Jie_Cheng[N]=1
        return 1
    if N in Jie_Cheng:
        return Jie_Cheng[N]
    elif N-1 in Jie_Cheng:
        res=Jie_Cheng[N-1]
        res=res*N
        Jie_Cheng[N]=res
        return res
    else:
        res=1
        for i in range(2,N+1):
            res=res*i
        Jie_Cheng[N]=res
        return res

Pission_Probablity={}

def get_chosen_blocks_numbers(expection,node_num,total_blks):
    '''(int) -> int
    Return chosen_block numbers in this epoch.

    process of choosing blocks are regarded as Pission distirbution.
    we choose one chosen_block_number according to probability.

    Pission distribution:
    P(X=k)=((\lambda^k)/(k!))*e^{-\lambda}, lambda is expection.
    '''
    if expection in Pission_Probablity:
        probability=Pission_Probablity[expection]
    else:
        # max_chosen_num is the max chosen num.
        max_chosen_num=2*expection+int(1/2*expection)

        # 0,1,...,max_chosen_num
        probability=[0]*(max_chosen_num+1)

        # total probability of [0,max_chosen_num-1]
        # pre_probability=0
        # 
        for i in range(max_chosen_num):
            probability[i]=(pow(expection,i)/jiecheng(i))/pow(np.e,expection)
            # pre_probability+=probability[i]
        probability[max_chosen_num]=1-np.sum(np.array(probability[:max_chosen_num]))
        if probability[max_chosen_num]<0:
            probability[max_chosen_num]=0
        Pission_Probablity[expection]=probability
    # print(probability)
    # choose one value based on probability
    chosen_number=[]
    for _nid in range(node_num):
        chosen_number.append(np.random.choice(range(len(probability)),replace=False,p=probability))
        if chosen_number[_nid]>total_blks:
            chosen_number[_nid]=total_blks
    return chosen_number

# used in multi times execution.
Cache_Zipf_Probability={}
Cache_Zipfr_Probability={}

def get_needed_blocks(beginID,endID,distribution_type,chosen_block_nums_all_nodes):
    """(int,int,list of list of int,str) -> list of int, list of int

    Return 'chosen_block_nums' blocks chosen by one node to complete some certin mission.
    Return rank_distribution for the next run.

    'rank_distribution' is for randomz distribution.
    We randomly get a distribution of popularity rank at the first time, if the rank_distribution is [].
    if len(rank_distribution) is not 0, we choose endID-beginID-len(rank_distribution) random numbers and insert them into rank_distribution,
    all the following rank are increased.

    3 types of distribution_type are allowed:
    'zipf': zipf distribution
    'uniform': uniform distribution
    'zipfr': zipf which which rank are randomly chosen
    """
    
    chosen_blocks=[]

    # probability of each node to be chosen.
    probabllity=[0]*(endID-beginID)
    # sum()=1

    
    
    chain_length=endID-beginID

    # get the distribution probability
    if distribution_type=='uniform':
        for i in range(len(probabllity)):
            probabllity[i]=1/(chain_length)
    elif distribution_type=='zipf':
        #zipf PMF=F(K=k)=1/ghn(N,s)*k^s. k is the rank, N is the total number, 
        # s is a parameter to describe zipf curve
        #s is a parameter used in zipf distribution
        global Cache_Zipf_Probability
        if endID in Cache_Zipf_Probability:
            probabllity=Cache_Zipf_Probability[endID]
        else:
            s=1.2
            for i in range(len(probabllity)):
                probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number(chain_length,s)*pow(i+1,s))
            Cache_Zipf_Probability[endID]=probabllity
    # elif distribution_type=='zipf8':
    #     s8=.8
    #     for i in range(len(probabllity)):
    #         probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number(chain_length,s8)*pow(i+1,s8))
    elif distribution_type=='zipfr':
        global Cache_Zipfr_Probability
        if endID in Cache_Zipfr_Probability:
            probabllity=Cache_Zipfr_Probability[endID]
        else:
            szr=1.2
            # new block: endID-1 is coming
            new_dict={}
            # key: block number
            # value: rank
            for i in range(chain_length):
                new_dict[i]=dsinit.CONSTANT_RANK[i]
            new_dict_rank=sorted(new_dict.items(),key=lambda x:x[1])
            rank_now=1
            for i in range(len(probabllity)):
                probabllity[new_dict_rank[i][0]]=1/(generalized_harmonic_number(chain_length,szr)*pow(rank_now,szr))
                rank_now+=1
            Cache_Zipfr_Probability[endID]=probabllity
    # elif distribution_type=='flyclient':
    #     # c and k are 2 params of flyclient, c\in (0,1],k\in N
    #     # delta=c^k
    #     c=0.5
    #     k=10
    #     neg_small=pow(c,k)
    #     #PDF of flyclient is g(x)=1/((x-1)*ln(δ)), δ is c^k. c\in (0,1],k\in N
    #     # in their test, δ=2^{-10}
    #     # flyclient use difficult percentage.
    #     # here we consider unchanged target only.
    #     # P(x=k)=F_{k+1/N}-F{k}=(1/ln(δ))*(ln|k+1/N-1|-ln|k-1|)
    #     ### math.log1p(x), Return the natural logarithm of 1+x (base e). 
    #     ln_delta=1/math.log1p(pow(c,k)-1)
    #     for i in range(len(probabllity)):
    #         percentage_k=i/(endID-beginID)
    #         percentage_k_step_forward=percentage_k+1/(endID-beginID)
    #         if i==len(probabllity)-1:
    #             percentage_k_step_forward-=neg_small
    #         probabllity[i]=ln_delta*(math.log1p(-percentage_k_step_forward)-math.log1p(-percentage_k))

    else:
        print("INVALID CHOSEN DISTRIBUTION TYPE! default('uniform') is set.")
        for i in range(len(probabllity)):
            probabllity[i]=1/(endID-beginID)
    
    # choose chosen_block_nums
    # if endID-beginID>=390:
    #     print('chosen blocks probability:',probabllity)
    for i in range(len(chosen_block_nums_all_nodes)):
        chosen_blocks.append(np.random.choice(range(beginID,endID),size=chosen_block_nums_all_nodes[i],replace=False,p=probabllity))
    ### deubg
    # if(distribution_type=='zipfr'):
    #     top_10_blocks=[]
    #     top_10_blocks_p=[]
    #     for i in range(len(rank_distribution)):
    #         if rank_distribution[i]<=10:
    #             top_10_blocks.append(beginID+i)
    #             top_10_blocks_p.append(probabllity[i])
    #     print('current top 10 probability distribution: ',top_10_blocks_p)
    #     print('current top 10 blocknumbers:',top_10_blocks)
    #     print('chosen blocknumbers: ',chosen_block_nums)
    #     print('chosen blocks: ',chosen_blocks)
    #     print('==')
    # if distribution_type=='uniform':
    #     print('chosen blocks:',sorted(chosen_blocks))
    ### end debug
    #return
    return chosen_blocks

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

Cache_Exp=[]
def generate_time_increasment_list(chosen_numbers_all_nodes,epoch_interval,lambdai):
    '''
    Generate request arriving time list for all nodes, which is expotional distribution with exception `lambdai`.
    we set the granularity as epoch_interval/20.
    epoch_interval=10*60

    CDF=1-e^{-\lambda x}, x>=0.
    '''
    #calculate the expontional probability
    granularity=100# granularity of time
    probability=[0]*granularity
    #请不要设置过大的（超过400的）lambdai
    happend_times=np.mean(chosen_numbers_all_nodes)#1.5*lambdai#+int(1/2*lambdai)
    one_interval=epoch_interval/happend_times# get a approximate time range for time increasment list.
    one_step=one_interval/granularity
    global Cache_Exp
    if len(Cache_Exp)!=0:
        probability=Cache_Exp
    else:
        this_point=0
        next_point=this_point+one_step
        this_lambdai=lambdai/epoch_interval
        for i in range(granularity-1):
            probability[i]=math.exp(-this_lambdai*this_point)-math.exp(-this_lambdai*next_point)
            this_point=next_point
            next_point+=one_step
        probability[granularity-1]=math.exp(-this_lambdai*this_point)
        Cache_Exp=probability
    
    # choose time interval list
    interval_lists=[]
    nodes_num=len(chosen_numbers_all_nodes)
    choose_range=[]
    start=one_step
    for i in range(granularity):
        choose_range.append(start)
        start=round(start+one_step,2)
    # debug
    # print(probability)
    # print(np.sum(probability,axis=1))
    # end
    for _nid in range(nodes_num):
        interval_lists.append(np.random.choice(choose_range,size=chosen_numbers_all_nodes[_nid],replace=True,p=probability))
        # print('sum_alst_',sum(interval_lists[_nid]))
    # debug_p=0
    # for i in range(len(interval_lists[0])):
    #     debug_p+=interval_lists[0][i]
    # print(debug_p,',',(chosen_numbers_all_nodes[0]))
    return interval_lists

def request_by_arriving_requests(interval_list,chosen_blocks,beginID,passive_type,fwrite,timeup):
    # if passive_type[:7]!='kadvary':
    #     return request_by_arriving_requests_not_kad(interval_list,chosen_blocks,beginID,passive_type,fwrite)
    # else:#passive_type==kad
    return request_by_arriveing_requests_kad_ver2(interval_list,chosen_blocks,beginID,fwrite,timeup,passive_type)

TEMP_COUT=0
MAX_MALICIOUS_TMUP=0
# 用于记录最大时间开销
TIME_MAX=1.317


def request_by_arriveing_requests_kad_ver2(interval_list,chosen_blocks,beginID,fwrite,timeup,passive_type):
    '''
    request by arriving time, get average access time, 
    get communication cost and data transamission amounts between each 2 nodes.

    PARAMS:
    `interval_list` is a list of list, 
    interval_list[i] stores node i's request arrival increasment time.

    `chosen_blocks` is a list of list, 
    chosen_blocks[i] stores node i's chosen block, corresponding to the arrival time of requests.

    `beginID` indicates id of begin blocks.

    `passive_type` tells the function which sort_of_dict to record and return.

    `fwrite` is a file pointer to write. the function writes request list into this file.

    `timeup` is the maxinum time that a node wait for response. np.inf is default.
    '''
    global MAX_TIME
    if timeup=='inf':
        timeup=np.inf
    else:
        timeup=float(timeup)
    # print('kadrequest')
    node_num=len(chosen_blocks)
    requests_list=[]
    server_queue=[]
    # server queue:[_server_node]:[from_node,request_block,arrive_time,time_cost,tag(fist_time_process/second_time_process/third_time_process),request_id]
    for i in range(node_num):
        server_queue.append([])
    # for communication update
    storage_per_node=[[0 for i in range(node_num)] for j in range(node_num)]#storage_per_node[from_nde][to_node]
    request_time_per_node=[[0 for i in range(node_num)] for j in range(node_num)]
    # for passive replicate : passive_type, just for return here.
    passive_type_blocks=[{} for i in range(node_num)]
    # for metrics record
    total_time_cost=[0 for i in range(node_num+1)]# stored by to_node
    total_access_times=[0 for i in range(node_num+1)]

    delayed_request=[0 for i in range(node_num)]
    delayed_time_per_request=[0 for i in range(node_num)]


    #get the happend time from increasment time list for each node.
    # fill in each request: [from_node,request_block,request_time,min_vector],min_vector=[[to_node,time_cost],...]
    for _nid in range(len(interval_list)):# 对于每一个节点
        happend_time=0
        for _tid in range(len(interval_list[_nid])):
            happend_time+=interval_list[_nid][_tid]
            min_vector,result_encode1,result_encode2,rob=dsrpal.get_block_from_which_xor(_nid,chosen_blocks[_nid][_tid])
            # get from local
            if min_vector==[-1,0]:
                dsrpal.nodes_stored_blocks_popularity[_nid][chosen_blocks[_nid][_tid]][1]+=1
                total_access_times[_nid]+=1
                storage_per_node[_nid][_nid]+=dsrpal.blocksizes[chosen_blocks[_nid][_tid]-beginID]
                if passive_type=='load' or passive_type=='load_kad':
                    passive_type_blocks[_nid][chosen_blocks[_nid][_tid]]=0
                elif passive_type=='popularity' or passive_type=='pop_kad':
                    passive_type_blocks[_nid][chosen_blocks[_nid][_tid]]=[0,0]

            else:
                # min_vector_2=min_vector[0:2]
                # min_vector_shuffle=(min_vector[3:])
                # random.shuffle(min_vector_shuffle)
                # for _min_vector_index in min_vector_shuffle:
                #     min_vector_2.append(_min_vector_index)
                min_vector_2=(min_vector)
                # random.shuffle(min_vector_2)
                requests_list.append([_nid,int(chosen_blocks[_nid][_tid]),float(happend_time),min_vector_2,result_encode1,result_encode2,rob])#1 represents not be processed yet
    # sort the request according to the happend time(request arrived time)
    requests_list=sorted(requests_list,key=lambda x:x[2])
    # issue these cmsd
    #注意，因为如果是第一次处理就成功，这个时候第二批第三批cmds应当还没发出，因此在第一批处理成功之后revoke第二批是完全没有影响的。
    # 同理，第二批处理完成之后revoke第三批也是，
    # 第二批、第三批处理完成之后revoke前面几批也是可以的，只是需要立即执行下一个命令
    
    request_res=[]#[[final_server_node,final_time_cost,excepted_cost,solve_tag，STATE，get_encode，get_blks，allreps]]
    #STATE：0：已经解决了，2：正在按照出错处理；4：按照解码处理ok；-1：尚未进行处理过
    # get_encode：现在获得的不同的编码分片们
    # get_blks：现在获得的不同的数据分片们
    # allreps：记录该区块一共有几个副本
    # 如果是经过解码过程得到结果，final_server_node是-1，final_time_cost是开始时间到最后时间的所经过的时间，excepted_cost是-1
    for i in range(len(requests_list)):
        request_res.append([])
    # request_res的index与request_list的index与server_queue中的RID是对应的。
    piece=3
    for i in range(len(requests_list)):
        from_node=requests_list[i][0]
        get_blk=requests_list[i][1]
        happen_time=requests_list[i][2]
        min_vector=requests_list[i][3]
        result_encode1=requests_list[i][4]
        result_encode1=requests_list[i][5]
        rob=requests_list[i][6]
        to_nodes=[mv_entry[0] for mv_entry in min_vector]
        real_time_cost=[mv_entry[1] for mv_entry in min_vector]
        real_piece=piece
        request_res[i]=[-1,-1,-1,-1,-1,[],[],len(to_nodes)]
        # if len(to_nodes)==1:
        #     print('lentonodes=1',request_res[i],',i=',i,'min_vector=',min_vector)
        if len(real_time_cost)<real_piece:
            real_piece=len(real_time_cost)
        for request_i_ in range(real_piece):
            rtc=real_time_cost[request_i_]
            if CRASH_TYPE=='crash' and to_nodes[request_i_] in crash_nodesid:
                continue
            server_queue[to_nodes[request_i_]].append([happen_time,rtc,1,i,0])
        xlimit=2*piece
        if xlimit>len(to_nodes):
            xlimit=len(to_nodes)
        for request_i_ in range(piece,xlimit):
            # print(xlimit)
            # print(request_i_)
            # print(len(real_time_cost))
            # if CRASH_TYPE=='crash' and to_nodes[request_i_] in crash_nodesid:
            #     continue
            server_queue[to_nodes[request_i_]].append([happen_time+timeup,real_time_cost[request_i_],2,i,0])
        for request_i_i in range(xlimit,len(to_nodes)):
            # if CRASH_TYPE=='crash' and to_nodes[request_i_i] in crash_nodesid:
            #     continue
            server_queue[to_nodes[request_i_i]].append([happen_time+2*timeup,real_time_cost[request_i_i],3,i,0])
        # 把编码分片crash时的请求也加上去，拜占庭错误时候的请求只能在处理请求消息时处理
        if CRASH_TYPE=='crash' or CRASH_TYPE=='byc':
            for re1 in result_encode1:# 注意这里没有加上解码时间开销哦
                # if CRASH_TYPE=='crash' and re1[0] in crash_nodesid:
                #     continue
                server_queue[re1[0]].append([happen_time+TIME_MAX,re1[1],4,i,0])
            for re2 in result_encode2:
                # if CRASH_TYPE=='crash' and re2[0] in crash_nodesid:
                #     continue
                server_queue[re2[0]].append([happen_time+TIME_MAX,re2[1],5,i,0])
            replicas_id=-1# 记录每一个不同的本批次其他数据分片id
            for mv_ in rob:# 对于所有需要请求的数据分片
                # print('mv_',mv_)
                replicas_id+=1
                # for mv_ in mvector_:# 对于每一个数据分片的所有可请求节点
                to_ns=[mv_entry[0] for mv_entry in mv_]
                real_time_ct=[mv_entry[1] for mv_entry in mv_]
                for request_i_ in range(len(to_ns)):# 处理每一个可请求节点
                    # if CRASH_TYPE=='crash' and to_ns[request_i_] in crash_nodesid:
                    #     continue
                    if to_ns[request_i_]==-1:
                        request_res[i][6].append(6+replicas_id)
                        # 直接下一个就OK
                        break
                    else:
                        server_queue[to_ns[request_i_]].append([happen_time+TIME_MAX,real_time_ct[request_i_],6+replicas_id,i,0])
    # get the respond time for each request.   
    # request...
    # nodes_service_queue=[0 for i in range(node_num)]
    # 按照happen_time进行排序
    for nid in range(10):
        server_queue[nid]=sorted(server_queue[nid],key=lambda x:x[0])
    #record queue#
    # print(requests_list)
    # if fwrite:
    #     print(json.dumps(requests_list),file=fwrite)

    get_blks_from_others={}

    node_cur_time=[0 for i in range(node_num)]
    HPTIME=0
    TCOST=1
    TAG=2
    RID=3
    LAST_FINISH_TIME=4
    # request_res中的编号
    STATE_FIELD=4
    GET_ENCODE_FIELD=5
    GET_BLKS_FIELD=6
    RPS_FIELD=7
    # print('start,server_queue length=',[len(sq) for sq in server_queue])
    # DEBUG0=0
    while True:   
        # DEBUG0+=1  
        next_complete_time=np.inf
        next_complete_node=-1
        next_complete_rid=-1
        next_happen_time=-1
        empty_node_count=0
        for snode in range(node_num):
            if (CRASH_TYPE=='crash' and snode in crash_nodesid) or (CRASH_TYPE=='byc' and snode==crash_nodesid[1]):
                # print('pass node=',snode)
                empty_node_count+=1
                continue
            if len(server_queue[snode])==0:
                empty_node_count+=1
                continue
            # crash节点不提供服务，拜占庭节点提供错误的服务
            #已经计算过并且不需要更新
            if server_queue[snode][0][LAST_FINISH_TIME]!=0:
                tmp_finish_time=server_queue[snode][0][LAST_FINISH_TIME]
            #否则计算结束时间
            else:
                if node_cur_time[snode]<=server_queue[snode][0][HPTIME]:#happen_time
                    tmp_finish_time=server_queue[snode][0][HPTIME]+server_queue[snode][0][TCOST]
                else:
                    tmp_finish_time=node_cur_time[snode]+server_queue[snode][0][TCOST]
                server_queue[snode][0][LAST_FINISH_TIME]=tmp_finish_time
            #使用各个节点的结束时间比较
            if next_complete_time>tmp_finish_time:
                next_complete_time=tmp_finish_time
                next_complete_node=snode
                next_complete_rid=server_queue[snode][0][RID]
                next_happen_time=server_queue[snode][0][HPTIME]
        # if next_complete_rid==-1:
        #     print('nextcomplete=-1,server_queue length=',[len(sq) for sq in server_queue])
        #     print('CRASH_NOES=',CRASH_NODES,',crash_nodesid=',crash_nodesid)
        if empty_node_count==node_num:# or (CRASH_TYPE=='crash' and empty_node_count>=node_num-CRASH_NODES) or (CRASH_TYPE=='byc' and empty_node_count>=node_num-1):
            # isexit=True
            # server_queue_length=[len(sq)for sq in server_queue]
            # for nid_ in range(node_num):
            #         if (CRASH_TYPE=='crash' and nid_ in crash_nodesid) or (CRASH_TYPE=='byc' and nid_==crash_nodesid[1])
            break
        # 开始处理不同请求的结果
        # if request_res[next_complete_rid]
        # process this cmd, get real_time_cost, server_node and revoke other request with the same RID
        # 如果该请求是第一次返回可能正确的结果
        if request_res[next_complete_rid][STATE_FIELD]==-1:
            # print('[request_by_arriveing_requests_kad_ver2]: cms update wrong!')
            # # print(request_res[next_complete_rid])
            # exit(-1)
            if server_queue[next_complete_node][0][TAG]<=3:
                # 说明是数据分片回来了，此时需要特殊考虑的只有拜占庭错误

                # 如果返回分片的是一个拜占庭节点，且类型是byzantine，此时才会算每一个节点的副本数并在处理过程中增加请求，否则统一执行超时发出请求
                if (next_complete_node in crash_nodesid and CRASH_TYPE=='byzantine'):
                    request_res[next_complete_rid][RPS_FIELD]-=1
                    # print('shard byzantine with replicas remains=',request_res[next_complete_rid],',next_complete_rid=',next_complete_rid)
                    # 如果发现所有的数据分片都不可以
                    if request_res[next_complete_rid][RPS_FIELD]==0:
                        # 拜占庭错误下所有副本节点全军覆没，此时才会考虑请求编码和副本节点
                        result_encode1=requests_list[next_complete_rid][4]
                        result_encode1=requests_list[next_complete_rid][5]
                        rob=requests_list[next_complete_rid][6]
                        # 获取每一个节点的应插入的位置 并在对应位置插入节点 同时将插入位置的头节点的LAST_FINISH_TIME 设置为0
                        placess=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
                        for re1 in result_encode1:
                            if placess[re1[0]]==-1:
                                cur=0
                                while(cur<len(server_queue[re1[0]]) and server_queue[re1[0]][cur][HPTIME]<next_complete_time):
                                    cur+=1
                                placess[re1[0]]=cur
                            server_queue[re1[0]].insert(placess[re1[0]],[next_complete_time,re1[1],4,next_complete_rid,0])
                        for re2 in result_encode2:
                            # if CRASH_TYPE=='crash' and re2[0] in crash_nodesid:
                            #     continue
                            if placess[re2[0]]==-1:
                                cur=0
                                while(cur<len(server_queue[re2[0]]) and server_queue[re2[0]][cur][HPTIME]<next_complete_time):
                                    cur+=1
                                placess[re2[0]]=cur
                            server_queue[re2[0]].insert(placess[re2[0]],[next_complete_time,re2[1],5,next_complete_rid,0])
                        replicas_id=-1
                        for mv_ in rob:
                            replicas_id+=1
                            # for mv_ in mvector_:
                            to_ns=[mv_entry[0] for mv_entry in mv_]
                            real_time_ct=[mv_entry[1] for mv_entry in mv_]
                            for request_i_ in range(len(to_ns)):
                                    # if CRASH_TYPE=='crash' and to_ns[request_i_] in crash_nodesid:
                                    #     continue
                                if to_ns[request_i_]==-1:
                                    # print('request_res append byzantine,next_compelte_rid=',next_complete_rid,'res=',request_res[next_complete_rid])
                                    request_res[next_complete_rid][6].append(6+replicas_id)
                                    # 直接下一个就OK
                                    break
                                else:
                                    if placess[to_ns[request_i_]]==-1:
                                        cur=0
                                        while(cur<len(server_queue[to_ns[request_i_]]) and server_queue[to_ns[request_i_]][cur][HPTIME]<next_complete_time):
                                            cur+=1
                                        placess[to_ns[request_i_]]=cur
                                    server_queue[to_ns[request_i_]].insert(placess[to_ns[request_i_]],[next_complete_time,real_time_ct[request_i_],6+replicas_id,next_complete_rid,0])
                        for i_ in range(len(placess)):
                            for j_ in range(placess[i_]):
                                server_queue[i_][j_][LAST_FINISH_TIME]=0
                        # 翻出这些请求后，修改状态为2，正在以错误进行处理
                        request_res[next_complete_rid][STATE_FIELD]=2
                elif (CRASH_TYPE=='byc' and next_complete_node==crash_nodesid[0]):
                    # 如果错误类型是byc且当前返回的节点是拜占庭节点，那么这个权当没收到，等待crash就ok
                    pass
                    # else:
                        #并非所有副本都不行，此时继续等待就ok，状态还是-1
                        # 此时还可以的副本可能在拜占庭节点，可能在crash节点，可能在ok的节点
                        # 对于拜占庭节点，只需等待返回就ok；对于crash节点，超时就会自动发出编码请求；对于ok的节点，只需要等待返回就ok
                        # 如果全部副本因为拜占庭错误二需要解码，才执行上述if中的过程

                else:# 返回的数据分片来自正常节点（这里不需要考虑crash，因为crash是直接不会成为next_complete_node的），因此此时一定是有效的返回
                    #此时可以正常处理并结束这个过程
                    # 可以直接使用nexthappendtime作为起始时间
                    request_res[next_complete_rid]=[next_complete_node,next_complete_time-next_happen_time,server_queue[next_complete_node][0][TCOST],server_queue[next_complete_node][0][TAG],0]# 完成后清空无用field
                    # print('DEBUG0=',DEBUG0)
            # 第一次返回的不是数据分片，可能是编码分片或者是本批次其他数据分片，
            # 改变状态，改成在错误情况下开始处理，
            # 注意如果是byc或byzantine的情况还需要判断是否请求到了拜占庭节点的分片，不要拜占庭节点的分片
            # 同时需要注意在状态2下也要注意是否直接返回副本
            else:
                request_res[next_complete_rid][STATE_FIELD]=2#正在以错误处理
                # 返回的是编码分片
                thistag=server_queue[next_complete_node][0][TAG]
                # 当返回节点不是拜占庭节点
                if (not (CRASH_TYPE=='byzantine' and next_complete_node in crash_nodesid)) and (not (CRASH_TYPE=='byc' and next_complete_node==crash_nodesid[0])):
                    if thistag==4 or thistag==5:
                        if not (thistag in request_res[next_complete_rid][GET_ENCODE_FIELD]):
                            request_res[next_complete_rid][GET_ENCODE_FIELD].append(thistag)
                    else:
                        if not(thistag in request_res[next_complete_rid][GET_BLKS_FIELD]):
                            request_res[next_complete_rid][GET_BLKS_FIELD].append(thistag)
                # else:
                #     #否则什么都不做
                #     pass
                # 看看得到的东西够不够
                # 如果够了，直接解码并填充结果改变状态
                    if len(request_res[next_complete_rid][GET_ENCODE_FIELD])+len(request_res[next_complete_rid][GET_BLKS_FIELD])>=DATA_SHARD:
                        happentime_=requests_list[next_complete_rid][2]
                        DECODE_TIME=DECODE_TIME1
                        if len(request_res[next_complete_rid][GET_ENCODE_FIELD])==2:
                            DECODE_TIME=DECODE_TIME2
                        request_res[next_complete_rid]=[-2,next_complete_time-happentime_+DECODE_TIME,-1,server_queue[next_complete_node][0][TAG],4]# 完成后清空无用field
        
        elif request_res[next_complete_rid][STATE_FIELD]==0 or request_res[next_complete_rid][STATE_FIELD]==1 or request_res[next_complete_rid][STATE_FIELD]==4:
            # 不应该出现这种情况
            # print('DEBUG0--=',DEBUG0)
            print('request_res',request_res[next_complete_rid])
            print('complete node=',next_complete_node,',nextcomplete rid=',next_complete_rid)
            print('error when request... error updating server_queue with state',request_res[next_complete_rid][STATE_FIELD])
            exit(-2)
        elif request_res[next_complete_rid][STATE_FIELD]==2:
            # 正在以错误处理的过程中得到了新的返回
            thistag=server_queue[next_complete_node][0][TAG]
            # 返回的节点是一个好节点
            if (not (CRASH_TYPE=='byzantine' and next_complete_node in crash_nodesid)) and (not (CRASH_TYPE=='byc' and next_complete_node==crash_nodesid[0])):
                if thistag<=3:#说明是数据分片直接返回
                    #中断错误处理过程，按照数据分片返回处理，标记状态为0，取消所有还没有完成的该请求id下的请求
                    request_res[next_complete_rid]=[next_complete_node,next_complete_time-next_happen_time,server_queue[next_complete_node][0][TCOST],server_queue[next_complete_node][0][TAG],0]# 完成后清空无用field
                elif thistag==4 or thistag==5:
                    if not (thistag in request_res[next_complete_rid][GET_ENCODE_FIELD]):
                        request_res[next_complete_rid][GET_ENCODE_FIELD].append(thistag)
                else:
                    if not(thistag in request_res[next_complete_rid][GET_BLKS_FIELD]):
                        request_res[next_complete_rid][GET_BLKS_FIELD].append(thistag)
                    # 看看得到的东西够不够
                    # 如果够了，直接解码并填充结果改变状态
                if thistag>3 and len(request_res[next_complete_rid][GET_ENCODE_FIELD])+len(request_res[next_complete_rid][GET_BLKS_FIELD])>=DATA_SHARD:
                    happentime_=requests_list[next_complete_rid][2]
                    DECODE_TIME=DECODE_TIME1
                    if len(request_res[next_complete_rid][GET_ENCODE_FIELD])==2:
                        DECODE_TIME=DECODE_TIME2
                    request_res[next_complete_rid]=[-2,next_complete_time-happentime_+DECODE_TIME,-1,server_queue[next_complete_node][0][TAG],4]# 完成后清空无用field
            # 返回的节点是一个不好的节点
            else:
                # 返回的是拜占庭节点，此时如果是副本，只能是byc的情况，不用处理，因为byc不通过好节点拿到副本就是通过超时获得解码
                # ，如果是byzantine，则出错，因为此时不该有副本了
                if thistag<=3:
                    if CRASH_TYPE=='byzantine':
                        # request_res[next_complete_rid][RPS_FIELD]-=1
                        print('error updating cms when state=2 and get tag<=3 from byzantine node')
                        print('request res=',request_res[next_complete_rid],',next_complete_rid=',next_complete_rid)
                        exit(-2)
                else:
                    pass#坏节点的数据，什么都不需要做
        else:
            print('error state=',request_res[next_complete_rid][STATE_FIELD])
            exit(-2)
        ####
        # if request_res[next_complete_rid][STATE_FIELD]==4:
        #     print('this solved request=',next_complete_rid,',content=',request_res[next_complete_rid])
        # 清理已经不需要的请求
        # 
        for sqlength in range(node_num):
            # crash节点不提供服务
            if (CRASH_TYPE=='crash' and sqlength in crash_nodesid) or ( CRASH_TYPE=='byc' and sqlength==crash_nodesid[1]):
                continue
            # 当前执行过的命令直接删除掉
            if sqlength==next_complete_node:
                node_cur_time[sqlength]=next_complete_time
                server_queue[sqlength]=server_queue[sqlength][1:]
                # print('clear front in node',sqlength,',now length=',len(server_queue[sqlength]))
                # continue
            sqindex=-1
            # 如果当前命令成功了，当前没有执行过的同rid的命令删除掉
            if request_res[next_complete_rid][STATE_FIELD]==0 or request_res[next_complete_rid][STATE_FIELD]==4:
                for sqinst in server_queue[sqlength][:]:#range(len(server_queue[sqlength])):
                    # print(type(server_queue))
                    # print(sqlength)
                    # print(sqindex)
                    # print(RID)
                    sqindex+=1
                    if sqinst[RID]==next_complete_rid:
                        # print('clear other cmds',sqinst[RID],',sqindex=',sqindex,',node=',sqlength,',rid=',next_complete_rid,',batch=',sqinst[TAG])
                        if request_res[next_complete_rid][STATE_FIELD]==2 and sqinst[TAG]<=3:
                            print('ERRRRRRRRRRRRRRRRRRRRR!')
                            exit(-2)
                        if sqindex==0:
                            #排名最前的cmd要么在执行一部分，要么根本还没开始执行，在当前已完成指令执行的时候在空等。无论是哪一种情况，
                            # 把需要revoke的命令的直接revoke，并把节点的当前时间设置为当前最靠前的命令执行完成的时间都是没问题的。
                            # 因为无论是正在执行还是空等，这部分时间都是真切地消耗了的，该节点后面的其他指令不会在这段时间执行。
                            server_queue[sqlength]=server_queue[sqlength][1:]
                            node_cur_time[sqlength]=next_complete_time
                            # break#这个节点不可能包含同一个请求的请求了
                        else: 
                            #not processing yet, as this cmd(next_complete_node the 0th cmd) is the first complete cmd.
                            # other cmds, which is not the 0th cmd of one node, have not been in processing yet
                            # just revoke them
                            # 不是排名最前的肯定还没开始执行，这个时候直接delete掉就可以了。
                            # print(len(server_queue[sqlength]))
                            server_queue[sqlength].remove(sqinst)#server_queue[sqlength][:sqindex]+server_queue[sqlength][sqindex+1:]
                            # print('af',len(server_queue[sqlength]))
                            # break
                        #因为每次都只会计算首个的LAST_FINISH_TIME，因此所有LAST_FINISH_TIME为之不是0的都是已经计算过且不需要更新的，
                        #是0的一定是没计算过，要么是前一个指令被revoke，要么是前一个指令正确完成被revoke
    # process request_res
    request_phase=[]#[final_serve_node]:[tag1 nums,tag2 nums,tag3 nums]
    for i in range(node_num):
        request_phase.append([0,0,0])
    for i in range(len(requests_list)):
        from_node=requests_list[i][0]
        final_serve_node=request_res[i][0]
        get_blk=requests_list[i][1]
        final_time_cost=request_res[i][1]
        excepted_time_cost=request_res[i][2]
        delay_tag=request_res[i][3]
        # request_phase[final_serve_node][delay_tag-1]+=1

        delay_time=final_time_cost-excepted_time_cost
        # if delay_time>0:
        #     delayed_request[final_serve_node]+=1
        #     delayed_time_per_request[final_serve_node]+=delay_time
        if final_serve_node>=0:
            dsrpal.nodes_stored_blocks_popularity[final_serve_node][get_blk][1]+=1
            total_access_times[final_serve_node]+=1
            total_time_cost[final_serve_node]+=final_time_cost
            storage_per_node[from_node][final_serve_node]+=dsrpal.blocksizes[get_blk-beginID]
            request_time_per_node[from_node][final_serve_node]+=final_time_cost
        else:
            if final_serve_node==-1:
                pass
                # print('err!request_res',request_res[i])
                # print('err!request_list',requests_list[i])
            else:
                total_access_times[10]+=1
                total_time_cost[10]+=final_time_cost
                # print('request_res',request_res[i])
                # print('request_list',requests_list[i])
        # if MAX_TIME<final_time_cost:
        #     MAX_TIME=final_time_cost
        if passive_type=='load' or passive_type=='load_kad':
            passive_type_blocks[from_node][get_blk]=final_time_cost
        elif (passive_type=='popularity' or passive_type=='pop_kad') and final_serve_node>0:
            passive_type_blocks[from_node][get_blk]=dsrpal.nodes_stored_blocks_popularity[final_serve_node][get_blk]
    if CRASH_TYPE!='nocrash':
        total_time=[np.sum(np.array(total_time_cost[:10])),total_time_cost[10]]
        total_acc_tm=[np.sum(np.array(total_access_times[:10])),total_access_times[10]]
    else:
        total_time=[np.sum(np.array(total_time_cost[:10])),0]#total_time_cost[10]
        total_acc_tm=[np.sum(np.array(total_access_times[:10])),0]#total_access_times[10]
        # average_time=/
    # print(average_time)
    #debug
    # print('delayed reuqest/total requests:',delayed_request,',',np.sum(np.array(total_access_times)),',ratio:',round(delayed_request/np.sum(np.array(total_access_times))*100,4))
    #end
    # total_access_times_scalar=np.sum(np.array(total_access_times))
    # print('======================================================')
    return total_time,storage_per_node,request_time_per_node,passive_type_blocks,delayed_request,delayed_time_per_request,total_access_times,total_time_cost,request_phase,total_acc_tm#round(delayed_request/total_access_times_scalar*100,4),round(delayed_time_per_request/total_access_times_scalar,6)


def request_by_arriving_requests_not_kad(interval_list,chosen_blocks,beginID,passive_type,fwrite):
    '''
    requesting by time interval, get average accessing time, 
    get communication cost and data transamission amounts between each 2 nodes.

    PARAMS:
    `interval_list` is a list of list, 
    interval_list[i] stores node i's request arrival increasment time.

    `chosen_blocks` is a list of list, 
    chosen_blocks[i] stores node i's chosen block, corresponding to the arrival time of requests.

    `beginID` indicates id of begin blocks.

    `passive_type` tells the function which sort_of_dict to record and return.

    `fwrite` is a file pointer to write. the function writes request list into this file.
    '''
    node_num=len(chosen_blocks)
    requests_list=[]
    #get the happend time from increasment time list for each node.
    # fill in each request: [from_node,to_node,request_block,request_time,time_cost]
    for _nid in range(len(interval_list)):
        happend_time=0
        for _tid in range(len(interval_list[_nid])):
            happend_time+=interval_list[_nid][_tid]
            to_node,time_cost=dsrpal.get_blockID_from_which(_nid,chosen_blocks[_nid][_tid])
            requests_list.append([_nid,int(to_node),int(chosen_blocks[_nid][_tid]),float(happend_time),time_cost])
    # sort the request according to the happend time
    requests_list=sorted(requests_list,key=lambda x:x[3])
    # get the respond time for each request.   
    # request...
    nodes_service_queue=[0 for i in range(node_num)]
    # for communication update
    storage_per_node=[[0 for i in range(node_num)] for j in range(node_num)]#storage_per_node[from_nde][to_node]
    request_time_per_node=[[0 for i in range(node_num)] for j in range(node_num)]
    # for passive replicate : passive_type
    passive_type_blocks=[{} for i in range(node_num)]
    # # for passive replicate: load
    # load_of_blocks=[{} for i in range(node_num)]# real_time_cost of [from_node][get_blk], it is a list of dict
    # # for passive replicate: popularity 
    # popularity_of_blocks=[{} for i in range(node_num)]
    # for metrics record
    total_time_cost=[0]*10# stored by to_node
    total_access_times=[0]*10
    delayed_request=[0 for i in range(node_num)]
    delayed_time_per_request=[0 for i in range(node_num)]
    #record queue#
    # print(requests_list)
    if fwrite:
        print(json.dumps(requests_list),file=fwrite)
    
    ##end##
    for i in range(len(requests_list)):
        from_node=requests_list[i][0]
        to_node=requests_list[i][1]
        get_blk=requests_list[i][2]
        happen_time=requests_list[i][3]
        time_cost=requests_list[i][4]
        dsrpal.nodes_stored_blocks_popularity[to_node][get_blk][1]+=1
        real_time_cost=time_cost
        if nodes_service_queue[to_node]>happen_time:
            real_time_cost+=(nodes_service_queue[to_node]-happen_time)
            nodes_service_queue[to_node]+=time_cost
            delayed_request[to_node]+=1
            delayed_time_per_request[to_node]+=(nodes_service_queue[to_node]-happen_time)
        else:
            nodes_service_queue[to_node]=happen_time+time_cost
        total_access_times[to_node]+=1
        total_time_cost[to_node]+=real_time_cost
        storage_per_node[from_node][to_node]+=dsrpal.blocksizes[get_blk-beginID]
        request_time_per_node[from_node][to_node]+=real_time_cost
        if passive_type=='load':
            passive_type_blocks[from_node][get_blk]=real_time_cost
        elif passive_type=='popularity':
            passive_type_blocks[from_node][get_blk]=dsrpal.nodes_stored_blocks_popularity[to_node][get_blk]
    average_time=np.sum(np.array(total_time_cost))/np.sum(np.array(total_access_times))
    #debug
    # print('delayed reuqest/total requests:',delayed_request,',',np.sum(np.array(total_access_times)),',ratio:',round(delayed_request/np.sum(np.array(total_access_times))*100,4))
    #end
    total_access_times_scalar=np.sum(np.array(total_access_times))
    return average_time,storage_per_node,request_time_per_node,passive_type_blocks,delayed_request,delayed_time_per_request,total_access_times,total_time_cost#round(delayed_request/total_access_times_scalar*100,4),round(delayed_time_per_request/total_access_times_scalar,6)


def request(bid,eid,epoch_interval,choose_distribution,nodes_num,lambdai,passive_type,fwrite,timeup):
    '''

    big request function, including all request modula logic.
    '''  
    global TEMP_COUT
    # print(DECODE_TIME1)
    # print(DECODE_TIME2)
    # 分别是：选择区块数目；选择区块编号；处理上次访问记录；生成时间序列；请求过程；数据处理
    # timearrays=[]
    # for i in range(6):
    #     timearrays.append(0)
    # choose block numbers
    # s1=time.time()
    chosen_numbers_total=get_chosen_blocks_numbers(lambdai,nodes_num,eid-bid)
    # s2=time.time()
    # timearrays[0]+=s2-s1
    # get blocks
    chosen_blocks=get_needed_blocks(bid,eid,choose_distribution,chosen_numbers_total)
    # s3=time.time()
    # timearrays[1]+=s3-s2
    # update block request epochid
    # print(dsrpal.master_node)
    # _tbs=0
    # for c in dsrpal.block_last_access_epochid:
    #     _tbs+=len(c)
    # blksnums=[len(dsrpal.master_node),_tbs]
    for blocks_set in chosen_blocks:
        for blocks in blocks_set:
            if blocks-bid in dsrpal.master_node:
                mnode=dsrpal.master_node[blocks-bid]
                if blocks in dsrpal.block_last_access_epochid[mnode] and (True not in [blocks in ebs for ebs in dsrpal.encode_blks_set]):
                    dsrpal.block_last_access_epochid[mnode][blocks]=eid
    # s4=time.time()
    # timearrays[2]+=s4-s3
    # get time intervals
    request_intervals=generate_time_increasment_list(chosen_numbers_total,epoch_interval,lambdai)
    # s5=time.time()
    # timearrays[3]+=s5-s4
    # for _nid in range(10):
    #     print(eid,',',_nid,",",request_intervals[_nid])
    #     if _nid==9:
    #         print(chosen_numbers_total)
    # request
    average_time,storage_per_node,request_time_per_node,passive_type_blks,delayed_request,delayed_time_per_request,total_access_times,total_time_cost,\
        request_tag,total_acc_tm=request_by_arriving_requests(
        request_intervals,chosen_blocks,bid,passive_type,fwrite,timeup)
    # s6=time.time()
    # timearrays[4]+=s6-s5
    # print(eid,':',request_time_per_node)
    # print('comm:')
    # for i in range(10):
    #     print(dsrpal.communication_cost[i])
    # print('comm-ori:')
    # for i in range(10):
    #     print(dsrpal.communication_cost_ori[i])
    
    # return
    # print(passive_type_blks)
    # print('delay_request=',delayed_request)
    # print('total-access-time',total_access_times)
    # print('delay-time-per=',delayed_time_per_request)
    # print('total_time-cost',total_time_cost)
    # count=-1
    # for i in total_access_times:
    #     count+=1
    #     if i==0:
    #         print('0 in total_access_times:count=',count)
    #         print(np.array([1,1])/np.array([0,1]))
    #         print('access-times:',total_access_times)
    #         print('delay-requests=',delayed_request)
    # count=-1
    # for j in total_time_cost:
    #     count+=1
    #     if j==0:
    #         print('0 in total-time-cost:count=',count)
    #         print(np.array([1,1])/np.array([0,1]))
    #         print('time-cost:',total_time_cost)
    #         print('delay-time-per=',delayed_time_per_request)
    # incase 0  be divided:
    for i in range(nodes_num):
        if total_access_times[i]==0:
            if delayed_request[i]!=0:
                print('[request]:error in delay request!')
            total_access_times[i]=1
    for i in range(nodes_num):
        if total_time_cost[i]==0:
            if delayed_time_per_request[i]!=0:
                print('[request]:error in delay_time-per-request!')
            total_time_cost[i]=1
    delay_percentile=np.array(delayed_request)/np.array(total_access_times[:nodes_num])
    delay_time_div_total_time=np.array(delayed_time_per_request)/np.array(total_time_cost[:nodes_num])
    # s7=time.time()
    # timearrays[5]+=s7-s6
    return average_time,storage_per_node,request_time_per_node,passive_type_blks,chosen_blocks,delay_percentile,delay_time_div_total_time,total_access_times,total_time_cost,request_tag,total_acc_tm

