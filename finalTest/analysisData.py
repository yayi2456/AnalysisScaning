import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import numpy as np

def load_avg_times(chosen_block_distribution,piece,passive_item,active_item,expel_item,total_times):
    # file_average_time='D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\averageTime-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'
    file_average_time='D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\A-'+chosen_block_distribution+'-'+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.txt'
    
    avg_time=[]
    with open(file_average_time, 'r') as datafile:
        i=0
        for dataline in datafile:
            if i ==0:
                datalineitem = dataline.split()
                # print(0,'-',datalineitem)
                begin=int(datalineitem[0])
                ends = int(datalineitem[1])
                step = int(datalineitem[2])
            elif i==1:
                avg_time=json.loads(dataline)
            i+=1
        # print(AvgTime)
    return avg_time,begin,ends,step

def plot_avg():
    avg_time=[] 
    # period_s=[0,1,2,3,4,5,6,7,np.inf]
    # for i in period_s:
    #     avgtime, b01, e01, s01 = load_avg_times(chosen_block_distribution,passive_replicate_type,passive_on,active_replicate_type,active_on,i,lambdai,top_num_to_offload)
    #     avg_time.append(avgtime)
    # avgtime,_,_,_=load_avg_times(chosen_block_distribution,passive_replicate_type,passive_on,active_replicate_type,active_on,np.inf,lambdai,top_num_to_offload)
    # avg_time.append(avgtime)
    distribution='zipf'
    replica_sum=3
    passive_item='load4'
    active_item='calculate3'
    expel_item='llu4'
    run_times=100
    # Avgtime01, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'llu2',run_times)
    # Avgtime02, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'llu3',run_times)
    # Avgtime03, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'llu4',run_times)
    Avgtime04, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'llu4',run_times)
    # Avgtime04r, b02, e02, s02 = load_avg_times('zipfr',replica_sum,passive_item,active_item,'llu5',run_times)
    # Avgtime04n, b01, e01, s01 = load_avg_times(distribution,replica_sum,'nopassive','noactive','noexpel',run_times)
    # Avgtime04rn, b02, e02, s02 = load_avg_times('zipfr',replica_sum,'nopassive','noactive','noexpel',run_times)
    # Avgtime05, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'llu6',run_times)

    # Avgtime011, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve1',run_times)
    # Avgtime022, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve2',run_times)
    # Avgtime033, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve3',run_times)
    # Avgtime033r, b02, e02, s02 = load_avg_times('zipfr',replica_sum,passive_item,active_item,'curve3',run_times)
    # Avgtime044, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve4',run_times)
    # Avgtime055, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve5',run_times)
    # Avgtime066, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve6',run_times)
    # Avgtime077, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve7',run_times)
    # Avgtime05, b02, e02, s02 = load_avg_times(distribution,5,'nopassive','noactive','noexpel',run_times)
    # Avgtime06, b02, e02, s02 = load_avg_times(distribution,6,'nopassive','noactive','noexpel',run_times)
    # Avgtime07, b02, e02, s02 = load_avg_times(distribution,7,'nopassive','noactive','noexpel',run_times)
    
    # Avgtime1inf, b14, e14, s14 = load_avg_times('nipopows','2^n','1','popularity',4,'calculate',3,'no',1,3,100)
    # Avgtime22, b22, e22, s22 = loadavgtimes(2, 2, 100)
    # Avgtime_12,b_12,e_12,s_12=loadavgtimes(-1,2,100)
    # Avgtime_11,b_11,e_11,s_11=loadavgtimes(-1,1,100)
    # Avgtime11,_,_,_=loadavgtimes(1,1,100)
    # Avgtime21,_,_,_=loadavgtimes(2,1,100)
    # Avgtime10,_,_,_=loadavgtimes(1,0,100)
    # Avgtime20,_,_,_=loadavgtimes(2,0,100)
    # Avgtime_10All,_,_,_=loadavgtimes(-1,0,100)
    # if b01 != b01 or e01 != e02 or s01 != s02:
    #     exit(-1)
    # if b12 != b22 or e12 != e22 or s12 != s22:
    #     exit(-1)
    # if b01 != b12 or e01 != e12 or s01 != s12:
    #     exit(-1)
    # if b12!=b_12 or e12!=e_12 or s12!=s_12:
    #     exit(-1)
    colors = ['blue', 'red', 'green', 'skyblue', 'pink', 'yellow', 'purple', 'black', 'cyan', 'orange']
    
    # for i in range(len(period_s)):
    #     plt.plot(range(b01, e01, s01), avg_time[i], color=colors[i], label=str(period_s[i]))
    # plt.plot(range(b01, e01, s01), Avgtime01, color=colors[0], label='nipopows')
    # plt.plot(range(b02, e02, s02), Avgtime01, color=colors[0], label='2')
    # plt.plot(range(b02, e02, s02), Avgtime02, color=colors[1], label='3')
    # plt.plot(range(b02, e02, s02), Avgtime03, color=colors[2], label='4')
    plt.plot(range(b02, e02, s02), Avgtime04, color=colors[3], label='4',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04r, color=colors[2], label='5r',marker='.')
    # plt.plot(range(b01, e01, s01), Avgtime04n, color=colors[0], label='3n',marker='.')
    # plt.plot(range(b01, e01, s01), Avgtime04rn, color=colors[1], label='3rn',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime05, color=colors[4], label='6')

    # plt.plot(range(b02, e02, s02), Avgtime011, color=colors[5], label='11')
    # plt.plot(range(b02, e02, s02), Avgtime022, color=colors[6], label='22')
    # plt.plot(range(b02, e02, s02), Avgtime033, color=colors[7], label='33',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime033r, color=colors[8], label='33r',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime044, color=colors[8], label='44')
    # plt.plot(range(b02, e02, s02), Avgtime055, color=colors[9], label='55')
    # plt.plot(range(b02, e02, s02), Avgtime066, color=colors[1], label='66')
    # plt.plot(range(b02, e02, s02), Avgtime077, color=colors[2], label='77')
    
    plt.legend()
    plt.xlabel('blocks')
    plt.ylabel('avg time')
    # plt.ylim(ymin=0,ymax=5)
    plt.show()

def load_storage(chosen_block_distribution,piece,passive_item,active_item,expel_item,total_times):
    file_storage_used='D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\S-'+chosen_block_distribution+'-'+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'.txt'
    NodesSizeAll =[] 
    BlockSize=[]
    with open(file_storage_used, 'r') as datafile:
        i = 0
        for dataline in datafile:
            if i == 0:
                datalineitem = dataline.split()
                begin = int(datalineitem[0])
                ends = int(datalineitem[1])
                step = int(datalineitem[2])
            elif i ==1:
                BlockSize=json.loads(dataline)
                NodesSizeAll=np.array([.0]*len(BlockSize))
            elif i>=2:
                NodesSize=np.array(json.loads(dataline))
                NodesSizeAll+=NodesSize
            i += 1
        # print('filename=', file_storage_used, '-------')
        # print(NodesSizeAll)
        NodesSizeAll=NodesSizeAll/10
        # print('filename=',file_storage_used,'-------')
        # print(NodesSizeAll)
    return BlockSize,NodesSizeAll, begin, ends, step

def plot_storage():
    distribution='zipf'
    replica_sum=3
    passive_item='load4'
    active_item='calculate3'
    expel_item='llu5'
    run_times=10
    
    # Blocksize01,NodeSize02, b01, e01, s01 = load_storage(distribution,replica_sum,passive_item,active_item,'llu2',run_times)
    # Blocksize01,NodeSize03, b01, e01, s01 = load_storage(distribution,replica_sum,passive_item,active_item,'llu3',run_times)
    Blocksize01,NodeSize04, b01, e01, s01 = load_storage(distribution,replica_sum,passive_item,active_item,'llu4',run_times)
    Blocksize01,NodeSize05, b01, e01, s01 = load_storage(distribution,replica_sum,passive_item,active_item,'llu5',run_times)
    # Blocksize01,NodeSize05r, b01, e01, s01 = load_storage('zipfr',replica_sum,passive_item,active_item,'llu5',run_times)
    # Blocksize01,NodeSize06, b01, e01, s01 = load_storage(distribution,replica_sum,passive_item,active_item,'llu6',run_times)

    # Blocksize01,NodeSize011, b01, e01, s01 = load_storage(distribution,replica_sum,passive_item,active_item,'curve1',run_times)
    # Blocksize01,NodeSize022, b01, e01, s01 = load_storage(distribution,replica_sum,passive_item,active_item,'curve2',run_times)
    Blocksize01,NodeSize033, b01, e01, s01 = load_storage(distribution,replica_sum,passive_item,active_item,'curve3',run_times)
    # Blocksize01,NodeSize033r, b01, e01, s01 = load_storage('zipfr',replica_sum,passive_item,active_item,'curve3',run_times)
    # Blocksize01,NodeSize044, b01, e01, s01 = load_storage(distribution,replica_sum,passive_item,active_item,'curve4',run_times)
    # Blocksize01,NodeSize055, b01, e01, s01 = load_storage(distribution,replica_sum,passive_item,active_item,'curve5',run_times)
    # Blocksize01,NodeSize066, b01, e01, s01 = load_storage(distribution,replica_sum,passive_item,active_item,'curve6',run_times)
    # Blocksize01,NodeSize077, b01, e01, s01 = load_storage(distribution,replica_sum,passive_item,active_item,'curve7',run_times)

    # Blocksize02,NodeSize02, b02, e02, s02 = loadstorage(0, 2)
    # Blocksize12,NodeSize12, b12, e12, s12 = loadstorage(1, 2)
    # Blocksize22,NodeSize22, b22, e22, s22 = loadstorage(2, 2)
    # print(NodeSize01)
    # print('-----')
    # print(NodeSize02)
    # print('-----')
    # print(NodeSize12)
    # print('-----')
    # print(NodeSize22)
    # print('-----')
    # if b01 != b01 or e01 != e02 or s01 != s02:
    #     exit(-1)
    # if b12 != b22 or e12 != e22 or s12 != s22:
    #     exit(-1)
    # if b01 != b12 or e01 != e12 or s01 != s12:
    #     exit(-1)
    colors = ['blue', 'red', 'green', 'skyblue', 'pink', 'yellow', 'purple', 'black', 'cyan', 'orange','gold']
    # plt.plot(range(b01, e01, s01),np.array(NodeSize02)/np.array(Blocksize01),color=colors[0],label='llu-2')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize03)/np.array(Blocksize01),color=colors[1],label='llu-3')
    plt.plot(range(b01, e01, s01),np.array(NodeSize04)/np.array(Blocksize01),color=colors[2],label='4')
    plt.plot(range(b01, e01, s01),np.array(NodeSize05)/np.array(Blocksize01),color=colors[3],label='5')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize05r)/np.array(Blocksize01),color=colors[4],label='5r')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize06)/np.array(Blocksize01),color=colors[4],label='6')

    # plt.plot(range(b01, e01, s01),np.array(NodeSize011)/np.array(Blocksize01),color=colors[5],label='curve-11')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize022)/np.array(Blocksize01),color=colors[6],label='22')
    plt.plot(range(b01, e01, s01),np.array(NodeSize033)/np.array(Blocksize01),color=colors[7],label='33')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize033r)/np.array(Blocksize01),color=colors[8],label='33r')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize044)/np.array(Blocksize01),color=colors[8],label='44')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize055)/np.array(Blocksize01),color=colors[9],label='55')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize066)/np.array(Blocksize01),color=colors[1],label='66')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize077)/np.array(Blocksize01),color=colors[0],label='77')
    # plt.plot(range(b01, e01, s01), NodeSize01, color=colors[0], label='01')
    # plt.plot(range(b01, e01, s01), NodeSize02, color=colors[1], label='02')
    # plt.plot(range(b01, e01, s01), NodeSize12, color=colors[2], label='12')
    # plt.plot(range(b01, e01, s01), NodeSize22, color=colors[3], label='22')
    plt.legend()
    # plt.ylim(ymin=0.2,ymax=.5)
    plt.xlabel('blocks')
    plt.ylabel('per node storage size/total size')
    plt.show()

def load_use_ratio(chosen_block_distribution,passive_replicate_type,passive_on,active_replicate_type,active_on,period,lambdai,top_num_to_offload):
    """

    """
    begin=0
    ends=0
    step=0
    # index0=block, index1= epoch
    use_ratio_of_each_block=[]

    file_use_ratio='D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\useRatio-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'

    with open(file_use_ratio, 'r') as datafile:
        i=0
        for dataline in datafile:
            if i ==0:
                datalineitem = dataline.split()
                # print(0,'-',datalineitem)
                begin=int(datalineitem[0])
                ends = int(datalineitem[1])
                step = int(datalineitem[2])
            elif i>=1:
                use_ration_block=json.loads(dataline)
                use_ratio_of_each_block.append(use_ration_block)
            i+=1
    return use_ratio_of_each_block,begin,ends,step

def plot_use_ratio():
    """
    """
    chosen_block_distribution = 'nipopows'
    passive_replicate_type='popularity'
    active_replicate_type='calculate'
    passive_on=True
    active_on=True
    period=6
    lambdai=4
    top_num_to_offload=3
    begin_static=200
    
    use_ratio01,b01,e01,s01=load_use_ratio(chosen_block_distribution,passive_replicate_type,passive_on,active_replicate_type,active_on,period,lambdai,top_num_to_offload)
    #debug
    # print(np.max(use_ratio01))
    # lengthof=len([1 for i in range(b01,e01,s01)])
    # print(np.argmax(use_ratio01)/lengthof)
    # print(np.argmax(use_ratio01)%lengthof)
    # modify
    # for i in range(len(use_ratio01)):
    #     for j in range(len(use_ratio01[i])):
    #         if use_ratio01[i][j]>=1:
    #             use_ratio01[i][j]=1

    fig = plt.figure()
    ax3=plt.axes(projection='3d')
    # ax = Axes3D(fig)
    # for i in range(len(use_ratio01)):
    #     ax.scatter([i+b01-begin_static for j in range(b01,e01,s01)], [j for j in range(b01,e01,s01)], use_ratio01[i])
    x=range(b01-begin_static,e01)
    y=range(b01,e01,s01)
    X,Y=np.meshgrid(y,x)
    print(np.shape(X),',',np.shape(Y),',',np.shape(use_ratio01))
    ax3.plot_surface(X,Y,np.array(use_ratio01),cmap='rainbow')
    # plt.plot(range(b01,e01,s01),use_ratio01[2225-b01])
    plt.xlabel('epoches')
    plt.ylabel('blocks')
    plt.show()




if __name__=='__main__':
    # plot_avg()
    # plot_storage()
    # plt.plot(range(begin+beginblock,end),RR[beginblock:],color='r',marker='.',label='needed-actual')
    # plt.bar(range(begin+beginblock,end),LL[beginblock:],color='grey',label='levels')
    # plt.plot(range(begin+beginblock,end),RN[beginblock:],label='needed',color='g')
    # plt.plot(range(begin+beginblock, end), RA[beginblock:], label='actual', color='b')
    # plt.axhline(y=0, color='grey')
    # plt.legend()
    # plt.title("REPLICANUMS: NEEDED-ACTUAL(lambdai="+str(lambdai))
    # plt.xlabel('numbers')
    # plt.ylabel('replicas\' amounts differences')
    # plt.show()
    # A=
# get_needed_blocks(0,100,'zipf',10,[])
    A=[0.0011049223105278451, 0.0011183288002366133, 0.0011320365577191767, 0.0011460555318899353, 0.0011603961073781482, 0.0011750691284024557, 0.001190085924221757, 0.0012054583362846182, 0.0012211987472102793, 0.0012373201117463367, 0.0012538359898614062, 0.0012707605821456784, 0.0012881087677084028, 0.0013058961447791801, 0.0013241390742396834, 0.0013428547263343263, 0.0013620611308326743, 0.0013817772309433823, 0.0014020229413094648, 0.001422819210448112, 0.001444188088035565, 0.0014661527974791685, 0.0014887378142652689, 0.0015119689506237213, 0.0015358734471082015, 0.0015604800717571102, 0.001585819227573616, 0.001611923069146468, 0.0016388256293268962, 0.001666562956982791, 0.0016951732669711313, 0.001724697103605426, 0.001755177519049127, 0.001786660268241332, 0.001819194022160996, 0.001852830601464057, 0.0018876252327889428, 0.001923636830325165, 0.0019609283055834164, 0.001999566908701227, 0.0020396246050746287, 0.002081178491633946, 0.0021243112576933855, 0.002169111696014439, 0.002215675270550476, 0.002264104748305787, 0.0023145109038731626, 0.0023670133065415233, 0.00242174120142787, 0.0024788344979329883, 0.0025384448810057175, 0.0026007370632970487, 0.0026658901993804832, 0.0027340994869173166, 0.002805577984089776, 0.0028805586779797527, 0.0029592968450478005, 0.003042072752732842, 0.003129194760785788, 0.0032210028927005738, 0.003317872962065533, 0.003420221356536792, 0.003528510604353633, 0.003643255876072963, 0.0037650326090695723, 0.0038944854864093755, 0.004032339057719019, 0.004179410361353551, 0.004336623999511108, 0.004505030237781586, 0.004685826857321405, 0.004880385694428149, 0.005090285076977883, 0.005317349735803605, 0.005563700268617474, 0.005831814918123824, 0.006124607373262158, 0.006445525630279646, 0.006798678835708647, 0.007189001748359949, 0.007622470427227634, 0.008106388653621226, 0.008649773529096825, 0.009263882484784262, 0.009962945708958145, 0.010765203205612047, 0.011694404188780901, 0.01278202669251491, 0.014070652829337903, 0.015619262389463363, 0.017511838481539862, 0.019871961247940842, 0.022888838693609977, 0.026866685708646112, 0.03232587151758965, 0.04023164011343723, 0.05258474271028453, 0.07426535087220147, 0.12080801489849234, 0.27754393596871085]
    B=list(range(0,100))
    plt.plot(B,A,marker='.')
    plt.show()