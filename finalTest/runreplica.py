#YaYi 2020.10.13

import InitChainAndNodes
import ReplicationAlgorithms

"""
the main program.

"""

def init_environment():
    """ () -> int
    
    Init global variables in ReplicationAlgorithms.i.e. get the running environment ready.
    Return max_level
    """
    begin_id=2016
    static_blks=200
    end_id=begin_id+400
    nodes_n=10
    communication_distribution_type='1'

    blk_list,max_level=InitChainAndNodes.build_block_list(begin_id,end_id)
    blk_size=InitChainAndNodes.load_blocksizes(begin_id,end_id)
    communication_cst=InitChainAndNodes.generate_communication_cost(nodes_n,communication_cst)
    
    ReplicationAlgorithms.init_all_settings(blk_list,blk_size,communication_cst,begin_id,end_id,static_blks,nodes_n)
    
    # all params needed can be accessed from ReplicationAlgorithms.param

    # return max_level
    return max_level

def get_average_time_cost():
    """ () -> (list of int)

    run a certain replica algorithm, and return the average cost time in every dynamic epoch
    """

    # params of NIPoPoWs
    m=3
    # chosen block type: default :nipopows
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
    total_times=100
    # average time
    avg_time=[]
    
    # statically assign params
    piece=1
    curve_type_replica='2^n'
    period=6
    curve_type_expel='2^n'

    for run_times in range(total_times):
        avg_time.append([])
        ReplicationAlgorithms.blocks_in_which_nodes_and_timelived.clear()
        ReplicationAlgorithms.nodes_stored_blocks_popularity.clear()
        ReplicationAlgorithms.nodes_storage_used.clear()
        ReplicationAlgorithms.static_assign_blocks(piece,curve_type_replica,period,curve_type_expel)



if __name__=='__main__':
    init_environment()