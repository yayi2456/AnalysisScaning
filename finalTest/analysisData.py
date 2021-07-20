import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import numpy as np
import time
import os
import popularity_analysis

def load_avg_times(chosen_block_distribution,static_type,piece,passive_item,active_item,expel_item,total_times,timeup,encode_type):
    # file_average_time='D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\averageTime-'+chosen_block_distribution+'-'+passive_replicate_type+'.'+str(passive_on)+'-'+active_replicate_type+'.'+str(active_on)+'-'+str(period)+'-'+str(lambdai)+'-'+str(top_num_to_offload)+'.txt'
    if timeup!='inf':
        timeup=float(timeup)
    file_average_time='D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\A-CLIENT'+chosen_block_distribution+'-'+static_type+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'-'+str(timeup)+'-'+encode_type+'.txt'
    last_time=time.ctime(os.stat(file_average_time).st_mtime)
    print('file modify time: ',last_time,', file: ',file_average_time)
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
    static_type='piecekad'
    replica_sum=3
    passive_type='pop_kad'
    passive_items_su=['10','100','200','300']
    passive_items=[passive_type+x for x in passive_items_su]
    active_item=['kadvary3']#,'kadvary3']
    expel_item='curve3'
    timeup=float(2)
    run_times=[100,10,5,4]#[10]*len(passive_items)#[15,10,6,5]
    encode_type="encode4-2-9"#"noencode"#
    # run_times[0]=100
    Avg=[]
    b=0
    e=0
    s=0
    colors = ['blue', 'red', 'green', 'skyblue', 'pink', 'yellow', 'purple', 'black', 'cyan', 'orange','lime','grey']
    # Avg2050p,b,e,s=load_avg_times(distribution,replica_sum,passive_item,active_item,expel_item,run_times)
    # Avg2050l,b,e,s=load_avg_times(distribution,replica_sum,'load20',active_item,expel_item,run_times)
    # Avgp,b,e,s=load_avg_times(distribution,replica_sum,'popularity10',active_item,expel_item,100)
    # Avgl,b,e,s=load_avg_times(distribution,replica_sum,'load10',active_item,expel_item,100)
    # Avg3p,b,e,s=load_avg_times(distribution,replica_sum,'popularity30',active_item,expel_item,30)
    # Avg3l,b,e,s=load_avg_times(distribution,replica_sum,'load30',active_item,expel_item,30)
    # Avg4p,b,e,s=load_avg_times(distribution,replica_sum,'popularity40',active_item,expel_item,25)
    # Avg4l,b,e,s=load_avg_times(distribution,replica_sum,'load40',active_item,expel_item,25)
    # Avg5p,b,e,s=load_avg_times(distribution,replica_sum,'popularity50',active_item,expel_item,20)
    # Avg5l,b,e,s=load_avg_times(distribution,replica_sum,'load50',active_item,expel_item,20)
    # passive_items=['nopassive10','nopassive50','nopassive100','nopassive150','nopassive200','nopassive250','kad10','kad50','kad100','kad150','kad200','kad250']
    label_items=[]#'kad400-kadv3-0','kad400-kadv3-1','kad400-kadv3-inf']
    for i in range(len(passive_items)):
        for j in active_item:
            judgePassive=passive_items[i][4:7]
            if (judgePassive=='kad' and j[:3]=='kad') or (judgePassive!='kad' and j[:3]!='kad'):
            
                if judgePassive!='kad' and j[:3]!='kad':
                    timeup_t=np.inf
                else:
                    timeup_t=timeup
                avg_t,b,e,s=load_avg_times(distribution,static_type,replica_sum,passive_items[i],j,expel_item,run_times[i],timeup_t,encode_type)
                Avg.append(avg_t)
                label_items.append(static_type+'-'+passive_items[i]+'-'+j+'-'+expel_item+'-'+encode_type)

    ## timeup=2 vs timeup=1
    
    # avg_t,b,e,s=load_avg_times(distribution,static_type,replica_sum,'kad400','kadvary3',expel_item,1,'0')
    # avg_t=[np.mean(avg_t[b:b+10]) for b in range(0,len(avg_t),10)]
    # Avg.append(avg_t)
    # avg_t,b,e,s=load_avg_times(distribution,static_type,replica_sum,'kad400','kadvary3',expel_item,1,'1')
    # avg_t=[np.mean(avg_t[b:b+10]) for b in range(0,len(avg_t),10)]
    # Avg.append(avg_t)
    # avg_t,b,e,s=load_avg_times(distribution,static_type,replica_sum,'kad400','kadvary3',expel_item,1,'inf')
    # avg_t=[np.mean(avg_t[b:b+10]) for b in range(0,len(avg_t),10)]
    # Avg.append(avg_t)
    # label_items=['kad400-kadv3-0','kad400-kadv3-1','kad400-kadv3-inf']
    #kadn，n越小发现timeup的设置没什么太大区别，只要在一定时间内，可能因为资源非常充足，而副本个数设置区别很大，因为这个时候通信开销著主导位置
    #n越大发现副本个数区别不大，n会带来区别，可能是因为网络比较饱和，选择较为不忙碌的节点跟家重要，delay很大，等待时间占主导位置。
    
    b_x=0
    e_x=len(Avg[0])
    s=5
    xaxis=range(0,e_x,s)
    count=0
    # for i in range(len(passive_items)):
    #     for j in active_item:
    #         if (passive_items[i][:3]=='kad' and j[:3]=='kad') or (passive_items[i][:3]!='kad' and j[:3]!='kad'):
    #             plt.plot(range(b, e, s), Avg[count][::s], color=colors[count], label=passive_items[i]+'-'+j)
    #             count+=1
    #### timeup=2 vs timeup=1
    for avg in Avg:
        yaxis=avg[::s]
        plt.plot(xaxis, yaxis, color=colors[count], label=label_items[count])#passive_items[i]+'-'+j)
        count+=1
    # plt.plot(range(b, e, s), Avg2050p[::s], color=colors[0], label='20-p')#,marker='.')
    # plt.plot(range(b, e, s), Avg2050l[::s], color=colors[1], label='20-l')#,marker='.')
    # plt.plot(range(b, e, s), Avgp[::s], color=colors[2], label='10-p')#,marker='.')
    # plt.plot(range(b, e, s), Avgl[::s], color=colors[3], label='10-l')#,marker='.')
    # plt.plot(range(b, e, s), Avg3p[::s], color=colors[4], label='30-p')#,marker='.')
    # plt.plot(range(b, e, s), Avg3l[::s], color=colors[5], label='30-l')#,marker='.')
    # plt.plot(range(b, e, s), Avg4p[::s], color=colors[6], label='40-p')#,marker='.')
    # plt.plot(range(b, e, s), Avg4l[::s], color=colors[7], label='40-l')#,marker='.')
    # plt.plot(range(b, e, s), Avg5p[::s], color=colors[8], label='50-p')#,marker='.')
    # plt.plot(range(b, e, s), Avg5l[::s], color=colors[9], label='50-l')#,marker='.')
    ### uniform初始分配策略：修改distribution
    # Avgtime01, b02, e02, s02 = load_avg_times(distribution,1,passive_item,active_item,expel_item,run_times)
    # Avgtime02, b02, e02, s02 = load_avg_times(distribution,2,passive_item,active_item,expel_item,run_times)
    # Avgtime03, b02, e02, s02 = load_avg_times(distribution,3,passive_item,active_item,expel_item,run_times)
    # Avgtime04, b02, e02, s02 = load_avg_times(distribution,4,passive_item,active_item,expel_item,run_times)
    # Avgtime05, b02, e02, s02 = load_avg_times(distribution,5,passive_item,active_item,expel_item,run_times)
    # Avgtime06, b02, e02, s02 = load_avg_times(distribution,6,passive_item,active_item,expel_item,run_times)
    # Avgtime07, b02, e02, s02 = load_avg_times(distribution,7,passive_item,active_item,expel_item,run_times)
    # ###  uniform初始分配策略 plot
    # plt.plot(range(b02, e02, s02), Avgtime01, color=colors[0], label='1',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime02, color=colors[1], label='2',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime03, color=colors[2], label='3',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04, color=colors[3], label='4',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime05, color=colors[4], label='5',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime06, color=colors[5], label='6',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime07, color=colors[6], label='7',marker='.')
    ###uniform初始分配策略 done

    ### 驱逐策略
    ## ： 副本生命周期
    # Avgtime01, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve1',run_times)
    # Avgtime02, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve2',run_times)
    # Avgtime03, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve3',run_times)
    # Avgtime04, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve4',run_times)
    # Avgtime05, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve5',run_times)
    # Avgtime06, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve6',run_times)
    # Avgtime07, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'curve7',run_times)
    # ##： llu
    # # Avgtime0llu, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'llu8',run_times)
    # # # # ## 驱逐策略 plot
    # # # # # ： 副本生命周期
    # plt.plot(range(b02, e02, s02), Avgtime01, color=colors[0], label='1',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime02, color=colors[1], label='2',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime03, color=colors[2], label='3',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04, color=colors[3], label='4',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime05, color=colors[4], label='5',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime06, color=colors[5], label='6',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime07, color=colors[6], label='7',marker='.')
    # #：llu
    # plt.plot(range(b02, e02, s02), Avgtime0llu, color=colors[7], label='llu-8',marker='.')
    ### 驱逐策略done
    ### 驱逐策略done

    ### 被动的比较：修改distribution/curve
    # Avgtime04rn, b02, e02, s02 = load_avg_times(distribution,replica_sum,'random10','noactive',expel_item,run_times)
    # Avgtime04nn, b02, e02, s02 = load_avg_times(distribution,replica_sum,'nopassive','noactive',expel_item,run_times)
    # Avgtime04pn, b01, e01, s01 = load_avg_times(distribution,replica_sum,'popularity10','noactive',expel_item,run_times)
    # Avgtime04ln, b02, e02, s02 = load_avg_times(distribution,replica_sum,'load10','noactive',expel_item,run_times)
    # Avgtime04pr, b01, e01, s01 = load_avg_times(distribution,replica_sum,'popularity10','random3',expel_item,run_times)
    # Avgtime04lr, b01, e01, s01 = load_avg_times(distribution,replica_sum,'load10','random3',expel_item,run_times)
    # Avgtime04pc, b02, e02, s02 = load_avg_times(distribution,replica_sum,'popularity10','calculate3',expel_item,run_times)
    # Avgtime04lc, b02, e02, s02 = load_avg_times(distribution,replica_sum,'load10','calculate3',expel_item,run_times)
    # ### 被动的比较plot
    # plt.plot(range(b02, e02, s02), Avgtime04nn, color=colors[2], label='n',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04rn, color=colors[3], label='r',marker='.')
    # plt.plot(range(b01, e01, s01), Avgtime04pn, color=colors[0], label='p',marker='.')
    # plt.plot(range(b01, e01, s01), Avgtime04ln, color=colors[1], label='l',marker='.')
    # plt.plot(range(b01, e01, s01), Avgtime04pr, color=colors[4], label='pr',marker='.')
    # plt.plot(range(b01, e01, s01), Avgtime04lr, color=colors[5], label='lr',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04pc, color=colors[6], label='pc',marker='*')
    # plt.plot(range(b02, e02, s02), Avgtime04lc, color=colors[7], label='lc',marker='*')
    ### 被动的比较 done

    ### 主动的比较：修改distribution/curve
    # this_passive='nopassive'
    # Avgtime04nc, b02, e02, s02 = load_avg_times(distribution,replica_sum,this_passive,'calculate3',expel_item,run_times)
    # Avgtime04nr, b02, e02, s02 = load_avg_times(distribution,replica_sum,this_passive,'random3',expel_item,run_times)
    # Avgtime04nn, b02, e02, s02 = load_avg_times(distribution,replica_sum,this_passive,'noactive',expel_item,run_times)
    # plt.plot(range(b02, e02, s02), Avgtime04nn, color=colors[3], label=this_passive[0]+'n',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04nc, color=colors[2], label=this_passive[0]+'c',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04nr, color=colors[0], label=this_passive[0]+'r',marker='.')

    ### random的加入：修改distribution/curve
    # Avgtime04nn, b02, e02, s02 = load_avg_times(distribution,replica_sum,'nopassive','noactive',expel_item,run_times)
    # Avgtime04nr, b02, e02, s02 = load_avg_times(distribution,replica_sum,'nopassive','random3',expel_item,run_times)
    # Avgtime04rn, b01, e01, s01 = load_avg_times(distribution,replica_sum,'random10','noactive',expel_item,run_times)
    # Avgtime04rr, b02, e02, s02 = load_avg_times(distribution,replica_sum,'random10','random3',expel_item,run_times)
    # ### random的加入plot
    # plt.plot(range(b02, e02, s02), Avgtime04nn, color=colors[3], label='nn',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04nr, color=colors[2], label='nr',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04rn, color=colors[0], label='rn',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04rr, color=colors[1], label='rr',marker='.')
    ### random的加入done

    ### 最终的比较：修改distribution/curve
    # Avgtime04rr, b02, e02, s02 = load_avg_times(distribution,replica_sum,'random10','random3',expel_item,run_times)
    # Avgtime04rc, b02, e02, s02 = load_avg_times(distribution,replica_sum,'random10','calculate3',expel_item,run_times)
    # Avgtime04pr, b01, e01, s01 = load_avg_times(distribution,replica_sum,'popularity10','random3',expel_item,run_times)
    # Avgtime04pc, b02, e02, s02 = load_avg_times(distribution,replica_sum,'popularity10','calculate3',expel_item,run_times)
    # Avgtime04lr, b01, e01, s01 = load_avg_times(distribution,replica_sum,'load10','random3',expel_item,run_times)
    # Avgtime04lc, b02, e02, s02 = load_avg_times(distribution,replica_sum,'load10','calculate3',expel_item,run_times)
    ### 最终的比较plot
    # plt.plot(range(b02, e02, s02), Avgtime04rr, color=colors[3], label='rr',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04rc, color=colors[2], label='rc',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04pr, color=colors[0], label='pr',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04pc, color=colors[1], label='pc',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04lr, color=colors[4], label='lr',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04lc, color=colors[5], label='lc',marker='.')
    ### 简化的plot
    # begin_x=0
    # end_x=len(Avgtime04pc)
    # step_x=50
    # x_axis_v=range(begin_x,end_x,step_x)
    
    
    # plt.plot(x_axis_v ,Avgtime04rr[::step_x], color=colors[3], label='rr',marker='.')
    # plt.plot(x_axis_v, Avgtime04rc[::step_x], color=colors[2], label='rc',marker='.')
    # plt.plot(x_axis_v, Avgtime04pr[::step_x], color=colors[0], label='pr',marker='.')
    # plt.plot(x_axis_v, Avgtime04pc[::step_x], color=colors[1], label='pc',marker='.')
    # plt.plot(x_axis_v, Avgtime04lr[::step_x], color=colors[4], label='lr',marker='*')
    # plt.plot(x_axis_v, Avgtime04lc[::step_x], color=colors[5], label='lc',marker='*')

    ### 最终的比较done

    ## popularity的比较
    # if distribution=='zipfr':
    #     p_r=popularity_analysis.plot_distribution_replia_nums_v3(654400)
    #     plt.plot(range(654000,654400),p_r,color='black',marker='*')
    # Avgtime04, b02, e02, s02 = load_avg_times(distribution,replica_sum,'popularity10','calculate3',expel_item,run_times)
    # Avgtime04r, b02, e02, s02 = load_avg_times(distribution,replica_sum,'popularity10','random3',expel_item,run_times)
    # Avgtime04o, b02, e02, s02 = load_avg_times('zipfori',replica_sum,'popularity10','calculate3',expel_item,run_times)
    # Avgtime04v, b02, e02, s02 = load_avg_times(distribution,replica_sum,'popularity10','calvary3',expel_item,run_times)
    # Avgtime04t, b02, e02, s02 = load_avg_times(distribution,replica_sum,'popularity10','caltwo3',expel_item,run_times)
    # print(Avgtime04)
    # plt.plot(range(b02,e02,s02),Avgtime04,color=colors[1],label='cal')#,marker='.')
    # # plt.plot(range(b02,e02,s02),Avgtime04r,color=colors[2],label='rand',marker='.')
    # # plt.plot(range(b02,e02,s02),Avgtime04o,color=colors[3],label='cal-ori',marker='.')
    # plt.plot(range(b02,e02,s02),Avgtime04v,color=colors[0],label='cal-vary')#,marker='.')
    # plt.plot(range(b02,e02,s02),Avgtime04t,color=colors[3],label='cal-2')#,marker='.')

    # x_axis_v=range(b02, e02, s02)
    # base=np.array(Avgtime04)
    # vary_s=np.array(Avgtime04v)
    # two_s=np.array(Avgtime04t)
    # vary_base=(vary_s-base)/base
    # two_base=(two_s-base)/base
    # plt.plot(x_axis_v,vary_base,color=colors[0],label='vary')
    # plt.plot(x_axis_v,two_base,color=colors[1],label='two')
    # print('calvary:',np.mean(vary_base))
    # print('caltwo:',np.mean(two_base))

    ### extra comparasion

    # Avgtime1,b,e,s=load_avg_times('zipf',replica_sum,'load10','calculate3','llu8',100)
    # Avgtime2,b,e,s=load_avg_times('zipf',replica_sum,'load10','calculate3','curve3',100)
    # Avgtime3,b,e,s=load_avg_times('zipfr',replica_sum,'load10','calculate3','curve3',100)
    # Avgtime11,b,e,s=load_avg_times('zipfr',replica_sum,'load10','calculate3','llu8',100)
    # Avgtime21,b,e,s=load_avg_times('zipf',replica_sum,'load10','access3','curve3',100)
    # Avgtime31,b,e,s=load_avg_times('zipfr',replica_sum,'load10','calculate3','llu8',100)
    # plt.plot(range(b, e, s), Avgtime1, color=colors[0], label='zipf-lc-l',marker='.')
    # plt.plot(range(b, e, s), Avgtime2, color=colors[1], label='zipf-lc-c',marker='.')
    # plt.plot(range(b, e, s), Avgtime3, color=colors[4], label='zipfr-lc-c',marker='.')
    # plt.plot(range(b, e, s), Avgtime11, color=colors[2], label='zipfr-lc-l',marker='.')
    # plt.plot(range(b, e, s), Avgtime21, color=colors[3], label='zipf-la-c',marker='.')
    # plt.plot(range(b, e, s), Avgtime31, color=colors[5], label='zipfr-lc-l',marker='.')

    # Avgtime04rr, b02, e02, s02 = load_avg_times(distribution,replica_sum,'random10','calculate3',expel_item,run_times)
    # Avgtime04rc, b02, e02, s02 = load_avg_times(distribution,replica_sum,'load10','calculate3',expel_item,run_times)
    # Avgtime04lr, b01, e01, s01 = load_avg_times(distribution,replica_sum,'load10','random3',expel_item,run_times)
    # Avgtime04lc, b02, e02, s02 = load_avg_times(distribution,replica_sum,'load10','calculate3',expel_item,run_times)
    ### 最终的比较plot
    # plt.plot(range(b02, e02, s02), Avgtime04rr, color=colors[3], label='rn',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04rc, color=colors[2], label='ln',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04lr, color=colors[0], label='lr',marker='.')
    # plt.plot(range(b02, e02, s02), Avgtime04lc, color=colors[1], label='lc',marker='.')

    # Avgtime01, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'llu2',run_times)
    # Avgtime02, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'llu3',run_times)
    # Avgtime03, b02, e02, s02 = load_avg_times(distribution,replica_sum,passive_item,active_item,'llu4',run_times)
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
    

    # if b01 != b01 or e01 != e02 or s01 != s02:
    #     exit(-1)
    # if b12 != b22 or e12 != e22 or s12 != s22:
    #     exit(-1)
    # if b01 != b12 or e01 != e12 or s01 != s12:
    #     exit(-1)
    # if b12!=b_12 or e12!=e_12 or s12!=s_12:
    #     exit(-1)

    # for i in range(len(period_s)):
    #     plt.plot(range(b01, e01, s01), avg_time[i], color=colors[i], label=str(period_s[i]))
    # plt.plot(range(b01, e01, s01), Avgtime01, color=colors[0], label='nipopows')
    # plt.plot(range(b02, e02, s02), Avgtime01, color=colors[0], label='2')
    # plt.plot(range(b02, e02, s02), Avgtime02, color=colors[1], label='3')
    # plt.plot(range(b02, e02, s02), Avgtime03, color=colors[2], label='4')
    
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
    plt.title(distribution)
    # plt.ylim(ymin=0,ymax=5)
    plt.show()

def load_storage(chosen_block_distribution,static_type,piece,passive_item,active_item,expel_item,total_times,timeup,encodetype):
    file_storage_used='D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\S-CLIENT'+chosen_block_distribution+'-'+static_type+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'-'+str(timeup)+'-'+encodetype+'.txt'
    NodesSizeAll =[] 
    BlockSize=[]
    NodeSize_se=[]
    Node_Num_se=[]
    last_time=time.ctime(os.stat(file_storage_used).st_mtime)
    print('file modify time: ',last_time,', file: ',file_storage_used)
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
            elif i>=2 and i<12:
                NodesSize=np.array(json.loads(dataline))
                # print('nodeid=',i-2,', \n',NodesSize)
                NodesSizeAll+=NodesSize
                NodeSize_se.append(NodesSize)
            elif i>=12 and i<22:
                Node_Num_se.append(json.loads(dataline))
            i += 1
        # print('filename=', file_storage_used, '-------')
        # print(NodesSizeAll)
        NodesSizeAll=NodesSizeAll#/10
        # print('filename=',file_storage_used,'-------')
        # print(NodesSizeAll)
        # print(BlockSize)
    return BlockSize,NodesSizeAll, begin, ends, step, NodeSize_se,Node_Num_se

def plot_storage():
    distribution='zipf'
    static_type='piecekad'
    replica_sum=3
    passive_type='pop_kad'
    passive_items_su=['10','100','200','300']#['10','20','40','60','95','96','97','100','150','155','160','200']
    passive_items=[passive_type+x for x in passive_items_su]
    active_item='kadvary3'
    expel_item='curve3'
    run_times=[10,10,5,4]
    encode_type="encode4-2-9"#"noencode"#
    timeup=float(2.0)
    colors = ['blue', 'red', 'green', 'skyblue', 'pink', 'yellow', 'purple', 'black', 'cyan', 'orange','gold','brown','grey','lime']

    blk,node100,b,e,s,eachnode100,node_num_se100=load_storage('zipf',static_type,3,'pop_kad50','kadvary3',expel_item,20,timeup,encode_type)
    x_axis=range(b,e,s)
    str_send='['
    len_10=len(node_num_se100[0])-1
    for i in range(len(node_num_se100)):
        # plt.plot(x_axis,node_num_se100[i],color=colors[i],label=str(i))
        str_send+=str(node_num_se100[i][len_10])+','
    print(str_send,']')
    print('blk=',blk)
    print('np.sum(node100,axis=0)=',np.sum(node100,axis=0))
    print('node100/blk=',sum(node100)/sum(blk))
    plt.title('total storage / one blokchcain')
    pltLabel=static_type+'-pop_kad200-kadvary3-'+encode_type

    # blk4,node4, b02, e02, s02,_,nn4 = load_storage(distribution,replica_sum,'popularity10','calculate3',expel_item,run_times)
    # blk4,node4v, b02, e02, s02,_,nn4 = load_storage(distribution,replica_sum,'popularity10','calvary3',expel_item,run_times)
    # blk4,node4t, b02, e02, s02,_,nn4 = load_storage(distribution,replica_sum,'popularity10','caltwo3',expel_item,run_times)
    # blk5,node5, b02, e02, s02,_,nn5 = load_storage(distribution,replica_sum,'random10','calculate3',expel_item,run_times)
    # blk5,node6, b02, e02, s02,_,nn6 = load_storage(distribution,replica_sum,'popularity10','random3',expel_item,run_times)
    # blk4,node7, b02, e02, s02,_,nn7 = load_storage(distribution,replica_sum,'load10','calculate3',expel_item,run_times)
    # blk4,node8, b02, e02, s02,_,nn8 = load_storage(distribution,replica_sum,'load10','random3',expel_item,run_times)
    # x_axis_v=range(b02, e02, s02)
    # base=np.array(node4)
    # vary_s=np.array(node4v)
    # two_s=np.array(node4t)
    # vary_base=(vary_s-base)/base
    # two_base=(two_s-base)/base
    # plt.plot(x_axis_v,vary_base,color=colors[0],label='vary')
    # plt.plot(x_axis_v,two_base,color=colors[1],label='two')
    # print('calvary:',np.mean(vary_base))
    # print('caltwo:',np.mean(two_base))
    #### plt.plot(range(b02, e02, s02), np.array(node2)/np.array(blk2), color=colors[2], label='rc',marker='.')
    # plt.plot(x_axis_v, np.array(node0)/np.array(blk3), color=colors[7], label='nn')#,marker='o')
    # plt.plot(x_axis_v, np.array(node1)/np.array(blk3), color=colors[1], label='nr')#,marker='.')
    # plt.plot(x_axis_v, np.array(node2)/np.array(blk3), color=colors[2], label='rn')#,marker='.')
    # plt.plot(x_axis_v, np.array(node3)/np.array(blk3), color=colors[0], label='rr')#,marker='*')
    # plt.plot(range(b02, e02, s02), np.array(node4)/np.array(blk4), color=colors[10], label='pc')#,marker='.')
    # plt.plot(range(b02, e02, s02), np.array(node4v)/np.array(blk4), color=colors[11], label='pcv')#,marker='.')
    # plt.plot(range(b02, e02, s02), np.array(node4t)/np.array(blk4), color=colors[12], label='pct')#,marker='.')
    # plt.plot(range(b02, e02, s02), np.array(node5)/np.array(blk4), color=colors[4], label='rc')#,marker='.')
    # plt.plot(range(b02, e02, s02), np.array(node6)/np.array(blk4), color=colors[5], label='pr')#,marker='.')
    # plt.plot(range(b02, e02, s02), np.array(node7)/np.array(blk4), color=colors[6], label='lc')#,marker='.')
    # plt.plot(range(b02, e02, s02), np.array(node8)/np.array(blk4), color=colors[7], label='lr')#,marker='.')
    ###
    # xx=np.sum(np.array(nn4),axis=0)-np.sum(np.array(nn7),axis=0)
    # plt.plot(range(len(xx)),xx)
    # y_axis_v=[]
    # for i in range
    # x_axis_v=range(b01, e01, s01)
    # print(nn2)
    # plt.plot(x_axis_v, np.sum(np.array(nn0),axis=0), color=colors[7], label='nn',marker='o')
    # plt.plot(x_axis_v, np.sum(np.array(nn1),axis=0), color=colors[1], label='nr',marker='.')
    # plt.plot(x_axis_v, np.sum(np.array(nn2),axis=0), color=colors[11], label='rn',marker='.')
    # plt.plot(x_axis_v, np.sum(np.array(nn3),axis=0), color=colors[10], label='nn',marker='*')
    # plt.plot(range(b02, e02, s02), np.sum(np.array(nn2),axis=0), color=colors[2], label='rn',marker='.')
    # plt.plot(range(b02, e02, s02), np.sum(np.array(nn7),axis=0), color=colors[0], label='lc',marker='.')
    # plt.plot(range(b02, e02, s02), np.sum(np.array(nn4),axis=0), color=colors[10], label='pc',marker='.')
    # plt.plot(range(b02, e02, s02), np.sum(np.array(nn5),axis=0)/np.array(range(11,401)), color=colors[4], label='rc',marker='.')
    # plt.plot(range(b02, e02, s02), np.sum(np.array(nn6),axis=0)/np.array(range(11,401)), color=colors[5], label='pr',marker='.')
    # plt.plot(range(b02, e02, s02), np.sum(np.array(nn7),axis=0)/np.array(range(11,401)), color=colors[6], label='lc',marker='.')
    ###
    # plt.plot(range(b02, e02, s02), np.array(node5)/np.array(blk5), color=colors[4], label='lc',marker='.')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize01)/np.array(Blocksize01),color=colors[13],label='llu7')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize02)/np.array(Blocksize01),color=colors[0],label='llu8')
    # # plt.plot(range(b01, e01, s01),np.array(NodeSize033),color=colors[10],label='SUM-block')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize03)/np.array(Blocksize01),color=colors[1],label='llu3')

    # # plt.plot(range(b01, e01, s01),np.array(NodeSize04),color='gold',label='SUM-block')
    # # plt.plot(range(b01, e01, s01),np.array(Blocksize01),color='brown',label='SUM')
    plt.plot(range(b, e, s),np.array(node100)/np.array(blk),color=colors[0],label=pltLabel)
    # for i in range(10):
    #     plt.plot(range(b, e, s),np.array(eachnode100[i])/np.array(blk),color=colors[i],label=str(i))
    # plt.plot(range(b01, e01, s01),np.array(NodeSize04)/np.array(Blocksize01),color=colors[2],label='llu4')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize05)/np.array(Blocksize01),color=colors[3],label='llu5')
    # # # plt.plot(range(b01, e01, s01),np.array(NodeSize05r)/np.array(Blocksize01),color=colors[4],label='5r')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize06)/np.array(Blocksize01),color=colors[4],label='llu6')

    # plt.plot(range(b01, e01, s01),np.array(NodeSize011)/np.array(Blocksize01),color=colors[5],label='curve-11')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize022)/np.array(Blocksize01),color=colors[6],label='22')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize033)/np.array(Blocksize01),color=colors[7],label='33')
    # # plt.plot(range(b01, e01, s01),np.array(NodeSize033r)/np.array(Blocksize01),color=colors[8],label='33r')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize044)/np.array(Blocksize01),color=colors[8],label='44')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize055)/np.array(Blocksize01),color=colors[9],label='55')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize066)/np.array(Blocksize01),color=colors[10],label='66')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize077)/np.array(Blocksize01),color=colors[11],label='77')
    # plt.plot(range(b01, e01, s01),np.array(NodeSize_no)/np.array(Blocksize01),color=colors[12],label='no-expel')
    # plt.plot(range(b01, e01, s01), NodeSize01, color=colors[0], label='01')
    # plt.plot(range(b01, e01, s01), NodeSize02, color=colors[1], label='02')
    # plt.plot(range(b01, e01, s01), NodeSize12, color=colors[2], label='12')
    # plt.plot(range(b01, e01, s01), NodeSize22, color=colors[3], label='22')
    plt.legend()
    # plt.ylim(ymin=0.2,ymax=.5)
    plt.xlabel('blocks')
    # plt.ylabel('per node storage size')
    
    # plt.title('s-'+distribution+str(replica_sum)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(run_times))
    plt.show()
    # store_file_name_1='./finalTest/finalRes/experimenta/extra/Combine-A.csv'
    # start=654010
    # with open(store_file_name_1,'w')as file_in:
    #     print('epoch,node1,node2,node3,node4,node5,node6,node7,node8,node9,node10,one replica,total block size in system',file=file_in)
    #     for line_index in range(len(blk4)):
    #         line2=str(start)
    #         start+=1
    #         for i in range(10):
    #             line2+=','+str(each_node_block[i][line_index])
    #         line2+=','+str(blk4[line_index])+','+str(node4[line_index])
    #         print(line2,file=file_in)

def load_delay_info(chosen_block_distribution,static_type,piece,passive_item,active_item,expel_item,total_times,timeup,encode_type):
    if timeup=='inf':
        timup=np.inf
    else:
        timeup=float(timeup)
    file_name='D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\D-CLIENT'+chosen_block_distribution+'-'+static_type+str(piece)+'-'+passive_item+'-'+active_item+'-'+expel_item+'-'+str(total_times)+'-'+str(timeup)+'-'+encode_type+'.txt'
    delay_percentile=[]
    delay_time_div_total_time=[]
    total_access_time=[]
    total_cost_time=[]
    requests_tag=[]
    last_delay_percentile=[]
    last_delay_time_div_total_time=[]
    last_total_access_time=[]
    last_total_cost_time=[]
    last_requests_tag=[]
    last_time=time.ctime(os.stat(file_name).st_mtime)
    print('file modify time: ',last_time,', file: ',file_name)
    with open(file_name, 'r') as datafile:
        i = 0
        for dataline in datafile:
            if i == 0:
                datalineitem = dataline.split()
                begin = int(datalineitem[0])
                ends = int(datalineitem[1])
                step = int(datalineitem[2])
            elif i==1:
                delay_percentile=json.loads(dataline)
            elif i==2:
                delay_time_div_total_time=json.loads(dataline)
            elif i==3:
                total_access_time=json.loads(dataline)
            elif i==4:
                total_cost_time=json.loads(dataline)
            elif i==5:
                requests_tag=json.loads(dataline)
            elif i==6:
                last_delay_percentile=json.loads(dataline)
            elif i==7:
                last_delay_time_div_total_time=json.loads(dataline)
            elif i==8:
                last_total_access_time=json.loads(dataline)
            elif i==9:
                last_total_cost_time=json.loads(dataline)
            elif i==10:
                last_requests_tag=json.loads(dataline)
            i+=1
    # print(delay_percentile)
    # print(delay_time_div_total_time)
    return delay_percentile,delay_time_div_total_time,total_access_time,total_cost_time,requests_tag,begin,ends,step,last_delay_percentile,last_delay_time_div_total_time,last_total_access_time,last_total_cost_time,last_requests_tag


def plot_delay():
    distribution='zipf'
    static_type='piecekad'
    replica_sum=3
    passive_type='kad'
    passive_items_su=['10','100','200','300']
    passive_items=[passive_type+x for x in passive_items_su]
    active_item='kadvary3'
    expel_item='curve3'
    timeup=float(2)
    run_times=[100,10,5,4]#[15]*len(passive_items_su)
    dps=[]
    dts=[]
    tas=[]
    tcs=[]
    encode_type="encode4-2-9"#"noencode"#
    colors = ['blue', 'red', 'green', 'skyblue', 'pink', 'yellow', 'purple', 'black', 'cyan', 'orange','gold','brown','grey','lime']
    # for i in range(len(passive_items)):
    #     dp,dt,ta,tc,b,e,s=load_delay_info(distribution,static_type,replica_sum,passive_items[i],active_item,expel_item,run_times[i])
    #     dps.append(dp)
    #     dts.append(dt)
    #     tas.append(ta)
    #     tcs.append(tc)
    
    # # dp5,dt5, b01, e01, s01 = load_delay_info(distribution,replica_sum,'popularity90',active_item,expel_item,20)

    # s01=s*10
    # x_axis=range(b,e,s01)

    # for i in range(len(dps)):
    #     plt.plot(x_axis,dts[i][::s01],color=colors[i],label=passive_items[i])
    # plt.ylabel('average delay time')
    #不区分节点
    # print((dps[0][0]))
    # for i in range(len(dps)):
    #     dps_isum=[sum(tcs[i][j]) for j in range(len(dps[i]))]
    #     plt.plot(x_axis,dps_isum[::s01],color=colors[i],label=passive_items[i])
    # # plt.ylabel('delay percentile(%)')
    # # plt.ylabel('delay time percent(%):total delay time/total cost time')
    # # plt.ylabel('total requests')
    # plt.ylabel('total cost time')
    #####################################
    dp,dt,ta,tc,rt,b,e,s,ldp,ldt,lta,ltc,lrt=load_delay_info(distribution,static_type,replica_sum,'pop_kad300',active_item,expel_item,4,2.0,encode_type)
    step=10
    for i in range(10):
        yaxisdp=[]
        yaxisdt=[]
        yaxista=[]
        yaxistc=[]
        yaxisrt=[]
        for j in range(len(dp)):
            yaxisdp.append(dp[j][i])
            yaxisdt.append(dt[j][i])
            yaxista.append(ta[j][i])
            yaxistc.append(tc[j][i])
            yaxisrt.append(rt[j][i])
        # plt.plot(range(b,e,step),np.array(yaxisdt[::step])*np.array(yaxistc[::step])/np.array(yaxista[::step]),color=colors[i],label=str(i))
        # plt.plot(range(b,e,step),np.array(yaxista[::step]),color=colors[i],label=str(i))
    plt.bar(range(0,10),np.mean(ta,axis=0),color='blue',label='total requests')
    plt.bar(range(0,10),np.mean(dp,axis=0)*np.mean(ta,axis=0),color='red',label='delay requets')
    plt.title(static_type+'-pop_kad300-'+active_item+'-'+encode_type)
    # plt.ylabel('averag total requests time of each node')
    # plt.bar(range(0,10),np.mean(ta,axis=0),color='blue',label='total requests')
    # plt.bar(range(0,10),np.mean(dp,axis=0)*np.mean(ta,axis=0),color='red',label='delay requets')
    # plt.ylabel('averag total requests of each node')
    
    # rtag=np.mean(rt,axis=0)#rt[len(rt)-1]#
    # print(rtag)
    # rtag1=[r[0] for r in rtag]
    # rtag2=[r[1]+r[0] for r in rtag]
    # rtag3=[r[2]+r[0]+r[1] for r in rtag]
    # plt.bar(range(0,10),rtag3,color='red',label='3')
    # plt.bar(range(0,10),rtag2,color='pink',label='2')
    # plt.bar(range(0,10),rtag1,color='b',label='1')

    # plt.title('delay')
    plt.xlabel('epoch')
    
    plt.legend()
    plt.show()


def _3_exp_time(lambdai,timeout):
    distribution='zipf'
    static_type='piecekad'
    replica_sum=3
    passive_type=['nopassive','kad','kad']
    passive_item_su=str(lambdai)
    passive_items=[x+passive_item_su for x in passive_type]
    active_item=['noactive','kadvary3','kadvary3']
    expel_item='curve3'
    timeup=[np.inf,float(timeout),float(timeout)]
    if(lambdai==10):
        run_times=100
    elif(lambdai==20):
        run_times=50
    elif(lambdai==50):
        run_times=20
    elif(lambdai==100):
        run_times=10
    elif(lambdai==200):
        run_times=5
    elif(lambdai==300):
        run_times=4
    encode_type=['noencode','noencode',"encode4-2-6"]
    colors = ['blue', 'red', 'green', 'skyblue', 'pink', 'yellow', 'purple', 'black', 'cyan', 'orange','lime','grey']
    label_items=[]
    Avg=[]
    for i in range(3):
        avg_t,b,e,s=load_avg_times(distribution,static_type,replica_sum,passive_items[i],active_item[i],expel_item,run_times,timeup[i],encode_type[i])
        Avg.append(avg_t)
        label_items.append(static_type+str(replica_sum)+'-'+passive_items[i]+'-'+active_item[i]+'-'+expel_item+'-'+encode_type[i]+'-'+str(np.mean(avg_t)))
    b_x=0
    e_x=len(Avg[0])
    s=1
    xaxis=range(0,e_x,s)
    count=0
    for avg in Avg:
        yaxis=avg[::s]
        plt.plot(xaxis, yaxis, color=colors[count], label=label_items[count])#passive_items[i]+'-'+j)
        count+=1
        plt.legend()
    ##
    with open('time_kad_'+str(lambdai)+'-'+str(timeout)+'.txt','w')as f:
        print('x '+label_items[0]+' '+label_items[1]+' '+label_items[2],file=f)
        for i in range(len(xaxis)):
            line1=str(xaxis[i])+' '+str(Avg[0][i])+' '+str(Avg[1][i])+' '+str(Avg[2][i])
            print(line1,file=f)
    ##
    plt.xlabel('blocks')
    plt.ylabel('avg time')
    plt.title(distribution)
    # plt.ylim(ymin=0,ymax=5)
    plt.show()

    
def _3_exp_storage(lambdai,timeout):
    distribution='zipf'
    static_type='piecekad'
    replica_sum=3
    passive_type=['nopassive','kad','kad']
    passive_item_su=str(lambdai)
    passive_items=[x+passive_item_su for x in passive_type]
    active_item=['noactive','kadvary3','kadvary3']
    expel_item='curve3'
    timeup=[np.inf,float(timeout),float(timeout)]
    if(lambdai==10):
        run_times=100
    elif(lambdai==20):
        run_times=50
    elif(lambdai==50):
        run_times=20
    elif(lambdai==100):
        run_times=10
    elif(lambdai==200):
        run_times=5
    elif(lambdai==300):
        run_times=4
    encode_type=['noencode','noencode',"encode4-2-6"]
    colors = ['blue', 'red', 'green', 'skyblue', 'pink', 'yellow', 'purple', 'black', 'cyan', 'orange','lime','grey']
    label_items=[]#'kad400-kadv3-0','kad400-kadv3-1','kad400-kadv3-inf'
    all_div_blk=[]
    for i in range(3):
        blk,node100,b,e,s,eachnode100,node_num_se100=load_storage(distribution,static_type,replica_sum,passive_items[i],active_item[i],expel_item,run_times,timeup[i],encode_type[i])
        all_div_blk_per=np.array(node100)/np.array(blk)
        all_div_blk.append(all_div_blk_per)
        label_items.append(static_type+str(replica_sum)+'-'+passive_items[i]+'-'+active_item[i]+'-'+expel_item+'-'+encode_type[i]+'-'+str(np.mean(all_div_blk_per)))
    b_x=0
    e_x=len(all_div_blk[0])
    s=1
    xaxis=range(0,e_x,s)
    count=0
    for avg in all_div_blk:
        yaxis=avg[::s]
        plt.plot(xaxis, yaxis, color=colors[count], label=label_items[count])
        count+=1
    ##
    with open('store_kad_'+str(lambdai)+'-'+str(timeout)+'.txt','w')as f:
        print('x '+label_items[0]+' '+label_items[1]+' '+label_items[2],file=f)
        for i in range(len(xaxis)):
            line1=str(xaxis[i])+' '+str(all_div_blk[0][i])+' '+str(all_div_blk[1][i])+' '+str(all_div_blk[2][i])
            print(line1,file=f)
    ##

    plt.legend()
    plt.xlabel('blocks')
    plt.title('total storage / one blokchcain')
    # plt.ylim(ymin=0,ymax=5)
    plt.show()

def _3_exp_delay(lambdai,timeout):
    distribution='zipf'
    static_type='piecekad'
    replica_sum=3
    passive_type=['nopassive','kad','kad']
    passive_item_su=str(lambdai)
    passive_items=[x+passive_item_su for x in passive_type]
    active_item=['noactive','kadvary3','kadvary3']
    expel_item='curve3'
    timeup=[np.inf,float(timeout),float(timeout)]
    if(lambdai==10):
        run_times=100
    elif(lambdai==20):
        run_times=50
    elif(lambdai==50):
        run_times=20
    elif(lambdai==100):
        run_times=10
    elif(lambdai==200):
        run_times=5
    elif(lambdai==300):
        run_times=4
    encode_type=['noencode','noencode',"encode4-2-6"]
    colors = ['blue', 'red', 'green', 'skyblue', 'pink', 'yellow', 'purple', 'black', 'cyan', 'orange','lime','grey']
    label_items=[]
    dpy=[]
    tay=[]
    for i in range(3):
        plt.subplot(220+i+1)
        dp,dt,ta,tc,rt,b,e,s,ldp,ldt,lta,ltc,lrt=load_delay_info(distribution,static_type,replica_sum,passive_items[i],active_item[i],expel_item,run_times,timeup[i],encode_type[i])
        step=10
        # plt.bar(range(0,10),np.mean(tc,axis=0),color='blue',label='total requests')
        plt.bar(range(0,10),(ta[len(ta)-1]),color='blue',label='total requests in last epoch')
        # print(i)
        label=static_type+str(replica_sum)+'-'+passive_items[i]+'-'+active_item[i]+'-'+expel_item+'-'+encode_type[i]+'-'+str(round(np.std(ta[len(ta)-1]),4))
        label_items.append(label)
        plt.title(label)
        dpy.append(np.mean(dp,axis=0))
        tay.append(np.mean(ta,axis=0))
    plt.show()
        ##
    with open('delay_kad_'+str(lambdai)+'-'+str(timeout)+'.txt','w')as f:
        print('x '+label_items[0]+' '+'delay_percentile '+label_items[1]+' '+'delay_percentile '+label_items[2]+''+'delay_percentile ',file=f)
        for i in range(10):
            line1=str(i)+' '+str(tay[0][i])+' '+str(dpy[0][i])+' '+str(tay[1][i])+' '+str(dpy[1][i])+' '+str(tay[2][i])+' '+str(dpy[2][i])
            print(line1,file=f)
    ##
    


if __name__=='__main__':
    lambdai=10
    time_out=0
    _3_exp_time(lambdai,time_out)
    _3_exp_storage(lambdai,time_out)
    _3_exp_delay(lambdai,time_out)
    # Avgtime04nn, b02, e02, s02 = load_avg_times('zipf',3,'nopassive','noactive','noexpel',100)
    # Avgtime04r, b02, e02, s02 = load_avg_times('zipfr',3,'nopassive','noactive','noexpel',100)
    # plt.figure()
    # plt.plot(range(b02,e02,s02),Avgtime04nn,color='r',marker='.',label='zipf')
    # plt.plot(range(b02,e02,s02),Avgtime04r,color='g',marker='.',label='zipfr')
    # plt.ylim(0,1)
    # plt.legend()
    # plt.show()

    # plot_delay()
    # plot_avg()
    # plot_storage()

    # plot_storage_end_epoch()

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
    # A=[0.0011049223105278451, 0.0011183288002366133, 0.0011320365577191767, 0.0011460555318899353, 0.0011603961073781482, 0.0011750691284024557, 0.001190085924221757, 0.0012054583362846182, 0.0012211987472102793, 0.0012373201117463367, 0.0012538359898614062, 0.0012707605821456784, 0.0012881087677084028, 0.0013058961447791801, 0.0013241390742396834, 0.0013428547263343263, 0.0013620611308326743, 0.0013817772309433823, 0.0014020229413094648, 0.001422819210448112, 0.001444188088035565, 0.0014661527974791685, 0.0014887378142652689, 0.0015119689506237213, 0.0015358734471082015, 0.0015604800717571102, 0.001585819227573616, 0.001611923069146468, 0.0016388256293268962, 0.001666562956982791, 0.0016951732669711313, 0.001724697103605426, 0.001755177519049127, 0.001786660268241332, 0.001819194022160996, 0.001852830601464057, 0.0018876252327889428, 0.001923636830325165, 0.0019609283055834164, 0.001999566908701227, 0.0020396246050746287, 0.002081178491633946, 0.0021243112576933855, 0.002169111696014439, 0.002215675270550476, 0.002264104748305787, 0.0023145109038731626, 0.0023670133065415233, 0.00242174120142787, 0.0024788344979329883, 0.0025384448810057175, 0.0026007370632970487, 0.0026658901993804832, 0.0027340994869173166, 0.002805577984089776, 0.0028805586779797527, 0.0029592968450478005, 0.003042072752732842, 0.003129194760785788, 0.0032210028927005738, 0.003317872962065533, 0.003420221356536792, 0.003528510604353633, 0.003643255876072963, 0.0037650326090695723, 0.0038944854864093755, 0.004032339057719019, 0.004179410361353551, 0.004336623999511108, 0.004505030237781586, 0.004685826857321405, 0.004880385694428149, 0.005090285076977883, 0.005317349735803605, 0.005563700268617474, 0.005831814918123824, 0.006124607373262158, 0.006445525630279646, 0.006798678835708647, 0.007189001748359949, 0.007622470427227634, 0.008106388653621226, 0.008649773529096825, 0.009263882484784262, 0.009962945708958145, 0.010765203205612047, 0.011694404188780901, 0.01278202669251491, 0.014070652829337903, 0.015619262389463363, 0.017511838481539862, 0.019871961247940842, 0.022888838693609977, 0.026866685708646112, 0.03232587151758965, 0.04023164011343723, 0.05258474271028453, 0.07426535087220147, 0.12080801489849234, 0.27754393596871085]
    # B=list(range(0,100))
    # plt.plot(B,A,marker='.')
    # plt.show()

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

def plot_storage_end_epoch():
    fname='./finalTest/finalRes/debug/store-nodes-runtime.txt'
    dict_last_epoch=[]
    with open(fname, 'r') as datafile:
        i=0
        for dataline in datafile:
            dict_last_epoch=json.loads(dataline)
    NodeStorage=[]
    X=[]#nodes index
    Y=[]#block index
    total_blocks=len(dict_last_epoch)
    for i in range(total_blocks):
        NodeStorage.append([])
    for blockindex in range(total_blocks):
        block_store_nodes=dict_last_epoch[blockindex]
        for kvs in block_store_nodes.items():
            NodeStorage[int(kvs[0])].append(blockindex)
            X.append(int(kvs[0]))
            Y.append(blockindex)
    plt.figure()
    plt.scatter(X,Y,marker='*')
    plt.xlabel('node index')
    plt.ylabel('block index')
    plt.show()