import numpy as np
import random
import math
import DS_init as dsinit
import DS_ReplicaAlgs as dsrpal
import json

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
    Return chosen_block numbers this epoch.

    process of choosing blocks are regarded as Pission distirbution.
    we choose one chosen_block_number according to probability

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
    We randomly get a distribution of popularity rank ate the first time, if the rank_distribution is [].
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
    happend_times=2*lambdai+int(1/2*lambdai)
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
    start=0
    for i in range(granularity):
        choose_range.append(start)
        start=round(start+one_step,2)
    # debug
    # print(probability)
    # print(np.sum(probability,axis=1))

    # end
    for _nid in range(nodes_num):
        interval_lists.append(np.random.choice(choose_range,size=chosen_numbers_all_nodes[_nid],replace=True,p=probability))
    return interval_lists


def request_by_arriving_requests(interval_list,chosen_blocks,beginID,passive_type,fwrite):
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
    delayed_request=0
    delayed_time_per_request=0
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
            delayed_request+=1
            delayed_time_per_request+=(nodes_service_queue[to_node]-happen_time)
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
    return average_time,storage_per_node,request_time_per_node,passive_type_blocks,round(delayed_request/total_access_times_scalar*100,4),round(delayed_time_per_request/total_access_times_scalar,6)


def request(bid,eid,epoch_interval,choose_distribution,nodes_num,lambdai,passive_type,fwrite):
    '''

    big request function, including all request modula logic.
    '''  
    # choose block numbers
    chosen_numbers_total=get_chosen_blocks_numbers(lambdai,nodes_num,eid-bid)
    # get blocks
    chosen_blocks=get_needed_blocks(bid,eid,choose_distribution,chosen_numbers_total)
    # get time intervals
    request_intervals=generate_time_increasment_list(chosen_numbers_total,epoch_interval,lambdai)
    # request
    average_time,storage_per_node,request_time_per_node,passive_type_blks,delay_percentile,delay_per_request=request_by_arriving_requests(
        request_intervals,chosen_blocks,bid,passive_type,fwrite)
    # print(eid,':',request_time_per_node)
    # print('comm:')
    # for i in range(10):
    #     print(dsrpal.communication_cost[i])
    # print('comm-ori:')
    # for i in range(10):
    #     print(dsrpal.communication_cost_ori[i])
    
    # return
    # print(passive_type_blks)
    return average_time,storage_per_node,request_time_per_node,passive_type_blks,chosen_blocks,delay_percentile,delay_per_request

