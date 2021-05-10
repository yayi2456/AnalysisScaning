import json
import numpy as np
import random
import time
import os
import matplotlib.pyplot as plt

MAX_LINE=1000

def load_txncount():
    filename='E:\\CUB\\bh.dat\\block-txncount-654000.csv'
    block_txncount=[]
    i=0
    with open(filename,'r')as datafile:
        for dataline in datafile:
            [blockid,txncount]=dataline.split(',')
            block_txncount.append([int(blockid),int(txncount)])
            i+=1
            if(i>=MAX_LINE):
                return block_txncount
    return block_txncount

def plot_txncount(block_txncount):
    # xaxis=[b_txnc[0] for b_txnc in block_txncount]
    xaxis=range(block_txncount[0][0],block_txncount[0][0]+len(block_txncount))
    yaxis=[b_txnc[1]for b_txnc in block_txncount]
    # print(len(xaxis),',',len(yaxis),block_txncount[0],block_txncount[-1])
    plt.scatter(xaxis,yaxis,marker='.')
    plt.title('txncount in every blk')
    plt.xlabel('block id')
    plt.xlabel('txn count')
    plt.show()

def txncount():
    block_txncount=load_txncount()
    plot_txncount(block_txncount)

#====================================


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

def accessTxinZipfr(blk_txncount):
    s=1.2
    new_dict={}
    blk_probability_map={}
    txns=sum([d[1]for d in blk_txncount])
    probabllity=[0]*(txns)
    for i in range(len(probabllity)):
        probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number(txns,s)*pow(i+1,s))
    # plt.scatter(range(0,len(probabllity)),sorted(probabllity),
    #         color='pink',label='ori probability',marker='.')
    random.shuffle(probabllity)
    # get blk probability
    blk_probability_map={}
    cur_pro=0
    for bt in blk_txncount:
        txncount=bt[1]
        blk_num=bt[0]
        blk_probability_map[blk_num]=0
        for pos in range(txncount):
            pro=probabllity[cur_pro]
            blk_probability_map[blk_num]+=pro
            cur_pro+=1
    return blk_probability_map

def get_blk_probability_map_zipfr():
    blk_txncount=load_txncount()
    blk_probability_map=accessTxinZipfr(blk_txncount)
    return blk_probability_map

def getZipfofLength(size):
    s=1.2
    txns=size
    probabllity=[0]*(txns)
    for i in range(len(probabllity)):
        probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number(txns,s)*pow(i+1,s))
    # print(sum(probabllity))
    return probabllity 

def get_txns_2_blk():
    blk_probability_map=get_blk_probability_map_zipfr()
    x_axis=range(len(blk_probability_map))
    plt.scatter(x_axis,sorted(list(blk_probability_map.values())),
            color='b',label='sum-up probability',marker='.')
    # print(len(blk_probability_map))
    probability_of_blk=getZipfofLength(len(blk_probability_map))
    plt.scatter(x_axis,probability_of_blk,color='r',label='zipf',marker='_')
    # plt.xlabel('blockID')
    plt.ylabel('access probability')
    plt.legend()
    plt.show()

if __name__=='__main__':
    # txncount()
    get_txns_2_blk()