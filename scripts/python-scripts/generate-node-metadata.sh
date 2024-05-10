#/bin/bash

python_file="$1"
info_file="$2"
classify-python-code.sh $python_file $info_file 2> /dev/null
file=$info_file 

KEYWORDS=("Modules:" "Function:" "Method:" "Class:" "Code:")
code_file=$(head -n1 $file | awk -F "|" '{print $NF}' | cut -d ":" -f 2)
for keyword in "${KEYWORDS[@]}" 
do
  if [[ $keyword == "Function:" ]]; then 
    function_names=$(cat $file | grep $keyword | cut -d "|" -f 1 | cut -d ":" -f 2)
    if [[ -n $function_names ]]; then 
      while read function_name; do 
        first_line_of_code=$(cat $file | grep "Function line: $function_name " | head -n1 | awk -F "|" '{print $(NF - 1)}' | cut -d ":" -f 2)
        first_line_of_code=$(cat $file | grep "Function: $function_name " | awk -F "|" '{print $(NF - 1)}' | cut -d ":" -f 2)
        if [[ $first_line_of_code -lt 0 ]]
        then 
          first_line_of_code=$((0))
        fi 
        last_line_of_code=$(cat $file | grep "Function line: $function_name " | tail -n1 | awk -F "|" '{print $(NF - 1)}' | cut -d ":" -f 2)
        function_metadata=$(cat $file | grep "$keyword $function_name " | awk -F "|" '{print $2}')
        echo "#- BEGIN FUNCTION: $function_name -#"
        echo "Function metadata: $function_metadata-$first_line_of_code,$last_line_of_code"
        sed -n "${first_line_of_code},${last_line_of_code}p" $code_file 2> /dev/null
        echo "#- END FUNCTION: $function_name -#"
      done <<< "$function_names"
    fi 
    
  elif [[ $keyword == "Method:" ]]; then 
    class_names=$(cat $file | grep $keyword | cut -d "|" -f 2 | cut -d ":" -f 2 | cut -d " " -f 2 | uniq)
    NOT_REPEAT_CLASSES=$class_names 
    if [[ -n $class_names ]]; then 
      while read class_name; do 
        methods_of_class=$(cat $file | grep $keyword | grep "$class_name ")  
        class_metadata=$(cat $file | grep "Class: $class_name " | awk -F "|" '{print $2}' | grep "Parent" | cut -d ":" -f 2)
        class_definition_line=$(cat $file | grep "Class: $class_name " | grep "Parent" | awk -F "|" '{print $(NF - 1)}'| cut -d ":" -f 2)
        while read method_line ; do 
          method=$(echo $method_line | awk -F "|" '{print $1}' | cut -d ":" -f 2 | cut -d " " -f 2)
          # method_definition_line=$(echo $method_line | awk -F "|" '{print $(NF-1)}' | cut -d ":" -f 2)
          method_definition_line=$(cat $file | grep "Method: $method " | grep " $class_name " | awk -F "|" '{print $(NF-1)}' | cut -d ":" -f 2)
          method_metadata=$(echo $method_line | awk -F "|" '{print $3}')
          method_begin_line=$(cat $file | grep "Method line: $method " | grep " $class_name " | head -n1 | awk -F "|" '{print $(NF-1)}' | cut -d ":" -f 2)
          method_end_line=$(cat $file | grep "Method line: $method " | grep " $class_name " | tail -n1 | awk -F "|" '{print $(NF-1)}' | cut -d ":" -f 2)
          echo "#- BEGIN METHOD OF CLASS $class_name: $method -#"
          echo "Method metadata: $method_metadata-$method_begin_line,$method_end_line" 
          sed -n "${method_definition_line},${method_end_line}p" $code_file 2> /dev/null
          echo "#- END METHOD OF CLASS $class_name: $method -#"
        done <<< "$methods_of_class" 
        echo "#- BEGIN CLASS: $class_name #-"
        echo "Class metadata: $class_metadata-$class_definition_line,$method_end_line"
        sed -n "${class_definition_line},${method_end_line}p" $code_file 2> /dev/null
        echo "#- END CLASS: $class_name #-"
      done <<< "$class_names"
    else 
     class_names=$(cat $file | grep "Class:" | cut -d "|" -f 1 | cut -d ":" -f 2 | cut -d " " -f 2 | uniq)
     if [[ -n $class_names ]]; then 
      while read class_name; do 
        begin_class_line=$(cat $file | grep "Class: $class_name " | awk -F "|" '{print $(NF - 1)}' | cut -d ":" -f 2)
        end_class_line=$(cat $file | grep "Class line: $class_name " | tail -n1 | awk -F "|" '{print $(NF - 1)}' | cut -d ":" -f 2)
        class_metadata=$(cat $file | grep "Class: $class_name " | awk -F "|" '{print $2}' | grep "Parent" | cut -d ":" -f 2)
        echo "#- BEGIN CLASS: $class_name #-"
        echo "Class metadata: $class_metadata-$begin_class_line,$end_class_line"
        sed -n "${begin_class_line},${end_class_line}p" $code_file 2> /dev/null
        echo "#- END CLASS: $class_name #-"
      done <<< "$class_names"
     fi  
    fi 

  elif [[ $keyword == "Class:" && -n $NOT_REPEAT_CLASSES ]]; then 
    class_names=$(cat $file | awk -F "|" '$1 ~ /Class:/' | cut -d "|" -f 1 | cut -d ":" -f 2 | cut -d " " -f 2 | uniq)
     if [[ -n $class_names ]]; then 
      while read class_name; do 
        for not_repeat_class_name in "${NOT_REPEAT_CLASSES[@]}"; do 
          if [[ $class_name == $not_repeat_class_name ]]; then 
            skip='true'
          else 
            skip=
          fi 
          if [[ -z $skip ]]; then 
            begin_class_line=$(cat $file | grep "Class: $class_name " | awk -F "|" '{print $(NF - 1)}' | cut -d ":" -f 2)
            end_class_line=$(cat $file | grep "Class line: $class_name " | tail -n1 | awk -F "|" '{print $(NF - 1)}' | cut -d ":" -f 2)
            class_metadata=$(cat $file | grep "Class: $class_name " | awk -F "|" '{print $2}' | grep "Parent" | cut -d ":" -f 2)
            echo "#- BEGIN CLASS: $class_name #-"
            echo "Class metadata: $class_metadata-$begin_class_line,$end_class_line"
            sed -n "${begin_class_line},${end_class_line}p" $code_file 2> /dev/null
            echo "#- END CLASS: $class_name #-"
          fi 
        done 
      done <<< "$class_names"
  fi 

  elif [[ $keyword == "Modules:" ]]; then 
    begin_module_line=$(cat $file | grep $keyword | head -n1 | awk -F "|" '{print $(NF-1)}' | cut -d ":" -f 2)
    end_module_line=$(cat $file | grep $keyword | tail -n1 | awk -F "|" '{print $(NF-1)}' | cut -d ":" -f 2)
    if [[ -n $end_module_line ]]; then 
      echo "#- BEGIN MODULES -#"
      sed -n "${begin_module_line},${end_module_line}p" $code_file 2> /dev/null
      echo "#- END MODULES -#"
    fi 
  fi
done 

begin_block=
end_code_block=
while read file_line; do 
  is_code_line=$(echo $file_line | grep "Code:")
  if [[ -n $is_code_line && -z $begin_block ]]; then 
    line_of_code=$(echo $file_line | awk -F "|" '{print $(NF-1)}' | cut -d ":" -f 2)
    if [[ -z $begin_block ]]; then 
      begin_block=$line_of_code
    fi 
  elif [[ -z $is_code_line && -n $begin_block ]]; then 
    end_code_block=$line_of_code
    echo "#- BEGIN BLOCK OF CODE -#"
    echo "Code block domain: $begin_block,$end_code_block"
    sed -n "${begin_block},${end_code_block}p" $code_file 2> /dev/null
    echo "#- END BLOCK OF CODE -#"
    last_reseted_begin=$begin_block
    last_reseted_end=$end_code_block
    begin_block=

  elif [[ -n $is_code_line && -n $begin_block ]]; then 
    line_of_code=$(echo $file_line | awk -F "|" '{print $(NF-1)}' | cut -d ":" -f 2)
    end_code_block=$line_of_code
  fi 

done < $file

if [[ $last_reseted_begin -ne $begin_block && $last_reseted_end -ne $end_code_block ]]; 
then 
  echo "#- BEGIN BLOCK OF CODE -#"
  echo "Code block domain: $begin_block,$end_code_block"
  sed -n "${begin_block},${end_code_block}p" $code_file 2> /dev/null
fi 

echo "#- END BLOCK OF CODE -#"