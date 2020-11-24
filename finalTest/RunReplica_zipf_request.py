#YaYi 2020.10.13

import numpy as np
import json
import matplotlib.pyplot as plt
import copy
import math
import sys

import InitChainAndNodes_zipf
import ReplicationAlgorithms_zipf

"""
the main program.

"""

# how many times is a block been accessed in step epoches.
block_access_times_in_each_epoch_step={}

request_block_ID=[]

def init_environment():
    """ () -> ( float)
    
    Init global variables in ReplicationAlgorithms_zipf.i.e. get the running environment ready.
    return all storage of one copy of all blocks.
    """
    begin_id=654000
    static_blks=600
    end_id=begin_id+1000
    nodes_n=10
    communication_distribution_type='normal'#'1'

    blk_size,all_storage=InitChainAndNodes_zipf.load_blocksizes(begin_id,end_id)
    communication_cst=InitChainAndNodes_zipf.generate_communication_cost(nodes_n,communication_distribution_type)
    
    ReplicationAlgorithms_zipf.init_all_settings(blk_size,communication_cst,begin_id,end_id,static_blks,nodes_n)
    
    # all params needed can be accessed from ReplicationAlgorithms_zipf.param

    # return max_level
    return all_storage

def replication_run(get_average_time=True,get_storage_used=False,get_replica_use_ratio=False):
    """ () - (list of float, list of list of float, list of list of float)

    run a certain replica algorithm, and store the average cost time in every dynamic epoch.
    1. time cost: index=epoch, value=time_cost of system
    2. storage used: index0=nodeID,index1=epoch,value=storage consumption
    3. use ratio: index0=blockID, index1=epoch, value=use ration of block replica

    """
    # system params
    '''
    1：distribution: zipf/zipfr
    2: replicas number(1,2,..)
    - : passive-type[additional params: lambda(exception of chosen block numbers).] (nopassive , random, popularity, load)
    - : active-type[additional params: topnumber]( noactive , random, calculate)
    - : expel-type[additional params:lifetime/topnumber](curve, llu, noexpel)
    - : total-running-times
    '''
    # params used to name files
    passive_item='nopassive'
    active_item='noactive'
    expel_item='noexpel'

    # chosen block type :nipopows
    chosen_block_distribution=sys.argv[1]
    # replica nummbers
    piece=int(sys.argv[2])
    # passive alg type
    passive_replicate_type=sys.argv[3]
    # next_params
    next_param_index=4
    lambdai=10 # default
    #switch on/off replicate
    passive_on=False
    if passive_replicate_type!='nopassive':
        passive_on=True
        # how many requests in step epoch
        lambdai=int(sys.argv[next_param_index])
        next_param_index+=1
        # modify the passive item of file name
        passive_item=passive_replicate_type+str(lambdai)
    # active alg type
    active_replicate_type=sys.argv[next_param_index]#'calculate'#'random'#'calculate'
    next_param_index+=1
    # active replica params- default = 3
    top_num_to_offload=3
    # switch on/off active replica
    active_on=False
    if active_replicate_type!='noactive':
        active_on=True
        # active replicate params
        top_num_to_offload=int(sys.argv[next_param_index])
        next_param_index+=1
        # modify the active item of file name
        active_item=active_replicate_type+str(top_num_to_offload)
    # expel type
    expel_type=sys.argv[next_param_index]#'curve'#'llu' 'noexpel' 'curve'
    next_param_index+=1
    # expel llu params
    last_num_to_expel=3
    # expel replica numbers
    period=3 # default
    if expel_type=='curve':
        period=int(sys.argv[next_param_index])
        next_param_index+=1
        expel_item=expel_type+str(period)
    elif expel_type=='llu':
        last_num_to_expel=int(sys.argv[next_param_index])
        next_param_index+=1
        expel_item=expel_type+str(last_num_to_expel)
    # total runing times - default 10/100
    total_times=int(sys.argv[next_param_index])
    next_param_index+=1
    

 ####### DO NOT TOUCH 

    # epoch gap 
    step=1
    
    if total_times!=1:
        get_replica_use_ratio=False


    # average time, a list of list of float
    avg_time=[]
    # blocks size stored by nodes, a list of list of float. key=nodeID,value=blocksize
    block_sizes_stored_by_nodes=[]
    total_storage_one_replica=[0]*(ReplicationAlgorithms_zipf.endID-ReplicationAlgorithms_zipf.beginID-ReplicationAlgorithms_zipf.static_blocks+1)
    total_storage_one_replica[0]=sum(ReplicationAlgorithms_zipf.blocksizes[:ReplicationAlgorithms_zipf.static_blocks])
    # use ratio of each block is each epoch.
    # a list of list of float. key=blockID, value=use ratio
    block_use_ratio=[]

    # rank_distribution , prepared for zipfr
    rank_distribution=[]
    if total_times!=1:
        total_times=1
    
    for i in range(10):
        request_block_ID.append([])
    
    

    # filename to store average_time_cost statistical data
    # file_average_time='./finalTest/averageTime-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'
    file_average_time='./finalTest/finalRes/A-'+chosen_block_distribution+'-'+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.txt'
    #file name to store storage used by each node in every runtime
    # file_storage_used='./finalTest/storageUsed-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'
    file_storage_used='./finalTest/finalRes/S-'+chosen_block_distribution+'-'+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.txt'
    #file name to store each blocks' use ratio in each epoch*step in every runtime
    # file_use_ratio='./finalTest/useRatio-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'
    file_use_ratio='./finalTest/finalRes/U-'+chosen_block_distribution+'-'+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.txt'

    #open storage used file to write if it's true
    if get_storage_used:
        file_storage_used_write=open(file_storage_used,'w')
        print(ReplicationAlgorithms_zipf.beginID+ReplicationAlgorithms_zipf.static_blocks,' ',ReplicationAlgorithms_zipf.endID,' ',step,file=file_storage_used_write)
    if get_replica_use_ratio:
        file_use_ratio_write=open(file_use_ratio,'w')
        print(ReplicationAlgorithms_zipf.beginID+ReplicationAlgorithms_zipf.static_blocks,' ',ReplicationAlgorithms_zipf.endID,' ',step,file=file_use_ratio_write)
    
    # file_single_time='./finalTest/finalRes/debug/Single-'+chosen_block_distribution+'-'+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.csv'
    # f_single_time=open(file_single_time,'w')
    fn='./finalTest/finalRes/debug/final-expel-a.txt'
    fw=open(fn,'w+')
    fp_name='./finalTest/finalRes/debug/expel-popularity-list.txt'
    fp=open(fp_name,'w')
    for run_times in range(total_times):
        # store all avg_time in each runtime
        print('(',run_times+1,'/',total_times,')')
        avg_time.append([])
        block_use_ratio_one_runtime=[]
        block_sizes_stored_by_nodes_tmp=[]

        ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived.clear()
        ReplicationAlgorithms_zipf.nodes_stored_blocks_popularity.clear()
        ReplicationAlgorithms_zipf.nodes_storage_used.clear()
        rank_distribution.clear()
        
        # statically assign
        ReplicationAlgorithms_zipf.static_assign_blocks(piece,period)
        # dynamic assign
        # active->request->passive->expel
        start_point=ReplicationAlgorithms_zipf.beginID+ReplicationAlgorithms_zipf.static_blocks
        ##!!!DEBUG
        # data_store_in=open('./finalTest/finalRes/debug/store-nodes-runtime.txt','w')
        # files_index=10
        # datafile_index=[]
        # expelfile_index=[]
        # activefile_index=[]
        # for i in range(files_index):
        #     datafile_index.append(open('./finalTest/finalRes/debug/'+str(active_item+'-'+expel_item)+'-popularity-node'+str(i)+'-runtime.txt','w'))
        #     expelfile_index.append(open('./finalTest/finalRes/debug/'+str(active_item+'-'+expel_item)+'-expel-chosen-block-node'+str(i)+'-runtime.txt','w'))
        #     activefile_index.append(open('./finalTest/finalRes/debug/'+str(active_item+'-'+expel_item)+'-active-chosen-block-node'+str(i)+'-runtime.txt','w'))
        ## end
        for end_since in range(ReplicationAlgorithms_zipf.beginID+ReplicationAlgorithms_zipf.static_blocks,ReplicationAlgorithms_zipf.endID,step):
            
            average_time_i=.0
            block_size_add_up=0
            # choose lambdai nodes randomly
            # replace = true
            block_access_times_in_each_epoch_step.clear()
            # shift popularity. before init new coming block == after init new coming block
            ReplicationAlgorithms_zipf.shift_popularity()
            ### !!!DEBUG
            # if run_times==0 and end_since==ReplicationAlgorithms_zipf.endID-1:
            #     # print(json.dumps(ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived),file=data_store_in)
            #     for i in range(ReplicationAlgorithms_zipf.beginID,ReplicationAlgorithms_zipf.endID):
            #         print(ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived[i-ReplicationAlgorithms_zipf.beginID],file=data_store_in)
            # if run_times==0:# and end_since==ReplicationAlgorithms_zipf.endID-1:
            #     for i in range(files_index):
            #         Popu_dict=ReplicationAlgorithms_zipf.nodes_stored_blocks_popularity[i]
            #         Popu_dict=sorted(Popu_dict.items(),key=lambda x:x[1][0]+x[1][1],reverse=True)
            #         print('epoch=',end_since,',',Popu_dict , file=datafile_index[i])
            ### end debug
            # init new coming block
            for i in range(10):
                request_block_ID[i].clear()

            for all_blocks in range(step):
                ReplicationAlgorithms_zipf.initial_assign_block(end_since+all_blocks,piece,period)
                block_size_add_up+=ReplicationAlgorithms_zipf.blocksizes[end_since+all_blocks-start_point]
            # active replicate
            if active_on:
                nodes_active_replicate=range(ReplicationAlgorithms_zipf.nodes_num)
                for nodeID in nodes_active_replicate:
                    _=ReplicationAlgorithms_zipf.active_dynamic_replication_one_node(nodeID,top_num_to_offload,active_replicate_type,period)
                    # cn_debug=sorted(cn_debug.items(),key=lambda x:x[0],reverse=False)
                    # print('epoch=',end_since,',',cn_debug,file=activefile_index[nodeID])
            # print(ReplicationAlgorithms_zipf.nodes_stored_blocks_popularity)
            #request
            block_numbers_sum=0
            # this_epoch_all_node_request_time=[]
            for nodeID in range(ReplicationAlgorithms_zipf.nodes_num):
                blocks_numbers=InitChainAndNodes_zipf.get_chosen_blocks_numbers(lambdai)
                if blocks_numbers>end_since-ReplicationAlgorithms_zipf.beginID:
                    blocks_numbers=end_since-ReplicationAlgorithms_zipf.beginID
                # if blocks_numbers>end_since-ReplicationAlgorithms_zipf.beginID:
                #     blocks_numbers=end_since-ReplicationAlgorithms_zipf.beginID
                # print(blocks_numbers)
                block_numbers_sum+=blocks_numbers
                average_time_i_tmp,rank_distribution,single_request_time,chosen_blocksID=get_one_total_time_and_replicate(nodeID,end_since+1,passive_replicate_type,period,blocks_numbers,chosen_block_distribution,True and passive_on,rank_distribution)
                # this_epoch_all_node_request_time.append(single_request_time)
                # printstring=str(average_time_i_tmp/len(chosen_blocksID))
                # i=0
                # for chosen_block_id in chosen_blocksID:
                #     bid=str(chosen_block_id)
                #     sst=str(single_request_time[i])
                #     sl=str(len(ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived[chosen_block_id-ReplicationAlgorithms_zipf.beginID]))
                #     printstring+=','+str(sst)
                #     i+=1
                # print('epoch=',end_since,': ',printstring,file=f_single_time)
                average_time_i+=average_time_i_tmp
            
            # average requesting time per block
            # print('sum:',block_numbers_sum)
            average_time_i/=block_numbers_sum
            avg_time[run_times].append(average_time_i)
            avg_request_time=average_time_i
            ##### output these times
            # p_string=''
            # std_v=0
            # max_request_time=0
            # max_request_time_block=0
            # min_request_time=np.inf
            # for _nid in range(len(this_epoch_all_node_request_time)):
            #     for _bid in range(len(this_epoch_all_node_request_time[_nid])):
            #         this_request_time=this_epoch_all_node_request_time[_nid][_bid]
            #         p_string+=str(this_request_time)+','
            #         # std_v+=(this_request_time-avg_request_time)*(this_request_time-avg_request_time)
            #         # if this_request_time>max_request_time:
            #         #     max_request_time=this_request_time
            #         #     max_request_time_block=_bid
            #         # if this_request_time<min_request_time:
            #         #     min_request_time=this_request_time
            # # std_v/=(block_numbers_sum)
            # # std_v=math.sqrt(std_v)
            # # p_string+=str(avg_request_time)+','
            # # p_string+=str(std_v)+','+str(max_request_time)+','+str(min_request_time)
            # p_string[1:]
            # if end_since>=ReplicationAlgorithms_zipf.endID-20:
            #     print(p_string,file=f_single_time)

            if end_since==ReplicationAlgorithms_zipf.endID:
                pstring=''
                
                print('requesting...')
                for i in range(100):
                    average_time_i_tmp,rank_distribution,single_request_time,chosen_blocksID=get_one_total_time_and_replicate(nodeID,end_since,passive_replicate_type,period,blocks_numbers,chosen_block_distribution,False and passive_on,rank_distribution)
                    for i in range(len(single_request_time)):
                        if ReplicationAlgorithms_zipf.endID-chosen_blocksID[i]<50:
                        # total_request_time_output.append(time_r)
                            pstring+=','+str(single_request_time[i])
                ##output:
                fname_output_100='./finalTest/finalRes/debug/only-request'+str(passive_item)+'-'+str(active_item)+'-'+str(expel_item)+'.csv'
                file_in=open(fname_output_100,'w')
                pstring=pstring[1:]
                print(pstring,file=file_in)
                file_in.close()

            # print('epoch=',end_since,'max_request_time_block:',max_request_time_block)
            # ### !!!DEBUG
            # if run_times==0 and end_since==ReplicationAlgorithms_zipf.endID-1:
            #     print(json.dumps(ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived),file=data_store_in)
            #     for i in range(ReplicationAlgorithms_zipf.beginID,ReplicationAlgorithms_zipf.endID):
            #         print(ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived[i-ReplicationAlgorithms_zipf.beginID],file=data_store_in)
            # if run_times==0:# and end_since==ReplicationAlgorithms_zipf.endID-1:
            #     for i in range(files_index):
            #         Popu_dict=ReplicationAlgorithms_zipf.nodes_stored_blocks_popularity[i]
            #         Popu_dict=sorted(Popu_dict.items(),key=lambda x:x[1][0]+x[1][1],reverse=True)
            #         print('epoch=',end_since,',',Popu_dict , file=datafile_index[i])
            #     # for i in range(ReplicationAlgorithms_zipf.beginID,ReplicationAlgorithms_zipf.endID):
            #     #     print(ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived[i-ReplicationAlgorithms_zipf.beginID],file=datafilein)
            # ### end debug
            # update lifetime and expel dead blocks
                

            if expel_type!='noexpel':
                debug_expel_blocks=ReplicationAlgorithms_zipf.expel_blocks(expel_type,end_since,step,last_num_to_expel,fp)

                if end_since>=ReplicationAlgorithms_zipf.endID-10:
                    
                    print('epoch=',end_since,file=fw)
                    for i in range(10):
                        print('blocks get from node ',i,': ',sorted([rb-654000 for rb in request_block_ID[i]]) ,file=fw)
                    print('======',file=fw)
                    for i in range(10):
                        print('blocks expelled by node ',i,': ',sorted([deb-654000 for deb in debug_expel_blocks[i]]),file=fw)
                    print('======',file=fw)
                    print('======',file=fw)
                # for i in range(len(expel_blocks)):
                #     print('epoch=',end_since,',',sorted(expel_blocks[i]),file=expelfile_index[i])
            # append storage_used if it's true
            if get_storage_used:
                # print(ReplicationAlgorithms_zipf.nodes_storage_used)
                storage_tmp=copy.copy(ReplicationAlgorithms_zipf.nodes_storage_used)
                block_sizes_stored_by_nodes_tmp.append(storage_tmp)
                # print(block_sizes_stored_by_nodes_tmp[0])
                total_storage_one_replica[end_since-(start_point)+1]=total_storage_one_replica[end_since-(start_point)]+block_size_add_up
            if get_replica_use_ratio:
                use_ratio_one_epoch=get_ratio_from_access_times(block_access_times_in_each_epoch_step)
                block_use_ratio_one_runtime.append(use_ratio_one_epoch)
        ##!!!DEBUG
        # for i in range(files_index):
        #     datafile_index[i].close()
        #     activefile_index[i].close()
        #     expelfile_index[i].close()
        ### end
        # data_store_in.close()
        # get sum of use ratio after 1 runtime
        if get_replica_use_ratio:
            block_use_ratio.append(block_use_ratio_one_runtime)
            block_use_ratio=[np.sum(block_use_ratio,axis=0)]
            # print(block_use_ratio)
            
        # get sum after 1 runtime
        if get_storage_used:
            block_sizes_stored_by_nodes.append(block_sizes_stored_by_nodes_tmp)
            # print(block_sizes_stored_by_nodes_tmp)
            block_sizes_stored_by_nodes=[np.sum(block_sizes_stored_by_nodes,axis=0)]
            # print(block_sizes_stored_by_nodes)
    # f_single_time.close()
    #get mean and store them
    if get_replica_use_ratio:
        block_use_ratio=np.array(block_use_ratio[0])/total_times
        block_use_ratio=block_use_ratio.T
        for i in range(len(block_use_ratio)):
            print(json.dumps(block_use_ratio[i].tolist()),file=file_use_ratio_write)
    # get mean and store them
    if get_storage_used:
        # get total storage by store one replica
        print(json.dumps(total_storage_one_replica[1:]),file=file_storage_used_write)

        block_sizes_stored_by_nodes=np.array(block_sizes_stored_by_nodes[0])/total_times
        block_sizes_stored_by_nodes=block_sizes_stored_by_nodes.T
        for i in range(len(block_sizes_stored_by_nodes)):
            # print(block_sizes_stored_by_nodes[i])
            print(json.dumps(block_sizes_stored_by_nodes[i].tolist()),file=file_storage_used_write)
    # got all average_time, which is a list of list of float
    # store them
    if get_average_time:
        with open(file_average_time,'w') as file_write:
            print(ReplicationAlgorithms_zipf.beginID+ReplicationAlgorithms_zipf.static_blocks,' ',ReplicationAlgorithms_zipf.endID,' ',step,file=file_write)
            avg_time_mean=np.mean(avg_time,axis=0)
            print(json.dumps(avg_time_mean.tolist()),file=file_write)
    if get_storage_used:
        file_storage_used_write.close()
    if get_replica_use_ratio:
        file_use_ratio_write.close()
    fw.close()
    fp.close()
   



def get_one_total_time_and_replicate(nodeID,end_since,passive_replicate_type,period,block_numbers,chosen_block_distribution,valid_replicate,rank_distribution):
    """(int,int,str,int,str,int,str,int,bool) -> float

    one requester request a set of blocks and get total request time.
    Return the total request time.
    Return rank_distribution after this time

    if valid_replicate is True, replicate and update popularity.
    """

    # time used to get all these blocks.
    time_used=0
    # chosen blocks
    chosen_blocks=[]
    # sort_value_dict is used for dynamic replication
    chosen_blocks_popularity={}
    chosen_blocks_load={}
    sort_value_dict=[]
    popularity_passing_dict={}

    # get block_numbers blocks based on chosen_block_distribution
    chosen_blocks,rd=InitChainAndNodes_zipf.get_needed_blocks(ReplicationAlgorithms_zipf.beginID,end_since,chosen_block_distribution,block_numbers,rank_distribution)
    #debug
    # num_of_blocks=len(chosen_blocks)
    # print(num_of_blocks,',',int(math.log2(end_since-ReplicationAlgorithms_zipf.beginID)))
    # update access times of chosen blocks and
    # calculate time
    signle_request_time=[]
    for blockID in chosen_blocks:
        min_node,time_cost=ReplicationAlgorithms_zipf.get_blockID_from_which(nodeID,blockID)
        # update this epoch popularity
        # print(ReplicationAlgorithms_zipf.nodes_stored_blocks_popularity[min_node][blockID])
        if valid_replicate:# and min_node!=nodeID:
            ReplicationAlgorithms_zipf.nodes_stored_blocks_popularity[min_node][blockID][1]+=1
        if end_since>=ReplicationAlgorithms_zipf.endID-10 and min_node!=nodeID:
            request_block_ID[min_node].append(blockID)
        if end_since>=ReplicationAlgorithms_zipf.endID-10 and min_node==nodeID:
            request_block_ID[min_node].append(blockID+1000)
        # record popularity, for choosing blocks and for popularity passing
        popularity_blockID=ReplicationAlgorithms_zipf.nodes_stored_blocks_popularity[min_node][blockID]
        chosen_blocks_popularity[blockID]=popularity_blockID[0]+popularity_blockID[1]
        popularity_passing_dict[blockID]=popularity_blockID
        # record time cost
        chosen_blocks_load[blockID]=time_cost
        #record access time
        # if blockID in block_access_times_in_each_epoch_step:
        #     block_access_times_in_each_epoch_step[blockID]+=1
        # else:
        #     block_access_times_in_each_epoch_step[blockID]=0
        # receive blocks one by one
        time_used+=time_cost
        signle_request_time.append(time_cost)
    # replicate if valid_replicate is True
    if valid_replicate:
        if passive_replicate_type=='popularity':
            sort_value_dict=chosen_blocks_popularity
        elif passive_replicate_type=='load':
            sort_value_dict=chosen_blocks_load
        else:
            sort_value_dict=[]
        ReplicationAlgorithms_zipf.passive_dynamic_replication_one_node(chosen_blocks,nodeID,passive_replicate_type,sort_value_dict,period,popularity_passing_dict)
    # return total time
    return time_used,rd,signle_request_time,chosen_blocks
    
def get_total_access_time():
    """ () -> dict
    Return total access time of each block based on ReplicationAlgorithms_zipf.nodes_stored_blocks_popularity
    """

    total_access_times={}

    # append popularity in each node of each block
    # popularity is a little lower as self-accesses are excluded
    for node_blocks in ReplicationAlgorithms_zipf.nodes_stored_blocks_popularity:
        for kvs in node_blocks.items():
            if kvs[0] in total_access_times:
                total_access_times[kvs[0]]+=(kvs[1][0]+kvs[1][1])
            else:
                total_access_times[kvs[0]]=0
    
    return total_access_times

def get_ratio_from_access_times(access_times_dict):
    """dict -> list of float

    Return use ratio for each block in ReplicationAlgorithms_zipf.beginID and ReplicationAlgorithms_zipf.endID in this epoch.
    """
    begin_id=ReplicationAlgorithms_zipf.beginID
    end_id=ReplicationAlgorithms_zipf.endID
    # use ratio of each replica
    use_ratio=[0]*(ReplicationAlgorithms_zipf.endID-ReplicationAlgorithms_zipf.beginID)
    # number of replicas of each block in this epoch
    replica_nums_of_blocks=[0]*(ReplicationAlgorithms_zipf.endID-ReplicationAlgorithms_zipf.beginID)

    # get replica num from ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived
    for i in range(0,len(ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived)):
        replica_nums_of_blocks[i]=len(ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived[i])

    for kvs in access_times_dict.items():
        use_ratio[kvs[0]-begin_id]=kvs[1]
    for i in range(len(use_ratio)):
        if replica_nums_of_blocks[i]:
            use_ratio[i]/=replica_nums_of_blocks[i]
    #debug
    # for i in range(len(use_ratio)):
    #     if use_ratio[i]!=0:
    #         print(access_times_dict[i+begin_id])
    #         print(replica_nums_of_blocks[i])
    #         print('---')    
    
    # return use ratio
    return use_ratio

def get_storage_place():
    """

    get current block distribution, and save them into file_store_distribution
    """

    file_store_distibution='./finalTest/storeDistribution.txt'
    with open(file_store_distibution,'w') as store_file:
        for i in range(len(ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived)):
            block_id=i+ReplicationAlgorithms_zipf.beginID
            actual=len(ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived[i])
            stored_nodes=[kvs[0] for kvs in  ReplicationAlgorithms_zipf.blocks_in_which_nodes_and_timelived[i].items()]
            print('block:',block_id,'replica nums=',actual,'stored nodes=',stored_nodes,file=store_file)


if __name__=='__main__':
    all_storage_cost=init_environment()
    replication_run(False,False,False)
    get_storage_place()
    print('running done')