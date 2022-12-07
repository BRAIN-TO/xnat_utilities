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
    
    #MPRAGE:
    t1w_mprage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRAGE_run-{item:02d}_T1w')
    t1w_mp2rage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MP2RAGE_run-{item:02d}_T1w')
    
    #T1w:
    #t1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_T1w')
    
    #SPACE:
    spc_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_T2w')
    spc_T1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_T1w')
    spc_FLAIR = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_FLAIR')
    
    #FLAIR:
    flair = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_FLAIR')
    
    #TSE
    tse = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-RARE_run-{item:02d}_T1w')
    
    #BOLD:
    bold = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_dir-{dir}_run-{item:02d}_bold')
    
    #Perfusion:
    asl = create_key('{bids_subject_session_dir}/perf/{bids_subject_session_prefix}_run-{item:02d}_asl')
    perfusion = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_perfusion')
    dce = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_dce')
    dsc = create_key('{bids_subject_session_dir}/extra/perf/{bids_subject_session_prefix}_run-{item:02d}_dsc')
    
    #Diffusion:
    dwi = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_dwi')
    dwi_FA = create_key('{bids_subject_session_dir}/extra/dwi/{bids_subject_session_prefix}_run-{item:02d}_FA')
    dwi_TENSOR = create_key('{bids_subject_session_dir}/extra/dwi/{bids_subject_session_prefix}_run-{item:02d}_TENSOR')
    dwi_TENSORB0 = create_key('{bids_subject_session_dir}/extra/dwi/{bids_subject_session_prefix}_run-{item:02d}_TENSORB0')
    
    #Field Maps:
    fmap_diff = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-phase_MEGRE')
    fmap_magnitude = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_part-mag_MEGRE')
    
    #Angiography
    angio = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_angio')
    
    #extra:
    extra = create_key('{bids_subject_session_dir}/extra/extra/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_extra')
    
    info = {t1w_mprage: [], spc_T2w: [], spc_T1w: [], spc_FLAIR: [], flair: [], tse: [], bold: [], asl: [], perfusion: [], dce: [], dsc: [], dwi: [], dwi_FA: [], dwi_TENSOR: [], dwi_TENSORB0: [], fmap_diff: [], fmap_magnitude: [], angio: [], extra: []}
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
        * image_type
        """
        
        #Angiography
        if ('ANGIO' in s.series_description().strip().upper()):
            info[angio].append(s.series_id)
            continue
        
        #Field Maps
        if (('FIELDMAPPING' in s.series_description.strip().upper()) or ('FIELD_MAPPING' in s.series_description.strip().upper())):   
            if ('GRE_FIELDMAPPING' in s.series_description.strip().upper()):
                if('P' in (s.image_type[2].strip()) ):
                    info[fmap_diff].append(s.series_id)
                    continue
                if('M' in (s.image_type[2].strip()) ):
                    info[fmap_magnitude].append(s.series_id)
                    continue
        
        #MPRAGE
        if ('MPR' in s.series_description.strip().upper() and (not 'MEMPRAGE' in s.series_description.strip().upper())):
            info[t1w_mprage].append(s.series_id)
            continue
            
        #MP2RAGE
        if (('MP2RAGE' in s.series_description.strip().upper()) and (not 'MEMP2RAGE' in s.series_description.strip().upper())):
                if ('T1' in (s.series_description).strip().upper()):
                    info[t1w_mp2rage].append(s.series_id)
                    continue
        
        #space
        if ('SPACE' in s.series_description.strip().upper() or 'SPC' in s.series_description.strip().upper()):
            if ('FLAIR' in s.series_description.strip().upper() or ('DA' in s.series_description.strip().upper() and 'FL' in s.series_description.strip().upper())):
                if (not 'ND' in s.series_description.strip().upper()):
                    info[spc_FLAIR].append(s.series_id)
                    continue
                else:
                    info[extra].append({'item':s.series_id, 'acq': s.series_description})
                    continue
            if ('T2' in s.series_description.strip().upper()): 
                info[spc_T2w].append(s.series_id)
                continue
            elif ('T1' in s.series_description.strip().upper()):
                info[spc_T1w].append(s.series_id)
                continue
            
        # FLAIR
        if ('FLAIR' in s.series_description.strip().upper() or ('DA' in s.series_description.strip().upper() and 'FL' in s.series_description.strip().upper())):
            info[flair].append(s.series_id)
            continue
        
        #BOLD
        if (('BOLD' in s.series_description.strip().upper()) or ('FMRI' in s.image_type[2].strip())):
            if ('PA' in s.series_description.strip().upper()):
                info[bold].append({'item': s.series_id, 'dir':'PA'})
                continue
            elif ('AP' in s.series_description.strip().upper()):
                info[bold].append({'item': s.series_id, 'dir':'AP'})
                continue
            
        #Perfusion
        if ('ASL' in s.image_type[2].strip() or 'perf' in s.series_description.strip().upp):
            if ('ORIGINAL' in s.image_type[0].strip()):
                info[asl].append(s.series_id)
                continue
            elif (('DERIVED' in s.image_type[0].strip()) and ('SUBTRACTION' in s.image_type[3].strip())):
                info[perfusion].append(s.series_id)
                continue
            
        if ('VIBE' in s.series_description.strip().upper()):
            info[dce].append(s.series_id)
            continue
        
        if ('SAGE' in s.series_description.strip().upper()):
            info[dsc].append(s.series_id)
            continue
            
        
        #dwi
        if (('DIFFUSION' in s.image_type[2].strip()) or ('DTI'in s.series_description.strip().upper()) or ('DWI' in s.series_description.strip().upper())):
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
    
        info[extra].append({'item': s.series_id, 'acq': s.series_description})
    
        
        

    return info
