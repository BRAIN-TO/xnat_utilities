import os

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
    
    # MPRAGE
    mprage_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRAGE_run-{item:02d}_T1w')
    mp2rage_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MP2RAGE_run-{item:02d}_T1w')
    
    # FGATIR
    fgatir_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-FGATIR_run-{item:02d}_T1w')
    edge3d_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-3DEDGE_run-{item:02d}_T1w')
    wair = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-WAIR_run-{item:02d}_T1w')
    stir = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-STIR_run-{item:02d}_T1w')
    
    #T1w
    #t1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_T1w')
    
    # SPACE
    spc_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_T2w')
    spc_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_T1w')
    spc_FLAIR = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_FLAIR')
    
    # FLAIR
    flair = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_FLAIR')
    
    # BOLD
    bold = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_dir-{dir}_run-{item:02d}_bold')
    bold_ref = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_dir-{dir}_run-{item:02d}_sbref')
    
    # Perfusion
    asl = create_key('{bids_subject_session_dir}/perf/{bids_subject_session_prefix}_dir-{dir}_run-{item:02d}_asl')
    perfusion = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_perfusion')
    dce = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_dce')
    dsc = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_dsc')
    rcbf = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_cbf')
    m0scan = create_key('{bids_subject_session_dir}/perf/{bids_subject_session_prefix}_dir-{dir}_run-{item:02d}_m0scan')
    bat = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_bat')
    
    # Diffusion
    dwi = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_dwi')
    dwi_FA = create_key('{bids_subject_session_dir}/extra/dwi/{bids_subject_session_prefix}_run-{item:02d}_FA')
    dwi_TENSOR = create_key('{bids_subject_session_dir}/extra/dwi/{bids_subject_session_prefix}_run-{item:02d}_TENSOR')
    dwi_TENSORB0 = create_key('{bids_subject_session_dir}/extra/dwi/{bids_subject_session_prefix}_run-{item:02d}_TENSORB0')
    
    # Field Maps
    # fm2d2r
    fmap_diff = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-phase_MEGRE')
    fmap_magnitude = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-mag_MEGRE')
    
    # MEGRE
    # fl2d2 + fieldmap in names -> fmap/two phase maps and two magnitude images -> check results whether it says 1 and 2
    # fl2d2 - fieldmap in names -> anat/..._MEGRE.nii
    fmap_megre_magnitude = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-MEGRE_magnitude')
    fmap_megre_phase = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_acq-MEGRE_phase')
    megre = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_MEGRE')
    
    #Angiography
    angio = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_angio')
    angio_MIP = create_key('{bids_subject_session_dir}/extra/anat/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_MIP')
    
    #extra
    extra = create_key('{bids_subject_session_dir}/extra/extra/{bids_subject_session_prefix}_acq-{acq}_{des}_run-{item:02d}_extra')
    
    info = {mprage_T1w: [], mp2rage_T1w: [], fgatir_T1w: [], edge3d_T1w: [], wair: [], stir: [], spc_T2w: [], spc_T1w: [], spc_FLAIR: [], flair: [], bold: [], bold_ref: [], asl: [], perfusion: [], dce: [], dsc: [], rcbf: [], m0scan: [], bat: [], dwi: [], dwi_FA: [], dwi_TENSOR: [], dwi_TENSORB0: [], fmap_megre_magnitude: [], fmap_megre_phase: [], megre: [], fmap_diff: [], fmap_magnitude: [], angio: [], angio_MIP: [], extra: []}
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
        
        # print("\n {} \n".format(s.TR))
        
        #Field Maps needs verification
        if ('fm2d2r' in s.sequence_name):
            if('P' in (s.image_type[2].strip()) ):
                    info[fmap_diff].append(s.series_id)
                    continue
            if('M' in (s.image_type[2].strip()) ):
                    info[fmap_magnitude].append(s.series_id)
                    continue

        #MEGRE
        if ('fl2d2' in s.sequence_name or \
            'qfl3d4' in s.sequence_name):
            if ('FIELD' in s.series_description.strip().upper() \
                and 'MAP' in s.series_description.strip().upper()):
                if('P' in (s.image_type[2].strip())):
                    info[fmap_megre_phase].append(s.series_id)
                    continue
                elif ('M' in (s.image_type[2].strip())):
                    info[fmap_megre_magnitude].append(s.series_id)
                    continue
            if (not ('FIELD' in s.series_description.strip().upper()) and not ('MAP' in s.series_description.strip().upper())):
                info[megre].append(s.series_id)
                continue
        
        #MPRAGE (1 image) + MP2RAGE (3 images)
        #FGATIR, 3d-EDGE, WAIR, STIR
        if ('tfl3d1' in s.sequence_name):
            if ('FGATIR' in s.series_description.strip().upper()):
                info[fgatir_T1w].append(s.series_id)
                continue
            elif ('3D-EDGE' in s.series_description.strip().upper()):
                info[edge3d_T1w].append(s.series_id)
                continue
            elif (s.series_files == 1):
                info[mprage_T1w].append(s.series_id)
                continue
            elif (s.series_files == 3):
                info[mp2rage_T1w].append(s.series_id)
                continue
            
          
        if ('tir2d1_7' in s.sequence_name):
            info[wair].append(s.series_id)
            continue
        
        if ('tir2d1rr15' in s.sequence_name):
            info[stir].append(s.series_id)
            continue
        
        #SPACE needs verification
        if ('spc' in s.sequence_name):
            if ('spcir' in s.sequence_name):
                info[spc_FLAIR].append(s.series_id)
                continue
            elif ('spcR' in s.sequence_name):
                if ('T2' in s.series_description.strip().upper()): 
                    info[spc_T2w].append(s.series_id)
                    continue
                elif ('T1' in s.series_description.strip().upper()):
                    info[spc_T1w].append(s.series_id)
                    continue  
        
        #BOLD
        if (('epfid2d' in s.sequence_name or 
            'epse2d' in s.sequence_name) and 'FMRI' in s.image_type[2].strip()):
            if ('SBREF' in s.series_description.strip().upper()):
                if ('PA' in s.series_description.strip().upper()):
                    info[bold_ref].append({'item': s.series_id, 'dir':'PA'})
                    continue
                elif ('AP' in s.series_description.strip().upper()):
                    info[bold_ref].append({'item': s.series_id, 'dir':'AP'})
                    continue
                else:
                    info[bold_ref].append({'item': s.series_id, 'dir':'none'})
                    continue
            if ('PA' in s.series_description.strip().upper()):
                info[bold].append({'item': s.series_id, 'dir':'PA'})
                continue
            elif ('AP' in s.series_description.strip().upper()):
                info[bold].append({'item': s.series_id, 'dir':'AP'})
                continue
            else:
                info[bold].append({'item': s.series_id, 'dir':'none'})
                continue
                        
        #Perfusion
        if ('ASL' in s.image_type[2].strip() or \
            'tgse3d1_3100' in s.sequence_name or \
            'WIPtgse3d1_2184' in s.sequence_name or \
            'WIPtgse3d1_930' in s.sequence_name):
            if ('ORIGINAL' in s.image_type[0].strip()):
                if ('MZERO' in s.series_description.strip().upper() or 'M0' in s.series_description.strip().upper()):
                    if ('PA' in s.series_description.strip().upper() and not 'PASL' in s.series_description.strip().upper()):
                        info[m0scan].append({'item': s.series_id, 'dir':'PA'})
                        continue
                    elif ('AP' in s.series_description.strip().upper()):
                        info[m0scan].append({'item': s.series_id, 'dir':'AP'})
                        continue
                else:
                    if ('PA' in s.series_description.strip().upper() and not 'PASL' in s.series_description.strip().upper()):
                        info[asl].append({'item': s.series_id, 'dir':'PA'})
                        continue
                    elif ('AP' in s.series_description.strip().upper()):
                        info[asl].append({'item': s.series_id, 'dir':'AP'})
                        continue
            elif (('DERIVED' in s.image_type[0].strip()) and ('SUBTRACTION' in s.image_type[3].strip())):
                info[perfusion].append(s.series_id)
                continue
            elif (('DERIVED' in s.image_type[0].strip()) and ('RCBF' in s.image_type[3].strip())):
                info[rcbf].append(s.series_id)
                continue
            elif (('DERIVED' in s.image_type[0].strip()) and ('BAT' in s.image_type[3].strip())):
                info[bat].append(s.series_id)
                continue
            
            
        #Diffusion
        if ('DIFFUSION' in s.image_type[2].strip() or \
            ('epse2d' in s.sequence_name and 'DWI' in s.series_description.strip().upper())):
            if ('ORIGINAL' in s.image_type[0].strip()):
                info[dwi].append(s.series_id)
                continue
            elif ('DERIVED' in s.image_type[0].strip()):
                if ('FA' in s.image_type[3].strip()):
                    info[dwi_FA].append(s.series_id)
                    continue
                elif ('TENSOR_B0' in s.image_type[3].strip()):
                    info[dwi_TENSORB0].append(s.series_id)
                    continue  
                elif ('TENSOR' in s.image_type[3].strip()):
                    info[dwi_TENSOR].append(s.series_id)
                    continue  
        
        #Angiography
        if ('fl3d1r' in s.sequence_name):
            if ('ORIGINAL' in s.image_type[0].strip()):
                info[angio].append(s.series_id)
                continue
            elif ('DERIVED' in s.image_type[0].strip()):
                if ('MIP' in s.series_description.strip().upper()):
                    if ('COR' in s.series_description.strip().upper()):
                        info[angio_MIP].append({'item': s.series_id, 'acq': 'coronal'})
                        continue
                    if ('SAG' in s.series_description.strip().upper()):
                        info[angio_MIP].append({'item': s.series_id, 'acq': 'sagittal'})
                        continue
                    
        info[extra].append({'item': s.series_id, 'acq': s.sequence_name, 'des': s.series_description})
                  
        
        """
        #hippocampus
        if ('tse2d1_15' in s.sequence_name):
        
        #MP2RAGE
        if (('MP2RAGE' in s.series_description.strip().upper()) and (not 'MEMP2RAGE' in s.series_description.strip().upper())):
                if ('T1' in (s.series_description).strip().upper()):
                    info[mp2rage_T1w].append(s.series_id)
                    continue
            
        # FLAIR
        if ('FLAIR' in s.series_description.strip().upper() or ('DA' in s.series_description.strip().upper() and 'FL' in s.series_description.strip().upper())):
            info[flair].append(s.series_id)
            continue   
                
        info[extra].append({'item': s.series_id, 'acq': s.series_description})
    """
    
        
        

    return info
