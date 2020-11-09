@REM: test :
@REM: 初始分配:zipf
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 1 nopassive noactive noexpel 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 2 nopassive noactive noexpel 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 nopassive noactive noexpel 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 4 nopassive noactive noexpel 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 5 nopassive noactive noexpel 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 6 nopassive noactive noexpel 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 7 nopassive noactive noexpel 100
@REM: 初始分配:zipfr
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipfr 1 nopassive noactive noexpel 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipfr 2 nopassive noactive noexpel 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipfr 3 nopassive noactive noexpel 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipfr 4 nopassive noactive noexpel 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipfr 5 nopassive noactive noexpel 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipfr 6 nopassive noactive noexpel 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipfr 7 nopassive noactive noexpel 100
@REM: above : done

@REM: 驱逐策略：period的选择
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 1 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 2 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 3 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 4 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 5 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 6 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 7 1
@REM: 驱逐策略 LLU: 5个，保证的是，llu驱逐个数与lifetime驱逐个数基本相同；period选3
@REM: LLU的空间使用探寻：run_times=1即可，需要去打开Storage文件的开关，这个开关在不做说明的时候，都处于关闭状态。
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 llu 2 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 llu 3 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 llu 4 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 llu 5 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 llu 6 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 1 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 2 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 3 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 4 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 5 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 6 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 curve 7 1
@REM: LLU在zipf/zipfr下的表现
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 llu 5 100
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipfr 3 load 4 calculate 3 llu 5 100

@REM: 被动比较： popularity与load
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 popularity 4 random 3 llu 5 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 random 3 llu 5 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 popularity 4 calculate 3 llu 5 1
@REM E:/Program_Files/Python/python.exe d:/Languages/PythonSpace/AnalysisSanning/finalTest/RunReplica_zipf.py zipf 3 load 4 calculate 3 llu 5 1