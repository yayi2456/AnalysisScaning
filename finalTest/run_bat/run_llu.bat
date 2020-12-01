
rem llu
rem called by ../new_run.bat

set distribution_type=%1

if "%distribution_type%"=="" (
    echo [%date% %time%]:[run_llu.bat]: distribution type is needed!
    exit 1
)

@REM rem passive only:
@REM set llu_param_pn=1
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive noactive llu %llu_param_pn% %total_run_times%
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% random %passive_param% noactive llu %llu_param_pn% %total_run_times%
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% popularity %passive_param% noactive llu %llu_param_pn% %total_run_times%
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% load %passive_param% noactive llu %llu_param_pn% %total_run_times%
@REM set llu_param_pn=2
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive noactive llu %llu_param_pn% %total_run_times%
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% random %passive_param% noactive llu %llu_param_pn% %total_run_times%
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% popularity %passive_param% noactive llu %llu_param_pn% %total_run_times%
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% load %passive_param% noactive llu %llu_param_pn% %total_run_times%
@REM set llu_param_pn=

@REM rem active only
@REM set llu_param_na=2
@REM @REM have run: python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive noactive llu %llu_param_na% %total_run_times%
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive random %active_param% llu %llu_param_na% %total_run_times%
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive calculate %active_param% llu %llu_param_na% %total_run_times%
@REM set llu_param_na=3
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive noactive llu %llu_param_na% %total_run_times%
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive random %active_param% llu %llu_param_na% %total_run_times%
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% nopassive calculate %active_param% llu %llu_param_na% %total_run_times%
@REM set llu_param_na=

rem mixed
set llu_param_pa=4
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% random %passive_param% random %active_param% llu %llu_param_pa% %total_run_times%
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% random %passive_param% calculate %active_param% llu %llu_param_pa% %total_run_times%
@REM python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% popularity %passive_param% random %active_param% llu %llu_param_pa% %total_run_times%
python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% popularity %passive_param% calculate %active_param% llu %llu_param_pa% %total_run_times%
set llu_param_pa=

rem llu itself. 5 is contained
@REM for /L %%i in (1,1,5) do (
@REM     if %%i NEQ 4 (
@REM         python ./finalTest/RunReplica_zipf.py %distribution_type% %replica_num% popularity %passive_param% calculate %active_param% llu %%i %total_run_times%
@REM     )
@REM )

set distribution_type=
