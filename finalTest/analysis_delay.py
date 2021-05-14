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

def each_node_delay_percentile(to_node_serve_queue):
    total_requests=[len(to_node_serve_queue[i])for i in range(len(to_node_serve_queue))]
    serve_time_queue=[]
    delay_requests=[0]*10
    for i in range(10):
        serve_time_queue.append(0)
    for _nid in range(len(to_node_serve_queue)):
        this_node_serve_queue=to_node_serve_queue[_nid]
        for request_time in this_node_serve_queue:
            if request_time[0]<serve_time_queue[_nid]:
                delay_requests[_nid]+=1
            serve_time_queue[_nid]=request_time[1]
    return total_requests,delay_requests

def print_delay_info():
    fnames=[]
    prefix_file='./finalTest/finalRes/request/REQ-'
    static_type=''
    # fnames.append(prefix_file+'zipf-3-popularity160-noactive-curve3-1'+'.txt')
    passive_='popularity'
    passive_num=[10,20,40,60,95,96,97,100,150,155,160,200]#'kad95','kad96','kad97','kad100','kad150','kad160','kad200']
    passive_type=[passive_+str(pn) for pn in passive_num]
    active_type='calculate3'
    for ptype in passive_type:
        fnames.append(prefix_file+'zipf-'+static_type+'3-'+ptype+'-'+active_type+'-curve3-15'+'.txt')
    for fname_i in fnames:
        print(fname_i[len(prefix_file):])
        requests_list=get_requests_list(fname_i)
        to_node_serve_queue=get_to_node_queue(requests_list)
        total_requests,delay_requests=each_node_delay_percentile(to_node_serve_queue)
        
        print('total requests=\n',total_requests)
        print('delay percentile(delay requests/total requests)=\n',[round(delay_requests[i]/total_requests[i],4) for i in range(10)])
        print()

if __name__=='__main__':
    print_delay_info()
    
    #
    # str_p=''
    # for i in range(10):
    #     str_p+=str(len(to_node_serve_queue[i]))+','
    # print(str_p)
    # for i in range(10):
    #     print('node:',i,',',to_node_serve_queue[i],'\n')