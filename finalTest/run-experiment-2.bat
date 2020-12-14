@REM: test :
@REM: 初始分配:zipf
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 1 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 2 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 4 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 5 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 6 nopassive noactive noexpel 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 7 nopassive noactive noexpel 100
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
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 1 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 2 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 4 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 5 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 6 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 7 100
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
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 1 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 2 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 3 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 4 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 5 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 6 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 7 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 8 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 1 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 2 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 3 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 4 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 5 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 6 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 7 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 noexpel 1
@REM: LLU在zipf/zipf8下的表现: 使用llu8进行下面的实验
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 llu 8 100

@REM: 被动比较： popularity与load
@REM: zipf
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 popularity 10 noactive llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 noactive llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 popularity 10 calculate 3 llu 8 100
@REM @REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 popularity 10 noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 popularity 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 3 100
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
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive noactive llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 random 10 noactive llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 random 10 random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 random 10 noactive curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive random 3 curve 3 100 
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 random 10 random 3 curve 3 100 
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
@REM @REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 random 10 random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 random 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 popularity 10 random 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 random 10 random 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 random 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 random 3 curve 3 100 
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 popularity 10 random 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 3 100
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
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive calculate 3 curve 3 100 
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 nopassive calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 nopassive calculate 3 curve 3 100
@REM: zipf8
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 random 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 random 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf8 3 load 10 calculate 3 llu 8 100

@REM: extra test
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 8 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive random 3 llu 8 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive calculate 3 llu 2 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 noactive llu 8 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive noactive llu 8 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive noactive llu 3 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive noactive llu 2 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive noactive llu 1 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive noactive llu 5 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive noactive noexpel 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 noactive noexpel 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 popularity 10 noactive noexpel 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive calculate 3 noexpel 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 noexpel 1
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py uniform 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 access 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 access 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 llu 8 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 calculate 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 raccess 3 curve 3 100
@REM python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 10 raccess 3 llu 8 100

python d:/Languages/PythonSpace/AnalysisSanning/finalTest/DS_CLIENT.py zipf 3 popularity 10 calculate 3 curve 3 100
python d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 popularity 10 calvary 3 curve 3 100