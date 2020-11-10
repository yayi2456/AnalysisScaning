#YaYi 2020.10.12

import numpy as np
import sys
import re
import random
import math

"""
build environment for replica algorithms.
1. read blocksize file and store
2. generate random communication cost
3. provide a function to determine how many blocks a node need
4. provide a function to determine blocks needed for proof
"""

# datasize of blocksize
FILESIZENAME='E:/CUB/bh.dat/blocksize-654000.csv'


### open
def load_blocksizes(beginID,endID):
    """(int,int) -> (list of float, float)

    Return blocksizes of blocks whose height are between [bgeinID,endID) base on file FILESIZENAME.
    Return total size of blocks whose height is in [beginID,endID)
    """

    blocksizes=[]

    # size sum of all blocks between [beginID,endID)
    storage_of_all_blocks=0

    with open(FILESIZENAME,'r') as size_file:
        for size_line in size_file:
            size_line_item=size_line.split(',')
            # get block height
            blockID=int(size_line_item[0])
            # skip blocks lower than beginID and no lower than endID
            if blockID<beginID:
                continue
            if blockID>=endID:
                break
            block_size=float(size_line_item[1])/1000000
            blocksizes.append(block_size)
            # sum this size up to storage_of_all_blocks
            storage_of_all_blocks+=block_size

    return blocksizes,storage_of_all_blocks


def get_needed_blocks(beginID,endID,distribution_type,chosen_block_nums,rank_distribution):
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

    #s is a parameter used in zipf distribution
    s=1.2
    chain_length=endID-beginID

    # get the distribution probability
    if distribution_type=='uniform':
        for i in range(len(probabllity)):
            probabllity[i]=1/(chain_length)
    elif distribution_type=='zipf':
        #zipf PMF=F(K=k)=1/ghn(N,s)*k^s. k is the rank, N is the total number, 
        # s is a parameter to describe zipf curve
        for i in range(len(probabllity)):
            probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number(chain_length,s)*pow(i+1,s))
        
        print(probabllity)
    elif distribution_type=='zipfr':
        # generate rank_distribution
        if len(rank_distribution)==0:
            rank_distribution=list(range(1,chain_length+1))
            # randomly shuffle
            random.shuffle(rank_distribution)
        elif chain_length-len(rank_distribution)>0:
            # append chain_length-len blocks
            rest_block_numbers=chain_length-len(rank_distribution)
            for block_i in range(rest_block_numbers):
                my_rank=random.randint(1,chain_length)
                # update rank that is behind me
                for i in range(len(rank_distribution)):
                    if rank_distribution[i]>=my_rank:
                        rank_distribution[i]+=1
                # append my rank
                rank_distribution.append(my_rank)
        elif chain_length-len(rank_distribution)<0:
            print("[initChainandNode_zipf]:get_needed_blocks: ERR!INVALID RANK_DISTRIBUTION!")
        # nothing to do if chain_length==len

        # get probability according to blocks' rank
        for i in range(len(probabllity)):
            probabllity[i]=1/(generalized_harmonic_number(chain_length,s)*pow(rank_distribution[i],s))
    else:
        print("INVALID CHOSEN DISTRIBUTION TYPE! default('uniform') is set.")
        for i in range(len(probabllity)):
            probabllity[i]=1/(endID-beginID)
    
    # choose chosen_block_nums
    chosen_blocks=np.random.choice(range(beginID,endID),size=chosen_block_nums,replace=False,p=probabllity)
    #return
    return chosen_blocks,rank_distribution

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


def get_chosen_blocks_numbers(expection):
    '''(int) -> int
    Return chosen_block numbers this epoch.

    process of choosing blocks are regarded as Pission distirbution.
    we choose one chosen_block_number according to probability

    Pission distribution:
    P(X=k)=((\lambda^k)/(k!))*e^{-\lambda}, lambda is expection.
    '''
    # max_chosen_num is the max chosen num.
    max_chosen_num=2*expection+int(1/2*expection)

    # 0,1,...,max_chosen_num
    probability=[0]*(max_chosen_num+1)

    # total probability of [0,max_chosen_num-1]
    pre_probability=0
    # 
    for i in range(max_chosen_num):
        probability[i]=(pow(expection,i)/jiecheng(i))/pow(np.e,expection)
        pre_probability+=probability[i]
    probability[max_chosen_num]=1-pre_probability
    # print(probability)
    # choose one value based on probability
    chosen_number=np.random.choice(range(max_chosen_num+1),replace=False,p=probability)
    return chosen_number





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




### open
def generate_communication_cost(nodes_num, distribution_type):
    """(int,str) -> list of list of float

    Return communication cost between every 2 nodes generated randomly in normal distribution.

    2 types are allowed:
    'normal'/'1'
    """

    communication_cost=[]

    # generate communication cost randomly
    try:
        # normal distribution
        if distribution_type=='normal':
            mu=1
            sigma=0.5

            communication_cost=np.absolute(np.random.normal(mu,sigma,[nodes_num,nodes_num]))
        # each pair of nodes communicate at 1 cost
        elif distribution_type=='1':
            communication_cost=np.absolute(np.random.normal(1,1,[nodes_num,nodes_num]))
        else:
            sys.exit(-2)
    except:
        print('INVALID DISTRIBUTION TYPE! must be \'normal\' or \'1\'. distribution_type=\'1\' set.')
        communication_cost=np.absolute(np.random.normal(1,1,[nodes_num,nodes_num]))
    # nodes have no communication cost with itself
    for i in range(nodes_num):
        communication_cost[i][i]=0
    
    return communication_cost
    
