@ECHO OFF
SETLOCAL enabledelayedexpansion


@REM put your files here
SET "DATA_FILE=Outputs/R123456.sav"



ECHO -
ECHO 1. read counts
ECHO read from: %DATA_FILE%
FOR /f "delims=" %%a in ('python src/launcher.py --program read_records_count --inpfile "%DATA_FILE%" --format autodetect ^&^& if !ERRORLEVEL! NEQ 0 ( echo ERROR: Failure ^&^& pause ^&^& goto CLEANUP ^&^& exit /b !ERRORLEVEL! )') DO SET "OUTPUT=%%a"
if !ERRORLEVEL! NEQ 0 ( echo ERROR: Failure && pause && goto CLEANUP && exit /b !ERRORLEVEL! )

ECHO -
ECHO The number of records is: !OUTPUT!
ECHO -


@REM ECHO -
@REM ECHO 7 del .json temporary files
@REM @REM DEL "%DATA_FILE%.json"

ECHO -
:CLEANUP
ECHO 999. Clean up
REM REM :: comment: just deleting trach .pyc files after the execution - they are saved when modules are loaded from within bndle file created with pinliner
REM REM :: however, it is necessary to delete these .pyc files before every call of the mdmtoolsap_bundle
REM REM :: it means, 6 more times here, in this script; but I don't do it cause I have this added to the linliner code - see my pinliner fork
DEL *.pyc
IF EXIST __pycache__ (
DEL /F /Q __pycache__\*
)
IF EXIST __pycache__ (
RMDIR /Q /S __pycache__
)

ECHO done!
exit /b !ERRORLEVEL!

