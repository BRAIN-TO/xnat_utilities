# xnat_utilities
Code base for XNAT applications

## Installation/Prerequisite
1. Docker engine (installation for [ubuntu](https://github.com/srikash/TheBeesKnees/wiki/Installing-Docker-on-Ubuntu) or official installation documentation [here](https://docs.docker.com/engine/install/))
2. Data are organized in sub-xx folders.

## BIDScoin
https://github.com/srikash/TheBeesKnees/wiki/Converting-DICOMs-to-BIDS-NIfTIs

*`qtcreator` may be required for opening the GUI.

## HeuDiConv
https://heudiconv.readthedocs.io/en/latest/
1. Type `docker pull nipy/heudiconv:latest` in terminal to install HeuDiConv
2. Get a heuristic file (also available in /heudiconv) that is compatible with your dicoms
3. For a single subject: `docker run --rm -it -v <base_dir>:/base nipy/heudiconv:latest -d <base_dir/dicoms_dir>/sub-{subject}/*/*.dcm -o <base_dir/bids_dir>/ -f <base_dir/heuristic_dir>/heuristic.py -s 01 -c dcm2niix -b --overwrite --minmeta`*

*Optional session flag `-ss` is available.

*Relative path from a base directory rather than absolute path is highly recommended.

## MRIQC
https://mriqc.readthedocs.io/en/latest/
1. Data have to be in BIDS. You can validate your data with the [validator](http://incf.github.io/bids-validator/). Some valid key labels may not be accepted by the validator but will not affect the overall performance of MRIQC.
2. To see whether mriqc works properly, use `docker run -it nipreps/mriqc:latest --version` to check the version
3. For a single subject: `docker run -it --rm -v <bids_dir>:/data:ro -v <output_dir>:/out nipreps/mriqc:latest /data /out participant --participant_label sub-01`




