#YaYi 2020.10.13

import numpy as np
import json
import matplotlib.pyplot as plt
import copy
import math
import InitChainAndNodes
import ReplicationAlgorithms

"""
the main program.

"""

# how many times is a block been accessed in step epoches.
block_access_times_in_each_epoch_step={}

def init_environment():
    """ () -> (int, float)
    
    Init global variables in ReplicationAlgorithms.i.e. get the running environment ready.
    Return max_level,return all storage of one copy of all blocks.
    """
    begin_id=2016
    static_blks=200
    end_id=begin_id+400
    nodes_n=10
    communication_distribution_type='1'

    blk_list,max_level=InitChainAndNodes.build_block_list(begin_id,end_id)
    blk_size,all_storage=InitChainAndNodes.load_blocksizes(begin_id,end_id)
    communication_cst=InitChainAndNodes.generate_communication_cost(nodes_n,communication_distribution_type)
    
    ReplicationAlgorithms.init_all_settings(blk_list,blk_size,communication_cst,begin_id,end_id,static_blks,nodes_n)
    
    # all params needed can be accessed from ReplicationAlgorithms.param

    # return max_level
    return max_level,all_storage

def replication_run(max_level,get_average_time=True,get_storage_used=False,get_replica_use_ratio=False):
    """ () - (list of float, list of list of float, list of list of float)

    run a certain replica algorithm, and store the average cost time in every dynamic epoch.
    1. time cost: index=epoch, value=time_cost of system
    2. storage used: index0=nodeID,index1=epoch,value=storage consumption
    3. use ratio: index0=blockID, index1=epoch, value=use ration of block replica

    """


    # params of NIPoPoWs
    m=3
    # chosen block type :nipopows
    chosen_block_distribution='nipopows'#'uniform'#'zipf'#'nipopows'#'flyclient'
    # passive alg type
    passive_replicate_type='popularity'
    # active alg type
    active_replicate_type='calculate'
    # how many requests in step epoch
    lambdai=4
    # epoch gap 
    step=1
    # total runing times
    total_times=100
    # average time, a list of list of float
    avg_time=[]
    # blocks size stored by nodes, a list of list of float. key=nodeID,value=blocksize
    block_sizes_stored_by_nodes=[]
    total_storage_one_replica=[0]*(ReplicationAlgorithms.endID-ReplicationAlgorithms.beginID-ReplicationAlgorithms.static_blocks+1)
    total_storage_one_replica[0]=sum(ReplicationAlgorithms.blocksizes[:ReplicationAlgorithms.static_blocks])
    # use ratio of each block is each epoch.
    # a list of list of float. key=blockID, value=use ratio
    block_use_ratio=[]
    
    # statically assign params
    piece=1
    curve_type_replica='2^n'
    period=np.inf
    curve_type_expel='2^n'

    #switch on/off replicate
    passive_on=True
    active_on=True

    # active replicate params
    top_num_to_offload=3


    # filename to store average_time_cost statistical data
    file_average_time='./finalTest/averageTime-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'
    #file name to store storage used by each node in every runtime
    file_storage_used='./finalTest/storageUsed-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'
    #file name to store each blocks' use ratio in each epoch*step in every runtime
    file_use_ratio='./finalTest/useRatio-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'

    #open storage used file to write if it's true
    if get_storage_used:
        file_storage_used_write=open(file_storage_used,'w')
        print(ReplicationAlgorithms.beginID+ReplicationAlgorithms.static_blocks,' ',ReplicationAlgorithms.endID,' ',step,file=file_storage_used_write)
    if get_replica_use_ratio:
        file_use_ratio_write=open(file_use_ratio,'w')
        print(ReplicationAlgorithms.beginID+ReplicationAlgorithms.static_blocks,' ',ReplicationAlgorithms.endID,' ',step,file=file_use_ratio_write)
    for run_times in range(total_times):
        # store all avg_time in each runtime
        avg_time.append([])
        block_use_ratio_one_runtime=[]
        block_sizes_stored_by_nodes_tmp=[]

        ReplicationAlgorithms.blocks_in_which_nodes_and_timelived.clear()
        ReplicationAlgorithms.nodes_stored_blocks_popularity.clear()
        ReplicationAlgorithms.nodes_storage_used.clear()
        
        # statically assign
        ReplicationAlgorithms.static_assign_blocks(piece,curve_type_replica,period,curve_type_expel)
        # dynamic assign
        start_point=ReplicationAlgorithms.beginID+ReplicationAlgorithms.static_blocks
        for end_since in range(ReplicationAlgorithms.beginID+ReplicationAlgorithms.static_blocks,ReplicationAlgorithms.endID,step):
            average_time_i=.0
            block_size_add_up=0
            # choose lambdai nodes randomly
            # replace = true
            block_access_times_in_each_epoch_step.clear()
            nodes_chosen=np.random.choice(range(ReplicationAlgorithms.nodes_num),size=lambdai,replace=True)
            for nodeID in nodes_chosen:
                average_time_i+=get_one_total_time_and_replicate(nodeID,end_since,max_level,passive_replicate_type,period,curve_type_expel,lambdai,chosen_block_distribution,m,True and passive_on)
            average_time_i/=lambdai
            avg_time[run_times].append(average_time_i)
            # update lifetime and expel dead blocks
            ReplicationAlgorithms.update_livetime_and_expel(end_since,step)
            # init new coming block
            for all_blocks in range(step):
                ReplicationAlgorithms.initial_assign_block(end_since+all_blocks,piece,curve_type_replica,period,curve_type_expel)
                block_size_add_up+=ReplicationAlgorithms.blocksizes[end_since+all_blocks-start_point]
            # active replicate
            if active_on:
                nodes_active_replicate=range(ReplicationAlgorithms.nodes_num)
                for nodeID in nodes_active_replicate:
                    ReplicationAlgorithms.active_dynamic_replication_one_node(nodeID,top_num_to_offload,active_replicate_type,period,curve_type_expel)
            # append storage_used if it's true
            if get_storage_used:
                # print(ReplicationAlgorithms.nodes_storage_used)
                storage_tmp=copy.copy(ReplicationAlgorithms.nodes_storage_used)
                block_sizes_stored_by_nodes_tmp.append(storage_tmp)
                # print(block_sizes_stored_by_nodes_tmp[0])
                total_storage_one_replica[end_since-(start_point)+1]=total_storage_one_replica[end_since-(start_point)]+block_size_add_up
            if get_replica_use_ratio:
                use_ratio_one_epoch=get_ratio_from_access_times(block_access_times_in_each_epoch_step)
                block_use_ratio_one_runtime.append(use_ratio_one_epoch)
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
            print(ReplicationAlgorithms.beginID+ReplicationAlgorithms.static_blocks,' ',ReplicationAlgorithms.endID,' ',step,file=file_write)
            avg_time_mean=np.mean(avg_time,axis=0)
            print(json.dumps(avg_time_mean.tolist()),file=file_write)
    if get_storage_used:
        file_storage_used_write.close()
    if get_replica_use_ratio:
        file_use_ratio_write.close()
   



def get_one_total_time_and_replicate(nodeID,end_since,max_level,passive_replicate_type,period,curve_type_expel,lambdai,chosen_block_distribution,m,valid_replicate):
    """(int,int,int,str,int,str,int,str,int,bool) -> float

    one requester request a set of blocks and get total request time.
    Return the total request time.

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

    # get log2(len(blocks)) blocks based on chosen_block_distribution
    if chosen_block_distribution=='nipopows':
        chosen_blocks=InitChainAndNodes.scan_blocklist_no_repeat(m,ReplicationAlgorithms.beginID,end_since,ReplicationAlgorithms.blocklist,max_level)
    else:
        chosen_blocks=InitChainAndNodes.get_needed_blocks(ReplicationAlgorithms.beginID,end_since,ReplicationAlgorithms.blocklist,chosen_block_distribution)
    #debug
    # num_of_blocks=len(chosen_blocks)
    # print(num_of_blocks,',',int(math.log2(end_since-ReplicationAlgorithms.beginID)))
    # update access times of chosen blocks and
    # calculate time
    for blockID in chosen_blocks:
        min_node,time_cost=ReplicationAlgorithms.get_blockID_from_which(nodeID,blockID)
        # update popularity
        if valid_replicate and min_node!=nodeID:
            ReplicationAlgorithms.nodes_stored_blocks_popularity[min_node][blockID]+=1
        # record popularity
        chosen_blocks_popularity[blockID]=ReplicationAlgorithms.nodes_stored_blocks_popularity[min_node][blockID]
        # record time cost
        chosen_blocks_load[blockID]=time_cost
        #record access time
        if blockID in block_access_times_in_each_epoch_step:
            block_access_times_in_each_epoch_step[blockID]+=1
        else:
            block_access_times_in_each_epoch_step[blockID]=0
        # receive blocks one by one
        time_used+=time_cost
    # replicate if valid_replicate is True
    if valid_replicate:
        if passive_replicate_type=='popularity':
            sort_value_dict=chosen_blocks_popularity
        elif passive_replicate_type=='load':
            sort_value_dict=chosen_blocks_load
        else:
            sort_value_dict=[]
        ReplicationAlgorithms.passive_dynamic_replication_one_node(chosen_blocks,nodeID,passive_replicate_type,sort_value_dict,period,curve_type_expel)
    # return total time
    return time_used
    
def get_total_access_time():
    """ () -> dict
    Return total access time of each block based on ReplicationAlgorithms.nodes_stored_blocks_popularity
    """

    total_access_times={}

    # append popularity in each node of each block
    # popularity is a little lower as self-accesses are excluded
    for node_blocks in ReplicationAlgorithms.nodes_stored_blocks_popularity:
        for kvs in node_blocks.items():
            if kvs[0] in total_access_times:
                total_access_times[kvs[0]]+=kvs[1]
            else:
                total_access_times[kvs[0]]=0
    
    return total_access_times

def get_ratio_from_access_times(access_times_dict):
    """dict -> list of float

    Return use ratio for each block in ReplicationAlgorithms.beginID and ReplicationAlgorithms.endID in this epoch.
    """
    begin_id=ReplicationAlgorithms.beginID
    end_id=ReplicationAlgorithms.endID
    # use ratio of each replica
    use_ratio=[0]*(ReplicationAlgorithms.endID-ReplicationAlgorithms.beginID)
    # number of replicas of each block in this epoch
    replica_nums_of_blocks=[0]*(ReplicationAlgorithms.endID-ReplicationAlgorithms.beginID)

    # get replica num from ReplicationAlgorithms.blocks_in_which_nodes_and_timelived
    for i in range(0,len(ReplicationAlgorithms.blocks_in_which_nodes_and_timelived)):
        replica_nums_of_blocks[i]=len(ReplicationAlgorithms.blocks_in_which_nodes_and_timelived[i])

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
        for i in range(len(ReplicationAlgorithms.blocks_in_which_nodes_and_timelived)):
            block_id=i+ReplicationAlgorithms.beginID
            level=ReplicationAlgorithms.blocklist[i][0]
            actual=len(ReplicationAlgorithms.blocks_in_which_nodes_and_timelived[i])
            stored_nodes=[kvs[0] for kvs in  ReplicationAlgorithms.blocks_in_which_nodes_and_timelived[i].items()]
            print('block:',block_id,',level=',level,',actual=',actual,'stored nodes=',stored_nodes,file=store_file)


if __name__=='__main__':
    max_level,all_storage_cost=init_environment()
    replication_run(max_level,True,True,True)
    get_storage_place()
    print('running done')