#随着不参与共识的节点数目的变化，系统中请求延迟的变化；
#共识节点的加入，调整分片的存储位置，系统中请求延迟的变化
#0.64(100Mbps) or 6.4 us(10Mbps)的传输时延，根据这个传输时延看卡能不能搞到排队时延
#传播时延我会找RTT
#ping baidu.com 17ms 10ms 13ms √
#ping github.com 105ms 
#ping  bt.nankai.edu.cn 10ms 13ms 16ms √
#ping ieeexplore.ieee.org 111ms 72ms 108ms
#ping blog.csdn.net 15ms √
#ping bilibili.com 25ms 11ms 14ms √

# final: u=15ms sigma=2ms
import numpy as np
import sys
import math

#总节点数目
NODES_NUM=256
#存储通信开销
CMM_COST=[]
#consensus节点数目，可通过参数更改
REPLICA_NUMS=16
#共识节点id
REPLICA_NODES=range(REPLICA_NUMS)
#存储哪个分片在哪里，行id对应分片，列id对应存储位置
REPLICAS_LOCATION=[]
#有效slot编号
K=[]
#有效slot长度
K_length=2
#一个epoch时长，通过set_EPOCH_INTERVAL调整
EPOCH_INTERVAL=57.84
#延迟时长，单位ms
PROCESS_TIME=.0064
#请求延迟
mu=15
sigma=2


def set_EPOCH_INTERVAL(k):
    '''
    k：即作为参数输入的K_length

    使用该函数完成不同k的EPOCH_INTERVAL设置
    '''
    global EPOCH_INTERVAL
    if k==16:
        EPOCH_INTERVAL=75.79
    if k==32:
        EPOCH_INTERVAL=102.72
    if k==64:
        EPOCH_INTERVAL=144.0
    if k==128:
        EPOCH_INTERVAL=237.36
    if k==256:
        EPOCH_INTERVAL=435.83



def generate_CMM_COST(distribution_type):
    """(int,str) -> list of list of float

    Return communication cost between every 2 nodes generated randomly in normal distribution.

    2 types are allowed:
    'normal'/'1'
    """
    global CMM_COST
    # generate communication cost randomly
    try:
        # normal distribution
        if distribution_type=='normal':
            CMM_COST=np.absolute(np.random.normal(mu,sigma,[NODES_NUM,NODES_NUM]))
        # each pair of nodes communicate at 1 cost
        elif distribution_type=='1':
            CMM_COST=np.absolute(np.random.normal(1,1,[NODES_NUM,NODES_NUM]))
        else:
            sys.exit(-2)
    except:
        print('INVALID DISTRIBUTION TYPE! must be \'normal\' or \'1\'. distribution_type=\'1\' set.')
        CMM_COST=np.absolute(np.random.normal(1,1,[NODES_NUM,NODES_NUM]))
    # nodes have no communication cost with itself
    for i in range(NODES_NUM):
        CMM_COST[i][i]=0

def init_location():
    '''
    使用均匀分布，选择初始化每个副本存在的位置，即随机初始化RELICA_LOCATION list
    '''
    global REPLICAS_LOCATION
    REPLICAS_LOCATION=np.trunc(np.random.uniform(0,len(REPLICA_NODES),[NODES_NUM,REPLICA_NUMS]))

    # for i in range(NODES_NUM):
    #     for j in range(REPLICA_NUMS):
    #         x=int(REPLICAS_LOCATION[i][j])
    #         thisnodeid=REPLICA_NODES[x]
    #         REPLICAS_LOCATION[i][j]=thisnodeid

def init_K():
    '''
    初始化K数组，使用均匀分布
    '''
    global K
    K=np.trunc(np.random.uniform(0,NODES_NUM,K_length))
    

def get_issue_nodes(my_id):
    '''
    my_id：显出请求的节点的id

    return：节点my_id请求的各个节点id
    '''
    node_issue=[]
    # print(len(K))
    for i in range(len(K)):
        min_value=0xFFFFFFFF
        min_node=-1
        for j in range(len(REPLICAS_LOCATION[int(K[i])])):
            x=int(REPLICAS_LOCATION[i][j])
            if(CMM_COST[my_id][x]<min_value):
                min_node=REPLICAS_LOCATION[i][j]
                min_value=CMM_COST[my_id][x]
        if min_node==-1:
            print("MIN_NODE==-1！")
        node_issue.append(min_node)
        # print('hhh',min_value,',',node_issue)
    return node_issue

def request():
    '''
    获得每一个节点的请求位置，返回一个int的list的list
    '''
    nodes_issues=[]
    for i in range(NODES_NUM):
        node_issue=get_issue_nodes(i)
        nodes_issues.append(node_issue)
        # print(node_issue)
        # for j in range(len(K)):
        #     x=int(node_issue[j])
        #     avg_time+=CMM_COST[i][x]
    # print(len(K))
    # print(NODES_NUM)
    # avg_time/=(len(K)*NODES_NUM)
    return nodes_issues

# def multi_request(is_replica,max_range):
#     total_avg_time=[]
#     generate_CMM_COST('normal')
#     init_K()
#     init_location()
#     start_num=NODES_NUM
#     for i in range(max_range-start_num):
#         total_avg_time.append(request())
#         # add_one_node(is_replica)
#     return total_avg_time

def generate_time_increasment_list():
    '''
    使用泊松分布，生成请求时间间隔。
    每一个节点生成一个数值，返回一个double的list
    '''
    global NODES_NUM
    global EPOCH_INTERVAL
    granularity=NODES_NUM# granularity of time
    probability=[0]*granularity
    happend_times=NODES_NUM#2*lambdai+int(1/2*lambdai)
    one_interval=EPOCH_INTERVAL/happend_times# get a approximate time range for time increasment list.
    one_step=one_interval/granularity
    this_point=0
    next_point=this_point+one_step
    this_lambdai=NODES_NUM/EPOCH_INTERVAL
    for i in range(granularity-1):
        probability[i]=math.exp(-this_lambdai*this_point)-math.exp(-this_lambdai*next_point)
        this_point=next_point
        next_point+=one_step
    probability[granularity-1]=math.exp(-this_lambdai*this_point)
    # choose time interval list
    # interval_lists=[]
    choose_range=[]
    start=0
    for i in range(granularity):
        choose_range.append(start)
        start=round(start+one_step,2)
    # debug
    # print(probability)
    # print(np.sum(probability,axis=1))
    # end
    interval_lists=(np.random.choice(choose_range,size=NODES_NUM,replace=True,p=probability))
    return interval_lists

def request_by_arriving_requests(interval_list,nodes_issues):
    '''
    interval_list：生成的时间间隔数组
    nodes_issues：各个节点请求的节点id的list，是一个int的list的list
    return：返回平均请求时间
    '''
    global NODES_NUM
    global REPLICA_NUMS
    requests_list=[]
    #get the happend time from increasment time list for each node.
    # fill in each request: [from_node,to_node,request_block,request_time,time_cost]
    time_cost_1=PROCESS_TIME
    for _nid in range(len(interval_list)):
        happend_time=0
        happend_time+=interval_list[_nid]
        for _iid in range(len(nodes_issues[_nid])):
            to_node=(int)(nodes_issues[_nid][_iid])
            # print(_nid," ",to_node)
            time_cost_2=CMM_COST[_nid][to_node]
            requests_list.append([_nid,int(to_node),float(happend_time),time_cost_1,time_cost_2])
    # sort the request according to the happend time
    requests_list=sorted(requests_list,key=lambda x:x[2])
    # get the respond time for each request.   
    # request...
    nodes_service_queue=[0 for i in range(REPLICA_NUMS)]
    # # for communication update
    # storage_per_node=[[0 for i in range(node_num)] for j in range(node_num)]#storage_per_node[from_nde][to_node]
    # request_time_per_node=[[0 for i in range(node_num)] for j in range(node_num)]
    # # for passive replicate : passive_type
    # passive_type_blocks=[{} for i in range(node_num)]
    # # for passive replicate: load
    # load_of_blocks=[{} for i in range(node_num)]# real_time_cost of [from_node][get_blk], it is a list of dict
    # # for passive replicate: popularity 
    # popularity_of_blocks=[{} for i in range(node_num)]
    # for metrics record
    total_time_cost=0#[0]*10# stored by to_node
    total_access_times=0#[0]*10
    # delayed_request=0
    # delayed_time_per_request=0
    #record queue#
    # print(requests_list)
    # if fwrite:
    #     print(json.dumps(requests_list),file=fwrite)
    ##end##
    for i in range(len(requests_list)):
        from_node=requests_list[i][0]
        to_node=requests_list[i][1]
        happen_time=requests_list[i][2]
        time_cost_1=requests_list[i][3]
        time_cost_2=requests_list[i][4]
        real_time_cost=time_cost_1+time_cost_2
        if nodes_service_queue[to_node]>happen_time:
            real_time_cost+=(nodes_service_queue[to_node]-happen_time)
            nodes_service_queue[to_node]+=time_cost_1
            # delayed_request+=1
            # delayed_time_per_request+=(nodes_service_queue[to_node]-happen_time)
        else:
            nodes_service_queue[to_node]=happen_time+time_cost_1
        total_access_times+=1
        total_time_cost+=real_time_cost
        # storage_per_node[from_node][to_node]+=dsrpal.blocksizes[get_blk-beginID]
        # request_time_per_node[from_node][to_node]+=real_time_cost
        
    # average_time=np.sum(np.array(total_time_cost))/np.sum(np.array(total_access_times))
    average_time=total_time_cost/total_access_times
    #debug
    # print('delayed reuqest/total requests:',delayed_request,',',np.sum(np.array(total_access_times)),',ratio:',round(delayed_request/np.sum(np.array(total_access_times))*100,4))
    #end
    # total_access_times_scalar=np.sum(np.array(total_access_times))
    return average_time
    #,storage_per_node,request_time_per_node,passive_type_blocks,round(delayed_request/total_access_times_scalar*100,4),round(delayed_time_per_request/total_access_times_scalar,6)


def init_env():
    '''
    解析命令行参数，初始化各个环境
    '''
    global K_length
    global REPLICA_NUMS
    global REPLICA_NODES
    global NODES_NUM
    K_length=int(sys.argv[1])
    REPLICA_NUMS=int(sys.argv[2])
    REPLICA_NODES=range(REPLICA_NUMS)
    NODES_NUM=int(sys.argv[3])
    generate_CMM_COST('normal')
    init_K()
    init_location()
    set_EPOCH_INTERVAL(K_length)

if __name__=='__main__':
    init_env()
    n=NODES_NUM
    nodes_issues=request()
    time_intervals=generate_time_increasment_list()
    request_time=request_by_arriving_requests(time_intervals,nodes_issues)
    print(request_time)


