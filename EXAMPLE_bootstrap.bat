@echo off

:: Update the path to your venv activate script
:: Comment out if venv is unused
call PATH\TO\VENV\ACTIVATE

:: Starts the server. Add "--debug" to the end to run in debug mode
call flask --app trackpack run --debug