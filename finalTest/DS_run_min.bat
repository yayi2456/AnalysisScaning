@REM: test :
@REM: 初始分配:zipf
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 1 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 2 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 4 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 5 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 6 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 7 nopassive noactive noexpel 100
@REM @REM: 初始分配:zipf8
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 1 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 2 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 4 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 5 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 6 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 7 nopassive noactive noexpel 100

@REM: 驱逐策略：period的选择.zipf和zipf8单独测试
@REM: zipf
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 1 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 2 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 4 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 5 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 6 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 7 100
@REM: zipf8
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 curve 1 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 curve 2 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 curve 4 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 curve 5 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 curve 6 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 curve 7 100
@REM: 驱逐策略 LLU: 8个，保证的是，llu驱逐个数与lifetime驱逐个数基本相同；period选3
@REM: LLU的空间使用探寻：run_times=1即可，需要去打开Storage文件的开关，这个开关在不做说明的时候，都处于关闭状态。
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 1 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 2 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 3 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 4 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 5 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 6 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 7 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 8 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 1 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 2 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 3 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 4 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 5 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 6 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 7 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 noexpel 1
@REM: LLU在zipf/zipf8下的表现: 使用llu8进行下面的实验
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 llu 8 100

@REM: 被动比较： popularity与load
@REM: zipf
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 popularity 10 noactive llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 noactive llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 popularity 10 calculate 3 llu 8 100
@REM @REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 popularity 10 noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 popularity 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 3 100
@REM: zipf8
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 popularity 10 noactive llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 noactive llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 popularity 10 calculate 3 llu 8 100
@REM @REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 popularity 10 noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 popularity 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 curve 3 100
@REM: uniform
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py uniform 3 popularity 10 noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py uniform 3 load 10 noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py uniform 3 popularity 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py uniform 3 load 10 calculate 3 curve 3 100

@REM: 随机复制的效果
@REM:zipf
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive noactive llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 random 10 noactive llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 random 10 random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 random 10 noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive random 3 curve 3 100 
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 random 10 random 3 curve 3 100 
@REM @REM:zipf8
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 nopassive noactive llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 random 10 noactive llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 nopassive random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 random 10 random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 nopassive noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 random 10 noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 nopassive random 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 random 10 random 3 curve 3 100
@REM: uniform
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py uniform 3 nopassive noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py uniform 3 random 10 noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py uniform 3 nopassive random 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py uniform 3 random 10 random 3 curve 3 100

@REM: 最终实验：四种复制策略的比较
@REM @REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 random 10 random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 random 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 popularity 10 random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 random 10 random 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 random 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 random 3 curve 3 100 
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 popularity 10 random 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 3 100
@REM:zipf8
@REM @REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 random 10 random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 random 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 popularity 10 random 3 llu 8 100
@REM @REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 llu 8 100
@REM @REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 random 10 random 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 random 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 random 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 popularity 10 random 3 curve 3 100
@REM @REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 curve 3 100

@REM： 补充实验：load/random + noactive
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive calculate 3 curve 3 100 
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 nopassive calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 nopassive calculate 3 curve 3 100
@REM: zipf8
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 random 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 random 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 llu 8 100

@REM: extra test
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 8 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive random 3 llu 8 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive calculate 3 llu 2 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 noactive llu 8 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive noactive llu 8 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive noactive llu 3 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive noactive llu 2 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive noactive llu 1 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive noactive llu 5 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive noactive noexpel 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 noactive noexpel 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 popularity 10 noactive noexpel 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 nopassive calculate 3 noexpel 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 noexpel 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py uniform 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 access 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 access 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 raccess 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 load 10 raccess 3 llu 8 100

@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/DS_CLIENT.py zipf piece 3 popularity 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf piece 3 popularity 10 calvary 3 curve 3 100

@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/DS_CLIENT.py zipf piece 3 random 10 random 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/DS_CLIENT.py zipf piece 3 nopassive random 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/DS_CLIENT.py zipf piece 3 random 10 noactive curve 3 100

@REM python ./finalTest/DS_CLIENT.py zipf piece 3 load 20 calculate 3 curve 3 50

@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 30 calculate 3 curve 3 30
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 load 30 calculate 3 curve 3 30

@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 40 calculate 3 curve 3 25
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 load 40 calculate 3 curve 3 25

@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 50 calculate 3 curve 3 20
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 load 50 calculate 3 curve 3 20

@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 30 noactive curve 3 30
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 40 noactive curve 3 25
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 50 noactive curve 3 20

@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 60 noactive curve 3 20

@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 80 noactive curve 3 12
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 90 noactive curve 3 15
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 95 noactive curve 3 15
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 96 noactive curve 3 15
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 97 noactive curve 3 15
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 100 noactive curve 3 15
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 150 noactive curve 3 15
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 160 noactive curve 3 15
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 200 noactive curve 3 15
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 nopassive 95 kadvary 3 curve 3 15


@rem @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   RUN  US  @@@@@@@

@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 10 noactive curve 3   10 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 50 noactive curve 3   10 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 100 noactive curve 3   10 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 150 noactive curve 3   10 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 200 noactive curve 3   10 2

@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 10 noactive curve 3   10 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 100 noactive curve 3   10 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 200 noactive curve 3   5 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 300 noactive curve 3   4 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 400 noactive curve 3   2 2
@rem min

@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 10 kadvary 3 curve 3   10 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 50 kadvary 3 curve 3   10 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 100 kadvary 3 curve 3   10 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 150 kadvary 3 curve 3   10 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 200 kadvary 3 curve 3   10 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 250 kadvary 3 curve 3   10 2
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 250 kadvary 3 curve 3   10 1
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 10 kadvary 3 curve 3   10 inf
@REM @REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 10 kadvary 3 curve 3   10 0.8
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 10 kadvary 3 curve 3   10 1
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 10 kadvary 3 curve 3   10 2



@rem @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  STOP  @@@@@@@

@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 50 kadvary 3 curve 3   10 inf
@REM @REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 10 kadvary 3 curve 3   10 0.8
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 50 kadvary 3 curve 3   10 1
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 50 kadvary 3 curve 3   10 2

@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 200 kadvary 3 curve 3   1 inf
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 200 kadvary 3 curve 3   1 1
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 200 kadvary 3 curve 3   1 0
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 200 kadvary 3 curve 3   1 2

@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 300 kadvary 3 curve 3   1 inf
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 300 kadvary 3 curve 3   1 1
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 300 kadvary 3 curve 3   1 0
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 300 kadvary 3 curve 3   1 2

@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 200 kadvary 3 curve 3 1 2
@rem 我发现运行次数越少，均衡越差，也就是说，其实负载还会和选中哪些块有关

@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 95 noactive curve 3 1
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 100 noactive curve 3 10
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 150 noactive curve 3 1
@REM python ./finalTest/DS_CLIENT.py zipf piece 3 popularity 160 noactive curve 3 1

@rem 0704只有初始散步
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 10 noactive curve 3   100  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 20 noactive curve 3   50  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 50 noactive curve 3   20  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 100 noactive curve 3   10 noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 200 noactive curve 3   5 noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 300 noactive curve 3   4 noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 400 noactive curve 3   2 noencode

@rem 0704 popkad
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 10 kadvary  3 curve 3   100 2  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 20 kadvary  3 curve 3   50 2  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 50 kadvary  3 curve 3   20 2  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 100 kadvary 3 curve 3   10 2 noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 200 kadvary 3 curve 3   5 2 noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 300 kadvary 3 curve 3   4 2 noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 400 kadvary 3 curve 3   2 2 noencode

@rem 0704 encoded
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 10 kadvary  3 curve 3   100 2  encode 4 2 6
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 20 kadvary  3 curve 3   50 2  encode 4 2 6
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 50 kadvary  3 curve 3   20 2  encode 4 2 6
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 100 kadvary 3 curve 3   10 2 encode 4 2 6
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 200 kadvary 3 curve 3   5 2 encode 4 2 6
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 300 kadvary 3 curve 3   4 2 encode 4 2 6

@rem 0717只有初始散步
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 10 noactive curve 3   100  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 20 noactive curve 3   50  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 50 noactive curve 3   20  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 nopassive 300 noactive curve 3   4  noencode

@rem 0717 popkad
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 10 kadvary  3 curve 3   100 0  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 20 kadvary  3 curve 3   50 0  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 50 kadvary  3 curve 3   20 0  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 load_kad 10 kadvary  3 curve 3   100 0  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 load_kad 20 kadvary  3 curve 3   50 0  noencode
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 load_kad 50 kadvary  3 curve 3   20 0  noencode
python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 10 kadvary  3 curve 3   100 0  noencode
python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 20 kadvary  3 curve 3   50 0  noencode
python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 50 kadvary  3 curve 3   20 0  noencode


@rem 0717 encoded
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 10 kadvary  3 curve 3   100 0  encode 4 2 6
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 20 kadvary  3 curve 3   50 0  encode 4 2 6
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 pop_kad 50 kadvary  3 curve 3   20 0  encode 4 2 6
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 load_kad 10 kadvary  3 curve 3   100 0  encode 4 2 6
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 load_kad 20 kadvary  3 curve 3   50 0  encode 4 2 6
@REM python ./finalTest/DS_CLIENT.py zipf piecekad 3 load_kad 50 kadvary  3 curve 3   20 0  encode 4 2 6
python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 10 kadvary  3 curve 3   100 0  encode 4 2 6
python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 20 kadvary  3 curve 3   50 0  encode 4 2 6
python ./finalTest/DS_CLIENT.py zipf piecekad 3 kad 50 kadvary  3 curve 3   20 0  encode 4 2 6
