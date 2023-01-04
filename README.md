# xnat_utilities
Code base for XNAT applications \
Instructions are based on Ubuntu 20.04.5 LTS \
Remember to change everything with <> below according to your own directory structure. 


## Prerequisite
1. Docker engine (installation for [ubuntu](https://github.com/srikash/TheBeesKnees/wiki/Installing-Docker-on-Ubuntu) or official installation documentation [here](https://docs.docker.com/engine/install/))
2. All dicoms are organized in sub-## folders (e.g., sub-01, sub-02...). No subfolders under each subject folder.
3. Virtual environment recommended.

## BIDScoin
https://github.com/srikash/TheBeesKnees/wiki/Converting-DICOMs-to-BIDS-NIfTIs*

\* `qtcreator` may be required for opening the GUI on ubuntu.

## HeuDiConv
https://heudiconv.readthedocs.io/en/latest/

### To get heudiconv (choose one):
1. Latest official heudiconv: Type `docker pull nipy/heudiconv:latest` in terminal
2. Our modified version:
    Clone [this repository](https://github.com/845127818virna/heudiconv). Go into the cloned folder, use `docker build -t heudiconv .` to build a docker image.

Method1 for a single subject:
1. Get a converter file (available in ./heudiconv/)
2. Use one of the following command. \
a. If you use the official version: `docker run --rm -it -v <base_dir>:/base nipy/heudiconv:latest -d <base_dir/dicoms_dir>/sub-{subject}/*.dcm -o <base_dir/bids_dir>/ -f <base_dir/heuristic_dir>/<heuristic_file> -s <subject_index> -c dcm2niix -b --overwrite --minmeta`\
b. If you use our version: `docker run --rm -it -v <base_dir>:/base heudiconv -d <base_dir/dicoms_dir>/sub-{subject}/*.dcm -o <base_dir/bids_dir>/ -f <base_dir/heuristic_dir>/<heuristic_file> -s <subject_index> -c dcm2niix -b --overwrite --minmeta`

\* Relative path from a base directory rather than absolute path is highly recommended. \
\* If you need to run heudiconv on the same data again, remove the existing BIDS folder first.

Method2 for a single subject using our version:
1. Get the heudiconv_test.sh and a converter file (available in ./heudiconv/)
2. Put the script in the parent directory (base_dir) of your dicom directory (and bids directory if exists). Put the converter in the base directory.
3. When you are in the base directory, run heudiconv_test.sh with four arguments: relative path to converter file, name of dicom directory, name of bids directory and subject index (e.g., 01)

### heuristic file provided by us
- heuristic_protocol.py: classification based on series description.
- heuristic_sequence.py: classification based on sequence name.


## MRIQC
https://mriqc.readthedocs.io/en/latest/
1. Data have to be in BIDS. You can validate your data with the [validator](http://incf.github.io/bids-validator/). Some valid key labels may not be accepted by the validator but will not affect the overall performance of MRIQC.
2. To see whether mriqc works properly, use `docker run -it nipreps/mriqc:latest --version` to check the version
3. For a single subject: `docker run -it --rm -v <bids_dir>:/data:ro -v <output_dir>:/out nipreps/mriqc:latest /data /out participant --participant_label <subject_folder_name>`