import random
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
def generate_ids():
    NODE_ID=[]
    BLOCK_ID=[]
    beginID=654000
    endID=654400
    b=0#beginID+10#beginID-10
    e=pow(2,16)#endID-10
    b2=0
    e2=pow(2,16)
    NODE_ID=np.random.choice(range(b,e),size=10,replace=False) 
    bidrange=range(b2,e2)
    BLOCK_ID=np.random.choice(bidrange,size=endID-beginID,replace=False)
    top_3=[]
    nid_NID={}
    bid_BID={}
    for i in range(10):
        nid_NID[i]=NODE_ID[i]
    for i in range(beginID,endID):
        bid_BID[i]=BLOCK_ID[i-beginID]

    for i in range(beginID,endID):
        tmp_id=nid_NID
        for j in range(10):
            tmp_id[j]=nid_NID[j]^bid_BID[i]
        tmp_id=sorted(tmp_id.items(),key=lambda x:x[1])[:3]
        top_3.append([x[0] for x in tmp_id])
    xtimes=[0 for i in range(10)]
    for le in top_3:
        for nid in le:
            xtimes[nid]+=1
    xtsum=sum(xtimes)
    xper=(np.array(xtimes)/xtsum)
    xper=[round(xp,2) for xp in xper]
    print(xper)
    print(NODE_ID)
    print(BLOCK_ID)

NODE_ID=[36168 ,14987 ,64837 ,14867 , 2348, 46855,  6335, 39719, 59885 ,11132]
BLOCK_ID=[14927, 60005, 50853, 50561 ,  434 ,52693, 26039 ,29320 ,57903 ,63559 ,34287 , 4859,
 43758 ,36160 ,54874, 55817 ,36359 ,16828 , 6253  , 438 ,29003, 35806 , 3204, 46628,
 20825  ,8464 ,19967 ,47377, 34195, 29356 ,40653 ,26477 ,16444, 22959, 43538 ,64447,
 54841, 16460, 57070, 64532, 25389,  2283  , 951 ,12764  ,1946, 32882, 62371 , 5413,
  3468 ,39375 ,52292 ,15594 , 8300 ,24973, 63779, 22173, 10192, 62634, 29129, 52106,
 42265 ,39634, 48699 ,37057 ,41466 ,46239,  7415, 32633, 14855 ,16124, 44662, 50380,
 44849 ,  783 ,50048 , 2971 ,57962 ,53133, 50530,   781, 22039 ,32578,  6252,  5381,
 40255 , 9448 ,60071 ,19632 ,37333 ,42086,  4662, 28351,  8623 ,38266, 26987, 44467,
 15689, 25408, 55413 , 6389 ,14349 ,43447, 65181, 34288, 58872 ,32139, 55211, 51399,
 62673, 63585, 43092 ,17828 ,27107, 51707,  9455, 50633, 59921 ,59325,  3615, 55242,
 36483, 62319 ,46487 ,24825 ,13092 ,33536, 14654, 39970, 44800 ,25139, 35799, 35764,
 42235, 13595, 47883 ,42993, 61195 ,10334, 52501, 23080, 57778 ,24817, 20067, 37560,
 15894, 37703, 36289 , 9487, 63484 ,34574, 12370, 33110, 58887 , 2276, 33741, 20375,
 22726, 36109, 58431 ,36966, 30027 ,34188, 16558, 30771, 58971 ,42169, 53660, 21764,
 23531, 13822, 58818 ,15049 ,12563 , 3820, 33149, 57798, 46256 ,30308, 42020, 32059,
 33004, 56094 ,56407 ,46144 ,57263 ,36546, 15190, 17303, 12507 ,63296, 35922, 18608,
 41818 , 1479 , 5893 ,16109 ,42856 ,26418, 21862, 17204, 32274 ,50079,  8234,  8605,
 63437, 20492, 27405 ,35648, 64862 ,22610,  6666, 14966, 24610 ,12878, 33442, 62841,
 59333,  5337, 37413 ,32124, 18093 ,23439, 27683, 48056, 45186 ,46963, 17851, 63374,
 50480 , 1955 ,45356 ,58332 ,46071 ,48657, 39094, 40361, 55781 ,56155, 27514, 40647,
  1046 ,51459,  2604 ,46114 ,45175 ,35116, 59402, 26657, 39053 , 5623, 24097, 31868,
  4119, 62466 ,42212 ,25000 ,33622 ,55696,  5160, 37720,   147 ,28285, 33471, 16240,
 42617, 17779, 24888 ,51771 ,61572 ,47544, 52212, 61810, 26336 ,45735, 48266,  1576,
 52963 ,25860 ,20827 ,23218, 28798 ,47222, 23228, 38965, 51772 ,50415, 11167, 32681,
 18081, 12116, 13353, 14196, 31682 ,  776, 45076, 22987, 49925 ,40410, 20870, 23548,
 32180 ,30753 ,42328 , 6814 ,35225 ,16858, 50535, 54141, 65059 ,15678, 55682,  7293,
  7181, 35552 , 7233 , 6606 ,  390 ,25001, 61445, 65372, 49745 ,37825, 34298 ,56730,
 53651 ,62380 ,62600 ,35304 ,31748 , 9509, 50715, 50241,  6816 ,13997, 50591 , 8681,
 61068, 34923, 25935 , 8125, 12573 ,20240, 45594,  4086, 60415 ,61382, 49239 ,62761,
 22975 ,34590 ,20619 ,29072, 12810 ,34023, 40054, 64316, 17066 ,24013,  2041 ,64611,
 27444 ,51126, 11478 ,58789 ,65446 ,49131 ,55792, 31036, 55606 ,47583, 19049 , 7933,
  7470 ,58520 ,12863 ,33915 ,57964 , 6611 ,45210, 14410, 52050 ,25128, 21451, 15334,
 45427 ,  890 ,21982 ,46986, 24613 ,50217 ,40303, 50972, 42185 ,54447, 45888,   926,
 45890 , 2637 ,12202, 30257]

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

maxcost=2.28277831

def duijiaoxian_0():
    global communication_cost
    for i in range(len(communication_cost)):
        communication_cost[i][i]=0

def calavgcmm():
    global communication_cost
    #因为是服务节点的开销，所以计算的是别人到i的开销的平均值
    avg_comm=np.mean(communication_cost,axis=0)
    print(json.dumps(avg_comm.tolist()))

avg_comm=[1.076801667, 0.8593266470000002, 0.946050746, 0.89489131, 0.9736247579999999, 1.0768540449999997, 1.1330439550000002, 0.762741658, 0.9888054660000002, 1.001343573]
avgcomm=[1.08, 0.86, 0.95, 0.89, 0.97, 1.08, 1.13, 0.76, 0.99, 1.0]
xper=[0.1, 0.11, 0.08, 0.11, 0.08, 0.12, 0.08, 0.11, 0.08, 0.13]

granularity=100# granularity of time
epoch_interval=600
probability=[0]*granularity
happend_times=2*lambdai+int(1/2*lambdai)
one_interval=epoch_interval/happend_times# get a approximate time range for time increasment list.
one_step=one_interval/granularity

plt.bar(range(0,10),np.array(xper)*10,color='black',label='10*xper')
plt.bar(range(0,10),np.array(avgcomm),color='pink',label='avgcomm')
plt.show()