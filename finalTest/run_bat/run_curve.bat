
rem curve
rem called by ../new_run.bat

set distribution_type=%1
set curve_param=3

if "%distribution_type%"=="" (
    echo [%date% %time%]:[run_llu.bat]: distribution type is needed!
    exit 1
)

rem initial assign amount
@REM for /L %%i in (1,1,7) do (
@REM     if %%i NEQ %replica_num% (
@REM         python ./finalTest/DS_CLIENT.py %distribution_type% %%i nopassive noactive noexpel %total_run_times%
@REM     )
@REM )

@REM rem passive only:

@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% nopassive noactive curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% random %passive_param% noactive curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% popularity %passive_param% noactive curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% load %passive_param% noactive curve %curve_param% %total_run_times%
python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% kad %passive_param% noactive curve %curve_param% %total_run_times%

@REM rem active only

@REM have run: python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% nopassive noactive curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% nopassive random %active_param% curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% nopassive calculate %active_param% curve %curve_param% %total_run_times%

rem random
@REM have run: python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% nopassive noactive curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% random %passive_param% noactive curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% nopassive random %active_param% curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% random %passive_param% random %active_param% curve %curve_param% %total_run_times%


rem mixed

@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% random %passive_param% random %active_param% curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% random %passive_param% calculate %active_param% curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% popularity %passive_param% random %active_param% curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% popularity %passive_param% calculate %active_param% curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% load %passive_param% random %active_param% curve %curve_param% %total_run_times%
@REM python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% load %passive_param% calculate %active_param% curve %curve_param% %total_run_times%


rem curve itself. 5 is contained
@REM for /L %%i in (1,1,7) do (
@REM     if %%i NEQ %curve_param% (
@REM         python ./finalTest/DS_CLIENT.py %distribution_type% %replica_num% popularity %passive_param% calculate %active_param% curve %%i %total_run_times%
@REM     )
@REM )

set curve_param=
