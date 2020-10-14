#YaYi 2020.10.12

import numpy as np
import sys
import re
import random
import math

"""
build environment for replica algorithms.
1. read blockdata file and construct the skip list
2. generate random communication cost
3. read blocksize file 
4. provide a function to determine blocks needed for proof
"""

# file stores blockhashes
FILEHASHNAME='E:/CUB/bh.dat/bh.dat'
# file stores bits
FILEBITSNAME='E:/CUB/bh.dat/btc.com_diff_2020-07-02_08_27_40.csv'
# file stores blocksize
FILESIZENAME='E:/CUB/bh.dat/blocksize.txt'

### open
def build_block_list(beginID,endID):
    """(int,int) -> (list of list,int)

    Return a skip list(i.e. blocklist) constructed by targets and blockhash. 
    Return maxlevel of all these blocks.  

    blocklist: [[mylevel,nextnodelevel1,nextnodelevel2,...,nextnodemylevel],...]
    """

    blocklist=[]

    max_level=0
    # last node id of level i I've met. i range from 0 to 256
    # for now I've only met beginID.
    last_node_of_level=[beginID]*256

    # load blockhashes and block targets
    blockhashes=load_blockhashes(beginID,endID)
    blocktargets=load_blockbits_and_targets(beginID,endID)

    # construct the skip list
    for blockID in range(beginID,endID):
        blocklist.append([])
        # calculate block level
        if blockID==beginID:
            block_level=256
        else:
            block_level=cal_level(blockhashes[blockID-beginID], blocktargets[int(blockID/2016)])
        # error detect
        if block_level==0:
            print('error occured at blockID=',blockID)
            exit(-1)
            
        # maxlevel update
        if block_level>max_level and blockID!=beginID:
            max_level=block_level
        # put mylevel in
        blocklist[blockID-beginID].append(block_level)
        # put mylevel items of endID in(i.e. the next block of level1,2...mylevel,which is unknown now)
        for i in range(block_level):
            blocklist[blockID-beginID].append(endID)
        # Update the (i+1)-th 'next' field of the last_node_of_level[i] I've met 
        # whose level is not higher than block_level to blockID.
        # As blockID is the next block whose level is [1,block_level].
        if blockID != beginID:
            for i in range(block_level):
                blocklist[last_node_of_level[i]-beginID][i+1]=blockID
        # update last_node_of_level
        for i in range(block_level):
            last_node_of_level[i]=blockID

    return blocklist, max_level


def load_blockhashes(beginID,endID):
    """(int,int) -> list of int

    Return blockhash of each blocks whose height are between [beginID,endID) 
    based on FILEHASHNAME
    """

    blockhashes=[]

    # open file and get blockheight(i.e. blockID) and blockhash
    with open(FILEHASHNAME,'r') as data_file:
        for data_line in data_file:
            data_line_item=data_line.split()
            # block height is the 1st item
            blockID=int(data_line_item[0])
            # skip blocks lower than beginID and higher than or equal to endID
            if blockID<beginID:
                continue
            if blockID>=endID:
                break
            # block hash is the 2nd item
            blockhashes.append(data_line_item[1])
    return blockhashes


def load_blockbits_and_targets(beginID,endID):
    """(int,int) ->  list of int

    Return calculated target of blocks whose height are between [beginID,endID) 
    based on bits in FILEBITSNAME
    """

    targets=[]

    # open file and load bits and calculate targets
    with open(FILEBITSNAME) as bits_file:
        # append bits of blocks 0-2015 first
        block_bit=('1d00ffff')
        # append target of blocks 0-2015 first
        targets.append(cal_target(block_bit))
        # remove the first line cause it has already been read
        bits_file.readline()
        for bits_line in bits_file:
            # split all data
            bits_line=bits_line.replace('\n','')
            bits_line_item=bits_line.split(',')
            bits_line_item=bits_line_item[0:5:4]
            # get bits and remove '0x'
            block_bit=bits_line_item[1][2:]
            # get calculated targets
            targets.append(cal_target(block_bit))
    return targets


def cal_target(block_bit):
    """(str) -> int

    Return block target calculated by bits.
    """

    # get exponation, in hex
    exp=int(block_bit[:2],16)
    # get coefficient, in hex
    coef=int(block_bit[2:8],16)

    # calculate target and return
    return coef*pow(256,exp-3)


def cal_level(block_hash, block_target):
    """(int,int) -> (int)

    Return level of a block based on its block_hash and block_target
    """

    # get int format of blockhash 
    blockhash_with_no_0=re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", block_hash)
    blockhash_value=int(blockhash_with_no_0,16)
    #calculate level
    level=1
    while blockhash_value<(block_target/pow(2,level)):
        level+=1
    # print('blockhash=', blockhash_value, 'target=', block_target, 'level=',level)
    return level


### open
def scan_blocklist_no_repeat(m,beginID,endID,blocklist,max_level):
    """(int,int,int,list of list of int,int) -> list of int

    Return a list of blockIDs that are used to construct a proof at endID.
    """

    chosen_blocks=[]

    this_level=max_level
    this_blockID=beginID
    # to determine if it's the first time that we access the block
    block_scanned_times=[0]*(endID-beginID)

    # append blocks useful for proof at endID
    while this_level>0:
        this_level_blocks=0
        while this_blockID<endID:
            # occur a valid block in level this_level
            if block_scanned_times[this_blockID-beginID]==0:
                this_level_blocks+=1
            # find the next block
            this_blockID=blocklist[this_blockID-beginID][this_level]
        # reset block pointer
        this_blockID=beginID
        # if this_level has less than m block, no blocks are appeded
        if this_level_blocks<m:
            this_level-=1
            # this_blockID=beginID
            continue
        # append the last m valid blocks
        scanned_blocks=0
        while scanned_blocks<this_level_blocks-m:
            if block_scanned_times[this_blockID-beginID]==0:
                scanned_blocks+=1
            this_blockID=blocklist[this_blockID-beginID][this_level]
        while scanned_blocks<this_level_blocks:
            if block_scanned_times[this_blockID-beginID]==0:
                block_scanned_times[this_blockID-beginID]=1
                scanned_blocks+=1
                # add this block
                chosen_blocks.append(this_blockID)
            this_blockID=blocklist[this_blockID-beginID][this_level]
        # step into the next level
        this_level-=1
        # reset the first block
        this_blockID=beginID
    
    return chosen_blocks

def get_needed_blocks(beginID,endID,blocklist,distribution_type):
    """(int,int,list of list of int,str) -> list of int

    Return blocks chosen by one node to complete some certin mission.

    3 types of distribution_type are allowed:
    'zipf': zipf distribution
    'uniform': uniform distribution
    'flyclient': flyclient distribution
    """
    
    chosen_blocks=[]

    # we choose log_2(block_nums) blocks each time
    chosen_block_nums=int(math.log2(endID-beginID))

    # probability of each node to be chosen.
    probabllity=[0]*(endID-beginID)
    # sum()=1

    #s is a parameter used in zipf distribution
    s=1

    # c and k are 2 params of flyclient, c\in (0,1],k\in N
    # delta=c^k
    c=0.5
    k=10
    neg_small=pow(c,k)

    # get the distribution probability
    if distribution_type=='uniform':
        for i in range(len(probabllity)):
            probabllity[i]=1/(endID-beginID)
    elif distribution_type=='zipf':
        #zipf PMF=F(K=k)=1/ghn(N,s)*k^s. k is the rank, N is the total number, 
        # s is a parameter to describe zipf curve
        for i in range(len(probabllity)):
            probabllity[i]=1/(generalized_harmonic_number(endID-beginID,s)*pow(i+1,s))
    elif distribution_type=='flyclient':
        #PDF of flyclient is g(x)=1/((x-1)*ln(δ)), δ is c^k. c\in (0,1],k\in N
        # in their test, δ=2^{-10}
        # flyclient use difficult percentage.
        # here we consider unchanged target only.
        # P(x=k)=F_{k+1/N}-F{k}=(1/ln(δ))*(ln|k+1/N-1|-ln|k-1|)
        ### math.log1p(x), Return the natural logarithm of 1+x (base e). 
        ln_delta=1/math.log1p(pow(c,k)-1)
        for i in range(len(probabllity)):
            percentage_k=i/(endID-beginID)
            percentage_k_step_forward=percentage_k+1/(endID-beginID)
            if i==len(probabllity)-1:
                percentage_k_step_forward-=neg_small
            probabllity[i]=ln_delta*(math.log1p(-percentage_k_step_forward)-math.log1p(-percentage_k))
    else:
        print("INVALID CHOSEN DISTRIBUTION TYPE! default('uniform') is set.")
        for i in range(len(probabllity)):
            probabllity[i]=1/(endID-beginID)
    
    # choose chosen_block_nums
    chosen_blocks=np.random.choice(range(beginID,endID),size=chosen_block_nums,replace=False,p=probabllity)
    #return
    return chosen_blocks


def generalized_harmonic_number(N,s):
    """(float,float) -> float

    used in zipf PMF.which F(K=k)=1/ghn(N,s)*k^s
    """
    sum_up=0
    for i in range(1,N+1):
        sum_up+=pow(1/i,s)
    return sum_up


### open
def load_blocksizes(beginID,endID):
    """(int,int) -> (list of float, float)

    Return blocksizes of blocks whose height are between [bgeinID,endID) base on file FILESIZENAME.
    Return total size of blocks between [beginID,endID)
    """

    blocksizes=[]

    # size sum of all blocks between [beginID,endID)
    storage_of_all_blocks=0

    with open(FILESIZENAME,'r') as size_file:
        for size_line in size_file:
            size_line_item=size_line.split()
            # get block height
            blockID=int(size_line_item[0])
            # skip blocks lower than beginID and no lower than endID
            if blockID<beginID:
                continue
            if blockID>=endID:
                break
            block_size=float(size_line_item[1])
            blocksizes.append(block_size)
            # sum this size up to storage_of_all_blocks
            storage_of_all_blocks+=block_size

    return blocksizes,storage_of_all_blocks


### open
def generate_communication_cost(nodes_num, distribution_type):
    """(int,str) -> list of list of float

    Return communication cost between every 2 nodes generated randomly in normal distribution.
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
    
