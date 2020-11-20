import json
import numpy as np
import sys

'''
args: argv 1-...
0: this running file name
1: write_filename
2-...: input filename
'''


def write_in_file():
    '''
    write len(sys.argv)-1 input file into 1 file.
    colunm1 colunm2 column3 ...
    x   y1  y2...
    '''
    if len(sys.argv)<2:
        exit(1)
    # get input files and write file name
    input_file_num=len(sys.argv)-1
    input_file_name=[]
    write_file_name=sys.argv[1]
    for input_name in sys.argv[2:]:
        input_file_name.append(input_name)
    with open(write_file_name,'w') as write_file:
        files_opend=[]
        for i in input_file_name:
            files_opend.append(open(i))
        lists=[]
        # get begin,end,step
        begin_end_step=files_opend[0].readline()
        datalineitem = begin_end_step.split()
        begin=int(datalineitem[0])
        ends = int(datalineitem[1])
        step = int(datalineitem[2])
        # read others file and discard the 1st line
        for i in files_opend[1:]:
            i.readline()
        # get each list
        for i in files_opend:
            dataline=i.readline()
            avg_time=json.loads(dataline)
            lists.append(avg_time)
        # composed
        online=""
        for i in range(begin,ends,step):
            online=str(i)
            for one_list in lists:
                online=online+','+str(one_list[i-begin])
            # print(online,file=write_file)
            write_file.write(online+'\n')
        
    return

if __name__=='__main__':
    write_in_file()

    

