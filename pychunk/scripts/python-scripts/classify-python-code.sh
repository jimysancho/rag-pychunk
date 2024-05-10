
#!/bin/bash

get_class_info() {
  local line=$1
  local class_name=$(echo $line | cut -d " " -f 2)
  local parent_class=$(echo $class_name | cut -d "(" -f 2)

  if [[ $parent_class != $class_name ]]
  then 
    local parent_class=$(echo $parent_class | cut -d ")" -f 1)
    local class_name=$(echo $class_name | cut -d "(" -f 1)
  else 
    local class_name=$(echo $class_name | cut -d ":" -f 1)
    local parent_class=""
  fi 

  echo $class_name $parent_class
}

get_function_info() {
  local function_line=$1
  local static_method=$2

  local is_async=$(echo $function_line | grep "async")
  if [[ -n $is_async ]]; then 
    local function_name=$(echo $function_line | cut -d " " -f 3 | cut -d "(" -f 1)
  else 
    local function_name=$(echo $function_line | cut -d " " -f 2 | cut -d "(" -f 1)
  fi 
  local args=$(echo $function_line | cut -d "(" -f 2 | cut -d ")" -f 1 | sed 's/,//g')
  self_in_line=$(echo $function_line | grep self)
  if [[ -n $self_in_line || -n $static_method ]]
  then 
    method="method"
    if [[ ! -n $static_method ]]; then 
      args="${args:4}" 
    else 
      args=$args
    fi 
  else 
    method="function" 
  fi 
  echo $method $function_name $args
}

classify_python_code() {

  file=$1
  line_num=0
  while IFS= read -r line; do
      ((line_num++))
      if [[ $line =~ [^[:space:][:blank:]] ]]
      then
        tabs=$(echo "$line" | grep -o "^[[:blank:]]*" | tr -d '\n' | wc -c)
        if [[ $tabs -eq 0 ]]
        then 
          CLASS_NAME=''
          FUNCTION_NAME=''
          METHOD=''
          first_word=$(echo $line | cut -d " " -f 1)
          second_word=$(echo $line | cut -d " " -f 2)
          decorator=
          decorator_line=
          case $first_word in 
            @*)
              decorator=$first_word
              decorator_line=$line_num
              ;;
            class) 
              class_info=$(get_class_info "$line")
              read class_name parent_class <<< $class_info
              CLASS_NAME=$class_name
              if [[ -n $decorator_line ]]; then 
                class_line=$decorator_line
              else
                class_line=$line_num
              fi  
              echo "Class: $class_name | Parent class: $parent_class | Line of code: $class_line | File: $file"
              ;;
            def|async) 
              if [[ ("$second_word" = "def" && "$first_word" = "async") || $first_word = "def" ]]; then 
                function_info=$(get_function_info "$line")
                read method function_name args <<< $function_info 
                FUNCTION_NAME=$function_name
                if [[ -n $decorator_line ]]; then 
                  func_line=$decorator_line
                else
                  func_line=$line_num
                fi  
                echo "Function: $function_name | Arguments: $args | Line of code: $func_line | File: $file"
              fi 
              ;;
            import|from)
              if [[ $first_word == 'import' ]]
              then 
                modules="${line#* }"
                echo "Modules: $modules | Parent module: $parent_module | Line of code: $line_num | File: $file"
              else 
                parent_module=$(echo $line | cut -d " " -f 2)
                modules="${line#* * * }"
                echo "Modules: $modules | Parent module: $parent_module | Line of code: $line_num | File: $file"
              fi 
              ;;
            *) 
              line="$(echo "$line"|tr -d '\n')"
              echo "Code: $line | Line of code: $line_num | File: $file"
              ;;
          esac 

        elif [[ $tabs -ne 0 && -n $CLASS_NAME ]]
        then 
          first_word=$(echo $line | cut -d " " -f 1)
          second_word=$(echo $line | cut -d " " -f 2)
          decorator=
          decorator_line=
          case $first_word in
            @*)
              decorator=$first_word
              decorator_line=$line_num
              ;;
            def|async)
              if [[ ("$second_word" = "def" && "$first_word" = "async") || $first_word = "def" ]]; then 
                function_info=$(get_function_info "$line" static)
                read method function_name args <<< $function_info
                METHOD=$function_name
                if [[ -n $decorator_line ]]; then 
                  meth_line=$decorator_line
                else
                  meth_line=$line_num
                fi   
                echo "Method: $METHOD | Class: $CLASS_NAME | Arguments: $args | Line of code: $meth_line | File: $file"
              fi
              ;; 
            *)
              echo "Class line: $CLASS_NAME | Method line: $METHOD | Line of code: $line_num | File: $file"
              ;;
          esac 
        elif [[ $tabs -ne 0 && -n $FUNCTION_NAME ]]
        then 
          echo "Function line: $FUNCTION_NAME | Line of code: $line_num | File: $file"
        else
          if [[ -z "${line//[$'\t ']/}" ]]; then 
            line="$(echo "$line"|tr -d '\n')"
            echo "Code: $line | Line of code: $line_num | File: $file"
          fi 
        fi 
      fi     
  done < "$file"
}

# while getopts c: OPTION; do 
#   case $OPTION in 
#     c) commit_state=$OTPARG;;
#     *) echo "Option not valid. -c COMMIT"
#        exit 1
#        ;; 
#   esac 
# done 

# shift $((OPTIND -1))

classify_python_code $1 > $2 2> /dev/null
