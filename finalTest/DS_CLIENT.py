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

def replication_run(get_average_time=True,get_storage_used=False,get_delay_info=True,get_popularity_list=False):
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
    # sttaic replica method
    static_rep_type=sys.argv[2]
    # replica nummbers
    piece=int(sys.argv[3])
    # passive alg type
    passive_replicate_type=sys.argv[4]
    # next_params
    next_param_index=5
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
    # delay percentile
    delay_percentile=[]
    # delay per request
    delay_time_div_total_time=[]
    total_access_time=[]
    total_cost_time=[]
    # blocks size stored by nodes, a list of list of float. key=nodeID,value=blocksize
    block_sizes_stored_by_nodes=[]
    block_nums_stored_by_nodes=[]
    total_storage_one_replica=[0]*(dsrpal.endID-dsrpal.beginID-dsrpal.static_blocks+1)
    total_storage_one_replica[0]=sum(dsrpal.blocksizes[:dsrpal.static_blocks])

    
    time_string= '['+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+']'
    print(time_string+': running: ',chosen_block_distribution+'-'+static_rep_type+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times))

    # filename to store average_time_cost statistical data
    # file_average_time='./finalTest/averageTime-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'
    file_average_time='./finalTest/finalRes/A-CLIENT'+chosen_block_distribution+'-'+static_rep_type+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.txt'
    #file name to store storage used by each node in every runtime
    # file_storage_used='./finalTest/storageUsed-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'
    file_storage_used='./finalTest/finalRes/S-CLIENT'+chosen_block_distribution+'-'+static_rep_type+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.txt'
    file_delay_info='./finalTest/finalRes/D-CLIENT'+chosen_block_distribution+'-'+static_rep_type+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.txt'
    #open storage used file to write if it's true
    
    ##debug
    if get_popularity_list:
        files_index=10
        datafile_index=[]
        for i in range(files_index):
            datafile_index.append(
                open('./finalTest/finalRes/debug/'+str(chosen_block_distribution+'-'+active_item+'-'+passive_item+'-'+expel_item)+'-PLCLIENT-'+str(i)+'-'+str(total_times)+'.txt','w'))
    ### end debug
    #record request list#
    file_write_request='./finalTest/finalRes/request/REQ-'+chosen_block_distribution+'-'+static_rep_type+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.txt'
    f_write_request=open(file_write_request,'w')
    # end record
    for run_times in range(total_times):
        # store all avg_time in each runtime
        # print('(',run_times+1,'/',total_times,')')
        avg_time.append([])
        # delay_time_div_total_time.append([])
        # delay_percentile.append([])
        block_sizes_stored_by_nodes_tmp=[]
        block_nums_stored_by_nodes_tmp=[]

        dsrpal.blocks_in_which_nodes_and_timelived.clear()
        dsrpal.nodes_stored_blocks_popularity.clear()
        dsrpal.nodes_storage_used.clear()
        dsrpal.set_communication_cost()
        
        # statically assign
        dsrpal.static_assign_blocks(piece,period,static_rep_type)
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
                dsrpal.initial_assign_block(end_since+all_blocks,piece,period,static_rep_type)
                block_size_add_up+=dsrpal.blocksizes[end_since+all_blocks-start_point]
            # active replicate
            # print('before: system blocks,',np.sum(np.array([len(dsrpal.nodes_stored_blocks_popularity[_nid]) for _nid in range(dsrpal.nodes_num)])))
            if active_on:
                offload_ac,stored_blocks=replicate_actively(top_num_to_offload,active_replicate_type,period,dsrpal.nodes_num)
                # print('active,runtime,',run_times,',epoch',end_since,',',offload_ac,'all system blocks,',np.sum(np.array([len(dsrpal.nodes_stored_blocks_popularity[_nid]) for _nid in range(dsrpal.nodes_num)])))
                
                # nodes_active_replicate=range(dsrpal.nodes_num)
                # for nodeID in nodes_active_replicate:
                #     _=dsrpal.active_dynamic_replication_one_node(nodeID,top_num_to_offload,active_replicate_type,period)
                    # cn_debug=sorted(cn_debug.items(),key=lambda x:x[0],reverse=False)
                    # print('epoch=',end_since,',',cn_debug,file=activefile_index[nodeID])
            # print(dsrpal.nodes_stored_blocks_popularity)
            #request
            give_in_writter=None
            # if end_since==dsrpal.endID-1:
            # if run_times==total_times-1:
            #     give_in_writter=f_write_request
            average_time_i,storage_per_node,request_time_per_node,passive_type_blks,chosen_blocks,\
                delay_p,delay_time_dtt,total_a_t,total_t_c=dsrequest.request(
                dsrpal.beginID,end_since+1,epoch_interval,chosen_block_distribution,dsrpal.nodes_num,lambdai,passive_replicate_type,give_in_writter)

            avg_time[run_times].append(average_time_i)
            end_since_index=end_since-(dsrpal.beginID+dsrpal.static_blocks)
            if get_delay_info :
                if run_times==0:
                    delay_percentile.append(delay_p)
                    delay_time_div_total_time.append(delay_time_dtt)
                    total_access_time.append(total_a_t)
                    total_cost_time.append(total_t_c)
                else:
                    # print('len-delay-per=',len(delay_percentile))
                    # print('len-inside=',len(delay_percentile[0]))
                    # print('len-per=',len(delay_p))
                    delay_percentile[end_since_index]=np.array(delay_percentile[end_since_index])+np.array(delay_p)
                    delay_time_div_total_time[end_since_index]=np.array(delay_time_div_total_time[end_since_index])+np.array(delay_time_dtt)
                    total_access_time[end_since_index]=np.array(total_access_time[end_since_index])+np.array(total_a_t)
                    total_cost_time[end_since_index]=np.array(total_cost_time[end_since_index])+np.array(total_t_c)

            # passive_replicate
            if passive_on:
                store_actually_all=replicate_passivly(chosen_blocks,passive_replicate_type,passive_type_blks,period,lambdai)
                # print('passive,runtime,',run_times,',epoch',end_since,',',store_actually_all)

            # broadcast local popularity
            #block end_since is included.
            ################################DO NOT UPDATE GLOBAL POPULARITY###########################################
            # dsrpal.broadcast_popularity_and_get_gobal_popularity(end_since)
            ##########################################################################################################
            # if end_since==end_since==dsrpal.endID-1:
            #         for i in range(dsrpal.nodes_num):
            #             # print('node=',i,',',sorted(stored_blocks[i]))
            #             print('node=',i,',',sorted(dsrpal.nodes_stored_blocks_popularity[i].items(),key=lambda x:x[1][0]+x[1][1],reverse=True))
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
                expel_blocks=dsrpal.expel_blocks(expel_type,end_since+1,step,last_num_to_expel,None)
                # if end_since==654055:
                #     for nodeid in range(10):
                #         if end_since-1 in dsrpal.nodes_stored_blocks_popularity[nodeid]:
                #             print('address of node',nodeid,',block',end_since-1,',is:',id(dsrpal.nodes_stored_blocks_popularity[nodeid][end_since-1]),', value is:',dsrpal.nodes_stored_blocks_popularity[nodeid][end_since-1])

                # for i in range(len(expel_blocks)):
                #     print('epoch=',end_since,',node=',i,',',sorted(expel_blocks[i]))

                # print('expel,runtime,',run_times,',epoch',end_since,',all system blocks,',np.sum(np.array([len(dsrpal.nodes_stored_blocks_popularity[_nid]) for _nid in range(dsrpal.nodes_num)])))
            
            # append storage_used if it's true
            if get_storage_used:
                # print(dsrpal.nodes_storage_used)
                storage_tmp=copy.copy(dsrpal.nodes_storage_used)
                block_sizes_stored_by_nodes_tmp.append(storage_tmp)
                # print(block_sizes_stored_by_nodes_tmp[0])
                total_storage_one_replica[end_since-(start_point)+1]=total_storage_one_replica[end_since-(start_point)]+block_size_add_up
                
                block_nums_stored_by_nodes_tmp.append([len(dsrpal.nodes_stored_blocks_popularity[_nid]) for _nid in range(dsrpal.nodes_num)])
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
            block_nums_stored_by_nodes.append(block_nums_stored_by_nodes_tmp)
            # print(block_sizes_stored_by_nodes_tmp)
            block_sizes_stored_by_nodes=[np.sum(block_sizes_stored_by_nodes,axis=0)]
            block_nums_stored_by_nodes=[np.sum(block_nums_stored_by_nodes,axis=0)]
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
        with open(file_storage_used,'w')as file_storage_used_write:
            print(dsrpal.beginID+dsrpal.static_blocks,' ',dsrpal.endID,' ',step,file=file_storage_used_write)
            # get total storage by store one replica
            print(json.dumps(total_storage_one_replica[1:]),file=file_storage_used_write)

            block_sizes_stored_by_nodes=np.array(block_sizes_stored_by_nodes[0])/total_times
            block_nums_stored_by_nodes=np.array(block_nums_stored_by_nodes[0])/total_times
            block_sizes_stored_by_nodes=block_sizes_stored_by_nodes.T
            block_nums_stored_by_nodes=block_nums_stored_by_nodes.T
            for i in range(len(block_sizes_stored_by_nodes)):
                # print(block_sizes_stored_by_nodes[i])
                print(json.dumps(block_sizes_stored_by_nodes[i].tolist()),file=file_storage_used_write)
            for i in range(len(block_nums_stored_by_nodes)):
                print(json.dumps(block_nums_stored_by_nodes[i].tolist()),file=file_storage_used_write)
            print(json.dumps((np.sum(block_nums_stored_by_nodes,axis=0)).tolist()),file=file_storage_used_write)
    # got all average_time, which is a list of list of float
    # store them
    if get_average_time:
        with open(file_average_time,'w') as file_write:
            print(dsrpal.beginID+dsrpal.static_blocks,' ',dsrpal.endID,' ',step,file=file_write)
            avg_time_mean=np.mean(avg_time,axis=0)
            print(json.dumps(avg_time_mean.tolist()),file=file_write)
    if get_delay_info:
        with open(file_delay_info,'w') as file_write:
            print(dsrpal.beginID+dsrpal.static_blocks,' ',dsrpal.endID,' ',step,file=file_write)
            delay_percentile=np.array(delay_percentile)/total_times
            delay_time_div_total_time=np.array(delay_time_div_total_time)/total_times
            total_access_time=np.array(total_access_time)/total_times
            total_cost_time=np.array(total_cost_time)/total_times

            # delay_p_mean=np.mean(delay_percentile,axis=0)
            # delay_p_r_mean=np.mean(delay_time_div_total_time,axis=0)
            print(json.dumps(delay_percentile.tolist()),file=file_write)
            print(json.dumps(delay_time_div_total_time.tolist()),file=file_write)
            print(json.dumps(total_access_time.tolist()),file=file_write)
            print(json.dumps(total_cost_time.tolist()),file=file_write)
    # close record file
    f_write_request.close()
    #end
   

def replicate_passivly(replicate_blocks,passive_type,sort_value_dict,period,lambdai):
    '''(list of list,string)
    
    choose replicate blocks in replicate_blocks and passively replicate them at local.

    PARAM:
    replicate_blocks is a list of list. replicate_blocks[i] stores all blocks node i has request in one epoch.
    '''
    _nodes_sum=len(replicate_blocks)
    store_actually_all=[]
    for i in range(_nodes_sum):
        s_a=dsrpal.passive_dynamic_replication_one_node(replicate_blocks[i],i,passive_type,sort_value_dict[i],period,lambdai)
        store_actually_all.append(s_a)
    return store_actually_all

def replicate_actively(top_to_offload,active_type,period,nodes_num):
    '''
    choose local top hot blocks and offload
    '''
    node_seq=(list(range(0,nodes_num)))
    random.shuffle(node_seq)
    offload_actually_all=[]
    stored_blocks=[]
    for i in range(dsrpal.nodes_num):
        stored_blocks.append([])
    for _nid in node_seq:
        _,offload_actually,sb=dsrpal.active_dynamic_replication_one_node(_nid,top_to_offload,active_type,period)
        offload_actually_all.append(offload_actually)
        for i in sb:
            stored_blocks[i].append(sb[i])
    return offload_actually_all,stored_blocks
    

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
    avg_s=True
    storage_s=True
    delay_s=True
    popu_s=True
    replication_run(avg_s,storage_s,delay_s,popu_s)
    get_storage_place()
    time_string= '['+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+']'
    print(time_string+': running-done. ')
