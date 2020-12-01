D:
cd D:\Languages\PythonSpace\AnalysisSanning\finalTest\finalRes\experimenta
rem thisdir: ./1-initial/zipf
@echo off
set this_dir=%1
if "%this_dir%"=="" (
    echo [%date% %time%]:[merge_1.bat]: dir is needed!
    exit 1
)
cd %this_dir%
set DIR="%cd%"
echo [mergefile]: directory: %cd%

setlocal enabledelayedexpansion
set filenames=Combined-A.csv
for /f "delims=" %%i in ('"dir /b/on A*.txt"') do (
    set filenames=!filenames! %%i
)
echo [%this_dir%]: contacted filename: %filenames%

python d:/Languages/PythonSpace/AnalysisSanning/finalTest/get_writefile.py %filenames%

set this_dir=
set DIR=
set filenames=
