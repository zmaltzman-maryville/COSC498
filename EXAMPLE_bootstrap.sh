#!/bin/sh

# Update the path to your venv activate script
# Comment out if venv is unused
. PATH/TO/VENV/ACTIVATE

# Starts the server. Add "--debug" to the end to run in debug mode
. flask --app trackpack run --debug