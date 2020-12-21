import json
import matplotlib.pyplot as plot

def get_requests_list(fname):
    requests_list=[]
    with open(fname,'r')as din:
        for dline in din:
            requests_list=json.loads(dline)
    return requests_list

def get_to_node_queue(reuqests_list):
    to_node_serve_queue=[]
    for i in range(10):
        to_node_serve_queue.append([])#each element: [start time,end time],sorted by start time
    for requests in reuqests_list:
        from_node=requests[0]
        to_node=requests[1]
        get_blk=requests[2]
        happen_time=requests[3]
        time_cost=requests[4]
        last_end_time=0
        if len(to_node_serve_queue[to_node])==0:
            last_end_time=happen_time+time_cost
        else:
            last_end_time=to_node_serve_queue[to_node][len(to_node_serve_queue[to_node])-1][1]
        if last_end_time>happen_time:
            real_end_time=last_end_time+time_cost
        else:
            real_end_time=happen_time+time_cost
        to_node_serve_queue[to_node].append([happen_time,real_end_time])
    return to_node_serve_queue

if __name__=='__main__':
    fnames=[]
    prefix_file='./finalTest/finalRes/request/REQ-'
    fnames.append(prefix_file+'zipf-3-popularity150-noactive-curve3-1'+'.txt')
    requests_list=get_requests_list(fnames[0])
    to_node_serve_queue=get_to_node_queue(requests_list)
    #
    str_p=''
    for i in range(10):
        str_p+=str(len(to_node_serve_queue[i]))+','
    print(str_p)
    # for i in range(10):
    #     print('node:',i,',',to_node_serve_queue[i],'\n')