@echo off
rem global
set replica_num=3
set passive_param=10
set active_param=3
set total_run_times=100
echo [%date% %time%]:[run_new]: new running start...
D:
cd d:/Languages/PythonSpace/AnalysisSanning

@REM set distribution_type=zipfr
rem call curve
@REM call ./finalTest/run_bat/run_curve.bat %distribution_type%
rem call llu
@REM call ./finalTest/run_bat/run_llu.bat %distribution_type%

set distribution_type=zipf
rem call curve
call ./finalTest/run_bat/run_curve.bat %distribution_type%

@REM set distribution_type=zipf
@REM rem call llu
@REM call ./finalTest/run_bat/run_llu.bat %distribution_type%


set replica_num=
set passive_param=
set active_param=
set total_run_times=