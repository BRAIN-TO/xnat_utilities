# xnat_utilities
Code base for XNAT applications \
Instructions are based on Ubuntu 20.04.5 LTS \
Remember to change everything with <> below according to your own directory structure. 


## Prerequisite
1. Docker engine (installation for [ubuntu](https://github.com/srikash/TheBeesKnees/wiki/Installing-Docker-on-Ubuntu) or official installation documentation [here](https://docs.docker.com/engine/install/))
2. All dicoms are organized in sub-## folders (e.g., sub-01, sub-02...) in the project folder. No subfolders under each subject folder.
3. Virtual environment recommended.

## BIDScoin
https://github.com/srikash/TheBeesKnees/wiki/Converting-DICOMs-to-BIDS-NIfTIs*

\* `qtcreator` may be required for opening the GUI on ubuntu.

## HeuDiConv
https://heudiconv.readthedocs.io/en/latest/

### To get heudiconv (choose one):
1. Latest official heudiconv: run `docker pull nipy/heudiconv:latest` in terminal
2. Our modified version:
    Clone [this repository](https://github.com/845127818virna/heudiconv). Go into the cloned folder, use `docker build -t heudiconv .` to build a docker image called "heudiconv".

Method1 for a single subject:
1. Get a converter file (available in ./heudiconv/)
2. Use one of the following command. \
a. If you use the official version: `docker run --rm -it -v <base_dir>:/base nipy/heudiconv:latest -d <base_dir/dicoms_dir>/sub-{subject}/*.dcm -o <base_dir/bids_dir>/ -f <base_dir/heuristic_dir>/<heuristic_file> -s <subject_index> -c dcm2niix -b --overwrite --minmeta`\
b. If you use our version: `docker run --rm -it -v <base_dir>:/base heudiconv -d <base_dir/dicoms_dir>/sub-{subject}/*.dcm -o <base_dir/bids_dir>/ -f <base_dir/heuristic_dir>/<heuristic_file> -s <subject_index> -c dcm2niix -b --overwrite --minmeta`

\* Relative path from a base directory rather than absolute path is highly recommended. \
\* If you need to run heudiconv on the same data again, remove the existing output folder first.

Method2 for a single subject using our version: (easier to use but less freedom)
1. Get the heudiconv_test.sh from this repository and a converter file (available in ./heudiconv/)
2. Put heudiconv_test.sh and the converter file in a base directory (base_dir). This base directory should be the parent directory of your project's dicom directory.
3. When you are in the base directory, use `chmod u+x heudiconv_test.sh` to make the script executable. Then you can run heudiconv_test.sh with three arguments: the name of the dicom directory, the name of the converter file and the subject index (e.g., `./heudiconv_test.sh Yuexin_project heuristic_sequence.py 01`). The output will be in the base directory (e.g., ./Yuexin_project_BIDS)

### heuristic file provided by us
- heuristic_protocol.py: classification based on series description.
- heuristic_sequence.py: classification based on sequence name. Users need to modify the output BOLD file name by themselves by replacing "taskName" with the actual task.
- heuristic_sequence_bold.py: classification based on sequence name. Users will be prompted to input the task name if fMRI data are present and the task will be in the file name.

## MRIQC
https://mriqc.readthedocs.io/en/latest/
1. Data have to be in BIDS. You can validate your data with the [validator](http://incf.github.io/bids-validator/). Some valid key labels may not be accepted by the validator but will not affect the overall performance of MRIQC.
2. To see whether mriqc works properly, use `docker run -it nipreps/mriqc:latest --version` to check the version
3. For a single subject: `docker run -it --rm -v <bids_dir>:/data:ro -v <output_dir>:/out nipreps/mriqc:latest /data /out participant --participant_label <subject_folder_name>`

## fMRIPrep
https://fmriprep.org/en/stable/
1. Data have to be in BIDS. You can validate your data with the [validator](http://incf.github.io/bids-validator/). Normally, no error or warning should be present for fMRIPrep to run properly (otherwise use `--skip_bids_validation` flag as below)
2. Get the docker image with `docker pull nipreps/fmriprep:latest`
3. Obtain Freesurfer software and its license.txt.
3. `docker run -it --rm -v <bids_dir>:/data:ro -v <output_dir>:/out -v <freesurfer_license_path>:/opt/freesurfer/license.txt nipreps/fmriprep:latest /data /out/out participant --skip_bids_validation --fs-no-reconall`

