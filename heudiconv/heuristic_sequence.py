import os

#Intended for for fmaps
POPULATE_INTENDED_FOR_OPTS = {
    'matching_parameters': ['Force'],
    'criterion': 'First'
}

dicoms2skip = ['localiser','setter','localizer', 'Head Scout']

def filter_dicom(dcmdata):
    """Return True if a DICOM dataset should be filtered out, else False"""
    for i in dicoms2skip:
        if (i in dcmdata.SeriesDescription):
            return True
    return False

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    
    #20221122 Yuexin Xi - bug: keyerror for extra - fixed: add key-value pair in all cases of extra
    #20230327 Yuexin Xi - bug: 'dir' should be put after task according to BIDS - fixed
    
    # MPRAGE, FGATIR, EDGE3D, WAIR, STIR, SPACE
    template_anat = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}{acq}_run-{item:02d}{part}_{suffix}')
    template_anat_derived = create_key('derivatives/scanner/{bids_subject_session_dir}/anat/{bids_subject_session_prefix}{acq}_run-{item:02d}{part}_{suffix}')
    
    # FLAIR
    #flair = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_FLAIR')
    
    # BOLD
    template_func = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-taskName{dir}_run-{item:02d}_{suffix}')
    epi = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_task-taskName{dir}_run-{item:02d}_epi')
    
    # Perfusion
    asl = create_key('{bids_subject_session_dir}/perf/{bids_subject_session_prefix}{dir}_run-{item:02d}_asl')
    m0scan = create_key('{bids_subject_session_dir}/perf/{bids_subject_session_prefix}{dir}_run-{item:02d}_m0scan')
    template_perf_derived = create_key('derivatives/scanner/{bids_subject_session_dir}/perf/{bids_subject_session_prefix}_run-{item:02d}_{suffix}')
    
    # Diffusion
    dwi = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_dwi')
    template_dwi_derived = create_key('derivatives/scanner/{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_{suffix}')
    
    # Field Maps
    # fm2d2r
    fmap_diff = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_phasediff')
    fmap_magnitude = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_magnitude')
    
    # MEGRE
    # fl2d2 + fieldmap in names -> fmap/two phase maps and two magnitude images
    # fl2d2 - fieldmap in names -> anat/..._MEGRE.nii
    fmap_megre_magnitude = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-MEGRE_magnitude')
    fmap_megre_phase = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-MEGRE_phase')
    megre = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_MEGRE')
    
    # Angiography
    angio = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_angio')
    angio_MIP = create_key('derivatives/scanner/{bids_subject_session_dir}/extra/anat/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_MIP')
    
    # SWI
    template_swi = create_key('{bids_subject_session_dir}/swi/{bids_subject_session_prefix}_run-{item:02d}{part}_{suffix}')
    
    # extra
    extra = create_key('{bids_subject_session_dir}/extra/{bids_subject_session_prefix}_acq-{acq}_{des}_run-{item:02d}_extra')
    
    info = {template_anat: [], \
        template_anat_derived: [], \
        template_func: [], \
        epi: [], \
        asl: [], \
        m0scan: [], \
        dwi: [], \
        template_dwi_derived: [], \
        template_perf_derived: [], \
        fmap_megre_magnitude: [], \
        fmap_megre_phase: [], \
        megre: [], \
        fmap_diff: [], \
        fmap_magnitude: [], \
        angio: [], \
        template_swi: [], \
        extra: []}
    # last_run = len(seqinfo)

    for idx, s in enumerate(seqinfo):
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * series_files
        * image_type
        * sequence_name
        """
        
        description = (s.series_description + '_' + s.protocol_name).strip().upper()
    
        #ABCD
        """
        if ('tfl_me3d1' in s.sequence_name):
            if ('MPR' in description):
                info[template_anat].append({'item': s.series_id, 'acq': '_acq-MPRAGE', 'part': '', 'suffix': 'T1w'})
                continue
            elif ('MP2RAGE' in description):
                info[template_anat].append({'item': s.series_id, 'acq': '_acq-MP2RAGE', 'part': '', 'suffix': 'T1w'})
                continue
            elif ('SPC' in description):
                if ('T2' in description): 
                    info[template_anat].append({'item': s.series_id, 'acq': '_acq-SPACE', 'part': '', 'suffix': 'T2w'})
                    continue
                elif ('T1' in description):
                    info[template_anat].append({'item': s.series_id, 'acq': '_acq-SPACE', 'part': '', 'suffix': 'T1w'})
                    continue
        """       
        
        # Field Maps, phasediff
        # fm_r + 2d + 2
        if ('fm2d2r' in s.sequence_name):
            if('P' in (s.image_type[2].strip()) ):
                info[fmap_diff].append(s.series_id)
                continue
            if('M' in (s.image_type[2].strip()) ):
                info[fmap_magnitude].append(s.series_id)
                continue

        # MEGRE, two phases images
        # fl + 2d + 2
        # qfl + 3d + 4
        if ('fl2d2' in s.sequence_name or \
            'qfl3d4' in s.sequence_name):
            if ('FIELD' in description \
                and 'MAP' in description):
                if('P' in (s.image_type[2].strip())):
                    info[fmap_megre_phase].append(s.series_id)
                    continue
                elif ('M' in (s.image_type[2].strip())):
                    info[fmap_megre_magnitude].append(s.series_id)
                    continue
            if (not ('FIELD' in description) and not ('MAP' in description)):
                info[megre].append(s.series_id)
                continue
        
        # MPRAGE (1 image) + MP2RAGE (3 images)
        # FGATIR, 3d-EDGE, WAIR, STIR
        # tfl + 3d + 1
        if ('tfl3d1' in s.sequence_name):
            if ('FGATIR' in description):
                info[template_anat].append({'item': s.series_id, 'acq': '_acq-FGATIR', 'part': '', 'suffix': 'T1w'})
                continue
            elif ('3D-EDGE' in description):
                info[template_anat].append({'item': s.series_id, 'acq': '_acq-EDGE', 'part': '', 'suffix': 'T1w'})
                continue
            elif (s.series_files == 1 or s.series_files == 192):
                info[template_anat].append({'item': s.series_id, 'acq': '_acq-MPRAGE', 'part': '', 'suffix': 'T1w'})
                continue
            elif (s.series_files == 3):
                info[template_anat].append({'item': s.series_id, 'acq': '_acq-MP2RAGE', 'part': '', 'suffix': 'T1w'})
                continue
        
        # tir_rr + 2d + 1
        if ('tir2d1rr' in s.sequence_name):
            info[template_anat].append({'item': s.series_id, 'acq': '_acq-STIR', 'part': '', 'suffix': 'T2w'})
            continue
            
        # tir + 2d + 1, dark fluid flair?
        if ('tir2d1' in s.sequence_name):
            info[template_anat].append({'item': s.series_id, 'acq': '_acq-WAIR', 'part': '', 'suffix': 'T2w'})
            continue
        
        # hippocampus
        # tse + 2d + 1
        if ('tse2d1' in s.sequence_name):
            info[template_anat].append({'item': s.series_id, 'acq': '', 'part': '', 'suffix': 'T2w'})
            continue
        
        # SPACE needs verification
        if ('spc' in s.sequence_name):
            # spc + ir
            if ('spcir' in s.sequence_name):
                info[template_anat].append({'item': s.series_id, 'acq': '_acq-SPACE', 'part': '', 'suffix': 'FLAIR'})
                continue
            # spc + R?
            elif ('spc' in s.sequence_name):
                if ('T2' in description): 
                    info[template_anat].append({'item': s.series_id, 'acq': '_acq-SPACE', 'part': '', 'suffix': 'T2w'})
                    continue
                elif ('T1' in description):
                    info[template_anat].append({'item': s.series_id, 'acq': '_acq-SPACE', 'part': '', 'suffix': 'T1w'})
                    continue  
        
        # BOLD
        # epfid + 2d
        # epse + 2d
        if (('epfid2d' in s.sequence_name or 
            'epse2d' in s.sequence_name) and 'FMRI' in s.image_type[2].strip()):
            myItem = {'item': s.series_id}
            if ('SBREF' in description):
                myItem['suffix'] = 'sbref'
            else:
                myItem['suffix'] = 'bold'
            if ('PA' in description):
                myItem['dir'] = '_dir-PA'
                info[epi].append(myItem)
                continue
            elif ('AP' in description): 
                myItem['dir'] = '_dir-AP'
            else:
                myItem['dir'] = ''
            info[template_func].append(myItem)
            continue
                      
                        
        # Perfusion
        # tgse + 3d + 1
        if ('ASL' in s.image_type[2].strip() or \
            'tgse3d1' in s.sequence_name):
            if ('ORIGINAL' in s.image_type[0].strip()):
                myItem = {'item': s.series_id}
                if ('PA' in description and not 'PASL' in description):
                    myItem['dir'] = '_dir-PA'
                elif ('AP' in description):
                    myItem['dir'] = '_dir-AP'
                else:
                    myItem['dir'] = ''    
                if ('MZERO' in description or 'M0' in description):
                    info[m0scan].append(myItem)
                    continue
                else:
                    info[asl].append(myItem)
                    continue
            if (('DERIVED' in s.image_type[0].strip()) and ('SUBTRACTION' in s.image_type[3].strip())):
                info[template_perf_derived].append({'item': s.series_id, 'suffix': 'perfusion'})
                continue
            elif (('DERIVED' in s.image_type[0].strip()) and ('RCBF' in s.image_type[3].strip())):
                info[template_perf_derived].append({'item': s.series_id, 'suffix': 'rcbf'})
                continue
            elif (('DERIVED' in s.image_type[0].strip()) and ('BAT' in s.image_type[3].strip())):
                info[template_perf_derived].append({'item': s.series_id, 'suffix': 'bat'})
                continue
            
            
        # Diffusion
        # epse + 2d
        if ('DIFFUSION' in s.image_type[2].strip() or \
            ('epse2d' in s.sequence_name and 'DWI' in description)):
            if ('ORIGINAL' in s.image_type[0].strip()):
                info[dwi].append(s.series_id)
                continue
            elif ('DERIVED' in s.image_type[0].strip()):
                if ('FA' in s.image_type[3].strip()):
                    info[template_dwi_derived].append({'item': s.series_id, 'suffix': 'FA'})
                    continue
                elif ('TENSOR_B0' in s.image_type[3].strip()):
                    info[template_dwi_derived].append({'item': s.series_id, 'suffix': 'TENSORB0'})
                    continue  
                elif ('TENSOR' in s.image_type[3].strip()):
                    info[template_dwi_derived].append({'item': s.series_id, 'suffix': 'TENSOR'})
                    continue
                elif ('TRACE' in s.image_type[3].strip()):
                    info[template_dwi_derived].append({'item': s.series_id, 'suffix': 'TRACE'})
                    continue
                elif ('ADC' in s.image_type[3].strip()):
                    info[template_dwi_derived].append({'item': s.series_id, 'suffix': 'ADC'})
                    continue  
        
        # Angiography, SWI
        # fl_r + 3d + 1: SWI?
        if ('fl3d' in s.sequence_name):
            if ('VESSEL' in description or 'ANGIO' in description):
                if ('ORIGINAL' in s.image_type[0].strip()):
                    info[angio].append(s.series_id)
                    continue
                elif ('DERIVED' in s.image_type[0].strip() and 'MIP' in s.image_type[2].strip()):
                    if ('COR' in description):
                        info[template_anat_derived].append({'item': s.series_id, 'acq': '_acq-coronal', 'part': '', 'suffix': 'MIP'})
                        continue
                    if ('SAG' in description):
                        info[template_anat_derived].append({'item': s.series_id, 'acq': '_acq-sagittal', 'part': '', 'suffix': 'MIP'})
                        continue    
            if ('ORIGINAL' in s.image_type[0].strip() and 'T2STAR' in description):
                if ('MAG' in description):
                    info[template_swi].append({'item': s.series_id, 'part': '_part-mag', 'suffix': 'GRE'})
                    continue
                elif ('PHA' in description):
                    info[template_swi].append({'item': s.series_id, 'part': '_part-phase', 'suffix': 'GRE'})
                    continue
                elif ('QSM' in description):
                    info[template_swi].append({'item': s.series_id, 'part': '_part-qsm', 'suffix': 'GRE'})
                    continue
                elif ('SWI' in description):
                    info[template_swi].append({'item': s.series_id, 'part': '', 'suffix': 'swi'})
                    continue
            if ('DERIVED' in s.image_type[0].strip() and 'SWI' in s.image_type[2].strip() and 'MINIMUM' in s.image_type[3].strip()):
                    info[template_swi].append({'item': s.series_id, 'part':'', 'suffix': 'minIP'})
                    continue
                    
               
        info[extra].append({'item': s.series_id, 'acq': s.sequence_name, 'des': s.series_description})
                  
        
        """
            
        # FLAIR
        if ('FLAIR' in description or ('DA' in description and 'FL' in description)):
            info[flair].append(s.series_id)
            continue   
                
    """
    

    return info