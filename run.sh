# !/bin/bash

echo City
read city
echo "FORECAST or Date (2024-09-28)" 
read type
echo "API KEY"
read API_KEY

python3 main.py "$city" $type $API_KEY
