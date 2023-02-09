#!/bin/bash

# if number of arguments is not 3
if [ $# -ne 3 ]
    then
    echo "Three arguments are required:"
    echo "1: name of the dicom directory (inputs)"
    echo "2: name of the converter file"
    echo "3: subject index"
    echo "e.g., ./heudiconv_test.sh Yuexin_project heuristic_sequence.py 01"
    echo "Prerequisites:"
    echo "Docker and heudiconv (docker image) are installed/built"
    echo "You should be in the parent directory of the dicom directory (and bids directory if exists)"
    echo "The converter file is in this directory"
    exit 1
fi

dicom_dir=${1}
converter=${2}
isubject=${3}

# Must remove existing .heudiconv/ before another execution
sudo rm -rf ./${dicom_dir}_BIDS/sub-${isubject}
sudo rm -rf ./${dicom_dir}_BIDS/.heudiconv/

: '
## loop through all folders
## If multiple runs exist, outputs from older runs are replaced by those from later runs
cd ./${dicom_dir}/sub-${isubject}/

list_of_folder=(*)

cd ../../

length=${#list_of_folder[@]}

for (( i=0; i<$length; i++))
do 
    printf "\n Now processing ${list_of_folder[i]} \n"
    sudo rm -rf /home/yuexin/Documents/TestData/Yuexin_BIDS2/.heudiconv/01
    docker run --rm -it -v ${PWD}:/base nipy/heudiconv:latest -d /base/${dicom_dir}/sub-{subject}/${list_of_folder[i]}/*.dcm -o /base/${bids_dir}/ -f /base/${converter} -s ${isubject} -c dcm2niix -b --overwrite --minmeta
done
'

: '
## one folder
printf "\n Now processing ${list_of_folder[11]} \n"
docker run --rm -it -v ${PWD}:/base nipy/heudiconv:latest -d /base/${dicom_dir}/sub-{subject}/${list_of_folder[11]}/*.dcm -o /base/${bids_dir}/ -f /base/${converter} -s ${isubject} -c dcm2niix -b --overwrite --minmeta
'

## all in one folder command
printf "\n Now processing ${dicom_dir} sub-${isubject} \n"
docker run --rm -it -v ${PWD}:/base heudiconv --files /base/${dicom_dir}/sub-${isubject}/ -o /base/${dicom_dir}_BIDS/ -f /base/${converter} -s ${isubject} -c dcm2niix -b --overwrite --minmeta

