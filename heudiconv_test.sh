#!/bin/bash

# if number of arguments is less than 4
if [ $# -lt 4 ]
    then
    echo "Four arguments are required:"
    echo "1: relative path to converter (heuristic.py)"
    echo "2: name of dicom directory (inputs)"
    echo "3: name of bids directory (outputs)"
    echo "4: subject number"
    echo "e.g., ./heudiconv_test.sh xnat_utilities/heudiconv/heuristic.py Yuexin_DICOM2 Yuexin_BIDS2 01"
    echo "Prerequisites:"
    echo "Docker and heudiconv are installed"
    echo "You are in a parent directory of the dicom directory (and bids directory if exists)"
    echo "The converter file is in this curent directory or sub-directories"
    exit 1
fi

converter=${1}
dicom_dir=${2}
bids_dir=${3}
isubject=${4}

# Must remove existing .heudiconv/ before next execution
sudo rm -rf ./${bids_dir}/sub-01
sudo rm -rf ./${bids_dir}/.heudiconv/

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
docker run --rm -it -v ${PWD}:/base nipy/heudiconv:latest -d /base/${dicom_dir}/sub-{subject}/*/*.dcm -o /base/${bids_dir}/ -f /base/${converter} -s ${isubject} -c dcm2niix -b --overwrite --minmeta

