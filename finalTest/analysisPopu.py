import numpy as np
import matplotlib
import matplotlib.pyplot as plt
filename='D:\\Languages\\PythonSpace\\AnalysisSanning\\active_chosen_popu.txt'

if __name__=='__main__':
    find_nodes=[]
    popu=[]
    actual_nodes=[]
    with open(filename,'r')as df_me:
        for line_data in df_me:
            line_items=[i for i in line_data.split(',')]
            find_nodes.append(int(line_items[0]))
            popu.append(float(line_items[1]))
            actual_nodes.append(int(line_items[2]))
    
    #bar:
    bar_popu_actual=[]
    bar_popu_find=[]

    replicas_actuall=[]
    replicas_find=[]
    for i in range(11):
        bar_popu_find.append([])
        bar_popu_actual.append([])
        replicas_actuall.append([])
        replicas_find.append([])
        for replica_num in range(3):
            replicas_actuall[i].append(0)
            replicas_find[i].append(0)
    for i in range(len(find_nodes)):
        index_popu=int(popu[i]*10)
        bar_popu_actual[index_popu].append(actual_nodes[i])
        bar_popu_find[index_popu].append(find_nodes[i])
        replicas_actuall[index_popu][actual_nodes[i]-1]+=1
        replicas_find[index_popu][find_nodes[i]-1]+=1
    
    # plot
    colors = ['blue', 'red', 'green', 'skyblue', 'pink', 'yellow', 'purple', 'black', 'cyan', 'orange','gold','brown','grey','lime']
    markers=['.','o','v','^','<','>','1','2','3','4','s','p','*','h','H','+','x','D','d','|','_']
    print(';',find_nodes==actual_nodes)
    for i in range(11):
        print(i,',',bar_popu_actual[i]==bar_popu_find[i])
    plt.figure()
    for i in range(5,11):
        plt.plot(range(len(bar_popu_actual[i])),np.array(bar_popu_find[i])-np.array(bar_popu_actual[i]),color=colors[i],label='popu-.'+str(i))
    plt.title('find-actual')
    plt.legend()
    plt.show()

    
    # plt.figure()
    # plt.subplot(121)
    # bar_width=.085
    # now_bar_width=0
    # for i in range(11):
    #     plt.bar([1+now_bar_width,2+now_bar_width,3+now_bar_width],replicas_actuall[i],width=bar_width,color=colors[i],label='popu-.'+str(i))#,marker=markers[i])
    #     now_bar_width+=bar_width
    # plt.xticks([1.4,2.4,3.4], [1,2,3])
    # plt.legend()
    # plt.title('actual')
    # plt.ylim([0,2900])
    # plt.subplot(122)
    # now_bar_width=0
    # for i in range(11):
    #     plt.bar([1+now_bar_width,2+now_bar_width,3+now_bar_width],replicas_find[i],width=bar_width,color=colors[i],label='popu-.'+str(i))#,marker=markers[i])
    #     now_bar_width+=bar_width
    # plt.xticks([1.4,2.4,3.4], [1,2,3])
    # plt.legend()
    # plt.title('find')
    # plt.ylim([0,2700])
    # plt.show()


