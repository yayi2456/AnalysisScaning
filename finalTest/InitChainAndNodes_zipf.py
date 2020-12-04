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
# x=[239, 39, 161, 24, 383, 46, 26, 249, 365, 108, 103, 17, 60, 276, 278, 345, 11, 360, 338, 320, 208, 327, 394, 262, 30, 90, 86, 375, 187, 396, 156, 101, 306, 176, 225, 168, 369, 47, 132, 340, 332, 123, 378, 374, 169, 299, 317, 6, 71, 255, 343, 361, 15, 14, 295, 21, 309, 63, 92, 265, 200, 246, 43, 177, 280, 251, 197, 364, 385, 190, 217, 57, 70, 134, 186, 329, 154, 363, 9, 219, 302, 16, 304, 127, 328, 314, 235, 288, 289, 181, 391, 357, 193, 386, 58, 189, 195, 149, 324, 260, 135, 85, 293, 204, 237, 271, 236, 59, 172, 290, 226, 50, 245, 2, 392, 141, 160, 116, 95, 115, 352, 336, 285, 277, 207, 150, 66, 286, 209, 107, 96, 284, 
# 61, 220, 113, 224, 316, 339, 145, 34, 287, 252, 201, 238, 397, 387, 110, 93, 175, 227, 322, 20, 27, 362, 88, 341, 51, 303, 128, 118, 202, 359, 82, 67, 167, 199, 194, 35, 33, 274, 376, 157, 379, 233, 390, 28, 106, 19, 389, 48, 292, 354, 178, 358, 163, 162, 8, 247, 382, 221, 281, 0, 125, 3, 121, 393, 97, 367, 351, 13, 153, 29, 38, 148, 54, 349, 335, 36, 89, 12, 69, 250, 143, 133, 313, 1, 347, 104, 155, 269, 272, 78, 
# 308, 5, 170, 398, 99, 142, 94, 355, 234, 353, 166, 384, 261, 112, 231, 399, 268, 174, 137, 230, 371, 102, 242, 373, 147, 315, 380, 337, 310, 395, 91, 223, 140, 105, 45, 25, 79, 388, 52, 22, 87, 350, 55, 68, 158, 348, 248, 139, 72, 283, 184, 264, 298, 62, 49, 173, 192, 258, 381, 323, 77, 130, 129, 73, 138, 41, 7, 171, 279, 243, 203, 56, 211, 80, 307, 10, 244, 205, 83, 84, 109, 164, 377, 206, 240, 23, 273, 146, 18, 229, 311, 366, 37, 301, 64, 326, 372, 346, 81, 183, 126, 275, 53, 370, 111, 185, 291, 256, 297, 241, 144, 159, 331, 270, 282, 215, 4, 344, 228, 100, 305, 210, 198, 180, 131, 254, 259, 40, 42, 267, 75, 151, 333, 330, 368, 214, 120, 325, 318, 266, 300, 32, 321, 294, 31, 342, 334, 188, 296, 136, 222, 98, 213, 182, 76, 152, 257, 216, 196, 212, 356, 191, 117, 124, 65, 232, 74, 218, 312, 122, 165, 179, 119, 114, 253, 44, 
# 263, 319]
#key: block number
#value: rank
CONSTANT_RANK={239: 0, 39: 1, 161: 2, 24: 3, 383: 4, 46: 5, 26: 6, 249: 7, 365: 8, 108: 9, 103: 10, 17: 11, 60: 12, 276: 13, 278: 14, 345: 15, 11: 16, 
360: 17, 338: 18, 320: 19, 208: 20, 327: 21, 394: 22, 262: 23, 30: 24, 90: 25, 86: 26, 375: 27, 187: 28, 396: 29, 156: 30, 101: 31, 306: 32, 176: 33, 225: 34, 
168: 35, 369: 36, 47: 37, 132: 38, 340: 39, 332: 40, 123: 41, 378: 42, 374: 43, 169: 44, 299: 45, 317: 46, 6: 47, 71: 48, 255: 49, 343: 50, 361: 51, 15: 52, 
14: 53, 295: 54, 21: 55, 309: 56, 63: 57, 92: 58, 265: 59, 200: 60, 246: 61, 43: 62, 177: 63, 280: 64, 251: 65, 197: 66, 364: 67, 385: 68, 190: 69, 217: 70, 
57: 71, 70: 72, 134: 73, 186: 74, 329: 75, 154: 76, 363: 77, 9: 78, 219: 79, 302: 80, 16: 81, 304: 82, 127: 83, 328: 84, 314: 85, 235: 86, 288: 87, 289: 88, 
181: 89, 391: 90, 357: 91, 193: 92, 386: 93, 58: 94, 189: 95, 195: 96, 149: 97, 324: 98, 260: 99, 135: 100, 85: 101, 293: 102, 204: 103, 237: 104, 271: 105, 
236: 106, 59: 107, 172: 108, 290: 109, 226: 110, 50: 111, 245: 112, 2: 113, 392: 114, 141: 115, 160: 116, 116: 117, 95: 118, 115: 119, 352: 120, 336: 121, 
285: 122, 277: 123, 207: 124, 150: 125, 66: 126, 286: 127, 209: 128, 107: 129, 96: 130, 284: 131, 61: 132, 220: 133, 113: 134, 224: 135, 316: 136, 339: 137, 
145: 138, 34: 139, 287: 140, 252: 141, 201: 142, 238: 143, 397: 144, 387: 145, 110: 146, 93: 147, 175: 148, 227: 149, 322: 150, 20: 151, 27: 152, 362: 153, 
88: 154, 341: 155, 51: 156, 303: 157, 128: 158, 118: 159, 202: 160, 359: 161, 82: 162, 67: 163, 167: 164, 199: 165, 194: 166, 35: 167, 33: 168, 274: 169, 
376: 170, 157: 171, 379: 172, 233: 173, 390: 174, 28: 175, 106: 176, 19: 177, 389: 178, 48: 179, 292: 180, 354: 181, 178: 182, 358: 183, 163: 184, 162: 185, 
8: 186, 247: 187, 382: 188, 221: 189, 281: 190, 0: 191, 125: 192, 3: 193, 121: 194, 393: 195, 97: 196, 367: 197, 351: 198, 13: 199, 153: 200, 29: 201, 38: 202, 
148: 203, 54: 204, 349: 205, 335: 206, 36: 207, 89: 208, 12: 209, 69: 210, 250: 211, 143: 212, 133: 213, 313: 214, 1: 215, 347: 216, 104: 217, 155: 218, 269: 219, 
272: 220, 78: 221, 308: 222, 5: 223, 170: 224, 398: 225, 99: 226, 142: 227, 94: 228, 355: 229, 234: 230, 353: 231, 166: 232, 384: 233, 261: 234, 112: 235, 231: 236, 
399: 237, 268: 238, 174: 239, 137: 240, 230: 241, 371: 242, 102: 243, 242: 244, 373: 245, 147: 246, 315: 247, 380: 248, 337: 249, 310: 250, 395: 251, 91: 252, 
223: 253, 140: 254, 105: 255, 45: 256, 25: 257, 79: 258, 388: 259, 52: 260, 22: 261, 87: 262, 350: 263, 55: 264, 68: 265, 158: 266, 348: 267, 248: 268, 139: 269, 
72: 270, 283: 271, 184: 272, 264: 273, 298: 274, 62: 275, 49: 276, 173: 277, 192: 278, 258: 279, 381: 280, 323: 281, 77: 282, 130: 283, 129: 284, 73: 285, 138: 286,
 41: 287, 7: 288, 171: 289, 279: 290, 243: 291, 203: 292, 56: 293, 211: 294, 80: 295, 307: 296, 10: 297, 244: 298, 205: 299, 83: 300, 84: 301, 109: 302, 164: 303, 
 377: 304, 206: 305, 240: 306, 23: 307, 273: 308, 146: 309, 18: 310, 229: 311, 311: 312, 366: 313, 37: 314, 301: 315, 64: 316, 326: 317, 372: 318, 346: 319, 81: 320, 
 183: 321, 126: 322, 275: 323, 53: 324, 370: 325, 111: 326, 185: 327, 291: 328, 256: 329, 297: 330, 241: 331, 144: 332, 159: 333, 331: 334, 270: 335, 282: 336, 
 215: 337, 4: 338, 344: 339, 228: 340, 100: 341, 305: 342, 210: 343, 198: 344, 180: 345, 131: 346, 254: 347, 259: 348, 40: 349, 42: 350, 267: 351, 75: 352, 
 151: 353, 333: 354, 330: 355, 368: 356, 214: 357, 120: 358, 325: 359, 318: 360, 266: 361, 300: 362, 32: 363, 321: 364, 294: 365, 31: 366, 342: 367, 334: 368, 
 188: 369, 296: 370, 136: 371, 222: 372, 98: 373, 213: 374, 182: 375, 76: 376, 152: 377, 257: 378, 216: 379, 196: 380, 212: 381, 356: 382, 191: 383, 117: 384, 
 124: 385, 65: 386, 232: 387, 74: 388, 218: 389, 312: 390, 122: 391, 165: 392, 179: 393, 119: 394, 114: 395, 253: 396, 44: 397, 263: 398, 319: 399}

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

    
    
    chain_length=endID-beginID

    # get the distribution probability
    if distribution_type=='uniform':
        for i in range(len(probabllity)):
            probabllity[i]=1/(chain_length)
    elif distribution_type=='zipf':
        #zipf PMF=F(K=k)=1/ghn(N,s)*k^s. k is the rank, N is the total number, 
        # s is a parameter to describe zipf curve
        #s is a parameter used in zipf distribution
        s=1.2
        for i in range(len(probabllity)):
            probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number(chain_length,s)*pow(i+1,s))
    elif distribution_type=='zipf8':
        s8=.8
        for i in range(len(probabllity)):
            probabllity[len(probabllity)-1-i]=1/(generalized_harmonic_number(chain_length,s8)*pow(i+1,s8))
    elif distribution_type=='zipfr':
        szr=1.2
        # new block: endID-1 is coming
        new_dict={}
        # key: block number
        # value: rank
        for i in range(chain_length):
            new_dict[i]=CONSTANT_RANK[i]
        new_dict_rank=sorted(new_dict.items(),key=lambda x:x[1])
        rank_now=1
        for i in range(len(probabllity)):
            probabllity[new_dict_rank[i][0]]=1/(generalized_harmonic_number(chain_length,szr)*pow(rank_now,szr))
            rank_now+=1
    elif distribution_type=='flyclient':
        # c and k are 2 params of flyclient, c\in (0,1],k\in N
        # delta=c^k
        c=0.5
        k=10
        neg_small=pow(c,k)
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

    elif distribution_type=='zipfr-old':
        sr=1.2
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
            probabllity[i]=1/(generalized_harmonic_number(chain_length,sr)*pow(rank_distribution[i],sr))
    else:
        print("INVALID CHOSEN DISTRIBUTION TYPE! default('uniform') is set.")
        for i in range(len(probabllity)):
            probabllity[i]=1/(endID-beginID)
    
    # choose chosen_block_nums
    # if endID-beginID>=390:
    #     print('chosen blocks probability:',probabllity)
    if chosen_block_nums!=0:
        chosen_blocks=np.random.choice(range(beginID,endID),size=chosen_block_nums,replace=False,p=probabllity)
    else:
        chosen_blocks=[]
    ### deubg
    # if(distribution_type=='zipfr'):
    #     top_10_blocks=[]
    #     top_10_blocks_p=[]
    #     for i in range(len(rank_distribution)):
    #         if rank_distribution[i]<=10:
    #             top_10_blocks.append(beginID+i)
    #             top_10_blocks_p.append(probabllity[i])
    #     print('current top 10 probability distribution: ',top_10_blocks_p)
    #     print('current top 10 blocknumbers:',top_10_blocks)
    #     print('chosen blocknumbers: ',chosen_block_nums)
    #     print('chosen blocks: ',chosen_blocks)
    #     print('==')
    # if distribution_type=='uniform':
    #     print('chosen blocks:',sorted(chosen_blocks))
    ### end debug
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

Pission_Probablity={}

def get_chosen_blocks_numbers(expection):
    '''(int) -> int
    Return chosen_block numbers this epoch.

    process of choosing blocks are regarded as Pission distirbution.
    we choose one chosen_block_number according to probability

    Pission distribution:
    P(X=k)=((\lambda^k)/(k!))*e^{-\lambda}, lambda is expection.
    '''
    if expection in Pission_Probablity:
        probability=Pission_Probablity[expection]
    else:
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
        Pission_Probablity[expection]=probability
    # print(probability)
    # choose one value based on probability
    chosen_number=np.random.choice(range(len(probability)),replace=False,p=probability)
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

            # communication_cost=np.absolute(np.random.normal(mu,sigma,[nodes_num,nodes_num]))
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
    
