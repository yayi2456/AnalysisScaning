#YaYi 2020.10.13

import numpy as np
import json
import InitChainAndNodes
import ReplicationAlgorithms

"""
the main program.

"""

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

def get_average_time_cost(max_level):
    """ () -> (list of int)

    run a certain replica algorithm, and return the average cost time in every dynamic epoch
    """


    # params of NIPoPoWs
    m=3
    # chosen block type :nipopows
    chosen_block_distribution='nipopows'
    # passive alg type
    passive_replicate_type='popularity'
    # active alg type
    active_replicate_type='calculate'
    # how many requests in step epoch
    lambdai=4
    # epoch gap 
    step=1
    # total runing times
    total_times=1
    # average time, a list of list of float
    avg_time=[]
    
    # statically assign params
    piece=1
    curve_type_replica='2^n'
    period=6
    curve_type_expel='2^n'

    #switch on/off replicate
    passive_on=True
    active_on=True

    # active replicate params
    top_num_to_offload=3

    # filename to store average_time_cost statistical data
    file_average_time='./finalTest/averageTime-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'

    for run_times in range(total_times):
        # store all avg_time in each runtime
        avg_time.append([])
        ReplicationAlgorithms.blocks_in_which_nodes_and_timelived.clear()
        ReplicationAlgorithms.nodes_stored_blocks_popularity.clear()
        ReplicationAlgorithms.nodes_storage_used.clear()
        # statically assign
        ReplicationAlgorithms.static_assign_blocks(piece,curve_type_replica,period,curve_type_expel)
        # dynamic assign
        for end_since in range(ReplicationAlgorithms.beginID+ReplicationAlgorithms.static_blocks,ReplicationAlgorithms.endID,step):
            average_time_i=.0
            # choose lambdai nodes randomly
            # replace = true
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
            # active replicate
            if active_on:
                nodes_active_replicate=range(ReplicationAlgorithms.nodes_num)
                for nodeID in nodes_active_replicate:
                    ReplicationAlgorithms.active_dynamic_replication_one_node(nodeID,top_num_to_offload,active_replicate_type,period,curve_type_expel)
    # got all average_time, which is a list of list of float
    # store them
    with open(file_average_time,'w') as file_write:
        print(ReplicationAlgorithms.beginID+ReplicationAlgorithms.static_blocks,' ',ReplicationAlgorithms.endID,' ',step,file=file_write)
        for run_times in range(len(avg_time)):
            print(json.dumps(avg_time[run_times]),file=file_write)





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
    




# if __name__=='__main__':
#     max_level,all_storage_cost=init_environment()
#     get_average_time_cost(max_level)

#     print('running done')