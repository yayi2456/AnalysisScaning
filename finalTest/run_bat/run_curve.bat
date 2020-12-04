
rem curve
rem called by ../new_run.bat

set distribution_type=%1
set curve_param=3

if "%distribution_type%"=="" (
    echo [%date% %time%]:[run_llu.bat]: distribution type is needed!
    exit 1
)

@REM rem passive only:

python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive noactive curve %curve_param% %total_run_times%
python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% random %passive_param% noactive curve %curve_param% %total_run_times%
python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% popularity %passive_param% noactive curve %curve_param% %total_run_times%
python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% load %passive_param% noactive curve %curve_param% %total_run_times%


@REM rem active only

@REM have run: python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive noactive curve %curve_param% %total_run_times%
python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive random %active_param% curve %curve_param% %total_run_times%
python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive calculate %active_param% curve %curve_param% %total_run_times%

rem random
@REM have run: python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive noactive curve %curve_param% %total_run_times%
python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% random %passive_param% noactive curve %curve_param% %total_run_times%
python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive random %active_param% curve %curve_param% %total_run_times%
python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% random %passive_param% random %active_param% curve %curve_param% %total_run_times%


rem mixed

@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% random %passive_param% random %active_param% curve %curve_param% %total_run_times%
python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% random %passive_param% calculate %active_param% curve %curve_param% %total_run_times%
python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% popularity %passive_param% random %active_param% curve %curve_param% %total_run_times%
python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% popularity %passive_param% calculate %active_param% curve %curve_param% %total_run_times%


rem curve itself. 5 is contained
for /L %%i in (1,1,7) do (
    if %%i NEQ %curve_param% (
        python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% popularity %passive_param% calculate %active_param% curve %%i %total_run_times%
    )
)

set curve_param=
