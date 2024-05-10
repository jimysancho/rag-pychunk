#!/bin/bash

# Function/class names file
NAMES_FILE="$1"
curr_dir=$(pwd)
PATH_TO_LOOK="$2"

while IFS= read -r line; do
    name=$(echo $line | cut -d " " -f 1)
    node_id=$(echo $line | cut -d " " -f 2)
    node_file=$(echo $line | cut -d " " -f 3)
    name=$(echo $name | tr -d '[:space:]')
    node_id=$(echo $node_id | tr -d '[:space:]')
    echo "#- BEGIN RELATIONSHIPS OF $name $node_id -#"
    grep -rnw "$PATH_TO_LOOK" -e "$name" --include="*.py" --exclude-dir=".venv" | 
        while read line; do 
            file_path=$(echo $line | cut -d ":" -f 1)
            line_of_occurence=$(echo $line | cut -d ":" -f 2)
            echo "File and line: ${file_path} - $line_of_occurence" 
        done 
    echo "#- END RELATIONSHIPS OF $name $node_id -#"
    
done < "$NAMES_FILE"
