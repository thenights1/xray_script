#!/bin/bash

cd /root/xray
# Generate filename with date
FILENAME="output_$(date +'%Y%m%d')"

# Run the Python script with the generated filename as argument, in the background
python3 /your_script_path/bat.py -o "$FILENAME" -html "$FILENAME" &

# Capture the PID of the background process
PID=$!

# Save the PID to a file
echo $PID > /tmp/my_script.pid

# Wait until tomorrow 3:00 AM
sleep 21600

# Check if the process is still running and kill it if necessary
if ps -p $PID > /dev/null; then
    echo "Killing process $PID"
    kill $PID
    pkill xray
fi