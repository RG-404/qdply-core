#!/bin/sh

dt=$(date '+%d/%m/%Y %H:%M:%S');

helpFunction()
{
   echo ""
   echo "Usage: $0 -a name -b path -c port"
   echo -e "\t-t Description of what is type"
   echo -e "\t-f Description of what is path"
   echo -e "\t-p Description of what is port"
   echo -e "\t-n Description of what is name"
   exit 1 # Exit script after printing help
}

while getopts "n:f:p:t:" opt
do
   case "$opt" in
      n ) name="$OPTARG" ;;
      f ) path="$OPTARG" ;;
      p ) port="$OPTARG" ;;
      t ) type="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$name" ] && [ -z "$path" ] && [ -z "$port" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
   return 11
fi

if [ $type == "react" ]
then
    echo "Staring REACT BUILD...."
    npm --prefix $path run build
    echo "Serving using pm2...."
    pm2 serve "$path/build" $port --name "$name-r" --spa
    return 0
elif [ $type == "static" ]
then
    echo "Serving static files using pm2..."
    pm2 serve $path $port --name "$name-s"
    return 0
else 
    return 13
fi