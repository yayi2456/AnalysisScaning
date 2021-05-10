rem llu
rem called by ../new_run.bat

echo [%date% %time%]: BS_Test.bat is running...
rem change consenssu
python ./finalTest/BS_Test.py 2 2 256
python ./finalTest/BS_Test.py 2 4 256
python ./finalTest/BS_Test.py 2 8 256
python ./finalTest/BS_Test.py 2 16 256
python ./finalTest/BS_Test.py 2 32 256
python ./finalTest/BS_Test.py 2 64 256
python ./finalTest/BS_Test.py 2 128 256

rem k
python ./finalTest/BS_Test.py 2 32 256
python ./finalTest/BS_Test.py 4 32 256
python ./finalTest/BS_Test.py 8 32 256
python ./finalTest/BS_Test.py 16 32 256
python ./finalTest/BS_Test.py 32 32 256
python ./finalTest/BS_Test.py 64 32 256
python ./finalTest/BS_Test.py 128 32 256
python ./finalTest/BS_Test.py 256 32 256
