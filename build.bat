@ECHO OFF

ECHO Clear up dist\...
IF EXIST dist (
    REM -
) ELSE (
    MKDIR dist
)
DEL /F /Q dist\*

ECHO Calling pinliner...
REM REM :: comment: please delete .pyc files before every call of the mdmtoolsreadometerap_bundle - this is implemented in my fork of the pinliner
@REM python src-make\lib\pinliner\pinliner\pinliner.py src -o dist/mdmtoolsreadometerap_bundle.py --verbose
python src-make\lib\pinliner\pinliner\pinliner.py src -o dist/mdmtoolsreadometerap_bundle.py
if %ERRORLEVEL% NEQ 0 ( echo ERROR: Failure && pause && exit /b %errorlevel% )
ECHO Done

ECHO Patching mdmtoolsreadometerap_bundle.py...
ECHO # ... >> dist/mdmtoolsreadometerap_bundle.py
ECHO # print('within mdmtoolsreadometerap_bundle') >> dist/mdmtoolsreadometerap_bundle.py
REM REM :: no need for this, the root package is loaded automatically
@REM ECHO # import mdmtoolsreadometerap_bundle >> dist/mdmtoolsreadometerap_bundle.py
ECHO from src import launcher >> dist/mdmtoolsreadometerap_bundle.py
ECHO launcher.main() >> dist/mdmtoolsreadometerap_bundle.py
ECHO # print('out of mdmtoolsreadometerap_bundle') >> dist/mdmtoolsreadometerap_bundle.py

PUSHD dist
COPY ..\run.bat .\run_read_number_of_records.bat
@REM REN mdmtoolsreadometerap_bundle.py mdmtoolsap.py
@REM powershell -Command "(gc 'run_read_number_of_records.bat' -encoding 'Default') -replace '(dist[/\\])?mdmtoolsreadometerap_bundle.py', 'mdmtoolsap.py' | Out-File -encoding 'Default' 'run_read_number_of_records.bat'"
powershell -Command "(gc 'run_read_number_of_records.bat' -encoding 'Default') -replace '(dist[/\\])?mdmtoolsreadometerap_bundle.py', 'mdmtoolsreadometerap_bundle.py' | Out-File -encoding 'Default' 'run_read_number_of_records.bat'"

ECHO End

