#YaYi 2020.10.13

import numpy as np
import json
import matplotlib.pyplot as plt
import copy
import math
import sys
import time
import random
sys.path.append('D:/Languages/PythonSpace/AnalysisSanning/finalTest')
import DS_init as dsinit
import DS_ReplicaAlgs as dsrpal
import DS_Client_Request as dsrequest


"""
the main program.

"""

# how many times is a block been accessed in step epoches.
block_access_times_in_each_epoch_step={}

def init_environment():
    """ () -> ( float)
    
    Init global variables in dsrpal.i.e. get the running environment ready.
    return all storage of one copy of all blocks.
    """
    begin_id=654000
    static_blks=10
    end_id=begin_id+400
    nodes_n=10
    communication_distribution_type='normal'#'1'

    blk_size,all_storage=dsinit.load_blocksizes(begin_id,end_id)
    # communication_cst=dsinit.generate_communication_cost(nodes_n,communication_distribution_type)
    
    dsrpal.init_all_settings(blk_size,begin_id,end_id,static_blks,nodes_n)
    
    # all params needed can be accessed from dsrpal.param

    # return max_level
    return all_storage

def replication_run(get_average_time=True,get_storage_used=False,get_popularity_list=False):
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

    epoch_interval=600
    # epoch gap 
    step=1
    # average time, a list of list of float
    avg_time=[]
    # blocks size stored by nodes, a list of list of float. key=nodeID,value=blocksize
    block_sizes_stored_by_nodes=[]
    total_storage_one_replica=[0]*(dsrpal.endID-dsrpal.beginID-dsrpal.static_blocks+1)
    total_storage_one_replica[0]=sum(dsrpal.blocksizes[:dsrpal.static_blocks])

    
    time_string= '['+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+']'
    print(time_string+': running: ',chosen_block_distribution+'-'+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times))

    # filename to store average_time_cost statistical data
    # file_average_time='./finalTest/averageTime-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'
    file_average_time='./finalTest/finalRes/A-'+chosen_block_distribution+'-'+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.txt'
    #file name to store storage used by each node in every runtime
    # file_storage_used='./finalTest/storageUsed-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'
    file_storage_used='./finalTest/finalRes/S-'+chosen_block_distribution+'-'+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.txt'
    
    #open storage used file to write if it's true
    if get_storage_used:
        file_storage_used_write=open(file_storage_used,'w')
        print(dsrpal.beginID+dsrpal.static_blocks,' ',dsrpal.endID,' ',step,file=file_storage_used_write)
    ##debug
    if get_popularity_list:
        files_index=10
        datafile_index=[]
        for i in range(files_index):
            datafile_index.append(open('./finalTest/finalRes/debug/'+str(chosen_block_distribution+'-'+active_item+'-'+passive_item+'-'+expel_item)+'-PL-node'+str(i)+'-'+str(total_times)+'.txt','w'))
    
    ### end debug
    for run_times in range(total_times):
        # store all avg_time in each runtime
        print('(',run_times+1,'/',total_times,')')
        avg_time.append([])
        block_use_ratio_one_runtime=[]
        block_sizes_stored_by_nodes_tmp=[]

        dsrpal.blocks_in_which_nodes_and_timelived.clear()
        dsrpal.nodes_stored_blocks_popularity.clear()
        dsrpal.nodes_storage_used.clear()
        dsrpal.set_communication_cost()
        
        # statically assign
        dsrpal.static_assign_blocks(piece,period)
        # dynamic assign
        # active->request->passive->expel
        start_point=dsrpal.beginID+dsrpal.static_blocks
        ##!!!DEBUG

        # expelfile_index=[]
        # activefile_index=[]
        # for i in range(files_index):
        #     datafile_index.append(open('./finalTest/finalRes/debug/'+str(active_item+'-'+expel_item)+'-popularity-node'+str(i)+'-'+str(total_times)+'.txt','w'))
            # expelfile_index.append(open('./finalTest/finalRes/debug/'+str(active_item+'-'+expel_item)+'-expel-chosen-block-node'+str(i)+'-runtime.txt','w'))
            # activefile_index.append(open('./finalTest/finalRes/debug/'+str(active_item+'-'+expel_item)+'-active-chosen-block-node'+str(i)+'-runtime.txt','w'))
        ## end
        for end_since in range(dsrpal.beginID+dsrpal.static_blocks,dsrpal.endID,step):
            
            average_time_i=.0
            block_size_add_up=0
            # choose lambdai nodes randomly
            # replace = true
            block_access_times_in_each_epoch_step.clear()
            # shift popularity. before init new coming block == after init new coming block
            dsrpal.shift_popularity()
            ### !!!DEBUG
            # if run_times==0 and end_since==dsrpal.endID-1:
            #     # print(json.dumps(dsrpal.blocks_in_which_nodes_and_timelived),file=data_store_in)
            #     for i in range(dsrpal.beginID,dsrpal.endID):
            #         print(dsrpal.blocks_in_which_nodes_and_timelived[i-dsrpal.beginID],file=data_store_in)
            # if run_times==0:# and end_since==dsrpal.endID-1:
            #     for i in range(files_index):
            #         # print(dsrpal.nodes_stored_blocks_popularity)
            #         Popu_dict_old=dsrpal.nodes_stored_blocks_popularity[i]
            #         Popu_dict={}
            #         for kvs in Popu_dict_old.items():
            #             Popu_dict[int(kvs[0]-dsrpal.beginID)]=Popu_dict_old[kvs[0]]
            #         # Popu_dict=sorted(Popu_dict.items(),key=lambda x:x[1][0]+x[1][1],reverse=True)
            #         str_print=json.dumps(Popu_dict)
            #         print(end_since,'$',str_print , file=datafile_index[i])
            ### end debug
            # init new coming block
            for all_blocks in range(step):
                dsrpal.initial_assign_block(end_since+all_blocks,piece,period)
                block_size_add_up+=dsrpal.blocksizes[end_since+all_blocks-start_point]
            # active replicate
            if active_on:
                nodes_active_replicate=range(dsrpal.nodes_num)
                for nodeID in nodes_active_replicate:
                    _=dsrpal.active_dynamic_replication_one_node(nodeID,top_num_to_offload,active_replicate_type,period)
                    # cn_debug=sorted(cn_debug.items(),key=lambda x:x[0],reverse=False)
                    # print('epoch=',end_since,',',cn_debug,file=activefile_index[nodeID])
            # print(dsrpal.nodes_stored_blocks_popularity)
            #request
            average_time_i,storage_per_node,request_time_per_node,passive_type_blks,chosen_blocks=dsrequest.request(dsrpal.beginID,end_since+1,epoch_interval,chosen_block_distribution,dsrpal.nodes_num,lambdai,passive_replicate_type)
            avg_time[run_times].append(average_time_i)

            # passive_replicate
            replicate_passivly(chosen_blocks,passive_replicate_type,passive_type_blks,period)

            # broadcast local popularity
            #block end_since is included.
            dsrpal.broadcast_popularity_and_get_gobal_popularity(end_since)
            # update communication cost
            dsrpal.update_communication(storage_per_node,request_time_per_node)


            # ### !!!DEBUG
            # if run_times==0 and end_since==dsrpal.endID-1:
            #     print(json.dumps(dsrpal.blocks_in_which_nodes_and_timelived),file=data_store_in)
            #     for i in range(dsrpal.beginID,dsrpal.endID):
            #         print(dsrpal.blocks_in_which_nodes_and_timelived[i-dsrpal.beginID],file=data_store_in)
            if get_popularity_list and end_since==dsrpal.endID-1:#run_times==0:# and 
                for i in range(files_index):
                    Popu_dict_old=dsrpal.nodes_stored_blocks_popularity[i]
                    Popu_dict={}
                    for kvs in Popu_dict_old.items():
                        Popu_dict[int(kvs[0]-dsrpal.beginID)]=Popu_dict_old[kvs[0]]
                    # Popu_dict=sorted(Popu_dict.items(),key=lambda x:x[1][0]+x[1][1],reverse=True)
                    str_print=json.dumps(Popu_dict)
                    print(run_times,'$',str_print , file=datafile_index[i])
                # for i in range(dsrpal.beginID,dsrpal.endID):
                #     print(dsrpal.blocks_in_which_nodes_and_timelived[i-dsrpal.beginID],file=datafilein)
            # ### end debug
            # update lifetime and expel dead blocks
            if expel_type!='noexpel':
                _=dsrpal.expel_blocks(expel_type,end_since+1,step,last_num_to_expel,None)
                # if end_since==654055:
                #     for nodeid in range(10):
                #         if end_since-1 in dsrpal.nodes_stored_blocks_popularity[nodeid]:
                #             print('address of node',nodeid,',block',end_since-1,',is:',id(dsrpal.nodes_stored_blocks_popularity[nodeid][end_since-1]),', value is:',dsrpal.nodes_stored_blocks_popularity[nodeid][end_since-1])

                # for i in range(len(expel_blocks)):
                #     print('epoch=',end_since,',',sorted(expel_blocks[i]),file=expelfile_index[i])
            
            # append storage_used if it's true
            if get_storage_used:
                # print(dsrpal.nodes_storage_used)
                storage_tmp=copy.copy(dsrpal.nodes_storage_used)
                block_sizes_stored_by_nodes_tmp.append(storage_tmp)
                # print(block_sizes_stored_by_nodes_tmp[0])
                total_storage_one_replica[end_since-(start_point)+1]=total_storage_one_replica[end_since-(start_point)]+block_size_add_up
        ##!!!DEBUG
        # for i in range(files_index):
        #     datafile_index[i].close()
            # activefile_index[i].close()
            # expelfile_index[i].close()
        ### end
        # data_store_in.close()
        # get sum of use ratio after 1 runtime
            # print(block_use_ratio)
            
        # get sum after 1 runtime
        if get_storage_used:
            block_sizes_stored_by_nodes.append(block_sizes_stored_by_nodes_tmp)
            # print(block_sizes_stored_by_nodes_tmp)
            block_sizes_stored_by_nodes=[np.sum(block_sizes_stored_by_nodes,axis=0)]
            # print(block_sizes_stored_by_nodes)
        # print(dsrpal.communication_cost)
        # print(np.mean(avg_time,axis=0))
    ### debug
    if get_popularity_list:
        for i in range(files_index):
            datafile_index[i].close()
    ### end
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
            print(dsrpal.beginID+dsrpal.static_blocks,' ',dsrpal.endID,' ',step,file=file_write)
            avg_time_mean=np.mean(avg_time,axis=0)
            print(json.dumps(avg_time_mean.tolist()),file=file_write)
    if get_storage_used:
        file_storage_used_write.close()
   

def replicate_passivly(replicate_blocks,passive_type,sort_value_dict,period):
    '''(list of list,string)
    
    choose replicate blocks in replicate_blocks and passively replicate them at local.

    PARAM:
    replicate_blocks is a list of list. replicate_blocks[i] stores all blocks node i has request in one epoch.
    '''
    _nodes_sum=len(replicate_blocks)
    for i in range(_nodes_sum):
        dsrpal.passive_dynamic_replication_one_node(replicate_blocks[i],i,passive_type,sort_value_dict[i],period)


    

def get_storage_place():
    """

    get current block distribution, and save them into file_store_distribution
    """

    file_store_distibution='./finalTest/storeDistribution.txt'
    with open(file_store_distibution,'w') as store_file:
        for i in range(len(dsrpal.blocks_in_which_nodes_and_timelived)):
            block_id=i+dsrpal.beginID
            actual=len(dsrpal.blocks_in_which_nodes_and_timelived[i])
            stored_nodes=[kvs[0] for kvs in  dsrpal.blocks_in_which_nodes_and_timelived[i].items()]
            print('block:',block_id,'replica nums=',actual,'stored nodes=',stored_nodes,file=store_file)


if __name__=='__main__':
    all_storage_cost=init_environment()
    replication_run(True,True,True)
    get_storage_place()
    print('running done')