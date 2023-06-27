# xnat_utilities
Code base for XNAT applications \
Instructions are based on Ubuntu 20.04.5 LTS \
Remember to change every field with <> below according to your own situation. 


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
2. Our modified version (XNAT ready): run `docker pull yuexinxi/heudiconv:latest` in terminal.

Method1 for a single subject:
1. Get a converter file.
2. Use one of the following command.\
If you use the official version: 
```
docker run --rm -it -v <base_dir>:/base nipy/heudiconv:latest --files /base/<dicoms_dir>/ -o /base/<bids_dir>/ -f /base/<heuristic_file> -s <subject_index> -c dcm2niix -b --overwrite --minmeta
```
If you use our version: 
```
docker run --rm -it -v <base_dir>:/base yuexinxi/heudiconv:latest --files /base/<dicoms_dir>/ -o /base/<bids_dir>/ -f /base/<heuristic_file> -s <subject_index> -c dcm2niix -b --overwrite --minmeta
```

Note: If you need to run heudiconv on the same data again, remove the existing output folder first. \
Note: To use a converter file already in the container heuristics folder, just use the name (e.g. `-f heuristic_sequence`)

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
3. For a single subject: 
```
docker run -it --rm -v <bids_dir>:/data:ro -v <output_dir>:/out nipreps/mriqc:latest /data /out participant --participant_label <subject_folder_name>
```

## fMRIPrep
https://fmriprep.org/en/stable/

1. Data have to be in BIDS. You can validate your data with the [validator](http://incf.github.io/bids-validator/). Normally, no error or warning should be present for fMRIPrep to run properly (otherwise use `--skip_bids_validation`).
2. Run `docker pull nipreps/fmriprep:latest` to get the latest docker image or `docker pull nipreps/fmriprep:<version>`
3. Obtain Freesurfer software and its license.txt.
4.
```
docker run -it --rm -v <bids_dir>:/data:ro -v <output_dir>:/out -v <freesurfer_license_path>:/opt/freesurfer/license.txt nipreps/fmriprep:latest /data /out participant --fs-no-reconall --md-only-boilerplate --output-spaces T1w
```

Note:\
`--fs-no-reconall` = skip surface reconstruction\
`--md-only-boilerplate` = skip generation of citation with pandoc\
`--output-spaces T1w` = register images to anatomical space (default is normalization to MNI space)

## Preprocessing_scripts
### bto_dualecho_fieldmap.sh
- This script takes the following arguments: 1st echo magnitude image, 2nd echo magnitude image, 1st echo phase image, 2nd echo phase image and delta TE (optional) to generate the fieldmap and json file in BIDS specification.
- Dependencies: [Synthstrip](https://surfer.nmr.mgh.harvard.edu/docs/synthstrip/), [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation), [jq](https://jqlang.github.io/jq/)
- Example:
```
bto_dualecho_fieldmap.sh --mag1=sub-01_ses-01_acq-GRE_run-1_echo-1_part-mag_T2starw.nii.gz --mag2=sub-01_ses-01_acq-GRE_run-1_echo-2_part-mag_T2starw.nii.gz --phs1=sub-01_ses-01_acq-GRE_run-1_echo-1_part-phase_T2starw.nii.gz --phs2=sub-01_ses-01_acq-GRE_run-1_echo-2_part-phase_T2starw.nii.gz --dte=2.46
```

### phasediff_fieldmap.sh
- This script takes the following arguments: 1st echo magnitude image, 2nd echo magnitude image, phasediff image and delta TE (optional) to generate the fieldmap and json file in BIDS specification.
- Dependencies: [Synthstrip](https://surfer.nmr.mgh.harvard.edu/docs/synthstrip/), [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation), [jq](https://jqlang.github.io/jq/)
- Example: 
```
phasediff_fieldmap.sh --mag1=sub-01_ses-01_acq-GRE_run-1_echo-1_magnitude1.nii.gz --mag2=sub-01_ses-01_acq-GRE_run-1_echo-2_magnitude2.nii.gz --phs=sub-01_ses-01_acq-GRE_run-1_echo-1_phasediff.nii.gz --dte=2.46
```

### run_fsl_flirt.py
- This script takes the following arguments: functional image, reference anatomical image, white matter sementation and fieldmap (optional) to perform registration of functional image to anatomical image based on boundary based registration. This is the same method as what fMRIPrep uses (by 23.0.2).
- Dependencies: [nipype](https://nipype.readthedocs.io/en/latest/users/install.html)
- Example:
```
python run_fsl_flirt.py sub-01_ses-01_task-rest_run-01_bold.nii.gz sub-01_acq-MPRAGE_run-01_T1w.nii.gz sub-01_acq-MPRAGE_run-03_label-WM_probseg.nii.gz nofieldmap
```

### run_fsl_topup.py
- This script takes the following arguments: two functional images of opposite phase encoding direction (with their metadata json files. Make sure the "AcquisitionMatrixPE" and "EffectiveEchoSpacing" fields are available) and the unwarp direction to perform distortion correction of functional image with topup method. The results will either be in the current directory or in a new directory ./output/contrasts/ depending on the method chosen.
- Dependencies: [nipype](https://nipype.readthedocs.io/en/latest/users/install.html) or [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation)
- Example:
```
python run_fsl_topup.py sub-01_ses-01_task-rest_dir-AP_bold.nii.gz sub-01_ses-01_task-rest_dir-PA_bold.nii.gz y-
```
