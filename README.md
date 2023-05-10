# xnat_utilities
Code base for XNAT applications \
Instructions are based on Ubuntu 20.04.5 LTS \
Remember to change every field with <> below according to your own directory structure. 


## Prerequisite
1. Docker engine (installation for [ubuntu](https://github.com/srikash/TheBeesKnees/wiki/Installing-Docker-on-Ubuntu) or official installation documentation [here](https://docs.docker.com/engine/install/))
2. All dicoms are organized inside sub-## folders (e.g., sub-01, sub-02...) in the project folder.
3. Virtual environment recommended.

## BIDScoin
https://github.com/srikash/TheBeesKnees/wiki/Converting-DICOMs-to-BIDS-NIfTIs

Note: `qtcreator` may be required for opening the GUI on ubuntu.

## HeuDiConv
https://heudiconv.readthedocs.io/en/latest/

### To get heudiconv (choose one):
1. Latest official heudiconv: run `docker pull nipy/heudiconv:latest` in terminal.
2. Our modified version:(XNAT ready in progress)
    Clone [this repository](https://github.com/845127818virna/heudiconv). Go into the cloned folder, use `docker build -t heudiconv .` to build a docker image called "heudiconv".

Method1 for a single subject:
1. Get a converter file (available in ./heudiconv/).
2. Use one of the following command. \
a. If you use the official version: `docker run --rm -it -v <base_dir>:/base nipy/heudiconv:latest --files /base/<dicoms_dir>/ -o /base/<bids_dir>/ -f /base/<heuristic_file> -s <subject_index> -c dcm2niix -b --overwrite --minmeta`\
b. If you use our version: `docker run --rm -it -v <base_dir>:/base heudiconv --files /base/<dicoms_dir>/ -o /base/<bids_dir>/ -f /base/<heuristic_file> -s <subject_index> -c dcm2niix -b --overwrite --minmeta`

Note: If you need to run heudiconv on the same data again, remove the existing output folder first.
Note: If you use a converter file already in the container heuristics folder, just use `-f <name>` and no need to put path to heuristic file.

Method2 for a single subject using our heudiconv and converter file: (easier to use but less freedom)
1. Get the heudiconv_test.sh from this repository.
2. Put heudiconv_test.sh in a base directory (base_dir). This base directory should be the parent directory of your project's dicom directory.
3. When you are in the base directory, use `chmod u+x heudiconv_test.sh` to make the script executable. Then you can run heudiconv_test.sh with two arguments: the name of the dicom directory and the subject index (e.g., `./heudiconv_test.sh Yuexin_project 01`). The output will be have "BIDS" as suffix (e.g., ./Yuexin_project_BIDS).

### heuristic files provided:
- [heuristic_protocol.py](https://github.com/BRAIN-TO/xnat_utilities/blob/main/heudiconv/heuristic_protocol.py): classification based on series description.
- [heuristic_sequence.py](https://github.com/BRAIN-TO/xnat_utilities/blob/main/heudiconv/heuristic_sequence.py): classification based on sequence name. Users need to modify the output BOLD file name on their own by replacing "taskName" with the actual task. 
- [heuristic_sequence_bold.py](https://github.com/BRAIN-TO/xnat_utilities/blob/main/heudiconv/heuristic_sequence_bold.py): classification based on sequence name. Users will be prompted to input the task name if fMRI data are present and the task will be in the output BOLD file name.

## MRIQC
https://mriqc.readthedocs.io/en/latest/

1. Data have to be in BIDS. You can validate your data with the [validator](http://incf.github.io/bids-validator/). Some valid key labels may not be accepted by the validator but will not affect the overall performance of MRIQC.
2. To see whether mriqc works properly, use `docker run -it nipreps/mriqc:latest --version` to check the version.
3. For a single subject: `docker run -it --rm -v <bids_dir>:/data:ro -v <output_dir>:/out nipreps/mriqc:latest /data /out participant --participant_label <subject_folder_name>`

## fMRIPrep
https://fmriprep.org/en/stable/

1. Data have to be in BIDS. You can validate your data with the [validator](http://incf.github.io/bids-validator/). Normally, no error or warning should be present for fMRIPrep to run properly (otherwise use `--skip_bids_validation` flag as below).
2. Get the docker image with `docker pull nipreps/fmriprep:latest`
3. Obtain Freesurfer software and its license.txt.
3. `docker run -it --rm -v <bids_dir>:/data:ro -v <output_dir>:/out -v <freesurfer_license_path>:/opt/freesurfer/license.txt nipreps/fmriprep:latest /data /out participant --skip_bids_validation --fs-no-reconall --md-only-boilerplate --output-spaces T1w`

Note:\
`--fs-no-reconall` = skip surface reconstruction\
`--md-only-boilerplate` = skip generation of citation with pandoc\
`--output-spaces T1w` = skip normalization to MNI space

## TOPUP
https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/topup

1. Two images of opposite phase encoding direction and their corresponding metadata json files are required. Make sure the "AcquisitionMatrixPE" and "EffectiveEchoSpacing" fields are available.
2. Get nipype using [docker, conda or Pypi](https://nipype.readthedocs.io/en/latest/users/install.html) or set up [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation). Virtual environment recommended.
2. Get the script and put it in the same folder as the data.
3. run `python run_fsl_topup.py <file_to_correct> <file_reverse_direction>` according to your preferred python version.
4. The results will either be in the current directory or in a new directory ./output/contrasts/ depending on the method chosen.

### scripts provided:
- [run_fsl_topup.py](https://github.com/BRAIN-TO/xnat_utilities/blob/main/run_fsl_topup.py): takes images of opposite phase encoding direction and run FSL TOPUP and FUGUE to generate the distortion corrected image. You can choose from "run_nipype_interface()", "run_nipype_workflow()", or "run_command()". ApplyTOPUP is also available in run_nipype_interface()

## FLIRT
https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FLIRT

1. The functional image, the reference anatomical image, the white matter sementation are required. fieldmap is optional.
2. Get nipype using [docker, conda or Pypi](https://nipype.readthedocs.io/en/latest/users/install.html). Virtual environment recommended.
3. run `python run_fsl_flirt.py <in_file> <ref_file> <wm_seg> <fmap_file>` or `python run_fsl_flirt.py <in_file> <ref_file> <wm_seg> nofieldmap` if no fieldmap available.
4. The result will be in the same directory as the input image.

### scripts provided:
- [run_fsl_flirt.py](https://github.com/BRAIN-TO/xnat_utilities/blob/main/run_fsl_flirt.py): takes functional image, reference anatomical image, white matter segmentation and a fieldmap to run FSL FLIRT with BBR cost function to generated the registered image using gray/white matter boundary. This is the same method as what fMRIPrep uses (by 23.0.2).
