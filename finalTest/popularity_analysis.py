import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

node_sum=10

def plot_popularity(epoch):
    popu_dicts=[]
    for nodeid in range(node_sum):
        fname=('D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\calculate3-llu8-popularity-node'+str(nodeid)+'-runtime.txt')
        # popu_dicts.append({})
        with open(fname, 'r') as datafile:
            j=0
            for dataline in datafile:
                datalineitem = dataline.split('$')
                epoch_id=int(datalineitem[0])
                if epoch_id==epoch and j==1:
                # print(datalineitem[1])
                    popu_dicts.append(json.loads(datalineitem[1]))
                elif epoch_id==epoch and j==0:
                    j=1
    #
    # print(popu_dicts[1])
    #node_sum
    fig = plt.figure()
    ax3=plt.axes(projection='3d')
    # ax = Axes3D(fig)
    # for i in range(len(use_ratio01)):
    #     ax.scatter([i+b01-begin_static for j in range(b01,e01,s01)], [j for j in range(b01,e01,s01)], use_ratio01[i])
    x=range(0,node_sum)
    y=range(654000,epoch+1)
    X,Y=np.meshgrid(y,x)
    plot_array_array=[]
    for nid in range(node_sum):
        plot_array_array.append([])
        for bid in range(0,epoch-654000+1):
            plot_array_array[nid].append(-1)
        for kvs in popu_dicts[nid].items():
            plot_array_array[nid][int(kvs[0])]=kvs[1][0]+kvs[1][1]
            # print(kvs[0])
    fname_store='D:\\Languages\\PythonSpace\\AnalysisSanning\\finalTest\\finalRes\\debug\\excel-paint.txt'
    with open(fname_store,'w')as datafile:
        for i in x:
            pstring=''
            for j in range(0,epoch-654000+1):
                if j!=epoch-654000:
                    pstring+=str(plot_array_array[i][j])+','
                else:
                    pstring+=str(plot_array_array[i][j])
            print(pstring,file=datafile)
    

    # ax3.bar(np.array(X).flatten(),np.array(Y).flatten(),np.array(plot_array_array).flatten())
    ax3.plot_surface(X,Y,np.array(plot_array_array))#,cmap='rainbow')
    # plt.plot(range(b01,e01,s01),use_ratio01[2225-b01])
    plt.xlabel('blocks')
    plt.ylabel('nodes')
    plt.show()

if __name__=='__main__':
    begin_epoch=654010
    plot_popularity(begin_epoch+30)