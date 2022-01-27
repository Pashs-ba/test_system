set arg1=%1
set arg2=%2
SET VS=C:\Program Files (x86)\Microsoft Visual Studio\2019
CALL "%VS%\Community\Common7\Tools\VsDevCmd.bat"
cl "%arg1%" /Fe%arg2%