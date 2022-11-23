# xnat_utilities
Code base for XNAT applications

## heudiconv
1. Install Docker
2. In terminal: docker pull nipy/heudiconv:latest
3. In terminal: docker run --rm -it -v /base_path:/base nipy/heudiconv:latest -d /base/to/my_dicomsfolder/sub-{subject}/*/*.dcm -o /base/to/my_bidsfolder/ -f /base/to/heuristic.py -s 01 -c dcm2niix -b --overwrite --minmeta


