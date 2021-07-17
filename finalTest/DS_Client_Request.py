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
    happend_times=1.5*lambdai#+int(1/2*lambdai)
    one_interval=epoch_interval/happend_times# get a approximate time range for time increasment list.
    one_step=one_interval#/granularity
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

########### do not use this ###################################################
# def request_by_arriveing_requests_kad(interval_list,chosen_blocks,beginID,fwrite,timeup,passive_type):
#     '''
#     request by arriving time, get average access time, 
#     get communication cost and data transamission amounts between each 2 nodes.

#     PARAMS:
#     `interval_list` is a list of list, 
#     interval_list[i] stores node i's request arrival increasment time.

#     `chosen_blocks` is a list of list, 
#     chosen_blocks[i] stores node i's chosen block, corresponding to the arrival time of requests.

#     `beginID` indicates id of begin blocks.

#     `passive_type` tells the function which sort_of_dict to record and return.

#     `fwrite` is a file pointer to write. the function writes request list into this file.

#     `timeup` is the maxinum time that a node wait for response. np.inf is default.
#     '''
#     node_num=len(chosen_blocks)
#     requests_list=[]
#     #get the happend time from increasment time list for each node.
#     # fill in each request: [from_node,request_block,request_time,min_vector],min_vector=[[to_node,time_cost],...]
#     for _nid in range(len(interval_list)):
#         happend_time=0
#         for _tid in range(len(interval_list[_nid])):
#             happend_time+=interval_list[_nid][_tid]
#             min_vector=dsrpal.get_block_from_which_xor(_nid,chosen_blocks[_nid][_tid])
#             requests_list.append([_nid,int(chosen_blocks[_nid][_tid]),float(happend_time),min_vector])
#     # sort the request according to the happend time(request arrived time)
#     requests_list=sorted(requests_list,key=lambda x:x[2])
#     # get the respond time for each request.   
#     # request...
#     nodes_service_queue=[0 for i in range(node_num)]
#     # for communication update
#     storage_per_node=[[0 for i in range(node_num)] for j in range(node_num)]#storage_per_node[from_nde][to_node]
#     request_time_per_node=[[0 for i in range(node_num)] for j in range(node_num)]
#     # for passive replicate : passive_type
#     passive_type_blocks=[{} for i in range(node_num)]
#     # for metrics record
#     total_time_cost=[0]*10# stored by to_node
#     total_access_times=[0]*10
#     total_request=0
#     total_valid_request=len(requests_list)
#     delayed_request=0
#     delayed_time_per_request=0
#     #record queue#
#     # print(requests_list)
#     if fwrite:
#         print(json.dumps(requests_list),file=fwrite)
    
#     ##end##
#     # request nodes sum:
#     piece=3
#     for i in range(len(requests_list)):
#         from_node=requests_list[i][0]
#         get_blk=requests_list[i][1]
#         happen_time=requests_list[i][2]
#         min_vector=requests_list[i][3]
#         ## process this request
#         to_nodes=[mv_entry[0] for mv_entry in min_vector]
#         real_time_cost=[mv_entry[1] for mv_entry in min_vector]
#         final_serve_node=-1
#         final_time_cost=np.inf
#         # request to the fixed `piece` nodes
#         min_nodes=-1
#         min_time_arrive=np.inf
#         for i in range(piece):
#             real_time_arrive=real_time_cost[i]+happen_time
#             to_node_i=to_nodes[i]
#             if nodes_service_queue[to_node_i]>happen_time:
#                 real_time_arrive=(nodes_service_queue[to_node_i])+real_time_cost[i]
#             if real_time_arrive<min_time_arrive:
#                 min_time_arrive=real_time_arrive
#                 min_nodes=to_node_i
#             total_request+=1
#         # if these request succeed:
#         if min_time_arrive-happen_time<timeup or len(to_nodes)<=piece:
#             final_serve_node=min_nodes
#             final_time_cost=min_time_arrive-happen_time
#             if nodes_service_queue[min_nodes]>happen_time:
#                 delayed_request+=1
#                 delayed_time_per_request+=(nodes_service_queue[min_nodes]-happen_time)
#             #update node_service queue
#             for i in range(piece):
#                 to_node_i=to_nodes[i]
#                 if nodes_service_queue[to_node_i]<min_time_arrive:
#                     nodes_service_queue[to_node_i]=min_time_arrive     
#             ###########
#             # print(min_time_arrive)
#             # print('dot1:',nodes_service_queue)
#             # ############# 
#         else:
#             # min_nodes=-1
#             # min_time_arrive=np.inf
#             # minnode应该继承前面的结果
#             tlimit=2*piece
#             if len(to_nodes)<2*piece:
#                 tlimit=len(to_nodes)
#             for i in range(piece,tlimit):
#                 real_time_arrive=real_time_cost[i]+happen_time+timeup
#                 to_node_i=to_nodes[i]
#                 if nodes_service_queue[to_node_i]>happen_time+timeup:
#                     real_time_arrive=(nodes_service_queue[to_node_i])+real_time_cost[i]
#                 if real_time_arrive<min_time_arrive:
#                     min_time_arrive=real_time_arrive
#                     min_nodes=to_node_i
#                 total_request+=1
#             # if these request succeed:
#             if min_time_arrive-happen_time-timeup<timeup or len(to_nodes)<=piece:
#                 final_serve_node=min_nodes
#                 final_time_cost=min_time_arrive-happen_time
#                 if nodes_service_queue[min_nodes]>happen_time:
#                     delayed_request+=1
#                     delayed_time_per_request+=(nodes_service_queue[min_nodes]-happen_time)
#                 #update node_service queue
#                 for i in range(tlimit):
#                     to_node_i=to_nodes[i]
#                     if nodes_service_queue[to_node_i]<min_time_arrive:
#                         nodes_service_queue[to_node_i]=min_time_arrive
#             else:
#                 for i in range(tlimit,len(to_nodes)):
#                     real_time_arrive=real_time_cost[i]+happen_time+2*timeup
#                     to_node_i=to_nodes[i]
#                     if nodes_service_queue[to_node_i]>happen_time+2*timeup:
#                         real_time_arrive=(nodes_service_queue[to_node_i])+real_time_cost[i]
#                     if real_time_arrive<min_time_arrive:
#                         min_time_arrive=real_time_arrive
#                         min_nodes=to_node_i
#                     total_request+=1
#                 final_serve_node=min_nodes
#                 final_time_cost=min_time_arrive-happen_time
#                 if nodes_service_queue[min_nodes]>happen_time:
#                     delayed_request+=1
#                     delayed_time_per_request+=(nodes_service_queue[min_nodes]-happen_time)
#                 #update node_service queue
#                 for i in range(tlimit):
#                     to_node_i=to_nodes[i]
#                     if nodes_service_queue[to_node_i]<min_time_arrive:
#                         nodes_service_queue[to_node_i]=min_time_arrive
#         #request done
#         # print(dsrpal.nodes_stored_blocks_popularity[final_serve_node].items())
#         # print('final_serve_node:',final_serve_node)
#         # print(dsrpal.blocks_in_which_nodes_and_timelived[get_blk-beginID].items())
#         # print(min_vector)
#         # print(nodes_service_queue)
#         if final_serve_node==-1:
#             if len(dsrpal.blocks_in_which_nodes_and_timelived[get_blk-beginID])==0:
#                 print('[FATAL]:[request_by_arriveing_requests_kad]: do not have any serve node!')
#             else:
#                 print('[FATAL]:[request_by_arriveing_requests_kad]:something wrong when requesting...')
#             exit(-1)
#         dsrpal.nodes_stored_blocks_popularity[final_serve_node][get_blk][1]+=1
#         total_access_times[final_serve_node]+=1
#         total_time_cost[final_serve_node]+=final_time_cost
#         storage_per_node[from_node][final_serve_node]+=dsrpal.blocksizes[get_blk-beginID]
#         request_time_per_node[from_node][final_serve_node]+=final_time_cost
#         if passive_type=='load' or passive_type=='load_kad':
#             passive_type_blocks[from_node][get_blk]=real_time_cost
#         elif passive_type=='popularity' or passive_type=='pop_kad':
#             passive_type_blocks[from_node][get_blk]=dsrpal.nodes_stored_blocks_popularity[final_serve_node][get_blk]
#     average_time=np.sum(np.array(total_time_cost))/np.sum(np.array(total_access_times))
#     #debug
#     # print('delayed reuqest/total requests:',delayed_request,',',np.sum(np.array(total_access_times)),',ratio:',round(delayed_request/np.sum(np.array(total_access_times))*100,4))
#     #end
#     total_access_times_scalar=np.sum(np.array(total_access_times))
#     return average_time,storage_per_node,request_time_per_node,passive_type_blocks,round(delayed_request/total_access_times_scalar*100,4),round(delayed_time_per_request/total_access_times_scalar,6)

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
    total_time_cost=[0 for i in range(node_num)]# stored by to_node
    total_access_times=[0 for i in range(node_num)]
    delayed_request=[0 for i in range(node_num)]
    delayed_time_per_request=[0 for i in range(node_num)]
    #get the happend time from increasment time list for each node.
    # fill in each request: [from_node,request_block,request_time,min_vector],min_vector=[[to_node,time_cost],...]
    for _nid in range(len(interval_list)):
        happend_time=0
        for _tid in range(len(interval_list[_nid])):
            happend_time+=interval_list[_nid][_tid]
            min_vector=dsrpal.get_block_from_which_xor(_nid,chosen_blocks[_nid][_tid])
            # get from local
            if min_vector==[[-1,0]]:
                dsrpal.nodes_stored_blocks_popularity[_nid][chosen_blocks[_nid][_tid]][1]+=1
                total_access_times[_nid]+=1
                storage_per_node[_nid][_nid]+=dsrpal.blocksizes[chosen_blocks[_nid][_tid]-beginID]
                if passive_type=='load' or passive_type=='load_kad':
                    passive_type_blocks[_nid][chosen_blocks[_nid][_tid]]=0
                elif passive_type=='popularity' or passive_type=='pop_kad':
                    passive_type_blocks[_nid][chosen_blocks[_nid][_tid]]=[0,0]

            else:
                requests_list.append([_nid,int(chosen_blocks[_nid][_tid]),float(happend_time),min_vector])#1 represents not be processed yet
    # sort the request according to the happend time(request arrived time)
    requests_list=sorted(requests_list,key=lambda x:x[2])
    # issue these cmsd
    #注意，因为如果是第一次处理就成功，这个时候第二批第三批cmds应当还没发出，因此在第一批处理成功之后revoke第二批是完全没有影响的。
    # 同理，第二批处理完成之后revoke第三批也是，
    # 第二批、第三批处理完成之后revoke前面几批也是可以的，只是需要立即执行下一个命令
    piece=3
    for i in range(len(requests_list)):
        from_node=requests_list[i][0]
        get_blk=requests_list[i][1]
        happen_time=requests_list[i][2]
        min_vector=requests_list[i][3]
        to_nodes=[mv_entry[0] for mv_entry in min_vector]
        real_time_cost=[mv_entry[1] for mv_entry in min_vector]
        real_piece=piece
        if len(real_time_cost)<real_piece:
            real_piece=len(real_time_cost)
        for request_i_ in range(real_piece):
            rtc=real_time_cost[request_i_]
            server_queue[to_nodes[request_i_]].append([happen_time,rtc,1,i,0])
        xlimit=2*piece
        if xlimit>len(to_nodes):
            xlimit=len(to_nodes)
        for request_i_ in range(piece,xlimit):
            # print(xlimit)
            # print(request_i_)
            # print(len(real_time_cost))
            server_queue[to_nodes[request_i_]].append([happen_time+timeup,real_time_cost[request_i_],2,i,0])
        for request_i_i in range(xlimit,len(to_nodes)):
            server_queue[to_nodes[request_i_i]].append([happen_time+2*timeup,real_time_cost[request_i_i],3,i,0])
    # get the respond time for each request.   
    # request...
    # nodes_service_queue=[0 for i in range(node_num)]
    
    #record queue#
    # print(requests_list)
    # if fwrite:
    #     print(json.dumps(requests_list),file=fwrite)

    request_res=[]#[[final_server_node,final_time_cost,excepted_cost,solve_tag]]
    for i in range(len(requests_list)):
        request_res.append([])
    
    node_cur_time=[0 for i in range(node_num)]
    HPTIME=0
    TCOST=1
    TAG=2
    RID=3
    LAST_FINISH_TIME=4
    while True:   
        next_complete_time=np.inf
        next_complete_node=-1
        next_complete_rid=-1
        next_happen_time=-1
        empty_node_count=0
        for snode in range(node_num):
            if len(server_queue[snode])==0:
                empty_node_count+=1
                continue
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
        if empty_node_count==node_num:
            break
        # process this cmd, get real_time_cost, server_node and revoke other request with the same RID
        if request_res[next_complete_rid]!=[]:
            print('[request_by_arriveing_requests_kad_ver2]: cms update wrong!')
            # print(request_res[next_complete_rid])
            exit(-1)
        request_res[next_complete_rid]=[next_complete_node,next_complete_time-next_happen_time,server_queue[next_complete_node][0][TCOST],server_queue[next_complete_node][0][TAG]]

        for sqlength in range(node_num):
            if sqlength==next_complete_node:
                node_cur_time[sqlength]=next_complete_time
                server_queue[sqlength]=server_queue[sqlength][1:]
                continue
            for sqindex in range(len(server_queue[sqlength])):
                # print(type(server_queue))
                # print(sqlength)
                # print(sqindex)
                # print(RID)
                if server_queue[sqlength][sqindex][RID]==next_complete_rid:
                    if sqindex==0:
                        #排名最前的cmd要么在执行一部分，要么根本还没开始执行，在当前已完成指令执行的时候在空等。无论是哪一种情况，
                        # 把需要revoke的命令的直接revoke，并把节点的当前时间设置为当前最靠前的命令执行完成的时间都是没问题的。
                        # 因为无论是正在执行还是空等，这部分时间都是真切地消耗了的，该节点后面的其他指令不会在这段时间执行。
                        server_queue[sqlength]=server_queue[sqlength][1:]
                        node_cur_time[sqlength]=next_complete_time
                        break#这个节点不可能包含同一个请求的请求了
                    else: 
                        #not processing yet, as this cmd(next_complete_node the 0th cmd) is the first complete cmd.
                        # other cmds, which is not the 0th cmd of one node, have not been in processing yet
                        # just revoke them
                        # 不是排名最前的肯定还没开始执行，这个时候直接delete掉就可以了。
                        # print(len(server_queue[sqlength]))
                        server_queue[sqlength]=server_queue[sqlength][:sqindex]+server_queue[sqlength][sqindex+1:]
                        # print('af',len(server_queue[sqlength]))
                        break
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
        request_phase[final_serve_node][delay_tag-1]+=1

        delay_time=final_time_cost-excepted_time_cost
        if delay_time>0:
            delayed_request[final_serve_node]+=1
            delayed_time_per_request[final_serve_node]+=delay_time
        dsrpal.nodes_stored_blocks_popularity[final_serve_node][get_blk][1]+=1
        total_access_times[final_serve_node]+=1
        total_time_cost[final_serve_node]+=final_time_cost
        storage_per_node[from_node][final_serve_node]+=dsrpal.blocksizes[get_blk-beginID]
        request_time_per_node[from_node][final_serve_node]+=final_time_cost
        if passive_type=='load' or passive_type=='load_kad':
            passive_type_blocks[from_node][get_blk]=real_time_cost
        elif passive_type=='popularity' or passive_type=='pop_kad':
            passive_type_blocks[from_node][get_blk]=dsrpal.nodes_stored_blocks_popularity[final_serve_node][get_blk]
    average_time=np.sum(np.array(total_time_cost))/np.sum(np.array(total_access_times))
    #debug
    # print('delayed reuqest/total requests:',delayed_request,',',np.sum(np.array(total_access_times)),',ratio:',round(delayed_request/np.sum(np.array(total_access_times))*100,4))
    #end
    # total_access_times_scalar=np.sum(np.array(total_access_times))
    return average_time,storage_per_node,request_time_per_node,passive_type_blocks,delayed_request,delayed_time_per_request,total_access_times,total_time_cost,request_phase#round(delayed_request/total_access_times_scalar*100,4),round(delayed_time_per_request/total_access_times_scalar,6)


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
    # choose block numbers
    chosen_numbers_total=get_chosen_blocks_numbers(lambdai,nodes_num,eid-bid)
    # get blocks
    chosen_blocks=get_needed_blocks(bid,eid,choose_distribution,chosen_numbers_total)
    # update block request epochid
    # print(dsrpal.master_node)
    for blocks_set in chosen_blocks:
        for blocks in blocks_set:
            mnode=dsrpal.master_node[blocks-bid]
            if dsrpal.block_last_access_epochid[mnode][blocks]!=np.inf:
                dsrpal.block_last_access_epochid[mnode][blocks]=eid
    # get time intervals
    request_intervals=generate_time_increasment_list(chosen_numbers_total,epoch_interval,lambdai)
    # request
    average_time,storage_per_node,request_time_per_node,passive_type_blks,delayed_request,delayed_time_per_request,total_access_times,total_time_cost,request_tag=request_by_arriving_requests(
        request_intervals,chosen_blocks,bid,passive_type,fwrite,timeup)
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
    for i in range(len(total_access_times)):
        if total_access_times[i]==0:
            if delayed_request[i]!=0:
                print('[request]:error in delay request!')
            total_access_times[i]=1
    for i in range(len(total_time_cost)):
        if total_time_cost[i]==0:
            if delayed_time_per_request[i]!=0:
                print('[request]:error in delay_time-per-request!')
            total_time_cost[i]=1
    delay_percentile=np.array(delayed_request)/np.array(total_access_times)
    delay_time_div_total_time=np.array(delayed_time_per_request)/np.array(total_time_cost)
    return average_time,storage_per_node,request_time_per_node,passive_type_blks,chosen_blocks,delay_percentile,delay_time_div_total_time,total_access_times,total_time_cost,request_tag

