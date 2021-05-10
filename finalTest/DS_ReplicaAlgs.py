### YaYi 2020.10.12

import numpy as np
import sys
import math
import random
import json

"""
multiple replica algorithms which can be embed into replication process.
1. replica numbers determining function
2. static replica algorithm: 
    - level: a new block have piece*2^level replicas, distributed among all nodes, before dynamic replication.
    - piece: a new block have piece replicas, randomly distributed among all nodes, before dynamic replication.
    - piecekad: a new block have piece replicas, 
        distributed in 'piece' nodes which have the top 'piece' hortest distance from blockid
3. initial replica algorithm: 
    - level: a new block have piece*2^level replicas, distributed among all nodes, before dynamic replication.
    - piece: a new block have piece replicas, randomly distributed among all nodes, before dynamic replication.
    - piecekad: a new block have piece replicas, 
        distributed in 'piece' nodes which have the top 'piece' hortest distance from blockid
4. dynaminc algorithms
    1. passive: 
        - random: when requester obtains x blocks reqtesed from other nodes, 
            it stores int(x/lambdai) random blocks locally
        - popularity based: when requester obtains x blocks requested from other nodes,
            it stores int(x/lambdai) most popular blocks locally. 
            Requester gets popularity of blocks from the node from which it get the block.
        - load based: when requester obtains x blocks requested from other nodes,
            it stores int(x/lambdai) highest-communication-cost blocks. 
        - kad：when requester obtains x blocks requested from other nodes, 
        it stores int(x/lambdai) random blocks into nodes which has shortest distance from these nodes.
    2. active:
        - random: every x epoch, nodes offload 3 most popular blocks to a random neighbour.
        - selective: every x epoch, nodes offload 3 most popular blocks to a select node, 
            which can maximize improvement of average communication cost.
6. expel policy: expel blocks that havn't been accessed for life_period long or llu.
7. init all global variables. These variables must be initialized.
8. which node the nodeA choose to get a certain block B, and the time cost.
"""

#minium blocks left
LEFT_BLOCKS=2

# blocksizes is the size of all blocks
blocksizes=[]

# communication_cost_ori is the communication cost between each 2 nodes.
communication_cost_ori=[]

# communication_cost is the communication cost between each 2 nodes after modification.
communication_cost=[]

# nodes_num is the total node number
nodes_num=10

# beginID is the starting block and endID is the ending block
beginID=654000
endID=beginID+400
# static_blocks is the number of blocks that shall be assigned statically
# assert(static_blocks<=endID-beginID)
static_blocks=10

# which nodes a block is stored and the corresponding lifetime left.
# a list of dictionary, whose index is blockID-beginID, value is a dict.
# dict's key is nodeIDs of nodes in which index block is stored, and value is the block's live time left.
blocks_in_which_nodes_and_timelived=[]

# blocks' popularity of nodes stored.
# a list of dictionary, whose index is nodeID, value is a dict.
# dict's key is blockIDs of blocks which is stored in the index node, and value is the block's popularity.
nodes_stored_blocks_popularity=[]

# nodes storage used at present
# a list of float, whose index is nodeID, and value is storage the index node have used.
nodes_storage_used=[]

# REPLICA_LIMIT=[.699,.299]
REPLICA_LIMIT=[5,3]

def static_assign_blocks(piece,period,type):
    """(int,int) - list of dict:(int, int), list of dict:(int,int), list of int

    Init nodes_storage_used and nodes_stored_blocks_popularity
    Statically assign blocks from beginID to beginID+static_blocks.
    Select storage node randomly.
    `piece`: how many replicas are stored
    `period`: lifetime of this block
    `type`: type of static assign alg

    Get the static assign result. a list , whose index is blockID-beginID and value is a dict. 
        the dict's key is nodeID and value is timelived.
    Get the initial popularity of each block in each node. a list, whose index is nodeID adn value is a dict.
        the dict's key is blockID and value is popularity.
    Get the storage of each nodes. a list, whose index is nodeID and value is the node's storage used.

    Must be called.
    """
    # init node_storage_used
    global nodes_storage_used
    nodes_storage_used=[0]*nodes_num

    #init nodes_stored_blocks_popularity
    for i in range(nodes_num):
        nodes_stored_blocks_popularity.append({})

    # statically assign each blocks one by one
    for blockID in range(beginID,beginID+static_blocks):
        assign_one_block(blockID,piece,period)#,[0,0])
    
    # nothing to return
    return

def assign_one_block(blockID,piece,period):#,popularity_epoch_list):
    """(int,int,int,list of float) - list of dict:(int, int), list of dict:(int,int), list of int

    assign block `blockID` to `piece` nodes , whose lifetime is `period` and popularity list is `popularity_epoch_list`.
    popularity_epoch_list: [.,.]
    this function is only used in initial assign of new coming block and static assign blocks.

    Select storage node randomly.
    `piece`: how many replicas are stored
    `period`: lifetime of this block

    Get the one block assign result. a list, whose index is blockID-beginID and value is a dict.
        the dict's key is nodeID and value is timelived.
    Get the initial popularity of each block in each node. a list, whose index is nodeID adn value is a dict.
        the dict's key is blockID and value is popularity.
    Get the storage of each nodes. a list, whose index is nodeID and value is the node's storage used.
    """
    
    # get replica numbers
    replica_numbers=piece
    if replica_numbers>nodes_num:
        replica_numbers=nodes_num
    # get time lived
    time_lived=period
    # sample random nodes
    nodes_store_replicas=random.sample(range(0,nodes_num),replica_numbers)
    ###debug
    # print('blockID=',blockID,', replica nodes=',nodes_store_replicas)
    ###
    # append one list value for the new block
    blocks_in_which_nodes_and_timelived.append({})
    # update blocks_in_which_nodes_and_timelived, update nodes_storage_used, update nodes_stored_blocks_popularity
    for node_replica in nodes_store_replicas:
        if node_replica not in blocks_in_which_nodes_and_timelived[blockID-beginID]:
            # print("size=",blocksizes[blockID-beginID])
            # print(blockID,'\n',beginID)
            nodes_storage_used[node_replica]+=blocksizes[blockID-beginID]
        blocks_in_which_nodes_and_timelived[blockID-beginID][node_replica]=time_lived
        # nodes_stored_blocks_popularity[node_replica][blockID]=popularity_epoch_list.copy()
        nodes_stored_blocks_popularity[node_replica][blockID]=[0,0]#popularity_epoch_list.copy()
    # nothing tpo return
    return

def initial_assign_block(blockID,piece,period):
    """(int,int,int) - list of dict:(int, int), list of dict:(int,int), list of int

    Assign the new coming block `blockID` to random `piece` nodes, whose lifetime is `period`.
    we assign the popularity_epoch_list to [0,0].
    This function is used to assign new coming blocks.
    """
    assign_one_block(blockID,piece,period)#,[0,0])

def passive_dynamic_replication_one_node(chosen_blocks,nodeID,passive_type,sort_value_dict,period,lambdai):#,popularity_passing_dict):
    """(int,list of int,int,str,dict,int,str) - list of dict:(int, int), list of dict:(int,int), list of int

    passive algorithms to replicate for 1 node.
    3 type of passive_type are allowed:'random','popularity','load','kad'.default is'random'.
    when passive_type=='random', sort_value_dict can be empty.
    when passive_type=='popularity', sort_value_dict must be the block provider's popularity of chosen blocks.
    when passive_type=='load', sort_value_dict must be the block requester's communication cost of chosen blocks.
    'kad',choose the node which is the nearest to blockID and has not stored this block.
    len(chosen)/nodes_num blocks are stored locally at nodeID. Stored blocks are chosen based on passive_type.
    """
    global nodes_num
    # if len(chosen_blocks)==0:
    #     print('passive_dynamic_replication_one_node: no chosen blocks. no need to replicate.')
    if (passive_type=='popularity' or passive_type=='load') and len(sort_value_dict)!=len(chosen_blocks):
        print('passive replication: bad sort_value_dict!','sort_value_dict:',len(sort_value_dict),'vs. chosen:',len(chosen_blocks))
    # blocksID that will be stored locally
    all_blocks_replicated=[]
    # inherent value of popularity correspond to all_blocks_replicated
    # popularity_value=[]
    # print(popularity_passing_dict)
    # amounts of blocks we want to replicate
    blocks_replicated_num=math.ceil(len(chosen_blocks)/lambdai)
    if blocks_replicated_num>len(chosen_blocks):
        blocks_replicated_num=len(chosen_blocks)

    if passive_type=='random':
        all_blocks_num=[]
        new_random_chosen_blocks=chosen_blocks
        random.shuffle(new_random_chosen_blocks)
        i=0
        for block_ids in new_random_chosen_blocks:
            if i>=blocks_replicated_num:
                break
            if nodeID not in blocks_in_which_nodes_and_timelived[block_ids-beginID]:
                all_blocks_replicated.append(block_ids)
                i+=1
        # if len(all_blocks_replicated)<blocks_replicated_num:
        #     print('passive replication: expected numbers:,',blocks_replicated_num,',actual numbers,',len(all_blocks_replicated))
        # popularity_value=[popularity_passing_dict[chosen_blocks[i]] for i in all_blocks_num]
    elif passive_type=='load' or passive_type=='popularity':
        # sort the dict by value value. reversed sort.
        kvs=sorted(sort_value_dict.items(),key=lambda x:x[1],reverse=True)
        chosen_kvs=[]
        i=0
        for kv in kvs:
            if i>=blocks_replicated_num:
                break
            if nodeID not in blocks_in_which_nodes_and_timelived[kv[0]-beginID]:
                all_blocks_replicated.append(kv[0])
                i+=1
        
        # if len(all_blocks_replicated)<blocks_replicated_num:
        #     print('passive replication: expected numbers:,',blocks_replicated_num,',actual numbers,',len(all_blocks_replicated))
        # get the top blocks_replicated_num
        # for blockID in all_blocks_replicated:
        #     popularity_value.append(popularity_passing_dict[blockID])
        # # get the top blocks_replicated_num
        # for blockID in all_blocks_replicated:
        #     popularity_value.append(popularity_passing_dict[blockID])
    elif passive_type=='kad':
        new_random_chosen_blocks=chosen_blocks
        random.shuffle(new_random_chosen_blocks)
        i=0
        for block_ids in new_random_chosen_blocks:
            if i>=blocks_replicated_num:
                break
            if len(blocks_in_which_nodes_and_timelived[block_ids-beginID])<nodes_num:
                all_blocks_replicated.append(block_ids)
                i+=1
    else:
        print("invalid passive_type. default('random') is set.")
        exit(-1)
        all_blocks_num=random.sample(range(0,len(chosen_blocks)),blocks_replicated_num)
        all_blocks_replicated=[chosen_blocks[i] for i in all_blocks_num]
        # popularity_value=[popularity_passing_dict[chosen_blocks[i]] for i in all_blocks_num]
    #debug
    # print('passive blocks stored=',len(all_blocks_replicated))
    #debug end
    # assign and update the 3 big list
    if passive_type!='kad':
        for i in range(len(all_blocks_replicated)):
            store_block_to_node(all_blocks_replicated[i],nodeID,period)#,popularity_value[i])
    else:#passive_type=='kad'
        for i in range(len(all_blocks_replicated)):
            not_stored_nodes=[]
            for nid in range(nodes_num):
                if nid not in blocks_in_which_nodes_and_timelived[all_blocks_replicated[i]-beginID]:
                    not_stored_nodes.append(nid)
            kvs=sorted(not_stored_nodes,key=lambda x:x^all_blocks_replicated[i],reverse=False)
            store_block_to_node(all_blocks_replicated[i],kvs[0],period)
    
    # nothing to return
    return len(all_blocks_replicated)

def active_dynamic_replication_one_node(nodeID,top_num_to_offload,active_type,period):
    """(int,int,,str) - list of dict:(int, int), list of dict:(int,int), list of int
    
    Active algorithms to replicate.
    . 

    2 type of active_type are allowed.
    'random': randomly offload top_num_to_offload most popular blocks to 1 node
    'calculate': choose the best nodes which can maxmize the reduction of communication cost
    'random' is default.
    """

    # node to be offload
    node_to_be_offload=nodeID
    # blocks to be offload
    blocks_to_be_offload=[]
    # print(nodes_stored_blocks_popularity[nodeID])
    # get the top_num_to_offload most popular blocks
    
    kvs=sorted(nodes_stored_blocks_popularity[nodeID].items(),key=lambda x:x[1][0]+x[1][1],reverse=True)
    
    # kvs=kvs[:top_num_to_offload]
    blocks_to_be_offload=[]#blockID[0] for blockID in kvs]
    off_load_num=0
    for b2p in kvs:
        if off_load_num>=top_num_to_offload:
            break
        if len(blocks_in_which_nodes_and_timelived[b2p[0]-beginID])<nodes_num:
            blocks_to_be_offload.append(b2p[0])
            off_load_num+=1
    # if len(blocks_to_be_offload)<top_num_to_offload:
    #     print('active replication: not enough blocks can be offloaded.',len(blocks_to_be_offload),' is collected.','i\'m node',nodeID)

    # popularity_passing_dict={blockID[0]:[blockID[1][0],blockID[1][1]] for blockID in kvs}
    ##debug
    Chosen_nodes_debug={}
    ###
    # get the target node_to_be_offload
    if active_type=='random':
        stored_blocks={}
        for blockID in blocks_to_be_offload:
            candidate_des=[]
            for nodeid in range(nodes_num):
                if nodeid not in blocks_in_which_nodes_and_timelived[blockID-beginID]:
                    candidate_des.append(nodeid)
            if len(candidate_des)==0:
                print('active: calculate: no endough andidate nodes!')
            node_to_be_offload=random.randint(0,len(candidate_des)-1)
            # while node_to_be_offload in blocks_in_which_nodes_and_timelived[blockID-beginID]:
            #     node_to_be_offload=random.randint(0,nodes_num-1)
            Chosen_nodes_debug[blockID]=candidate_des[node_to_be_offload]
            # print('before store:',candidate_des[node_to_be_offload],', stored blocks=',len(nodes_stored_blocks_popularity[candidate_des[node_to_be_offload]]))
            stored_blocks[candidate_des[node_to_be_offload]]=blockID
            store_block_to_node(blockID,candidate_des[node_to_be_offload],period)#,popularity_passing_dict[blockID])
            # print('after store:',candidate_des[node_to_be_offload],', stored blocks=',len(nodes_stored_blocks_popularity[candidate_des[node_to_be_offload]]))
        return [],len(blocks_to_be_offload),stored_blocks
    elif active_type=='access':
        candidate_blocks=[]
        # popularity_passing_dict_new={}
        for blockIDkv in nodes_stored_blocks_popularity[nodeID].items():
            if nodes_stored_blocks_popularity[nodeID][blockIDkv[0]]!=0 and len(blocks_in_which_nodes_and_timelived[blockIDkv[0]-beginID])<nodes_num:
                candidate_blocks.append(blockIDkv[0])
                # popularity_passing_dict_new[blockIDkv[0]]=[blockIDkv[1][0],blockIDkv[1][1]]
        # for i in candidate_blocks:
        #     if len(blocks_in_which_nodes_and_timelived[i-beginID])==nodes_num:
        #             print('***initial candidate choose error :access: trying to choose a block shich is full!')
        if len(candidate_blocks)>top_num_to_offload:
            candidate_blocks=np.random.choice(candidate_blocks,size=top_num_to_offload,replace=False)
        # if len(candidate_blocks)!=top_num_to_offload:
        #     print('***candidate choose warning :access: ,',len(candidate_blocks),', blocks are chosen.')
        for blockID in candidate_blocks:
            # largest improvement is brought by which nodes_test
            max_improve=0
            max_improve_node=nodeID
            # which node shall I store blockID
            for nodes_test in range(nodes_num):
                # improvement brought by storing blockID in nodes_test
                total_saved_in_node_test =0
                # caculate total improvement by adding each node's improvement if I store node into nodes_test
                for each_node_in_system in range(nodes_num):
                    # node each_node_in_system's improvement brought by storing blockID in nodes_test
                    this_node_saved_in_node_test=0
                    storage_nodes_of_blockID=blocks_in_which_nodes_and_timelived[blockID-beginID].keys()
                    min_communicate_before_store=np.inf
                    # current min_communication.
                    # if communication_cost[nodes_test][each_node_in_system]<min_communication currently,
                    # there is a improvemnt >0
                    for nodes_store in storage_nodes_of_blockID:
                        this_communication_cost=communication_cost[each_node_in_system][nodes_store]
                        if this_communication_cost<min_communicate_before_store:
                            min_communicate_before_store=this_communication_cost
                    # if blockID is stored in node_test, node each_node_in_system can improve by 
                    # (min_communicate_before_store-communication_cost[each_node_in_system][nodes_test])*blockIDsize
                    if min_communicate_before_store>communication_cost[each_node_in_system][nodes_test]:
                        this_node_saved_in_node_test+=blocksizes[blockID-beginID]*(min_communicate_before_store>communication_cost[each_node_in_system][nodes_test])
                        total_saved_in_node_test+=this_node_saved_in_node_test
                if total_saved_in_node_test>max_improve:
                    max_improve=total_saved_in_node_test
                    max_improve_node=nodes_test
            # got the best position for blockID to store
            ##debug
            Chosen_nodes_debug[blockID]=max_improve_node
            # if max_improve_node in blocks_in_which_nodes_and_timelived[blockID-beginID]:
            #     if len(blocks_in_which_nodes_and_timelived[blockID-beginID])==nodes_num:
            #         print('active replication:access: trying to store a block to a node in which the block is already exist!')
            #     if len(blocks_in_which_nodes_and_timelived[blockID-beginID])<nodes_num:
            #         print('active replication:access: NOT FULL!bad choice of node!')

            ##end
            store_block_to_node(blockID,max_improve_node,period)#,popularity_passing_dict_new[blockID])
    elif active_type=='raccess':
        candidate_blocks=[]
        # popularity_passing_dict_new={}
        for blockIDkv in nodes_stored_blocks_popularity[nodeID].items():
            if nodes_stored_blocks_popularity[nodeID][blockIDkv[0]]!=0 and len(blocks_in_which_nodes_and_timelived[blockIDkv[0]-beginID])<nodes_num:
                candidate_blocks.append(blockIDkv[0])
                # popularity_passing_dict_new[blockIDkv[0]]=[blockIDkv[1][0],blockIDkv[1][1]]
        if len(candidate_blocks)>top_num_to_offload:
            candidate_blocks=np.random.choice(candidate_blocks,top_num_to_offload)
        for blockID in candidate_blocks:
            node_to_be_offload=random.randint(0,nodes_num-1)
            while len(blocks_in_which_nodes_and_timelived[blockID-beginID])<nodes_num and node_to_be_offload in blocks_in_which_nodes_and_timelived[blockID-beginID]:
                node_to_be_offload=random.randint(0,nodes_num-1)
            Chosen_nodes_debug[blockID]=node_to_be_offload
            store_block_to_node(blockID,node_to_be_offload,period)#,popularity_passing_dict_new[blockID])
    elif active_type=='calculate':
        # if len(blocks_to_be_offload)!=top_num_to_offload:
        #     print('***candidate choose warning :calculate: ,',len(blocks_to_be_offload),', blocks are chosen.')
        # print(communication_cost)
        stored_blocks={}
        for blockID in blocks_to_be_offload:
            # largest improvement is brought by which nodes_test
            max_improve=0
            max_improve_node=-1
            # which node shall I store blockID
            considered_nodes=[]
            for nodeid in range(nodes_num):
                if nodeid not in blocks_in_which_nodes_and_timelived[blockID-beginID]:
                    considered_nodes.append(nodeid)
            if len(considered_nodes)==0:
                print('active: calculate: no endough andidate nodes!')
            for nodes_test in considered_nodes:
                # improvement brought by storing blockID in nodes_test
                total_saved_in_node_test =0
                # caculate total improvement by adding each node's improvement if I store node into nodes_test
                for each_node_in_system in range(nodes_num):
                    # node each_node_in_system's improvement brought by storing blockID in nodes_test
                    this_node_saved_in_node_test=0
                    storage_nodes_of_blockID=blocks_in_which_nodes_and_timelived[blockID-beginID].keys()
                    min_communicate_before_store=np.inf
                    # current min_communication.
                    # if communication_cost[nodes_test][each_node_in_system]<min_communication currently,
                    # there is a improvemnt >0
                    for nodes_store in storage_nodes_of_blockID:
                        this_communication_cost=communication_cost[each_node_in_system][nodes_store]
                        if this_communication_cost<min_communicate_before_store:
                            min_communicate_before_store=this_communication_cost
                    # if blockID is stored in node_test, node each_node_in_system can improve by 
                    # (min_communicate_before_store-communication_cost[each_node_in_system][nodes_test])*blockIDsize
                    if min_communicate_before_store>communication_cost[each_node_in_system][nodes_test]:
                        this_node_saved_in_node_test+=blocksizes[blockID-beginID]*(min_communicate_before_store>communication_cost[each_node_in_system][nodes_test])
                        total_saved_in_node_test+=this_node_saved_in_node_test
                if total_saved_in_node_test>=max_improve:
                    max_improve=total_saved_in_node_test
                    max_improve_node=nodes_test
            # got the best position for blockID to store
            ##debug
            Chosen_nodes_debug[blockID]=max_improve_node
            ##end
            if blockID in nodes_stored_blocks_popularity[max_improve_node]:
                print('cal: going to store ',blockID,' into ',max_improve_node,',improve is:',max_improve,'blocks\'s list is',blocks_in_which_nodes_and_timelived[blockID-beginID],',considered nodes are:',considered_nodes )
            store_block_to_node(blockID,max_improve_node,period)#,popularity_passing_dict[blockID])
            stored_blocks[max_improve_node]=blockID
        return [],len(blocks_to_be_offload),stored_blocks
        ##debug

        ##end
    elif active_type=='calvary':
        # print(len(blocks_to_be_offload))
        # if len(blocks_to_be_offload)!=top_num_to_offload:
        #     print('***candidate choose warning :calculate: ,',len(blocks_to_be_offload),', blocks are chosen.')
        stored_blocks={}
        for blockID in blocks_to_be_offload:
            # largest improvement is brought by which nodes_test
            max_improve=[]#顺序是：0最大，1其次，2最后
            max_improve_node=[]
            cost_and_nodes={}
            # which node shall I store blockID
            considered_nodes=[]
            for nodeid in range(nodes_num):
                if nodeid not in blocks_in_which_nodes_and_timelived[blockID-beginID]:
                    considered_nodes.append(nodeid)
            if len(considered_nodes)==0:
                print('active: calculate: no endough andidate nodes!')
            for nodes_test in considered_nodes:
                # improvement brought by storing blockID in nodes_test
                total_saved_in_node_test =0
                # caculate total improvement by adding each node's improvement if I store node into nodes_test
                for each_node_in_system in range(nodes_num):
                    # node each_node_in_system's improvement brought by storing blockID in nodes_test
                    this_node_saved_in_node_test=0
                    storage_nodes_of_blockID=blocks_in_which_nodes_and_timelived[blockID-beginID].keys()
                    min_communicate_before_store=np.inf
                    # current min_communication.
                    # if communication_cost[nodes_test][each_node_in_system]<min_communication currently,
                    # there is a improvemnt >0
                    for nodes_store in storage_nodes_of_blockID:
                        this_communication_cost=communication_cost[each_node_in_system][nodes_store]
                        if this_communication_cost<min_communicate_before_store:
                            min_communicate_before_store=this_communication_cost
                    # if blockID is stored in node_test, node each_node_in_system can improve by 
                    # (min_communicate_before_store-communication_cost[each_node_in_system][nodes_test])*blockIDsize
                    if min_communicate_before_store>communication_cost[each_node_in_system][nodes_test]:
                        this_node_saved_in_node_test+=blocksizes[blockID-beginID]*(min_communicate_before_store>communication_cost[each_node_in_system][nodes_test])
                        total_saved_in_node_test+=this_node_saved_in_node_test
                cost_and_nodes[nodes_test]=total_saved_in_node_test
                # if total_saved_in_node_test>max_improve[0]:
                #     max_improve[0]=total_saved_in_node_test
                #     max_improve_node[0]=nodes_test
                # elif total_saved_in_node_test<=max_improve[0] and total_saved_in_node_test>max_improve[1]:
                #     max_improve[1]=total_saved_in_node_test
                #     max_improve_node[1]=nodes_test
                # elif total_saved_in_node_test<=max_improve[1] and total_saved_in_node_test>max_improve[2]:
                #     max_improve[2]=total_saved_in_node_test
                #     max_improve_node[2]=nodes_test
            # got the best position for blockID to store
            cost_and_nodes_kvs=sorted(cost_and_nodes.items(),key=lambda x:x[1],reverse=True)
            nums_3=0
            for kvs in cost_and_nodes_kvs:
                if nums_3>=3:
                    break
                max_improve_node.append(kvs[0])
                max_improve.append(kvs[1])
                nums_3+=1
            ##debug
            Chosen_nodes_debug[blockID]=max_improve_node
            ##end
            # for i in range(len(max_improve)):
            #     if max_improve[i]<0:
            #         max_improve_node[i]=-1
            if np.sum(max_improve_node)==-3:
                print('[calv]: invalid block chosen!')
            n_popu_1=nodes_stored_blocks_popularity[nodeID][blockID][0]
            #get popularity distribution
            # get this with >> redirection
            len_max_prove_nodes=0
            for i in max_improve_node:
                if i!=-1:
                    len_max_prove_nodes+=1
            actual_replica_store=0
            if n_popu_1>REPLICA_LIMIT[0]:
                # actual_replica_store=len(max_improve_node)
                # print("[calv]: me:",nodeID,'block:',blockID,'popularity[1]:',n_popu_1,'already store nodes:',sorted(blocks_in_which_nodes_and_timelived[blockID-beginID]),', this node set:',max_improve_node)
                for i in range(len(max_improve_node)):
                    store_block_to_node(blockID,max_improve_node[i],period)#,popularity_passing_dict[blockID])
                    stored_blocks[max_improve_node[i]]=blockID
            elif n_popu_1<=REPLICA_LIMIT[0] and nodes_stored_blocks_popularity[nodeID][blockID][1]>REPLICA_LIMIT[1]:
                # actual_replica_store=len(max_improve_node)-1
                # print("[calv]: me:",nodeID,'block:',blockID,'popularity[1]:',n_popu_1,'already store nodes:',sorted(blocks_in_which_nodes_and_timelived[blockID-beginID]),', this node set:',max_improve_node)
                upper_bound=2
                if len(max_improve_node)<upper_bound:
                    upper_bound=len(max_improve_node)
                for i in range(upper_bound):
                    store_block_to_node(blockID,max_improve_node[i],period)#,popularity_passing_dict[blockID])
                    stored_blocks[max_improve_node[i]]=blockID
            else:
                # actual_replica_store=1
                # print("[calv]: me:",nodeID,'block:',blockID,'popularity[1]:',n_popu_1,'already store nodes:',sorted(blocks_in_which_nodes_and_timelived[blockID-beginID]),', this node set:',max_improve_node)
                upper_bound=1
                if len(max_improve_node)<upper_bound:
                    upper_bound=len(max_improve_node)
                for i in range(upper_bound):
                    store_block_to_node(blockID,max_improve_node[i],period)#,popularity_passing_dict[blockID])
                    stored_blocks[max_improve_node[i]]=blockID
            
            # print(json.dumps([len_max_prove_nodes,n_popu_1]))
            # if actual_replica_store>len_max_prove_nodes:
            #     actual_replica_store=len_max_prove_nodes
            # print(str(len_max_prove_nodes)+','+str(n_popu_1)+','+str(actual_replica_store))
            #end
        return [],len(blocks_to_be_offload),stored_blocks
    elif active_type=='caltwo':
        replica_nums_=2
        # print(len(blocks_to_be_offload))
        # if len(blocks_to_be_offload)!=top_num_to_offload:
        #     print('***candidate choose warning :calculate: ,',len(blocks_to_be_offload),', blocks are chosen.')
        stored_blocks={}
        for blockID in blocks_to_be_offload:
            # largest improvement is brought by which nodes_test
            max_improve=[]
            max_improve_node=[]
            cost_and_nodes={}
            # which node shall I store blockID
            considered_nodes=[]
            for nodeid in range(nodes_num):
                if nodeid not in blocks_in_which_nodes_and_timelived[blockID-beginID]:
                    considered_nodes.append(nodeid)
            if len(considered_nodes)==0:
                print('active: calculate: no endough andidate nodes!')
            for nodes_test in considered_nodes:
                # improvement brought by storing blockID in nodes_test
                total_saved_in_node_test =0
                # caculate total improvement by adding each node's improvement if I store node into nodes_test
                for each_node_in_system in range(nodes_num):
                    # node each_node_in_system's improvement brought by storing blockID in nodes_test
                    this_node_saved_in_node_test=0
                    storage_nodes_of_blockID=blocks_in_which_nodes_and_timelived[blockID-beginID].keys()
                    min_communicate_before_store=np.inf
                    # current min_communication.
                    # if communication_cost[nodes_test][each_node_in_system]<min_communication currently,
                    # there is a improvemnt >0
                    for nodes_store in storage_nodes_of_blockID:
                        this_communication_cost=communication_cost[each_node_in_system][nodes_store]
                        if this_communication_cost<min_communicate_before_store:
                            min_communicate_before_store=this_communication_cost
                    # if blockID is stored in node_test, node each_node_in_system can improve by 
                    # (min_communicate_before_store-communication_cost[each_node_in_system][nodes_test])*blockIDsize
                    if min_communicate_before_store>communication_cost[each_node_in_system][nodes_test]:
                        this_node_saved_in_node_test+=blocksizes[blockID-beginID]*(min_communicate_before_store>communication_cost[each_node_in_system][nodes_test])
                        total_saved_in_node_test+=this_node_saved_in_node_test
                cost_and_nodes[nodes_test]=total_saved_in_node_test
            # got the best position for blockID to store
            cost_and_nodes_kvs=sorted(cost_and_nodes.items(),key=lambda x:x[1],reverse=True)
            nums_2=0
            for kvs in cost_and_nodes_kvs:
                if nums_2>=replica_nums_:
                    break
                max_improve_node.append(kvs[0])
                max_improve.append(kvs[1])
                nums_2+=1
            ##debug
            Chosen_nodes_debug[blockID]=max_improve_node
            ##end
            # for i in range(len(max_improve)):
            #     if max_improve[i]<=0:
            #         max_improve_node[i]=-1
            if np.sum(max_improve_node)==-2:
                print('[calthree]: invalid block chosen!')
            # print("[calthree]: me:",nodeID,'block:',blockID,',already store nodes:',sorted(blocks_in_which_nodes_and_timelived[blockID-beginID]),', this node set:',max_improve_node)
            replica_num_upper_bound=replica_nums_
            if replica_num_upper_bound>len(max_improve_node):
                replica_num_upper_bound=len(max_improve_node)
            for i in range(replica_num_upper_bound):
                store_block_to_node(blockID,max_improve_node[i],period)#,popularity_passing_dict[blockID])
                stored_blocks[max_improve_node[i]]=blockID
        return [],len(blocks_to_be_offload),stored_blocks
    else:
        print("invalid active type! default('random') is set.")
        node_to_be_offload=random.randint(0,nodes_num-1)
        for blockID in blocks_to_be_offload:
            store_block_to_node(blockID,node_to_be_offload,period)#,popularity_passing_dict[blockID])
    # nothing else to return 
    return Chosen_nodes_debug,len(blocks_to_be_offload)

    
def store_block_to_node(blockID,nodeID,period):#,popularity_value):
    """(int,int,int,str) - list of dict:(int, int), list of dict:(int,int), list of int

    store 1 block to 1 node.
    update the 3 big lists.
    """
    if nodeID==-1:
        print('[store_block_to_node]: invalid store.')
        return -1
    if nodeID in blocks_in_which_nodes_and_timelived[blockID-beginID]:
        print("[store_block_to_node]: trying to store a block to a node in which the block is already exist!")
        if len(blocks_in_which_nodes_and_timelived[blockID-beginID])<nodes_num:
            print('[store_block_to_node]: NOT FULL: bad chioce of node!')
    # get lifetime
    time_lived=period
    # update the storage used
    if nodeID not in blocks_in_which_nodes_and_timelived[blockID-beginID]:
        nodes_storage_used[nodeID]+=blocksizes[blockID-beginID]
    # update lifetime
    blocks_in_which_nodes_and_timelived[blockID-beginID][nodeID]=time_lived
    # update popularity
    # popularity is inherent from giving node
    if blockID not in nodes_stored_blocks_popularity[nodeID]:
        nodes_stored_blocks_popularity[nodeID][blockID]=[0,0]#popularity_value.copy()

def update_livetime_and_expel(end_since,epochs,fp):
    """(int,int) - list of dict,key is int,value is int

    update live time of blocks and expel expired blocks.
    this is called every 'epochs' epochs.
    """

    # blocks in which node to be expeled
    # a list of list of int
    dead_blocks=[]

    ###debug
    delete_blocks_debug=[]
    for i in range(nodes_num):
        delete_blocks_debug.append([])
    ### end

    # update livetime and find dead blocks
    for blockID in range(beginID,end_since):
        dead_blocks.append([])
        for kv in blocks_in_which_nodes_and_timelived[blockID-beginID].items():
            if kv[1]<=epochs:
                dead_blocks[blockID-beginID].append(kv[0])
            blocks_in_which_nodes_and_timelived[blockID-beginID][kv[0]]-=epochs
    # expel dead blocks
    for blockID in range(beginID,end_since):
        for nodeID in dead_blocks[blockID-beginID]:
            if len(blocks_in_which_nodes_and_timelived[blockID-beginID])>LEFT_BLOCKS:
                # update popularity
                nodes_stored_blocks_popularity[nodeID].pop(blockID)
                # update storage_used
                if nodeID in blocks_in_which_nodes_and_timelived[blockID-beginID]:
                    nodes_storage_used[nodeID]-=blocksizes[blockID-beginID]
                # update time_lived
                blocks_in_which_nodes_and_timelived[blockID-beginID].pop(nodeID)
                delete_blocks_debug[nodeID].append(blockID)
    # nothing to return
    return delete_blocks_debug

def expel_blocks_LLU(last_num_to_expel,end_since,fp):
    '''
    expel blocks whose popularity is the last nums in nodes_stored_blocks_popularity
    '''
    
    # expel blocks in every node
    random_node=list(range(nodes_num))
    # randomly shuffle
    random.shuffle(random_node)
    ###DEBUG

    # print(random_node)
    ###end
    ###debug
    # expel_last_num=[0]*nodes_num
    delete_blocks_debug=[]
    for i in range(nodes_num):
        delete_blocks_debug.append([])
    ### end
    # print(fp)
    if fp:
        # if end_since>=endID-100:
        #     print('\n epoch=',end_since,file=fp)
        total_length=0
    for nodeID in random_node:
        # find dead blocks: whose popularity is the least
        kvs=sorted(nodes_stored_blocks_popularity[nodeID].items(),key=lambda x:x[1][0]+x[1][1],reverse=False)
        chosen_kvs=[]
        i=0
        for kv in kvs:
            if i>= last_num_to_expel:
                break
            if len(blocks_in_which_nodes_and_timelived[kv[0]-beginID])>LEFT_BLOCKS:
                chosen_kvs.append(kv)
                delete_blocks_debug[nodeID].append(kv[0])
                i+=1
        if end_since>=endID-100:
            new_dict={}
            for kv in kvs:
                if len(blocks_in_which_nodes_and_timelived[kv[0]-beginID])>LEFT_BLOCKS:
                    new_dict[kv[0]]=kv[1]
            # if fp:
            # #     print('node=',nodeID,'total length:',len(new_dict),',expel blocks sort:',new_dict,file=fp)
            #     # total_length+=len(new_dict)
            #     total_length+=len(chosen_kvs)
        if fp:
            total_length+=len(chosen_kvs)
    
        ### debug
        # expel_last_num[nodeID]=i
        ### end
        # dead blocks that going to be expelled
        dead_blocks=[blockID[0] for blockID in chosen_kvs]
        # expel these blocks except there are only one left
        for blockID in dead_blocks:
            if len(blocks_in_which_nodes_and_timelived[blockID-beginID])<=LEFT_BLOCKS:
                print('[expel-llu]: bad expel block chosen: cannot be deleted!')
            if len(blocks_in_which_nodes_and_timelived[blockID-beginID])>LEFT_BLOCKS:
                # update popularity
                nodes_stored_blocks_popularity[nodeID].pop(blockID)
                # update storage used
                if nodeID in blocks_in_which_nodes_and_timelived[blockID-beginID]:
                    nodes_storage_used[nodeID]-=blocksizes[blockID-beginID]
                # update time_lived
                blocks_in_which_nodes_and_timelived[blockID-beginID].pop(nodeID)
    # nothing to return
    ##debug
    # print('expel number:',expel_last_num)
    ###
    if fp:
        # if end_since>=endID-100:
            # print('\n epoch=',end_since,'total blocks can be deleted:',total_length,file=fp)
        print('epoch,',end_since,',total blocks can be deleted:,',total_length,file=fp)
    return delete_blocks_debug

def expel_blocks(expel_type,end_since,epochs,last_num_to_expel,fp):
    '''
    expel blocks.

    expel_type: 'curve' or 'llu'.
    'curve': end_since and epoch must be given
    'llu': last_num_to_expel must be given<default>
    '''
    delete_blocks_debug=[]
    if expel_type =='curve':
        if end_since==beginID and epochs ==1:
            print("[expel_blocks]: initial settings!")
        delete_blocks_debug=update_livetime_and_expel(end_since,epochs,fp)
    elif expel_type=='llu':
        delete_blocks_debug=expel_blocks_LLU(last_num_to_expel,end_since,fp)
    else:
        print("expel_type invalid. llu is set")
    return delete_blocks_debug

def shift_popularity():
    '''
    shift popularity list, which length is 2.
    this function shall be called just after new issuing block, before active replica, request, passive replica and expel.
    '''
    for nodeID in range(nodes_num):
        nodes_stored_blocks_popularity[nodeID]={x[0]:[x[1][1],0] for x in nodes_stored_blocks_popularity[nodeID].items()}
    
    return

def broadcast_popularity_and_get_gobal_popularity(last_blockID):
    '''
    get local popularity list and calculate the global popularity.
    blockID\in [beginID,last_blockID], last_blockID is included.
    '''
    block_global_popularity=[0]*(last_blockID+1-beginID)
    for blockID in range(beginID,last_blockID+1):
        for nodeID in range(nodes_num):
            if blockID in nodes_stored_blocks_popularity[nodeID]:
                block_global_popularity[blockID-beginID]+=nodes_stored_blocks_popularity[nodeID][blockID][1]
    # update
    for blockID in range(beginID,last_blockID+1):
        # replica_sum=len(blocks_in_which_nodes_and_timelived[blockID-beginID])
        for nodeID in range(nodes_num):
            if blockID in nodes_stored_blocks_popularity[nodeID]:
                nodes_stored_blocks_popularity[nodeID][blockID][1]=block_global_popularity[blockID-beginID]
                # print(nodes_stored_blocks_popularity[nodeID][blockID][1])
    # print('update done')
    #
def update_communication(chosen_blocks_storage_per_node,chosen_blocks_request_time_per_node):
    for i in range(len(chosen_blocks_request_time_per_node)):
        for j in range(len(chosen_blocks_request_time_per_node[i])):
            if chosen_blocks_request_time_per_node[i][j]!=0:
                communication_cost[i][j]=chosen_blocks_request_time_per_node[i][j]/chosen_blocks_storage_per_node[i][j]
    
def get_block_from_which_xor(nodeID,blockID):
    storage_nodes_of_blockID=blocks_in_which_nodes_and_timelived[blockID-beginID].keys()
    min_distance=np.inf
    min_node=-1
    for nodes_store in storage_nodes_of_blockID:
        this_distance=blockID^nodes_store
        if this_distance<min_distance:
            min_distance=this_distance
            min_node=nodes_store
    if min_node==-1:
        print("no block stored now! for blocks:",blockID,',requesting node:',nodeID,',store block nodes:',storage_nodes_of_blockID)
        exit(-1)
    time_cost=communication_cost_ori[nodeID][min_node]*blocksizes[beginID-beginID]
    return min_node,time_cost



def get_blockID_from_which(nodeID,blockID):
    """(int,int) -> (int,float)

    nodeID will choose the node with smallest communication cost to get block blockID.
    Return the node chosen and communication cost * blocksize
    """
    # storage nodes of blockID
    storage_nodes_of_blockID=blocks_in_which_nodes_and_timelived[blockID-beginID].keys()

    # current min_communication.
    min_communication=np.inf
    min_node=-1
    
    for nodes_store in storage_nodes_of_blockID:
        this_communication=communication_cost[nodeID][nodes_store]
        if this_communication<min_communication:
            min_communication=this_communication
            min_node=nodes_store
    if min_communication ==np.inf:
        print("no block stored now! for blocks:",blockID,',requesting node:',nodeID,',store block nodes:',storage_nodes_of_blockID,'cmm_cost=',[communication_cost[nodeID][i] for i in storage_nodes_of_blockID])
        print(communication_cost)
        exit(-1)
    # get time cost
    time_cost=communication_cost_ori[nodeID][min_node]*blocksizes[beginID-beginID]
    # time_cost=min_communication*blocksizes[beginID-beginID]
    # return min_node and time cost   
    return min_node, time_cost

def init_all_settings(blksizes,beginid=2016,endid=2016+400,static_blks=200,nodes_n=10):
    """(list of list of int,list of int,list of list of float)

    Must be called primarily to init global variables.
    """
    global blocksizes
    
    global nodes_storage_used
    global beginID
    global nodes_num
    global endID
    global static_blocks

    blocksizes=blksizes
    
    # communication_cost_ori=communication_cst.copy()

    beginID=beginid
    endID=endid
    static_blocks=static_blks
    nodes_num=nodes_n

def set_communication_cost():
    global communication_cost
    global communication_cost_ori
    communication_cost=[[0.9283573 , 1.20546818, 0.73509698, 1.88864734, 1.29204335,
        2.09526447, 1.5963019 , 0.02879965, 0.02458762, 0.91872697],
       [0.30036054, 1.00466097, 1.52191513, 0.65414875, 1.50644343,
        0.68382484, 0.92965741, 0.42839557, 1.17236144, 1.02996051],
       [0.56822564, 1.27541919, 0.61683779, 0.84236014, 1.0612637 ,
        0.92658329, 0.99121881, 1.81738219, 1.78517851, 0.24705094],
       [1.79836131, 1.09191752, 1.60516537, 0.37575595, 1.38438759,
        1.63279625, 0.70583861, 1.06731513, 1.42392138, 0.7188484 ],
       [1.03360349, 0.18936742, 0.59310497, 0.50183122, 1.1486868 ,
        1.05833852, 1.38323434, 1.13598478, 1.16539371, 0.96001515],
       [0.93136753, 1.12780837, 0.13849183, 1.14214214, 0.60152085,
        0.55402053, 1.10870503, 0.67730834, 0.68433858, 0.66241989],
       [1.79465379, 0.80143361, 0.98104521, 0.30108855, 1.00392018,
        0.94334858, 0.67497941, 0.8915002 , 1.36297052, 0.63732797],
       [0.76799253, 0.58418479, 0.93061772, 1.50013164, 0.8554365 ,
        1.77693385, 0.64691308, 0.82144779, 0.4348138 , 1.91490114],
       [0.98391884, 1.19110244, 1.01538815, 0.69359769, 0.53632453,
        0.97916297, 1.01081265, 0.38186164, 0.44921611, 1.96850188],
       [1.6611757 , 0.12190398, 1.32284431, 1.04920968, 0.34622065,
        0.11826715, 2.28277831, 0.37742129, 1.38527299, 0.95568288]]
    for i in range(nodes_num):
        communication_cost[i][i]=0
    communication_cost_ori=[[0.9283573 , 1.20546818, 0.73509698, 1.88864734, 1.29204335,
        2.09526447, 1.5963019 , 0.02879965, 0.02458762, 0.91872697],
       [0.30036054, 1.00466097, 1.52191513, 0.65414875, 1.50644343,
        0.68382484, 0.92965741, 0.42839557, 1.17236144, 1.02996051],
       [0.56822564, 1.27541919, 0.61683779, 0.84236014, 1.0612637 ,
        0.92658329, 0.99121881, 1.81738219, 1.78517851, 0.24705094],
       [1.79836131, 1.09191752, 1.60516537, 0.37575595, 1.38438759,
        1.63279625, 0.70583861, 1.06731513, 1.42392138, 0.7188484 ],
       [1.03360349, 0.18936742, 0.59310497, 0.50183122, 1.1486868 ,
        1.05833852, 1.38323434, 1.13598478, 1.16539371, 0.96001515],
       [0.93136753, 1.12780837, 0.13849183, 1.14214214, 0.60152085,
        0.55402053, 1.10870503, 0.67730834, 0.68433858, 0.66241989],
       [1.79465379, 0.80143361, 0.98104521, 0.30108855, 1.00392018,
        0.94334858, 0.67497941, 0.8915002 , 1.36297052, 0.63732797],
       [0.76799253, 0.58418479, 0.93061772, 1.50013164, 0.8554365 ,
        1.77693385, 0.64691308, 0.82144779, 0.4348138 , 1.91490114],
       [0.98391884, 1.19110244, 1.01538815, 0.69359769, 0.53632453,
        0.97916297, 1.01081265, 0.38186164, 0.44921611, 1.96850188],
       [1.6611757 , 0.12190398, 1.32284431, 1.04920968, 0.34622065,
        0.11826715, 2.28277831, 0.37742129, 1.38527299, 0.95568288]]
    for i in range(nodes_num):
        communication_cost_ori[i][i]=0



    